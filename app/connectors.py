from rndrols import MinMaxDie as mmd, dice_loop
from logger import LoggerService as ls

_log = ls.get_logger()


def rolldice(dice: dict):
    return mmd.dice_loop(dice=dice)
