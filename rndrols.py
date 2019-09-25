import random
from db_service import db_session
from models import Dice

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

    def rolls_db_service(self, rolls):
        """
        Unpacks dict from dice_n_sides and does a few minor mediation calculations before submitting to db
        :param rolls:
        :return:
        """
        db = db_session()
        di = Dice()
        di.num_dice = rolls['num_dice']
        di.num_sides = rolls['num_side']
        di.num_rolls = rolls['num_rolls']
        di.rolls = rolls['rolls']
        di.max_num = max(rolls['rolls'])
        di.min_num = min(rolls['rolls'])
        di.avg_num = sum(rolls['rolls'])/len(rolls['rolls'])
        di.max_thresh = rolls['rolls'].count(max(rolls['rolls']))
        db.add(di)
        db.commit()

    def dice_roller(self, dice_bag, num_rolls):
        """
        Unpacks dice_bag
        :param dice_bag:
        :param num_rolls:
        :return:
        """
        for dice in dice_bag:
            rols = self.dice_n_sides(num_dice=dice[0], num_side=dice[1], num_rolls=num_rolls)
            self.rolls_db_service(rolls=rols)


if __name__ == '__main__':
    mmd = MinMaxDie()
    dice_bag = [[1,12],[2,6],[3,4],[6,2]]
    num_rolls = 1000000
    data_set = 10
    z = data_set
    print('Rolling polyhedrons... NERD!')
    while z > 0:
        mmd.dice_roller(dice_bag=dice_bag, num_rolls=num_rolls)
        z -= 1
    print('Rolling completed... NERD!')