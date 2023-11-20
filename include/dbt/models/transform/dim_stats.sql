WITH stat_cte AS(
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed']) }} AS dim_stats_key,
        id as pokemon_id,
        hp, 
        attack, 
        defense,
        sp_atk,
        sp_def,
        speed
    FROM {{ source('pokemon','pokemon') }}
)
SELECT *
FROM stat_cte