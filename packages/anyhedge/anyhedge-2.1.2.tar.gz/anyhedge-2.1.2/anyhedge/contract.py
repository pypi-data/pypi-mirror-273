# Built-in imports
from __future__ import annotations  # allow pre-definition use of types
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Sequence, Type

# Local imports
from .bch_primitives import (
    DUST,
    MAX_REASONABLE_SATS,
    MIN_REASONABLE_DIVISION_STEPS,
    SATS_PER_BCH,
    SCRIPT_INT_MAX,
    PublicKey,
    Sats,
    ScriptTimestamp,
    UtxoSats,
)
from .contract_primitives import (
    LongLeverage,
    NominalOracleUnitsXSatsPerBch,
    Role,
    ShortLeverage,
    Side,
)
from .fee import (
    aggregate_fee_sats_to_role,
    FeeAgreement,
)
from .javascript import round_half_up
from .oracle import (
    oracle_pubkey_to_unit_class,
    OracleUnit,
    ScriptPriceInOracleUnitsPerBch,
)


class UnredeemableError(Exception):
    pass


# In this library design, there is no explicit multiplier to establish a liquidation price
# in the case of a simple hedge (short leverage = 1). We choose simply 10x.
DEFAULT_HIGH_LIQUIDATION_PRICE_MULTIPLIER_FOR_SIMPLE_HEDGE = 10.0


# TODO: add "forced maturation" to differentiate from normal case in records?
class RedemptionType(str, Enum):
    LIQUIDATION = 'Liquidation'
    MATURATION = 'Maturation'
    MUTUAL = 'Mutual'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_string(cls, redemption_type_string: str) -> RedemptionType:
        # use a strict lookup (with lowercase) to ensure KeyError with unknown value
        lookup = {
            'liquidation': cls.LIQUIDATION,
            'maturation': cls.MATURATION,
            'mutual': cls.MUTUAL,
        }
        redemption_type = lookup[redemption_type_string.lower()]
        return redemption_type


# TODO: this should be broken into independent parts TimingIntent, UserIntent, MoneyIntent
@dataclass(frozen=True)
class GenericContractIntent:
    """A representation of intent for a contract that translates to a Contract Proposal."""
    # 1. A specific intent pattern must provide a set of parameters from which a contract can be created

    # 2. The proposal property (or it could be parameterized... maybe... implements the translation from intent parameters to a contract
    @property
    def proposal(self, *args, **kwargs) -> ContractProposal:
        raise NotImplementedError()


@dataclass(frozen=True)
class ContractFromNominalHedgeAndLeverages(GenericContractIntent):
    """This is the canonical intent, although it turns out to be a pain to use in user interfaces."""
    # Timing Intent
    start_timestamp: ScriptTimestamp
    maturity_timestamp: ScriptTimestamp

    # Money Intent
    nominal_oracleUnits: OracleUnit
    short_leverage: ShortLeverage
    long_leverage: LongLeverage
    start_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch

    # User Intent
    maker_side: Side
    short_mutual_redeem_public_key: PublicKey | '' = ''
    long_mutual_redeem_public_key: PublicKey | '' = ''

    @property
    def proposal(self) -> ContractProposal:
        # Before calculating key values below, this is an outline of the setup, using relevant variable names.
        #
        # AnyHedge 0.12 with leveraged shorts works on the same concept as previous "simple/nominal hedge" versions.
        # By including one more number, explained below, the contract can now provide independent leverage to Short and Long.
        #
        # In summary, Long uses AnyHedge to "buy" an asset now, "selling" it later for hopefully a higher price, and
        # Short uses AnyHedge to "sell" an asset now, "buying" it later for hopefully a lower price.
        #
        # The hedge value / simple hedge / nominal hedge is a fixed asset value that the rest of the contract centers around.
        # The original idea of AnyHedge is that at any price within the liquidation (more commonly "margin call") range,
        # Short receives exactly the nominal hedge value at the end, paid in Bch. This is the definition of behavior for
        # short leverage = 1, i.e. virtually holding another asset, using BCH as the vehicle instead of the asset itself.
        #
        # The setting of liquidation values is mathematically equivalent to setting leverage for Short and Long.
        # In the original setup, only Long was mathematically bound to the liquidation price, establishing leverage.
        # Short on the other hand had a liquidation price for safety purposes, but the behavior of Short payout was not bound
        # mathematically to that liquidation price. The contract simply always paid out Short for the full hedge value,
        # which at the absurd extreme can be achieved with one satoshi at a price approaching infinity.
        #
        # The current arrangement described below allows Short to achieve leverage by tying behavior to the high
        # liquidation price if desired, or to retain original behavior by disconnecting from the high liquidation price.
        # Given this setup at start, the contract is fully collateralized to handle any outcome within the liquidation range.
        #
        # The relationship between liquidation prices and effective leverage are not explained in depth here,
        # but the summary is:
        #     shortLeverage = 1 + (1 / ((highLiquidationPrice / startPrice) - 1))
        #     longLeverage  = 1 / (1 - (lowLiquidationPrice / startPrice))
        #
        #  *Price in Asset/Bch*            *Cost of Hedge at Price (higher price ==> lower cost)*
        # --------------------------------------------------------------------------------------------------------------------
        #                        ^
        #                        |
        #  highLiquidationPrice  -    ---- satsForHedgeAtHighLiq (this is the new reference that allows short leverage)
        #                        |    ||||                       (in the past, the assumption was zero cost at infinity)
        #                        |    ||||
        #                        |    |||| } shortInputSats = worst case "sell low buy high" case for short
        #                        |    ||||                  = satsForHedgeAtStart - satsForHedgeAtHighLiq
        #                        |    ||||
        #                        |    ||||
        #            startPrice  -    ---- satsForHedgeAtStart
        #                        |    ||||
        #                        |    |||| } longInputSats = worst case "buy high sell low" case for long
        #                        |    ||||                 = satsForHedgeAtLowLiq - satsForHedgeAtStart
        #                        |    ||||
        #   lowLiquidationPrice  -    ---- satsForHedgeAtLowLiq (to reiterate, lowest price ==> highest cost)
        #                        |
        #                        |
        #                        - 0
        #
        # Payout at the end of the contract is the same picture, except based on the end price instead of start Price.
        #
        #  *Price in Asset/Bch*            *Cost of Hedge at Price (higher price ==> lower cost)*
        # --------------------------------------------------------------------------------------------------------------------
        #                        ^
        #                        |
        #  highLiquidationPrice  -    ---- satsForHedgeAtHighLiq (zero at infinity for simple hedge)
        #                        |    ||||
        #                        |    |||| } shortPayoutSats = satsForHedgeAtEnd - satsForHedgeAtHighLiq
        #                        |    ||||
        #              endPrice  -    ---- satsForHedgeAtEnd (price moved up, Short gets more Bch, Long gets less)
        #                        |    ||||
        #                        |    ||||
        #            startPrice  -    ||||
        #                        |    ||||
        #                        |    |||| } longPayinSats = satsForHedgeAtLowLiq - satsForHedgeAtEnd
        #                        |    ||||
        #                        |    ||||
        #   lowLiquidationPrice  -    ---- satsForHedgeAtLowLiq
        #                        |
        #                        |
        #                        - 0

        # 1. Low liquidation price: the low price that triggers liquidation of the Long party.
        # The value is rounded to achieve a result as close as possible to intent.
        # There should be no integer-level loss of precision given the 32-bit range of oracle prices.
        # In order to align with methodology of the canonical anyhedge library,
        # we do an initial step to convert leverage to a price multiplier
        low_liquidation_price_multiplier = 1 - (1 / self.long_leverage)
        low_liquidation_price_oracleUnits_per_bch = ScriptPriceInOracleUnitsPerBch(round_half_up(low_liquidation_price_multiplier * float(self.start_price_oracleUnits_per_bch)))

        # 2. High liquidation price: the high price that triggers liquidation of the Short party.
        # The value is rounded to achieve a result as close as possible to intent.
        # There should be no integer-level loss of precision given the 32-bit range of oracle prices.
        # In order to align with methodology of the canonical anyhedge library,
        # we do an initial step to convert leverage to a price multiplier and detect if this is effectively
        # a simple hedge or not.
        try:
            high_liquidation_price_multiplier = 1 + (1 / (self.short_leverage - 1))
            is_simple_hedge = False
        except ZeroDivisionError:
            high_liquidation_price_multiplier = DEFAULT_HIGH_LIQUIDATION_PRICE_MULTIPLIER_FOR_SIMPLE_HEDGE
            is_simple_hedge = True

        # Use the multiplier to set the price
        high_liquidation_price_oracleUnits_per_bch = ScriptPriceInOracleUnitsPerBch(round_half_up(high_liquidation_price_multiplier * float(self.start_price_oracleUnits_per_bch)))

        # 3. Composite number representing the nominal hedge value in asset terms.
        # In the diagrams above, this is the value discussed as "Hedge"
        # Note: Rather than using the nominal hedge value alone, the number is calculated as
        #       (nominal hedge units * 1e8 sats/bch). This allows the critical calculation in the contract to be simple
        #       division, and is also a carryover from previous BCH VM versions (before May 2022) that did not have
        #       multiplication. I.e. this value divided by the oracle price directly yields satoshis for
        #       nominal hedge value at the given price, which is the final units we need to establish payouts.
        # Note: DO NOT CONVERT THE COMPOSITE VALUE TO A floating point NUMBER FOR ANY REASON.
        #       Any such calculations or transmissions (e.g. through simple JSON) must be
        #       considered to introduce undefined behavior and be rejected.
        #       The initial float calculation is a one way translation from floating precision
        #       nominalUnits input to BigInt.
        nominal_oracleUnits_x_satsPerBch = NominalOracleUnitsXSatsPerBch(round_half_up(self.nominal_oracleUnits * SATS_PER_BCH))

        # 4. Cost in sats of the nominal hedge at high liquidation price.
        # This is the value satsForHedgeAtHighLiq in the diagrams above.
        # In summary, this value is needed to calculate Short's payout.
        # Calculation of the value is discontinuous as follows:
        if is_simple_hedge:
            # a) For a simple hedge (short leverage = 1), the value is exactly 0. This
            # represents the concept and calculation that Long must cover the full range
            # of Short payouts from current price to infinity (where the cost becomes zero, this value).
            cost_sats_for_nominal_value_at_high_liquidation = Sats(0)
        else:
            # b) For a leveraged short (short leverage > 1), the value is calculated from the
            # other parameters in a simple cost relationship.
            # Note: cost is floored for safety by bigint division in order to ensure that the
            #       total sats in the contract cover a range that may be at worst +1 or +2 from
            #       the "real" full precision value. This is valuable to ensure that contract
            #       calculations never result in a value more than the total sats available.
            cost_sats_for_nominal_value_at_high_liquidation = Sats(nominal_oracleUnits_x_satsPerBch // high_liquidation_price_oracleUnits_per_bch)

        # 5. Cost in sats of the nominal hedge at low liquidation.
        # This is the value satsForHedgeAtLowLiq in the diagrams above.
        # In summary, this value is needed to calculate total input.
        # Note: Here we use simple integer division and accept the loss of rounding.
        #       Safety is ensured outside the zero case by validation.
        # Note: We do zero testing here because this happens before parameter validation
        #       which would catch it otherwise.
        if low_liquidation_price_oracleUnits_per_bch <= 0:
            raise ValueError('low liquidation price must be greater than zero')
        cost_sats_for_nominal_value_at_low_liquidation = UtxoSats(nominal_oracleUnits_x_satsPerBch // low_liquidation_price_oracleUnits_per_bch)

        # 6. Total input satoshis: the difference between worst case long and short outcomes.
        total_input_sats = UtxoSats(cost_sats_for_nominal_value_at_low_liquidation - cost_sats_for_nominal_value_at_high_liquidation)

        return ContractProposal(
            address='',
            short_mutual_redeem_public_key=self.short_mutual_redeem_public_key,
            long_mutual_redeem_public_key=self.long_mutual_redeem_public_key,
            start_timestamp=self.start_timestamp,
            maturity_timestamp=self.maturity_timestamp,
            nominal_oracleUnits_x_satsPerBch=nominal_oracleUnits_x_satsPerBch,
            cost_sats_for_nominal_value_at_high_liquidation=cost_sats_for_nominal_value_at_high_liquidation,
            total_input_sats=total_input_sats,
            start_price_oracleUnits_per_bch=self.start_price_oracleUnits_per_bch,
            high_liquidation_price_oracleUnits_per_bch=high_liquidation_price_oracleUnits_per_bch,
            low_liquidation_price_oracleUnits_per_bch=low_liquidation_price_oracleUnits_per_bch,
            oracle_public_key=self.nominal_oracleUnits.public_key,
            maker_side=self.maker_side,
        )


@dataclass(frozen=True)
class ContractFromInputSatsAndLeverages(GenericContractIntent):
    """This is a more user-interface friendly intent."""
    # TODO: when TimingIntent intent is isolated, it will make more sense to have both duration and maturity TimingIntent. For now, user is expected to translate as needed.
    # Timing Intent
    start_timestamp: ScriptTimestamp
    maturity_timestamp: ScriptTimestamp

    # Money Intent
    # Note here that we can set either the short or long input sats, but not both
    fixed_input_sats: Sats
    fixed_input_side: Side
    oracle: Type[OracleUnit]
    short_leverage: ShortLeverage
    long_leverage: LongLeverage
    start_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch

    # User Intent
    maker_side: Side
    short_mutual_redeem_public_key: PublicKey | '' = ''
    long_mutual_redeem_public_key: PublicKey | '' = ''

    @property
    def proposal(self) -> ContractProposal:
        # 1. Low liquidation price: the low price that triggers liquidation of the Long party.
        # The value is rounded to achieve a result as close as possible to intent.
        # There should be no integer-level loss of precision given the 32-bit range of oracle prices.
        # In order to align with methodology of the canonical anyhedge library,
        # we do an initial step to convert leverage to a price multiplier
        low_liquidation_price_multiplier = 1 - (1 / self.long_leverage)
        low_liquidation_price_oracleUnits_per_bch = ScriptPriceInOracleUnitsPerBch(round_half_up(low_liquidation_price_multiplier * float(self.start_price_oracleUnits_per_bch)))

        # 2. High liquidation price: the high price that triggers liquidation of the Short party.
        # The value is rounded to achieve a result as close as possible to intent.
        # There should be no integer-level loss of precision given the 32-bit range of oracle prices.
        # In order to align with methodology of the canonical anyhedge library,
        # we do an initial step to convert leverage to a price multiplier and detect if this is effectively
        # a simple hedge or not.
        try:
            high_liquidation_price_multiplier = 1 + (1 / (self.short_leverage - 1))
            is_simple_hedge = False
        except ZeroDivisionError:
            high_liquidation_price_multiplier = DEFAULT_HIGH_LIQUIDATION_PRICE_MULTIPLIER_FOR_SIMPLE_HEDGE
            is_simple_hedge = True

        # Use the multiplier to set the price
        high_liquidation_price_oracleUnits_per_bch = ScriptPriceInOracleUnitsPerBch(round_half_up(high_liquidation_price_multiplier * float(self.start_price_oracleUnits_per_bch)))

        # 3. nominal hedge value in asset terms.
        # Departing from the canonical intent derivation, here we calculate nominal hedge from the other parameters available
        if self.fixed_input_side == Side.SHORT:
            # Derive from short input sats
            # Short needs to put in enough to cover movement on the short-losing (price increasing) side of the contract
            #   short_input_sats = cost_sats_for_nominal_value_at_start - cost_sats_for_nominal_value_at_high_liquidation
            # This further depends on whether this is a simple hedge or not as follows
            if is_simple_hedge:
                # For simple hedge, the cost at high liquidation is 0 (price is infinity). Therefore:
                #   short_input_sats = cost_sats_for_nominal_value_at_start
                # Expanding so that we can get at the nominal value
                #   short_input_sats = nominal_oracleUnits_x_satsPerBch / start_price_oracleUnits_per_bch
                #   nominal_oracleUnits_x_satsPerBch = short_input_sats * start_price_oracleUnits_per_bch
                raw_nominal_oracleUnits_x_satsPerBch = self.fixed_input_sats * self.start_price_oracleUnits_per_bch
                nominal_oracleUnits_x_satsPerBch = NominalOracleUnitsXSatsPerBch(round(raw_nominal_oracleUnits_x_satsPerBch))
            else:
                # For a leveraged short, the cost at high liquidation must be included as it is not zero.
                # Expanding so that we can get at the nominal value
                #   short_input_sats = (nominal_oracleUnits_x_satsPerBch / start_price_oracleUnits_per_bch) - (nominal_oracleUnits_x_satsPerBch / high_liquidation_price_oracleUnits_per_bch)
                #   short_input_sats = nominal_oracleUnits_x_satsPerBch (1/start_price_oracleUnits_per_bch - 1/high_liquidation_price_oracleUnits_per_bch)
                #   nominal_oracleUnits_x_satsPerBch = short_input_sats / (1/start_price_oracleUnits_per_bch - 1/high_liquidation_price_oracleUnits_per_bch)
                raw_nominal_oracleUnits_x_satsPerBch = float(self.fixed_input_sats) / ((1 / self.start_price_oracleUnits_per_bch) - (1 / high_liquidation_price_oracleUnits_per_bch))
                nominal_oracleUnits_x_satsPerBch = NominalOracleUnitsXSatsPerBch(round(raw_nominal_oracleUnits_x_satsPerBch))
        else:
            # Derive from long input sats
            # Long needs to put in enough to cover movement on the long-losing (price decreasing) side of the contract
            #   long_input_sats = cost_sats_for_nominal_value_at_low_liquidation - cost_sats_for_nominal_value_at_start
            # Expanding so that we can get at the nominal value
            #   long_input_sats = (nominal_oracleUnits_x_satsPerBch / low_liquidation_price_oracleUnits_per_bch) - (nominal_oracleUnits_x_satsPerBch / start_price_oracleUnits_per_bch)
            #   long_input_sats = nominal_oracleUnits_x_satsPerBch (1/low_liquidation_price_oracleUnits_per_bch - 1/start_price_oracleUnits_per_bch)
            #   nominal_oracleUnits_x_satsPerBch = long_input_sats / (1/low_liquidation_price_oracleUnits_per_bch - 1/start_price_oracleUnits_per_bch)
            raw_nominal_oracleUnits_x_satsPerBch = float(self.fixed_input_sats) / ((1 / low_liquidation_price_oracleUnits_per_bch) - (1 / self.start_price_oracleUnits_per_bch))
            nominal_oracleUnits_x_satsPerBch = NominalOracleUnitsXSatsPerBch(round(raw_nominal_oracleUnits_x_satsPerBch))

        # 5. Cost in sats of the nominal hedge at high liquidation price.
        # This is the value satsForHedgeAtHighLiq in the diagrams above.
        # In summary, this value is needed to calculate Short's payout.
        # Calculation of the value is discontinuous as follows:
        if is_simple_hedge:
            # a) For a simple hedge (short leverage = 1), the value is exactly 0. This
            # represents the concept and calculation that Long must cover the full range
            # of Short payouts from current price to infinity (where the cost becomes zero, this value).
            cost_sats_for_nominal_value_at_high_liquidation = Sats(0)
        else:
            # b) For a leveraged short (short leverage > 1), the value is calculated from the
            # other parameters in a simple cost relationship.
            # Note: cost is floored for safety by bigint division in order to ensure that the
            #       total sats in the contract cover a range that may be at worst +1 or +2 from
            #       the "real" full precision value. This is valuable to ensure that contract
            #       calculations never result in a value more than the total sats available.
            cost_sats_for_nominal_value_at_high_liquidation = Sats(nominal_oracleUnits_x_satsPerBch // high_liquidation_price_oracleUnits_per_bch)

        # 6. Cost in sats of the nominal hedge at low liquidation.
        # This is the value satsForHedgeAtLowLiq in the diagrams above.
        # In summary, this value is needed to calculate total input.
        # Note: Here we use simple integer division and accept the loss of rounding.
        #       Safety is ensured outside the zero case by validation.
        # Note: We do zero testing here because this happens before parameter validation
        #       which would catch it otherwise.
        if low_liquidation_price_oracleUnits_per_bch <= 0:
            raise ValueError('low liquidation price must be greater than zero')
        cost_sats_for_nominal_value_at_low_liquidation = UtxoSats(nominal_oracleUnits_x_satsPerBch // low_liquidation_price_oracleUnits_per_bch)

        # 7. Total input satoshis: the difference between worst case long and short outcomes.
        total_input_sats = UtxoSats(cost_sats_for_nominal_value_at_low_liquidation - cost_sats_for_nominal_value_at_high_liquidation)

        return ContractProposal(
            address='',
            short_mutual_redeem_public_key=self.short_mutual_redeem_public_key,
            long_mutual_redeem_public_key=self.long_mutual_redeem_public_key,
            start_timestamp=self.start_timestamp,
            maturity_timestamp=self.maturity_timestamp,
            nominal_oracleUnits_x_satsPerBch=nominal_oracleUnits_x_satsPerBch,
            cost_sats_for_nominal_value_at_high_liquidation=cost_sats_for_nominal_value_at_high_liquidation,
            total_input_sats=total_input_sats,
            start_price_oracleUnits_per_bch=self.start_price_oracleUnits_per_bch,
            high_liquidation_price_oracleUnits_per_bch=high_liquidation_price_oracleUnits_per_bch,
            low_liquidation_price_oracleUnits_per_bch=low_liquidation_price_oracleUnits_per_bch,
            oracle_public_key=self.oracle.public_key,
            maker_side=self.maker_side,
        )


@dataclass(frozen=True)
class ContractProposal:
    """Details of a proposed contract between a maker and taker. Does not include any funding oriented details such as fees."""
    # Unvalidated items, use empty string when unknown
    address: str
    short_mutual_redeem_public_key: PublicKey | ''
    long_mutual_redeem_public_key: PublicKey | ''

    # Time
    start_timestamp: ScriptTimestamp
    maturity_timestamp: ScriptTimestamp

    # Position settings
    nominal_oracleUnits_x_satsPerBch: NominalOracleUnitsXSatsPerBch
    cost_sats_for_nominal_value_at_high_liquidation: Sats
    total_input_sats: UtxoSats

    # Start price is not an actual contract parameter, but one of start price, leverage,
    # or separated side inputs are needed in order for the contract to be fully specified.
    start_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch

    # Liquidation prices
    high_liquidation_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch
    low_liquidation_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch

    # Price oracle
    oracle_public_key: PublicKey

    # Relationship between Roles and Sides
    maker_side: Side

    def __post_init__(self):
        # Note: can make validation a switch with unsafe construction if needed
        self.validate()

    ###############
    # Parameterized Input Values
    ###############
    @cached_property
    def _input_sats_lookup(self) -> dict[(Role | None, Side | None), UtxoSats | None]:
        # Total sats is a hard contract parameter established by whatever method during construction.
        # Here we split it back into its two parts: short side, and for strict numerical safety, everything else as long side

        # The definition of short's input is that it needs to be enough to fully cover the worst case outcome of selling low
        # and buying high. That amount is the difference between the cost of the nominal assets at short/high liquidation vs
        # the cost at the start price. Note that in our inverted price scheme of BCH/Asset, the lower cost is at the higher price.
        short_input_sats = UtxoSats(self.cost_sats_for_nominal_value_at_start - self.cost_sats_for_nominal_value_at_high_liquidation)

        # Long input sats is everything needed to cover the rest of the total
        long_input_sats = UtxoSats(self.total_input_sats - short_input_sats)

        return {
            (None,       None):       self.total_input_sats,
            (None,       Side.SHORT): short_input_sats,
            (None,       Side.LONG):  long_input_sats,
            (Role.MAKER, None):       short_input_sats if self.maker_side == Side.SHORT else long_input_sats,
            (Role.MAKER, Side.SHORT): short_input_sats if self.maker_side == Side.SHORT else None,
            (Role.MAKER, Side.LONG):  long_input_sats  if self.maker_side == Side.LONG  else None,
            (Role.TAKER, None):       short_input_sats if self.taker_side == Side.SHORT else long_input_sats,
            (Role.TAKER, Side.SHORT): short_input_sats if self.taker_side == Side.SHORT else None,
            (Role.TAKER, Side.LONG):  long_input_sats  if self.taker_side == Side.LONG  else None,
        }

    def input_sats(self, role: Role | None = None, side: Side | None = None) -> UtxoSats:
        key = (role, side)
        value = self._input_sats_lookup[key]
        if value is None:
            raise ValueError(f'mismatch of role and side query ({key}) with actual contract roles (maker={self.maker_side})')
        return value

    def input_oracleUnits(self, role: Role | None = None, side: Side | None = None) -> OracleUnit:
        unit = self.oracle_unit_cls
        bch = self.input_sats(side=side, role=role).bch
        return unit(bch * float(self.start_price_oracleUnits_per_bch))

    ###############
    # Derivative values
    ###############
    @property
    def oracle_unit_cls(self) -> Type[OracleUnit]:
        return oracle_pubkey_to_unit_class[self.oracle_public_key]

    @property
    def duration_seconds(self) -> int:
        return self.maturity_timestamp - self.start_timestamp

    @property
    def effective_nominal_value_oracleUnits(self) -> OracleUnit:
        return self.oracle_unit_cls(self.nominal_oracleUnits_x_satsPerBch / SATS_PER_BCH)

    @property
    def cost_sats_for_nominal_value_at_start(self) -> UtxoSats:
        return UtxoSats(self.nominal_oracleUnits_x_satsPerBch // self.start_price_oracleUnits_per_bch)

    @property
    def effective_short_leverage(self) -> ShortLeverage:
        # There is a special case where even if the liquidation price must be recorded at some max value,
        # The fundamental cost for the position at liquidation is hard-lined at zero. That is the definition
        # of a hard hedge position, emulating the original anyhedge contract behavior.
        if self.cost_sats_for_nominal_value_at_high_liquidation == 0:
            return ShortLeverage(1)

        # Derivation of the calculation:
        #   short liq price = high liq price = start price (1 + 1 / (short leverage - 1))
        #   1 + 1 / (short leverage - 1) = short liq price / start price
        #   1 / (short leverage - 1) = (short liq price / start price) - 1
        #   short leverage - 1 = 1 / ((short liq price / start price) - 1)
        #   short leverage = 1 + 1 / ((short liq price / start price) - 1)
        return ShortLeverage(1 + 1 / (self.high_liquidation_price_oracleUnits_per_bch / self.start_price_oracleUnits_per_bch - 1))

    @property
    def effective_long_leverage(self) -> LongLeverage:
        # Derivation of the calculation:
        #   long liq price = low liq price = start price (1 - 1 / long leverage)
        #   1 - 1 / long leverage = long liq price / start price
        #   1 / long leverage = 1 - (long liq price / start price)
        #   long leverage = 1 / (1 - (long liq price / start price))
        return LongLeverage(1 / (1 - self.low_liquidation_price_oracleUnits_per_bch / self.start_price_oracleUnits_per_bch))

    @property
    def taker_side(self) -> Side:
        return self.maker_side.other_side

    @property
    def short_role(self) -> Role:
        if self.maker_side == Side.SHORT:
            return Role.MAKER
        return Role.TAKER

    @property
    def long_role(self) -> Role:
        if self.maker_side == Side.LONG:
            return Role.MAKER
        return Role.TAKER

    ###############
    # Property access to input sats
    ###############
    @property
    def short_input_sats(self) -> UtxoSats:
        return self.input_sats(side=Side.SHORT)

    @property
    def long_input_sats(self) -> UtxoSats:
        return self.input_sats(side=Side.LONG)

    @property
    def maker_input_sats(self) -> UtxoSats:
        return self.input_sats(role=Role.MAKER)

    @property
    def taker_input_sats(self) -> UtxoSats:
        return self.input_sats(role=Role.TAKER)

    ###############
    # Property access to unit conversions of inputs
    ###############
    @property
    def total_input_oracleUnits(self) -> OracleUnit:
        return self.input_oracleUnits()

    @property
    def short_input_oracleUnits(self) -> OracleUnit:
        return self.input_oracleUnits(side=Side.SHORT)

    @property
    def long_input_oracleUnits(self) -> OracleUnit:
        return self.input_oracleUnits(side=Side.LONG)

    @property
    def maker_input_oracleUnits(self) -> OracleUnit:
        return self.input_oracleUnits(role=Role.MAKER)

    @property
    def taker_input_oracleUnits(self) -> OracleUnit:
        return self.input_oracleUnits(role=Role.TAKER)

    def neutralize(self,
                   current_price_oracleUnitsPerBch: ScriptPriceInOracleUnitsPerBch,
                   current_timestamp: ScriptTimestamp,
                   ) -> ContractProposal:
        neutralizing_proposal = ContractProposal(
            # reset / unimplemented
            address='',

            # update to settlement timing / price
            start_timestamp=current_timestamp,
            start_price_oracleUnits_per_bch=current_price_oracleUnitsPerBch,

            # swap sides
            maker_side=self.taker_side,
            short_mutual_redeem_public_key=self.long_mutual_redeem_public_key,
            long_mutual_redeem_public_key=self.short_mutual_redeem_public_key,

            # the rest remains the same
            maturity_timestamp=self.maturity_timestamp,
            nominal_oracleUnits_x_satsPerBch=self.nominal_oracleUnits_x_satsPerBch,
            cost_sats_for_nominal_value_at_high_liquidation=self.cost_sats_for_nominal_value_at_high_liquidation,
            total_input_sats=self.total_input_sats,
            high_liquidation_price_oracleUnits_per_bch=self.high_liquidation_price_oracleUnits_per_bch,
            low_liquidation_price_oracleUnits_per_bch=self.low_liquidation_price_oracleUnits_per_bch,
            oracle_public_key=self.oracle_public_key,
        )
        return neutralizing_proposal

    def fund(self, fee_agreements: Sequence[FeeAgreement]) -> ContractFunding:
        return ContractFunding(
            base_proposal=self,
            fee_agreements=tuple(fee_agreements),
        )

    def validate(self):
        # There is a separate formal analysis of AnyHedge that identifies a set of input guarantees
        # for which the output is guaranteed to meet certain safety and policy requirements.
        # The formal analysis can be run from here:
        # https://gitlab.com/unauth/contract-validators/-/blob/main/validate-anyhedge-v12.py?ref_type=heads
        # Here we validate the parameters against the result of the analysis.
        # Some validations may be redundant, which is not considered a problem.

        # Positive duration
        if not (self.duration_seconds > 0):
            raise ValueError(f'contract duration must be positive but got {self.duration_seconds}')

        # High liquidation price
        if not (self.start_price_oracleUnits_per_bch < self.high_liquidation_price_oracleUnits_per_bch <= ScriptPriceInOracleUnitsPerBch.largest_allowed()):
            raise ValueError(f'high liquidation price ({self.high_liquidation_price_oracleUnits_per_bch}) must be in the range ({self.start_price_oracleUnits_per_bch}, {ScriptPriceInOracleUnitsPerBch.largest_allowed()}]')

        # Low liquidation price
        if not (1 <= self.low_liquidation_price_oracleUnits_per_bch < self.start_price_oracleUnits_per_bch):
            raise ValueError(f'low liquidation price ({self.low_liquidation_price_oracleUnits_per_bch}) must be in the range [1, {self.start_price_oracleUnits_per_bch})')

        # Compound nominal value
        if not (SATS_PER_BCH <= self.nominal_oracleUnits_x_satsPerBch <= SCRIPT_INT_MAX):
            raise ValueError(f'compound nominal value ({self.nominal_oracleUnits_x_satsPerBch}) must be in the range [{SATS_PER_BCH}, {SCRIPT_INT_MAX}]')

        # Cost for nominal value at high liquidation
        if not (self.cost_sats_for_nominal_value_at_high_liquidation >= 0):
            raise ValueError(f'cost for nominal value at high liquidation ({self.cost_sats_for_nominal_value_at_high_liquidation}) must be zero or greater')

        # Total input sats
        if not (DUST <= self.total_input_sats <= MAX_REASONABLE_SATS):
            raise ValueError(f'compound nominal value ({self.nominal_oracleUnits_x_satsPerBch}) must be in the range [{SATS_PER_BCH}, {SCRIPT_INT_MAX}]')

        # Mixed
        if not (self.nominal_oracleUnits_x_satsPerBch // self.high_liquidation_price_oracleUnits_per_bch >= 1):
            raise ValueError(f'Unexpectedly found nominal composite ({self.nominal_oracleUnits_x_satsPerBch}) and high liquidation price ({self.high_liquidation_price_oracleUnits_per_bch}) that are unable to ensure safe payout.')

        # Mixed
        if not (self.nominal_oracleUnits_x_satsPerBch // self.low_liquidation_price_oracleUnits_per_bch <= MAX_REASONABLE_SATS):
            raise ValueError(f'Unexpectedly found nominal composite ({self.nominal_oracleUnits_x_satsPerBch}) and low liquidation price ({self.low_liquidation_price_oracleUnits_per_bch}) that are unable to ensure safe payout.')

        # Mixed
        if not (self.nominal_oracleUnits_x_satsPerBch // self.high_liquidation_price_oracleUnits_per_bch - self.cost_sats_for_nominal_value_at_high_liquidation >= 0):
            raise ValueError(f'Unexpectedly found nominal composite (${self.nominal_oracleUnits_x_satsPerBch}), high liquidation price (${self.high_liquidation_price_oracleUnits_per_bch}), and nominal cost at high liquidation ({self.cost_sats_for_nominal_value_at_high_liquidation}) that are unable to ensure safe payout.')

        # Mixed
        if not (self.total_input_sats - (self.nominal_oracleUnits_x_satsPerBch // self.low_liquidation_price_oracleUnits_per_bch) + self.cost_sats_for_nominal_value_at_high_liquidation >= 0):
            raise ValueError(f'Unexpectedly found payoutSats ({self.total_input_sats}), nominal composite ({self.nominal_oracleUnits_x_satsPerBch}), low liquidation price ({self.low_liquidation_price_oracleUnits_per_bch}), and nominal cost at high liquidation ({self.cost_sats_for_nominal_value_at_high_liquidation}) that are unable to ensure safe payout.')

        # Policy for minimum calculation precision
        actual_division_precision_steps = self.nominal_oracleUnits_x_satsPerBch // self.high_liquidation_price_oracleUnits_per_bch
        if not (actual_division_precision_steps >= MIN_REASONABLE_DIVISION_STEPS):
            raise ValueError(f'The compound nominal value and high liquidation price are too close to each other: only {actual_division_precision_steps} division steps when {MIN_REASONABLE_DIVISION_STEPS} are required')


@dataclass(frozen=True)
class ContractFunding:
    """Funding details and actions, typically derived from a contract proposal."""
    base_proposal: ContractProposal
    fee_agreements: tuple[FeeAgreement, ...]

    @property
    def fee_sats_to_maker(self) -> Sats:
        return aggregate_fee_sats_to_role(self.fee_agreements, Role.MAKER)

    @property
    def fee_sats_to_taker(self) -> Sats:
        return aggregate_fee_sats_to_role(self.fee_agreements, Role.TAKER)

    @property
    def fee_sats_to_short(self) -> Sats:
        if self.base_proposal.maker_side == Side.SHORT:
            return self.fee_sats_to_maker
        return self.fee_sats_to_taker

    @property
    def fee_sats_to_long(self) -> Sats:
        if self.base_proposal.maker_side == Side.LONG:
            return self.fee_sats_to_maker
        return self.fee_sats_to_taker

    ###############
    # Unit value calculations
    ###############
    @property
    def fee_oracleUnits_to_maker(self) -> OracleUnit:
        fee_bch = self.fee_sats_to_maker.bch
        fee_oracleUnits = self.base_proposal.oracle_unit_cls(fee_bch * float(self.base_proposal.start_price_oracleUnits_per_bch))
        return fee_oracleUnits

    @property
    def fee_oracleUnits_to_taker(self) -> OracleUnit:
        fee_bch = self.fee_sats_to_taker.bch
        fee_oracleUnits = self.base_proposal.oracle_unit_cls(fee_bch * float(self.base_proposal.start_price_oracleUnits_per_bch))
        return fee_oracleUnits

    @property
    def fee_oracleUnits_to_short(self) -> OracleUnit:
        if self.base_proposal.maker_side == Side.SHORT:
            return self.fee_oracleUnits_to_maker
        return self.fee_oracleUnits_to_taker

    @property
    def fee_oracleUnits_to_long(self) -> OracleUnit:
        if self.base_proposal.maker_side == Side.LONG:
            return self.fee_oracleUnits_to_maker
        return self.fee_oracleUnits_to_taker

    ###############
    # Actions
    ###############
    def redeem(self,
               price_timestamp: ScriptTimestamp,
               price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch,
               force_maturity: bool,
               is_mutual_redemption: bool = False,
               fee_agreements: Sequence[FeeAgreement] = tuple(),
               ) -> ContractRedemption:
        """
        Redeem the contract according to market conditions or raise an unredeemable error for invalid conditions.
        Note that is_mutual_redemption takes precedence over force_maturity.
        """
        reached_maturity_time = price_timestamp >= self.base_proposal.maturity_timestamp
        reached_liquidation_price = (
                price_oracleUnits_per_bch <= self.base_proposal.low_liquidation_price_oracleUnits_per_bch
                or
                price_oracleUnits_per_bch >= self.base_proposal.high_liquidation_price_oracleUnits_per_bch
        )

        if is_mutual_redemption:
            # Mutual redemption
            redemption_type = RedemptionType.MUTUAL
        elif reached_maturity_time or force_maturity:
            # Maturation, even in the case of a liquidation price
            redemption_type = RedemptionType.MATURATION
        elif reached_liquidation_price:
            # Liquidation
            redemption_type = RedemptionType.LIQUIDATION
        else:
            raise UnredeemableError

        return ContractRedemption(
            base_funding=self,
            end_price_timestamp=price_timestamp,
            naive_end_price_oracleUnits_per_bch=price_oracleUnits_per_bch,
            redemption_type=redemption_type,
            fee_agreements=tuple(fee_agreements),
        )


@dataclass(frozen=True)
class ContractRedemption:
    """Outcome of a redeemed contract, especially with respect to the two counterparties."""
    base_funding: ContractFunding
    end_price_timestamp: ScriptTimestamp
    naive_end_price_oracleUnits_per_bch: ScriptPriceInOracleUnitsPerBch
    redemption_type: RedemptionType
    fee_agreements: tuple[FeeAgreement, ...]

    ###############
    # Parameterized Payout Values
    ###############
    @cached_property
    def _payout_sats_lookup(self) -> dict[(Role | None, Side | None), UtxoSats | None]:
        # Hedge payout sats is the payout side of the fundamental definition of an AnyHedge contract
        # Note that due to dust safety in the contract, the total actual payout can be greater than total inputs.
        # In reality, the extra dust is covered by an amount sitting on the contract that the contract is not aware of.
        # Use divmod (instead of //) to make it crystal clear this represents integer division of the contract.
        _unsafe_hedge_payout_sats, _ = divmod(self.base_funding.base_proposal.nominal_oracleUnits_x_satsPerBch, self.clamped_end_price_oracleUnits_per_bch)

        # With leveraged shorts, the short is no longer necessarily paying out the full value of the nominal position.
        # If short leverage is not 1, the short only pays up to the planned liquidation point
        unsafe_short_payout_sats = _unsafe_hedge_payout_sats - self.base_funding.base_proposal.cost_sats_for_nominal_value_at_high_liquidation
        short_payout_sats = UtxoSats(max(DUST, unsafe_short_payout_sats))

        # Long Payout Sats
        unsafe_long_payout_sats = self.base_funding.base_proposal.total_input_sats - short_payout_sats
        long_payout_sats = UtxoSats(max(DUST, unsafe_long_payout_sats))

        # Total payout sats is just the combination of short and long
        # Note: This can be different from total input in the case of liquidation where dust protection is pulled in from outside the contract
        # Any extra dust is covered by an amount sitting on the contract's utxo that the contract is not aware of.
        total_payout_sats = UtxoSats(short_payout_sats + long_payout_sats)

        # visual shortcut for the maker/taker sides
        maker_side = self.base_funding.base_proposal.maker_side
        taker_side = self.base_funding.base_proposal.taker_side

        return {
            (None,       None):       total_payout_sats,
            (None,       Side.SHORT): short_payout_sats,
            (None,       Side.LONG):  long_payout_sats,
            (Role.MAKER, None):       short_payout_sats if maker_side == Side.SHORT else long_payout_sats,
            (Role.MAKER, Side.SHORT): short_payout_sats if maker_side == Side.SHORT else None,
            (Role.MAKER, Side.LONG):  long_payout_sats  if maker_side == Side.LONG  else None,
            (Role.TAKER, None):       short_payout_sats if taker_side == Side.SHORT else long_payout_sats,
            (Role.TAKER, Side.SHORT): short_payout_sats if taker_side == Side.SHORT else None,
            (Role.TAKER, Side.LONG):  long_payout_sats  if taker_side == Side.LONG  else None,
        }

    def payout_sats(self, role: Role | None = None, side: Side | None = None) -> UtxoSats:
        key = (role, side)
        value = self._payout_sats_lookup[key]
        if value is None:
            raise ValueError(f'mismatch of role and side query ({key}) with actual contract roles (maker={self.base_funding.base_proposal.maker_side})')
        return value

    def payout_oracleUnits(self, role: Role | None = None, side: Side | None = None) -> OracleUnit:
        unit = self.base_funding.base_proposal.oracle_unit_cls
        bch = self.payout_sats(side=side, role=role).bch
        # NOTE: using actual end price, not clamped, to determine unit value including any potential slippage
        return unit(bch * float(self.naive_end_price_oracleUnits_per_bch))

    ###############
    # Derivative values
    ###############
    @property
    def clamped_end_price_oracleUnits_per_bch(self) -> ScriptPriceInOracleUnitsPerBch:
        return max(self.naive_end_price_oracleUnits_per_bch, self.base_funding.base_proposal.low_liquidation_price_oracleUnits_per_bch)

    @property
    def cost_sats_for_nominal_value_at_redemption(self) -> Sats:
        return Sats(round_half_up(SATS_PER_BCH * (self.base_funding.base_proposal.effective_nominal_value_oracleUnits / float(self.clamped_end_price_oracleUnits_per_bch))))

    ###############
    # Timing
    ###############
    @property
    def real_duration_seconds(self) -> int:
        return self.end_price_timestamp - self.base_funding.base_proposal.start_timestamp

    ###############
    # Property access to payout sats
    ###############
    @property
    def total_payout_sats(self) -> UtxoSats:
        return self.payout_sats()

    @property
    def short_payout_sats(self) -> UtxoSats:
        return self.payout_sats(side=Side.SHORT)

    @property
    def long_payout_sats(self) -> UtxoSats:
        return self.payout_sats(side=Side.LONG)

    @property
    def maker_payout_sats(self) -> UtxoSats:
        return self.payout_sats(role=Role.MAKER)

    @property
    def taker_payout_sats(self) -> UtxoSats:
        return self.payout_sats(role=Role.TAKER)

    ###############
    # Property access to unit conversions of payouts
    ###############
    @property
    def total_payout_oracleUnits(self) -> OracleUnit:
        return self.payout_oracleUnits()

    @property
    def short_payout_oracleUnits(self) -> OracleUnit:
        return self.payout_oracleUnits(side=Side.SHORT)

    @property
    def long_payout_oracleUnits(self) -> OracleUnit:
        return self.payout_oracleUnits(side=Side.LONG)

    @property
    def maker_payout_oracleUnits(self) -> OracleUnit:
        return self.payout_oracleUnits(role=Role.MAKER)

    @property
    def taker_payout_oracleUnits(self) -> OracleUnit:
        return self.payout_oracleUnits(role=Role.TAKER)

    ###############
    # Gains - see funding class for details of fee and gain calculations
    # TODO: These could also be parameterized with a lookup
    ###############
    @property
    def short_gain_sats(self) -> Sats:
        payout_sats = self.short_payout_sats
        input_sats = self.base_funding.base_proposal.short_input_sats
        fee_sats = self.base_funding.fee_sats_to_short + self.fee_sats_to_short
        return Sats(payout_sats - input_sats + fee_sats)

    @property
    def long_gain_sats(self) -> Sats:
        payout_sats = self.long_payout_sats
        input_sats = self.base_funding.base_proposal.long_input_sats
        fee_sats = self.base_funding.fee_sats_to_long + self.fee_sats_to_long
        return Sats(payout_sats - input_sats + fee_sats)

    @property
    def short_gain_oracleUnits(self) -> OracleUnit:
        # Note that this is not the same as (end sats - start sats) * end price.
        # position start value depends on start price
        # position end value, and both fee values (since they are handled in sats) depend on the end price
        # Note that we use naive end price. This represents reality of slippage in liquidations.
        payout_oracleUnits = self.short_payout_oracleUnits
        input_oracleUnits = self.base_funding.base_proposal.short_input_oracleUnits
        fee_oracleUnits = (self.base_funding.fee_sats_to_short.bch * float(self.naive_end_price_oracleUnits_per_bch)) + self.fee_oracleUnits_to_short
        return self.base_funding.base_proposal.oracle_unit_cls(payout_oracleUnits - input_oracleUnits + fee_oracleUnits)

    @property
    def long_gain_oracleUnits(self) -> OracleUnit:
        # Note that this is not the same as (end sats - start sats) * end price.
        # position start value depends on start price
        # position end value, and both fee values (since they are handled in sats) depend on the end price
        # Note that we use naive end price. This represents reality of slippage in liquidations.
        payout_oracleUnits = self.long_payout_oracleUnits
        input_oracleUnits = self.base_funding.base_proposal.long_input_oracleUnits
        fee_oracleUnits = (self.base_funding.fee_sats_to_long.bch * float(self.naive_end_price_oracleUnits_per_bch)) + self.fee_oracleUnits_to_long
        return self.base_funding.base_proposal.oracle_unit_cls(payout_oracleUnits - input_oracleUnits + fee_oracleUnits)

    ###############
    # Relative gains
    ###############
    @property
    def short_gain_percent_of_own_input(self) -> float:
        return 100.0 * float(self.short_gain_sats) / float(self.base_funding.base_proposal.short_input_sats)

    @property
    def long_gain_percent_of_own_input(self) -> float:
        return 100.0 * float(self.long_gain_sats) / float(self.base_funding.base_proposal.long_input_sats)

    ###############
    # Sided views on gains
    ###############
    @property
    def maker_gain_sats(self) -> Sats:
        if self.base_funding.base_proposal.maker_side == Side.SHORT:
            return self.short_gain_sats
        return self.long_gain_sats

    @property
    def taker_gain_sats(self) -> Sats:
        if self.base_funding.base_proposal.taker_side == Side.SHORT:
            return self.short_gain_sats
        return self.long_gain_sats

    @property
    def maker_gain_oracleUnits(self) -> OracleUnit:
        if self.base_funding.base_proposal.maker_side == Side.SHORT:
            return self.short_gain_oracleUnits
        return self.long_gain_oracleUnits

    @property
    def taker_gain_oracleUnits(self) -> OracleUnit:
        if self.base_funding.base_proposal.taker_side == Side.SHORT:
            return self.short_gain_oracleUnits
        return self.long_gain_oracleUnits

    @property
    def maker_gain_percent_of_own_input(self) -> float:
        if self.base_funding.base_proposal.maker_side == Side.SHORT:
            return self.short_gain_percent_of_own_input
        return self.long_gain_percent_of_own_input

    @property
    def taker_gain_percent_of_own_input(self) -> float:
        if self.base_funding.base_proposal.taker_side == Side.SHORT:
            return self.short_gain_percent_of_own_input
        return self.long_gain_percent_of_own_input

    ###############
    # Redemption Fees (Especially for early redemption)
    ###############
    @property
    def fee_sats_to_maker(self) -> Sats:
        return aggregate_fee_sats_to_role(self.fee_agreements, Role.MAKER)

    @property
    def fee_sats_to_taker(self) -> Sats:
        return aggregate_fee_sats_to_role(self.fee_agreements, Role.TAKER)

    @property
    def fee_sats_to_short(self) -> Sats:
        if self.base_funding.base_proposal.maker_side == Side.SHORT:
            return self.fee_sats_to_maker
        return self.fee_sats_to_taker

    @property
    def fee_sats_to_long(self) -> Sats:
        if self.base_funding.base_proposal.maker_side == Side.LONG:
            return self.fee_sats_to_maker
        return self.fee_sats_to_taker

    ###############
    # Unit value of fees
    ###############
    @property
    def fee_oracleUnits_to_maker(self) -> OracleUnit:
        fee_bch = self.fee_sats_to_maker.bch
        # NOTE: using actual end price, not clamped, to determine unit value including any potential slippage
        fee_oracleUnits = self.base_funding.base_proposal.oracle_unit_cls(fee_bch * float(self.naive_end_price_oracleUnits_per_bch))
        return fee_oracleUnits

    @property
    def fee_oracleUnits_to_taker(self) -> OracleUnit:
        fee_bch = self.fee_sats_to_taker.bch
        # NOTE: using actual end price, not clamped, to determine unit value including any potential slippage
        fee_oracleUnits = self.base_funding.base_proposal.oracle_unit_cls(fee_bch * float(self.naive_end_price_oracleUnits_per_bch))
        return fee_oracleUnits

    @property
    def fee_oracleUnits_to_short(self) -> OracleUnit:
        if self.base_funding.base_proposal.maker_side == Side.SHORT:
            return self.fee_oracleUnits_to_maker
        return self.fee_oracleUnits_to_taker

    @property
    def fee_oracleUnits_to_long(self) -> OracleUnit:
        if self.base_funding.base_proposal.maker_side == Side.LONG:
            return self.fee_oracleUnits_to_maker
        return self.fee_oracleUnits_to_taker
