from rndrols import MinMaxDie
from logger import LoggerService
from db_service import DataRetrieval

ls = LoggerService()
_log = ls.get_logger()

dr = DataRetrieval()

def rolldice(**kwargs):
    mmd = MinMaxDie()
    return mmd.dice_loop(dice=kwargs)


def get_summary(session_id):
    return dr.summarize_stats(session_id=session_id)


def get_avg(session_id):
    return dr.df_plot_avg_vs_num_dice(session_id=session_id)


def get_min_max(session_id):
    return dr.df_plot_max_thresh_vs_num_dice(session_id=session_id)


def export_session_to_csv(session_id):
    return dr.dump_to_csv(session_id)
