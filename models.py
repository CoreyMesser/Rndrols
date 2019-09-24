from sqlalchemy import Column, Integer, Text, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Dice(Base):
    __tablename__ = 'dices'

    id = Column(Integer, primary_key=True, server_default=text("nextval('dices_id_seq'::regclass)"))
    num_dice = Column(Integer)
    num_sides = Column(Integer)
    num_rolls = Column(Integer)
    rolls = Column(Text)
    max_num = Column(Integer)
    min_num = Column(Integer)
    max_thresh = Column(Integer)
    avg_num = Column(Integer)


class DiceTemplate(object):
    def __init__(self):
        self.num_dice = 0
        self.num_sides = 0
        self.num_rolls = 0
        self.rolls = []
        self.max_num = 0
        self.min_num = 0
        self.max_tresh = 0
        self.avg_num = 0

