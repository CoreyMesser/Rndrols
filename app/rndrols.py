import random
import re

from db_service import db_session, get_session_id
from logger import LoggerService
from models import Dice

ls = LoggerService()
_log = ls.get_logger()


class MinMaxDie(object):

    def dice_n_sides(self, num_dice, num_side, num_rolls):
        """
        Rolls dice groups returns a dict of values
        :param num_dice:
        :param num_side:
        :param num_rolls:
        :return:
        """
        rolls = []
        a = num_rolls
        while a > 0:
            die_grp = []
            b = num_dice
            while b > 0:
                die_grp.append(random.randint(1, num_side))
                b -= 1
            rolls.append(sum(die_grp))
            a -= 1
        return {'rolls': rolls, 'num_dice': num_dice, 'num_side': num_side, 'num_rolls': num_rolls}

    def rolls_db_service(self, rolls, session_id):
        """
        Unpacks dict from dice_n_sides and does a few minor mediation calculations before submitting to db
        :param session_id:
        :param rolls:
        :return:
        """
        db = db_session()
        di = Dice()
        di.session_id = session_id
        di.num_dice = rolls['num_dice']
        di.num_sides = rolls['num_side']
        di.num_rolls = rolls['num_rolls']
        di.rolls = rolls['rolls']
        di.max_num = max(rolls['rolls'])
        di.min_num = min(rolls['rolls'])
        avg = sum(rolls['rolls'])/len(rolls['rolls'])
        di.avg_num = avg
        di.max_thresh = rolls['rolls'].count(rolls['num_side'] * rolls['num_dice'])
        di.min_thresh = rolls['rolls'].count(rolls['num_dice'])
        di.avg_thresh = rolls['rolls'].count(int(avg))
        db.add(di)
        db.commit()

    def dice_roller(self, dice_bag, num_rolls, session_id):
        """
        :param dice_bag:
        :param num_rolls:
        :param session_id:
        :return:
        """
        for dice in dice_bag:
            _log.info("[DICE ROLLER]Rolling...")
            rolls = self.dice_n_sides(num_dice=dice[0], num_side=dice[1], num_rolls=num_rolls)
            self.rolls_db_service(rolls=rolls, session_id=session_id)

    def get_avg(self):
        pass

    def parse_request(self, req_dict):
        d_list = re.findall(r"\d{1,10}.\d{1,10}", req_dict['body']['dice_bag'])
        dice_bag = []
        for dice in d_list:
            d = (dice.split(','))
            dice_bag.append([int(d[0]), int(d[1])])
        return {'dice_bag': dice_bag,
                'num_rolls': int(req_dict['body']['num_rolls']),
                'data_set': int(req_dict['body']['data_set'])}

    def dice_dict(self, dice):
        try:
            if len(dice) < 1:
                return {
                    'dice_bag': [[1, 12], [2, 6], [3, 4], [6, 2]],
                    'num_rolls': 1000000,
                    'data_set': 10
                }
            else:
                return dice
        except Exception as e:
            _log.error(f"[DICE DICT][ERROR] You rolled a Nat 1 : {e}")

    def dice_loop(self, dice):
        dice = self.parse_request(req_dict=dice)
        dice = self.dice_dict(dice=dice)
        session_id = get_session_id()
        try:
            _log.info('Rolling polyhedrons...')
            z = int(dice['data_set'])
            while z > 0:
                _log.info(f'[DICE LOOP]Rolling set {z}...')
                self.dice_roller(dice_bag=dice['dice_bag'], num_rolls=dice['num_rolls'], session_id=session_id)
                z -= 1
            _log.info('Rolling completed... NERD!')
        except Exception as e:
            _log.error(f"[DICE LOOP][ERROR] You rolled a Nat 1 : {e}")
