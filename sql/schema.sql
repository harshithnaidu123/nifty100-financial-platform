CREATE TABLE dim_company (
    symbol VARCHAR(20) PRIMARY KEY,
    company_name TEXT,
    sector TEXT
);

CREATE TABLE fact_profit_loss (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    year VARCHAR(20),
    sales NUMERIC,
    net_profit NUMERIC,
    net_profit_margin_pct NUMERIC
);

CREATE TABLE fact_balance_sheet (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    year VARCHAR(20),
    borrowings NUMERIC,
    reserves NUMERIC,
    debt_to_equity NUMERIC
);

CREATE TABLE fact_cash_flow (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20),
    year VARCHAR(20),
    operating_activity NUMERIC,
    investing_activity NUMERIC,
    free_cash_flow NUMERIC
);