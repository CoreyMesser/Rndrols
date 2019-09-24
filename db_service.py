from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgres://localhost/rndrols")
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))
conn = engine.connect()
db_session = sessionmaker(bind=engine)

conn.execute("""CREATE TABLE IF NOT EXISTS dices (
  id INT PRIMARY KEY,
  num_dice INT,
  num_sides INT,
  num_rolls INT,
  rolls TEXT,
  max_num INT,
  min_num INT,
  max_thresh INT,
  avg_num INT
)""")