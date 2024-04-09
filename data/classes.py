import psycopg2


class DBManager:
    def __init__(self, database_name):
        self.vac_salary = None
        self.avg_salary = None
        self.data_vac = None
        self.data_comp = None
        self.database = database_name

    def get_companies_and_vacancies_count(self, params):
        """получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=self.database, **params)

        with conn.cursor() as cur:
            cur.execute("SELECT company_id, title, vacancies FROM companies")
            self.data_comp = cur.fetchone()
        conn.commit()
        conn.close()
        return self.data_comp

    def get_all_vacancies(self, params):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию."""
        conn = psycopg2.connect(dbname=self.database, **params)

        with conn.cursor() as cur:
            cur.execute("SELECT companies.title, vacancies.title, salary, url FROM vacancies JOIN companies USING "
                        "(company_id)")
            self.data_vac = cur.fetchone()
        conn.commit()
        conn.close()
        return self.data_vac

    def get_avg_salary(self, params):
        """получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname=self.database, **params)

        with conn.cursor() as cur:
            cur.execute("SELECT AVG(salary_from, salary_to) FROM vacancies WHERE salary_from IS NOT NULL AND "
                        "salary_to IS NOT NULL")
            self.avg_salary = cur.fetchone()
        conn.commit()
        conn.close()
        return self.avg_salary

    def get_vacancies_with_higher_salary(self, params):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=self.database, **params)

        with conn.cursor() as cur:
            cur.execute(
                f"SELECT vacancy_id, title, salary_from, salary_to FROM vacancies WHERE salary_from > {self.avg_salary} OR salary_to > {self.avg_salary}")
            self.vac_salary = cur.fetchone()
        conn.commit()
        conn.close()
        return self.vac_salary

    def get_vacancies_with_keyword(self, params, word):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        conn = psycopg2.connect(dbname=self.database, **params)

        with conn.cursor() as cur:
            cur.execute(f"SELECT title, salary, url FROM vacancies WHERE title LIKE '%{word}%'")
            self.data_vac = cur.fetchone()
        conn.commit()
        conn.close()
        return self.data_vac
