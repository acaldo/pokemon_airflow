SELECT
    t.primary_type,
    t.secondary_type,
    COUNT(t.pokemon_id) AS full_type
FROM {{ ref('dim_type') }} t 
GROUP BY t.primary_type, t.secondary_type
ORDER BY full_type DESC
LIMIT 10