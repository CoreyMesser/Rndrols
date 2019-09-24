CREATE TABLE IF NOT EXISTS dices
(
    id SERIAL PRIMARY KEY NOT NULL,
    num_dice   INT,
    num_sides  INT,
    num_rolls  INT,
    rolls      TEXT,
    max_num    INT,
    min_num    INT,
    max_thresh INT,
    avg_num    INT
)


