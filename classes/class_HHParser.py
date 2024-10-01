import requests


class HHParser:
    @staticmethod
    def __get_response_hh_employers():
        """
        Функция получения сведений по работодателям с открытыми вакансиями с сайта HeadHunter в JSON-формате
        :return:
        """
        params = {'sort_by': 'by_vacancies_open', 'per_page': 10}
        response = requests.get('http://api.hh.ru/employers', params=params)
        if response.status_code == 200:
            return response.json()['items']

    def get_employers(self):
        """
        Функция формирования списка работодателей по заданным критериям
        :return:
        """
        data_from_response = self.__get_response_hh_employers()
        employers_list = []
        for employer in data_from_response:
            employers_list.append({'employer_id': employer['id'], 'employer_name': employer['name']})
        return employers_list

    def get_response_hh_vacancies(self):
        """
        Функция получения сведений о вакансиях у ранее отобранных работодателей с сайта HeadHunter
        :return:
        """
        employers_list = self.get_employers()
        vacancies_list = []
        for employer in employers_list:
            params = {'employer_id': employer['employer_id']}
            response = requests.get('http://api.hh.ru/vacancies', params=params)
            if response.status_code == 200:
                filtered_vacancies_list = self.__get_filtered_vacancies(response.json()['items'])
                vacancies_list.extend(filtered_vacancies_list)
        return vacancies_list

    @staticmethod
    def __get_filtered_vacancies(vacancies_list: list):
        """
        Функция фильтрации и выборки имеющихся вакансий по заданным параметрам
        :param vacancies_list:
        :return:
        """
        filtered_vacancies = []
        for vacancy in vacancies_list:
            if vacancy['salary'] is None:
                salary_from = 0
                salary_to = 0
            else:
                salary_from = vacancy['salary']['from'] if vacancy['salary']['from'] else 0
                salary_to = vacancy['salary']['to'] if vacancy['salary']['to'] else 0
            filtered_vacancies.append(
                {
                    'vacancy_id': vacancy['id'],
                    'vacancy_name': vacancy['name'],
                    'vacancy_link': vacancy['alternate_url'],
                    'salary_from': salary_from,
                    'salary_to': salary_to,
                    'employer_id': vacancy['employer']['id']
                }
            )
        return filtered_vacancies