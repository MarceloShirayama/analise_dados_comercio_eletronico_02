/*
Regra de Negócio

BB - baixo valor e baixa frequência
AV - alto valor
AF - alta frequência
P - produtivo
SP - Super produtivo 

I - Início
R - Retenção
A - Ativo
*/


SELECT T1.*,
    CASE
        WHEN pct_receita <= 0.5 AND pct_freq <= 0.5 THEN 'BB'
        WHEN pct_receita > 0.5 AND pct_freq <= 0.5 THEN 'AV'
        WHEN pct_receita <= 0.5 AND pct_freq > 0.5 THEN 'AF'
        WHEN pct_receita < 0.9 OR pct_freq < 0.9 THEN 'P'
        ELSE 'SP'
    END AS segmento_valor_freq,

    CASE
        WHEN qtde_dias_base <= 60 THEN 'I'
        WHEN qtde_dias_ult_venda >= 300 THEN 'R'
        ELSE 'A'
    END AS segmento_vida,

    '{date_end}' AS dt_sgmt

FROM(

    SELECT T1.*,
        percent_rank() over(ORDER BY receita_total)
            AS pct_receita,
        percent_rank() over(ORDER BY qtde_pedidos)
            AS pct_freq

    FROM(

        SELECT T2.seller_id,
            sum(T2.price) AS receita_total,
            count(T1.order_id) AS qtde_pedidos,
            count(T2.product_id) AS qtde_produtos,
            count(DISTINCT T2.product_id) AS qtde_prod_dist,
            min(CAST(julianday('{date_end}') 
                - julianday(T1.order_approved_at) AS Int))
                AS qtde_dias_ult_venda,
            max(T1.order_approved_at) AS dt_ult_venda,
            min(CAST(julianday('{date_end}') 
                - julianday(dt_inicio) AS Int))
                AS qtde_dias_base

        FROM tb_orders AS T1

        LEFT JOIN tb_order_items AS T2
        ON T1.order_id = T2.order_id

        LEFT JOIN(
            SELECT T2.seller_id,
                min(date(T1.order_approved_at))
                AS dt_inicio
            FROM tb_orders AS T1
            LEFT JOIN tb_order_items AS T2
            ON T1.order_id = T2.order_id
            GROUP BY T2.seller_id
        ) AS T3
        ON T2.seller_id = T3.seller_id

        WHERE T1.order_approved_at 
        BETWEEN '{date_init}' 
        AND '{date_end}'

        GROUP BY T2.seller_id
    ) AS T1
) AS T1

WHERE seller_id IS NOT NULL
