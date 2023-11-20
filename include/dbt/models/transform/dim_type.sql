WITH type_cte AS(
    SELECT DISTINCT
        {{ dbt_utils.generate_surrogate_key(['type1', 'type2']) }} AS dim_type_key,
        type1 AS primary_type,
        type2 AS secondary_type
    FROM {{ source('pokemon','pokemon') }}
)
SELECT *
FROM type_cte