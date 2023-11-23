from datetime import datetime, timedelta
from random import choice, randint, random


def generate_samples(samples_cnt: int=64) -> list:
    '''
    DESCR: Generate random realistic samples of operations
    REQ: datetime, random
    ARGS:
        -samples_cnt: amount of samples, default is 64
    RETURN: list of sample-tuples
    '''

    cats = {
    'Приход': ['Выплата по работе', 'Премия', 'Подарок',],
    'Расход': ['Еда', 'Одежда', 'Ремонт', 'Автомобиль', 'Животные', 'Услуги', 'Подарки'],
    'Возврат': ['Возврат']
    }
    optypes = ['Приход', 'Расход', 'Возврат']
    dt1 = datetime.strptime('2021-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    dates = [dt1 + timedelta(hours=i) for i in range(25000)]
    samples = []
    for i in range(30):
        dt = choice(dates)
        tp = choice(optypes)
        ct = choice(cats[tp])
        val = randint(50, 30000) + round(random(), 2)
        samples.append((dt, tp, ct, val,))

    return samples

print(generate_samples(15))
