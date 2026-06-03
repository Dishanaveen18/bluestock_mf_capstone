-- sql/queries.sql

-- 1. Identify Top 5 Funds by Highest Assets Under Management (AUM) Value
SELECT amfi_code, scheme_name, fund_house, aum_crore 
FROM dim_fund 
ORDER BY aum_crore DESC 
LIMIT 5;

-- 2. Calculate the average NAV per fund scheme across months
SELECT amfi_code, STRFTIME('%Y-%m', nav_date) AS nav_month, AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, nav_month
ORDER BY nav_month DESC
LIMIT 10;

-- 3. Total Transaction Inflow Value Broken Down by Investment Type
SELECT transaction_type, COUNT(*) as total_count, SUM(amount) AS total_inflow_value
FROM fact_transactions
GROUP BY transaction_type;

-- 4. Geographical distribution profile of transaction metrics ordered by volume count
SELECT state, COUNT(*) as transaction_count, SUM(amount) as transactional_volume_spent
FROM fact_transactions
GROUP BY state
ORDER BY transaction_count DESC;

-- 5. Track fund schemes filtering for low overhead expense options
SELECT f.amfi_code, f.scheme_name, p.expense_ratio 
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;