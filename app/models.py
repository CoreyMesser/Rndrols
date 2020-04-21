from sqlalchemy import Column, Integer, Text, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Dice(Base):
    __tablename__ = 'dices'

    id = Column(Integer, primary_key=True, server_default=text("nextval('dices_id_seq'::regclass)"))
    session_id = Column(Integer)
    num_dice = Column(Integer)
    num_sides = Column(Integer)
    num_rolls = Column(Integer)
    rolls = Column(Text)
    max_num = Column(Integer)
    min_num = Column(Integer)
    avg_num = Column(Integer)
    max_thresh = Column(Integer)
    min_thresh = Column(Integer)
    avg_thresh = Column(Integer)
