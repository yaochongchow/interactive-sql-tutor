SELECT
    employee_id,
    product_id,
    sales
FROM
    Sales AS s
WHERE
    product_id = (
        SELECT product_id
        FROM Sales
        WHERE employee_id = s.employee_id
        AND Sales = (
            SELECT MAX(sales)
            FROM Sales
            WHERE employee_id = s.employee_id
        )
        ORDER BY product_id ASC
        LIMIT 1
    )
ORDER BY
    employee_id ASC;