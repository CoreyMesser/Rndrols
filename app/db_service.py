from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
import re
import pandas as pd
import numpy as np
from matplotlib import pyplot as mp

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

    def __init__(self):
        self.db = db_session()

    def summarize_stats(self, stats):
        pass

    def db_get_avg(self):
        pass

    def db_get_min_man(self):
        pass


class DataRetrieval(object):

    def __init__(self):
        self.ds = Stats()

    def parse_str_int_list(self, str_list):
        int_list = []
        for x in str_list:
            int_list.append(int(x))
        return int_list

    def df_plot_rolls(self, session_id):
        ses_df = self.df_get_session(session_id)
        plot_dict = {}
        sc = 0
        for index, row in ses_df.iterrows():
            x = str(row['num_dice']) + 'd' + str(row['num_sides']) + f'(set{str(sc)})'
            rolls_list = re.findall(r"\d{1,3}", row['rolls'])
            y = self.parse_str_int_list(str_list=rolls_list)
            sc += 1
            plot_dict[x] = y
        plot_dict_df = pd.DataFrame(plot_dict)
        plot_dict_df.plot(x='5d4(set1)', y=['1d20(set3)'], kind='line')
        mp.show()
        return ses_df

    def df_plot_avg_vs_num_dice(self, session_id):
        ses_df = self.df_get_session(session_id)
        ses_df.plot(x=['avg_num'], y=['num_dice'],kind='scatter')
        mp.show()
        return "[PLOT AVG] Success"

    def df_plot_max_thresh_vs_num_dice(self, session_id):
        ses_df = self.df_get_session(session_id)
        ses_df.plot(x='num_dice', y=['max_thresh', 'min_thresh'], kind='bar')
        mp.show()
        return "[PLOT MAX THRESH] Success"

    def collate_rolls(self, rolls_list):
        pass

    def summarize_stats(self, session_id):
        sc = 0
        ses_df = self.df_get_session(session_id=session_id)
        summary = {}
        for index, row in ses_df.iterrows():
            x = str(row['num_dice']) + 'd' + str(row['num_sides']) + f'(set{str(sc)})'
            summary[x] = {'session': session_id,
                          'num_rolls': row['num_rolls'],
                          'max_num': row['max_num'],
                          'min_num': row['min_num'],
                          'avg_num': row['avg_num'],
                          'max_thresh': row['max_thresh'],
                          'min_thresh': row['min_thresh'],
                          'avg_thresh': row['avg_thresh']}
            sc += 1
        return summary

    def df_get_session(self, session_id):
        sql = f"""SELECT * FROM dices WHERE session_id = {session_id} ORDER BY num_sides"""
        ses_df = pd.read_sql(sql=sql, con=conn)
        return ses_df

    def dump_to_csv(self, session_id):
        ses_df = self.df_get_session(session_id=session_id)
        ses_df.to_csv(f'../../dices_session{session_id}')
        return "[CSV]Your nerd numbers have been exported!"
