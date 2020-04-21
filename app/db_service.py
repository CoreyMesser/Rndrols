from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgres:///rndrolls")
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))
conn = engine.connect()
db_session = sessionmaker(bind=engine)

conn.execute("""CREATE TABLE IF NOT EXISTS dices
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
""")


def get_session_id():
    db = db_session()
    session_id = db.execute("""
    SELECT MAX(session_id) FROM dices""")
    try:
        ses_id = parse_resultsproxy_to_dict(result=session_id)
        ses_id = ses_id[0]['max']
        ses_id += 1
        return ses_id
    except TypeError:
        session_id = 0
        return session_id


def parse_resultsproxy_to_dict(result):
    d, a = {}, []
    for rowproxy in result:
        for column, value in rowproxy.items():
            d = {**d, **{column: value}}
        a.append(d)
    return a

class Stats(object):

    def db_get_avg(self):
        pass

    def db_get_min_man(self):
        pass
