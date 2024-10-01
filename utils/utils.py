import psycopg2
from utils.config import config
from classes.class_HHParser import HHParser


def create_database(db_name: str):
    """
    Функция по созданию базы данных по заданному пользователем имени
    :param db_name:
    :return:
    """
    con = psycopg2.connect(dbname='postgres', **config())
    con.autocommit = True
    cur = con.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')

    cur.close()
    con.close()


def create_tables(db_name: str):
    """
    Функция по созданию в базе данных таблиц по предустановленным параметрам
    :param db_name:
    :return:
    """
    con = psycopg2.connect(dbname=db_name, **config())
    with con:
        with con.cursor() as cur:
            cur.execute('CREATE TABLE employers'
                        '(employer_id INTEGER PRIMARY KEY,'
                        'employer_name VARCHAR(100))')
            cur.execute('CREATE TABLE vacancies'
                        '(vacancy_id INTEGER PRIMARY KEY,'
                        'vacancy_name VARCHAR(150),'
                        'link VARCHAR(150),'
                        'salary_from INTEGER,'
                        'salary_to INTEGER,'
                        'employer_id INTEGER REFERENCES employers(employer_id))')
    con.close()


def fill_tables(db_name: str):
    """
    Функция по внесению в таблицы данных, полученных в результате парсинга
    :param db_name:
    :return:
    """
    hh = HHParser()
    employers = hh.get_employers()
    vacancies = hh.get_response_hh_vacancies()
    con = psycopg2.connect(dbname=db_name, **config())
    with con:
        with con.cursor() as cur:
            for employer in employers:
                cur.execute('INSERT INTO employers '
                            'VALUES(%s, %s)', (employer['employer_id'], employer['employer_name']))
            for vacancy in vacancies:
                cur.execute('INSERT INTO vacancies '
                            'VALUES(%s, %s, %s, %s, %s, %s)',
                            (vacancy['vacancy_id'], vacancy['vacancy_name'],
                             vacancy['vacancy_link'], vacancy['salary_to'], vacancy['salary_from'],
                             vacancy['employer_id']))
    con.close()