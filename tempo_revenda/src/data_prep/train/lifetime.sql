SELECT T1.*

FROM (

    SELECT T1.*,
        julianday(date(order_approved_at)) - julianday(date(last_sale)
            ) AS resale_time,
        row_number() over(
            partition BY T1.seller_id, T1. product_category_name
            ORDER BY random()
            ) as random

    FROM(

        SELECT T2.seller_id,
            T3.product_category_name,
            T1.order_approved_at,
            lag(T1.order_approved_at) over(
                partition BY T2.seller_id, T3.product_category_name
                ORDER BY T1.order_approved_at
                ) AS last_sale

        FROM tb_orders AS T1

        LEFT JOIN tb_order_items AS T2
        ON T1.order_id = T2.order_id

        LEFT JOIN tb_products AS T3
        ON T2.product_id = T3.product_id

        WHERE T2.seller_id IS NOT NULL
        and T3.product_category_name IS NOT NULL

        ORDER BY T2.seller_id, T1.order_approved_at

    ) AS T1

    WHERE T1.last_sale IS NOT NULL
    AND julianday(date(order_approved_at)) - julianday(date(last_sale)) >= 1

) AS T1

WHERE random = 1