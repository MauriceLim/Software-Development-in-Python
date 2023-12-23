"""Pydantic models for you to work with"""

from enum import Enum

from pydantic import BaseModel


class BenefitTypeEnum(str, Enum):
    PRINCIPAL_BACK = "PRINCIPAL_BACK"
    FOR_LIFE = "FOR_LIFE"


class RatchetTypeEnum(str, Enum):
    NO_RATCHET = "NO_RATCHET"
    CONSTANT = "CONSTANT"


class MortalityTable(BaseModel):
    qx: list[float]


class ScenarioParameters(BaseModel):
    risk_free_rate: float
    dividend_yield: float
    volatility: float


class PolicyholderRecord(BaseModel):
    id: int
    issue_age: int
    initial_premium: float
    fee_pct_av: float
    benefit_type: BenefitTypeEnum
    ratchet_type: RatchetTypeEnum
    guarantee_wd_rate: float


class ProjectionAssumptions(BaseModel):
    mortality_multiplier: float
    wd_age: float
    min_wd_delay: float


class ProjectionParameters(BaseModel):
    proj_periods: int
    num_paths: int
    seed: int
