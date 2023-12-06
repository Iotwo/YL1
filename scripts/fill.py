from datetime import datetime, timedelta
from random import choice, randint, random
import sqlite3


def generate_samples(samples_cnt: int=64) -> list:
    """
    DESCR: Generate random realistic samples of operations
    REQ: datetime, random
    ARGS:
        -samples_cnt: amount of samples, default is 64
    RETURN: list of sample-tuples
    """

    cats = {
    "Доход": ["Выплата по работе", "Премия", "Подарок",],
    "Расход": ["Еда", "Одежда", "Ремонт", "Автомобиль", "Животные", "Услуги", "Подарки", "Развлечения"],
    }
    optypes = ["Доход", "Расход"]
    dt1 = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    dates = [dt1 + timedelta(hours=i) for i in range(36000)]
    samples = []
    for i in range(samples_cnt):
        dt = choice(dates)
        tp = choice(optypes)
        ct = choice(cats[tp])
        val = randint(50, 30000) + round(random(), 2)
        samples.append((dt, tp, ct, val,))

    return samples

def insert_samples(db: str, samples: list) -> None:

    cnt = sqlite3.connect(db)
    crs = cnt.cursor()

    crs.executemany("INSERT INTO Actions_log(action_datetime, optype, category, amount) VALUES(?, ?, ?, ?)", samples)
    cnt.commit()

    crs.close()
    cnt.close()
    
    return None

insert_samples("D:\\Project\\YL1\\opdb.db", generate_samples(400))
