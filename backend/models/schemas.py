from pydantic import BaseModel
from typing import List, Optional

# --- PYG ---
class PYGYearProjection(BaseModel):
    year: int
    revenue: float
    cogs: float
    gross_profit: float
    operating_expenses: float
    ebit: float
    tax: float
    net_income: float
    net_margin: float

class PYGProjectionInput(BaseModel):
    current_revenue: float
    revenue_growth_rate: float
    cogs_as_percent_of_revenue: float
    operating_expenses: float
    tax_rate: float
    years: int

class PYGProjectionOutput(BaseModel):
    summary: str
    projections: List[PYGYearProjection]

# --- Cash Flow ---
class CashFlowYearProjection(BaseModel):
    year: int
    beginning_cash: float
    cash_from_operations: float
    cash_from_investing: float
    cash_from_financing: float
    ending_cash: float
    free_cash_flow: float

class CashFlowProjectionInput(BaseModel):
    pyg_assumptions: PYGProjectionInput
    working_capital_percent_of_revenue: float
    initial_cash_balance: float
    depreciation_rate: float
    capex_per_year: float
    debt_issued_per_year: float
    debt_repayment_per_year: float

class CashFlowProjectionOutput(BaseModel):
    summary: str
    years: List[CashFlowYearProjection]

# --- Financial Health ---
class FinancialIndicatorYear(BaseModel):
    year: int
    revenue: float
    net_income: float
    free_cash_flow: float
    operating_cash_flow: float
    ebit_margin: Optional[float]
    net_margin: Optional[float]
    fcf_to_revenue: Optional[float]
    ocf_to_net_income: Optional[float]

class FinancialHealthOutput(BaseModel):
    summary: str
    recommendations: List[str]
    indicators: List[FinancialIndicatorYear]
