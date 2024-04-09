import os

import config
from data.funcs import get_hh_data, create_database

POSTGRESKEY


def main():
    channel_ids = [
        'UC-OVMPlMA3-YCIeg4z5z23A',  # moscowpython
        'UCwHL6WHUarjGfUM_586me8w',  # highload

    ]
    data_vacancies = get_hh_data('http://api.hh.ru/vacancies')
    data_companies = get_hh_data('https://api.hh.ru/employers')
    create_database()


if __name__ == '__main__':
    main()
