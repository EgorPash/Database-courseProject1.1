from utils.utils import create_database, create_tables, fill_tables
from classes.classes_DBManager import DBManager


def user_interface():
    """
    Функция пользовательского интерфейса
    :return:
    """
    db_name = input('Введите название создаваемой базы данных:\n')
    create_database(db_name)
    create_tables(db_name)
    fill_tables(db_name)

    print(f'База {db_name} создана и готова к использованию.')
    print()

    while True:
        print('Для получения сведений о всех вакансиях, нажмите 1')
        print('Для получения сведений о размере средней заработной платы, нажмите 2')
        print('Для получения сведений о компаниях с имеющимися вакансиями, нажмите 3')
        print('Для получения сведений о вакансиях, где заработок выше среднего, нажмите 4')
        print('Для получения сведений о всех вакансиях по ключевому слову, нажмите 5')
        print('Для выхода из программы, нажмите 0')
        answer = input()
        if answer.isdigit():
            if int(answer) == 0:
                print('Программа завершена')
                break
            elif int(answer) == 1:
                item = DBManager(db_name)
                print(item.get_all_vacancies())
            elif int(answer) == 2:
                item = DBManager(db_name)
                print(item.get_avg_salary())
            elif int(answer) == 3:
                item = DBManager(db_name)
                print(item.get_companies_and_vacancies_count())
            elif int(answer) == 4:
                item = DBManager(db_name)
                print(item.get_vacancies_with_higher_salary())
            elif int(answer) == 5:
                key_word = input('Введите ключевое слово')
                item = DBManager(db_name)
                print(item.get_vacancies_with_keyword(key_word[1:]))
            else:
                print('Введено некорректное число')
        else:
            print('Попробуйте снова, вы ввели не число')


if __name__ == '__main__':
    user_interface()