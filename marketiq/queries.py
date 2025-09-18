MONTHLY_KPIS = '''
SELECT date(date_trunc) AS month,
       SUM(revenue) AS revenue,
       COUNT(*) AS orders,
       COUNT(DISTINCT customer_id) AS customers,
       AVG(revenue) AS aov
FROM v_sales_monthly
WHERE date_trunc BETWEEN :start AND :end
GROUP BY 1
ORDER BY 1;
'''

CHANNEL_SHARE = '''
SELECT channel_name, SUM(revenue) AS revenue
FROM v_sales
WHERE date_id BETWEEN :start AND :end
GROUP BY 1 ORDER BY 2 DESC;
'''

TOP_PRODUCTS = '''
SELECT product_id, category, subcategory, SUM(revenue) AS revenue
FROM v_sales
WHERE date_id BETWEEN :start AND :end
GROUP BY 1,2,3 ORDER BY revenue DESC LIMIT 15;
'''
