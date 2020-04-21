from rndrols import MinMaxDie
from logger import LoggerService

ls = LoggerService()
_log = ls.get_logger()


def rolldice(**kwargs):
    mmd = MinMaxDie()
    return mmd.dice_loop(dice=kwargs)


def get_avg(session_id):
    pass


def get_min_max(session_id):
    pass
