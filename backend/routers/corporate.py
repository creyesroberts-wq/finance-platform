from fastapi import APIRouter
from backend.models.schemas import (
    PYGProjectionInput,
    PYGProjectionOutput,
    CashFlowProjectionInput,
    CashFlowProjectionOutput,
    FinancialHealthOutput
)
from backend.core.calculations_corporate import (
    build_pyg_projection,
    build_cash_flow_projection,
    build_financial_health_analysis
)

router = APIRouter()

@router.post("/pyg-projection", response_model=PYGProjectionOutput)
def pyg_projection(input_data: PYGProjectionInput):
    return build_pyg_projection(input_data)

@router.post("/cash-flow-projection", response_model=CashFlowProjectionOutput)
def cash_flow_projection(input_data: CashFlowProjectionInput):
    return build_cash_flow_projection(input_data)

@router.post("/financial-health", response_model=FinancialHealthOutput)
def financial_health_analysis(input_data: CashFlowProjectionInput):
    return build_financial_health_analysis(input_data)
