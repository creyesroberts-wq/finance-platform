from backend.models.schemas import (
    PYGProjectionInput, PYGProjectionOutput, PYGYearProjection,
    CashFlowProjectionInput, CashFlowProjectionOutput, CashFlowYearProjection,
    FinancialHealthOutput, FinancialIndicatorYear
)
from statistics import mean

def build_pyg_projection(data: PYGProjectionInput) -> PYGProjectionOutput:
    projections = []
    revenue = data.current_revenue
    for i in range(1, data.years + 1):
        year_revenue = revenue * (1 + data.revenue_growth_rate) if i == 1 else projections[-1].revenue * (1 + data.revenue_growth_rate)
        year_cogs = year_revenue * data.cogs_as_percent_of_revenue
        gross_profit = year_revenue - year_cogs
        opex = data.operating_expenses
        ebit = gross_profit - opex
        tax = max(0, ebit * data.tax_rate)
        net_income = ebit - tax
        net_margin = net_income / year_revenue if year_revenue > 0 else 0
        projections.append(PYGYearProjection(
            year=i,
            revenue=round(year_revenue, 2),
            cogs=round(year_cogs, 2),
            gross_profit=round(gross_profit, 2),
            operating_expenses=round(opex, 2),
            ebit=round(ebit, 2),
            tax=round(tax, 2),
            net_income=round(net_income, 2),
            net_margin=round(net_margin, 4)
        ))
    summary = f"Projected revenue grows from {projections[0].revenue} to {projections[-1].revenue} over {data.years} years."
    return PYGProjectionOutput(summary=summary, projections=projections)

def build_cash_flow_projection(data: CashFlowProjectionInput) -> CashFlowProjectionOutput:
    pyg_output = build_pyg_projection(data.pyg_assumptions)
    years_cf = []
    prev_wc = data.working_capital_percent_of_revenue * data.pyg_assumptions.current_revenue
    cash = data.initial_cash_balance
    for pyg_year in pyg_output.projections:
        bc = cash
        wc = data.working_capital_percent_of_revenue * pyg_year.revenue
        delta_wc = wc - prev_wc
        dep = data.depreciation_rate * pyg_year.revenue
        cfo = pyg_year.net_income + dep - delta_wc
        cfi = -data.capex_per_year
        cff = data.debt_issued_per_year - data.debt_repayment_per_year
        ec = bc + cfo + cfi + cff
        fcf = cfo + cfi
        years_cf.append(CashFlowYearProjection(
            year=pyg_year.year,
            beginning_cash=round(bc, 2),
            cash_from_operations=round(cfo, 2),
            cash_from_investing=round(cfi, 2),
            cash_from_financing=round(cff, 2),
            ending_cash=round(ec, 2),
            free_cash_flow=round(fcf, 2)
        ))
        cash = ec
        prev_wc = wc
    summary = f"Cash balance evolves from {years_cf[0].beginning_cash} to {years_cf[-1].ending_cash}."
    return CashFlowProjectionOutput(summary=summary, years=years_cf)

def build_financial_health_analysis(data: CashFlowProjectionInput) -> FinancialHealthOutput:
    pyg = build_pyg_projection(data.pyg_assumptions)
    cf = build_cash_flow_projection(data)
    indicators = []
    for pyg_year, cf_year in zip(pyg.projections, cf.years):
        ebit_margin = pyg_year.ebit / pyg_year.revenue if pyg_year.revenue > 0 else None
        net_margin = pyg_year.net_income / pyg_year.revenue if pyg_year.revenue > 0 else None
        fcf_to_rev = cf_year.free_cash_flow / pyg_year.revenue if pyg_year.revenue > 0 else None
        ocf_to_net = cf_year.cash_from_operations / pyg_year.net_income if pyg_year.net_income != 0 else None
        indicators.append(FinancialIndicatorYear(
            year=pyg_year.year,
            revenue=round(pyg_year.revenue, 2),
            net_income=round(pyg_year.net_income, 2),
            free_cash_flow=round(cf_year.free_cash_flow, 2),
            operating_cash_flow=round(cf_year.cash_from_operations, 2),
            ebit_margin=round(ebit_margin, 4) if ebit_margin else None,
            net_margin=round(net_margin, 4) if net_margin else None,
            fcf_to_revenue=round(fcf_to_rev, 4) if fcf_to_rev else None,
            ocf_to_net_income=round(ocf_to_net, 4) if ocf_to_net else None
        ))
    avg_net = mean([i.net_margin for i in indicators if i.net_margin is not None])
    avg_fcf = mean([i.fcf_to_revenue for i in indicators if i.fcf_to_revenue is not None])
    risk = "high" if avg_fcf < 0 else "medium" if avg_fcf < 0.05 else "low"
    recs = []
    if avg_net < 0.05:
        recs.append("Review pricing and expenses.")
    if avg_fcf < 0.03:
        recs.append("Optimize working capital and CAPEX.")
    if any(y.ending_cash < 0 for y in cf.years):
        recs.append("Evaluate short-term financing.")
    if not recs:
        recs.append("Company shows healthy cash generation.")
    summary = f"Average net margin: {avg_net:.2%}, free cash flow: {avg_fcf:.2%}, risk: {risk}"
    return FinancialHealthOutput(summary=summary, recommendations=recs, indicators=indicators)
