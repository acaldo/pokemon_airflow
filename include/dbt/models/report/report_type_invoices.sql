SELECT
    t.type1,
    t.type2
    COUNT(pi.dim_move_type) AS full_type
FROM {{ ref('fct_pokemon') }} pi
JOIN {{ ref('dim_type') }} t on pi.dim_move_type = t.dim_move_type
GROUP BY t.type1, t.type2
ORDER BY full_type DESC
LIMIT 10