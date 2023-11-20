WITH fct_pokemon_cte AS (
    SELECT
        id,
        name,
        weight,
        height,
        type1,
        type2,
        hp + attack + defense + sp_atk + sp_def + speed AS total
    FROM {{ source('pokemon', 'pokemon') }}
)
SELECT DISTINCT
    pi.id,
    pi.name,
    pi.weight,
    pi.height,
    pi.total,
    t.dim_type_key,
    s.dim_stats_key,
    m.dim_move_key,
    s.gender_rate,
    s.base_happiness,
    s.is_baby,
    s.is_legendary,
    s.is_mythical,
    s.hatch_counter
FROM fct_pokemon_cte pi
INNER JOIN {{ ref('dim_type') }} t ON t.primary_type = pi.type1 AND (t.secondary_type = pi.type2 OR (t.secondary_type IS NULL AND pi.type2 IS NULL))
INNER JOIN {{ ref('dim_stats') }} s ON s.pokemon_id = pi.id
INNER JOIN {{ ref('dim_move') }} m on m.pokemon_id = pi.id
INNER JOIN {{ source('pokemon', 'species') }} s ON pi.id = s.id