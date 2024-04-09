from typing import Any
import psycopg2
import requests


def get_hh_data(url, params) -> list[dict[str, Any]]:
    """Получение данных о компаниях-работодателях с помощью API hh.ru"""

    headers = {'User-Agent': 'HH-User-Agent'}
    params = {'page': 0, 'per_page': 100, 'search_field': 'name'}

    new_list = []

    while params.get('page') != 50:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        clear_data = data['items']
        new_list.extend(clear_data)
        params['page'] += 1

    return new_list


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о вакансиях и компаниях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
                company_id INTEGER PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                vacancies INTEGER,
                url VARCHAR(100) NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                company_id INTEGER NOT NULL,
                salary VARCHAR(100),
                url VARCHAR(100)
            )
        """)

    conn.commit()
    conn.close()

    def save_data_to_database(vacancies: list[dict[str, Any]], companies: list[dict[str, Any]], database_name: str,
                              params: dict):
        """Сохранение данных о вакансиях и компаниях в базу данных."""

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            for vacancy in vacancies:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_id, title, company_id, salary, url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (vacancy['id'], vacancy['name'], vacancy['employer']['id'],
                     f"от {vacancy['salary']['from']} до {vacancy['salary']['to']}",
                     vacancy['alternate_url'])
                )

            for company in companies:
                cur.execute(
                    """
                    INSERT INTO companies (company_id, title, vacancies, url)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (company['id'], company['name'], company['open_vacancies'],
                     company['alternate_url'])
                )

        conn.commit()
        conn.close()
