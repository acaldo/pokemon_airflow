WITH MovesData AS (
  SELECT
    id ,
    JSON_EXTRACT_ARRAY(moves, '$') AS moves_array
    FROM {{ source('pokemon','pokemon') }}
), 
move_cte AS(
    SELECT
    id AS pokemon_id,
    JSON_EXTRACT_SCALAR(move, '$.move') AS move,
    JSON_EXTRACT_SCALAR(move, '$.url') AS url,
    JSON_EXTRACT_SCALAR(move, '$.id') AS id
    FROM
    MovesData,
    UNNEST(moves_array) AS move
)
SELECT 
     {{ dbt_utils.generate_surrogate_key(['pokemon_id']) }} AS dim_move_key,
    pokemon_id,
    move,
    url,
    id
    FROM move_cte