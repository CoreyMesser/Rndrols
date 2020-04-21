CREATE TABLE IF NOT EXISTS dices
(
    id SERIAL PRIMARY KEY NOT NULL,
    session_id INT,
    num_dice   INT,
    num_sides  INT,
    num_rolls  INT,
    rolls      TEXT,
    max_num    INT,
    min_num    INT,
    avg_num    INT,
    max_thresh INT,
    min_thresh INT,
    avg_thresh INT
)


