import psycopg2
from utils.config import config


class DBManager:
    """
    Класс для работы с базой данных
    """
    def __init__(self, db_name):
        self.__db_name = db_name

    def __execute_query(self, query: str):
        """
        Функция по получению данных из базы в соответствии с полученным запросом
        :param query:
        :return:
        """
        con = psycopg2.connect(dbname=self.__db_name, **config())
        with con:
            with con.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        con.close()
        return result

    def get_all_vacancies(self):
        """
        Функция по получению пользователем сведений по работодателям и вакансиям
        :return:
        """
        query = ('SELECT vacancy_name, employer_name, salary_from, salary_to, link FROM vacancies JOIN employers ON '
                 'vacancies.employer_id = employers.employer_id')
        return self.__execute_query(query)

    def get_avg_salary(self):
        """
        Функция по получению пользователем сведений о средней заработной плате
        :return:
        """
        query = 'SELECT AVG(salary_to) AS avg_salary FROM vacancies'
        return self.__execute_query(query)

    def get_companies_and_vacancies_count(self):
        """
        Функция по получению пользователем сведений о количестве вакансий у работодателей
        :return:
        """
        query = ('SELECT employer_name, COUNT(vacancy_id) AS count_of_vacancies FROM employers JOIN vacancies ON '
                 'employers.employer_id = vacancies.employer_id GROUP BY employer_name')
        return self.__execute_query(query)

    def get_vacancies_with_higher_salary(self):
        """
        Функция по получению пользователем сведений о вакансиях, с зарплатой выше средней среди имеющихся в базе
        :return:
        """
        query = ('SELECT vacancy_name AS highest_salary FROM vacancies WHERE salary_to > (SELECT AVG(salary_to) FROM '
                 'vacancies)')
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, key_word: str):
        """
        Функция получения пользователем списка вакансий по ключевому слову
        :param key_word:
        :return:
        """
        query = f"SELECT vacancy_name FROM vacancies WHERE vacancy_name LIKE '%{key_word}%'"
        return self.__execute_query(query)