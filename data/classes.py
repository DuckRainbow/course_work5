import psycopg2


class DBManager:
    def __init__(self):
        self.vac_salary = None
        self.avg_salary = None
        self.data_vac = None
        self.data_comp = None
        

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        cur.execute("SELECT company_id, title, vacancies FROM companies")
        self.data_comp = cur.fetchone()
        return self.data_comp

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
        вакансию."""
        cur.execute("SELECT companies.title, vacancies.title, salary, url FROM vacancies JOIN companies USING "
                        "(company_id)")
        self.data_vac = cur.fetchone()
        return self.data_vac

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        cur.execute("SELECT AVG(salary_from, salary_to) FROM vacancies WHERE salary_from IS NOT NULL AND "
                        "salary_to IS NOT NULL")
        self.avg_salary = cur.fetchone()
        return self.avg_salary

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        cur.execute(
                f"SELECT vacancy_id, title, salary_from, salary_to FROM vacancies WHERE salary_from > {self.avg_salary} OR salary_to > {self.avg_salary}")
        self.vac_salary = cur.fetchone()
        return self.vac_salary

    def get_vacancies_with_keyword(self, params, word):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        cur.execute(f"SELECT title, salary, url FROM vacancies WHERE title LIKE '%{word}%'")
        self.data_vac = cur.fetchone()
        return self.data_vac
