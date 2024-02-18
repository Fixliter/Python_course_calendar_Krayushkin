"""
Позволяет зайти по логину-паролю или создать нового пользователя (а так же выйти из аккаунта)
Позволяет выбрать календарь, узнать ближайшие события, события из промежутка времени а так же
Создать событие или удалить событие
После создания события можно добавить туда пользователей
Если нас добавили в событие или удалили мы получаем уведомление.

в main можно использовать ТОЛЬКО interface
"""

from Backend import Backend
from time import sleep
import asyncio


class Interface:
    _login = ""
    state = "start"
    backend = None

    func_request = list()

    def __init__(self):
        pass

    @staticmethod
    def work_app():
        Interface.func_request = [Interface.start_app]

        while Interface.func_request:
            Interface.func_request[0]()
            del Interface.func_request[0]

            print(Interface.func_request)  # - после отладки закомментить

        print("Интерфейс календаря закончил работу")

    @staticmethod
    def start_app():
        Interface.state = "start"
        Interface.backend = Backend()

        async def running_line():
            for i in range(10):
                sleep(0.5)
                print("///" * i)
            print("=====Запуск приложения Календаридзе=====")

        async def check_connection_db():
            Interface.backend.connection_db_check()

        async def main():
            task1 = asyncio.create_task(check_connection_db())
            task2 = asyncio.create_task(running_line())

            await asyncio.sleep(1)
            await task1
            await task2

        asyncio.run(main())

        # Interface.func_request.append(Interface.check_connection_db())

        print(f"Здравствуйте! Пожалуйста, выберите следующий шаг:\n"
              "'1' - ввести логин и пароль для дальнейшей работы с календарем \n"
              "'2' - зарегистрировать нового пользователя \n"
              "'3' - остановка программы и завершение работы)"
              "")
        selection = int(input(f" Ввод: "))
        if selection == 1:
            Interface.func_request.append(Interface.log_in)
        if selection == 2:
            Interface.func_request.append(Interface.reg_user)
        if selection == 3:
            Interface.func_request.append(Interface.stop_interface)
        else:
            while selection not in (1, 2, 3):
                print('Введена неверная команда, пожалуйста, повторите')
                selection = int(input(f" Ввод: "))
                if selection == 1:
                    Interface.func_request.append(Interface.log_in)
                if selection == 2:
                    Interface.func_request.append(Interface.reg_user)
                if selection == 3:
                    Interface.func_request.append(Interface.stop_interface)

    @staticmethod
    def log_in(_login=None, _password=None):
        if _login is None or _password is None:
            _login = input("Введите логин пользователя: ")
            _password = input("Введите пароль пользователя: ")

        Interface.backend.launch_session(_login, _password)
        Interface.func_request.append(Interface.main_menu_calendar)

    @staticmethod
    def main_menu_calendar():
        selection = int(input(f" Выберите дальнейшие действия:\n"
                              f"'1' - создать календарь"
                              f"'2' - открыть календарь"
                              f"'3' - создать новое событие"
                              f"'4' - удалить событие/я"
                              f"'5' - обновить состояние календаря"
                              f"'6' - показать события на период"
                              f"'7' - сохранить данные"
                              f"'8' - загрузить данные"
                              f"'9' - найти и выбрать событие для дальнейшей работы с ним"
                              f"'10' - изменить данные пользователя"
                              f"'11' - выход и завершение работы"
                              f"'12' - выход из учетной записи"))
        if selection == 1:
            Interface.func_request.append(Interface.backend.create_calendar())
        if selection == 2:
            Interface.func_request.append(Interface.backend.open_calendar())
        if selection == 3:
            pass
        if selection == 4:
            pass
        if selection == 5:
            pass
        if selection == 6:
            pass
        if selection == 7:
            pass
        if selection == 8:
            pass
        if selection == 9:
            Interface.func_request.append(Interface.stop_interface)
        if selection == 10:
            Interface.func_request.append(Interface.log_out)

    @staticmethod
    def load_state(login, password):
        if Interface.backend is None:
            Interface.backend = Backend()
        Interface.backend.launch_session(login, password)

    @staticmethod
    def log_out():
        Interface.stop_interface()
        Interface.backend = None
        Interface.func_request.append(Interface.start_app)

    @staticmethod
    def stop_interface():
        Interface.backend.close_session()

    @staticmethod
    def reg_user():
        Interface.backend.register_new_user()
        Interface.log_in(*Interface.backend.register_new_user())

    @staticmethod
    def create_calendar():
        Interface.backend.register_new_user()

    @staticmethod
    def open_calendar():
        Interface.backend.open_calendar()

    @staticmethod
    def close_calendar():
        pass

    @staticmethod
    def del_calendar():
        pass

    @staticmethod
    def create_event():
        pass

    @staticmethod
    def del_event():
        pass

    @staticmethod
    def change_title_event():
        pass

    @staticmethod
    def change_descr_event():
        pass

    @staticmethod
    def change_start_event():
        pass

    @staticmethod
    def change_end_event():
        pass

    @staticmethod
    def change_params_user():
        pass

    @staticmethod
    def change_params_calendar():
        pass

    @staticmethod
    def change_params_event():
        pass

    @staticmethod
    def change_periodic_event():
        pass

    @staticmethod
    def change_name_calendar():
        pass

    @staticmethod
    def message():
        pass

    @staticmethod
    def save_data():
        pass

    @staticmethod
    def event_info():
        pass

    @staticmethod
    def find_event_by_start_time():
        pass

    @staticmethod
    def find_event_by_title():
        pass

    @staticmethod
    def find_event_by_id():
        pass

    @staticmethod
    def find_calendar_by_id():
        pass

    @staticmethod
    def find_calendar_by_owner():
        pass

    @staticmethod
    def find_user_by_id():
        pass

    @staticmethod
    def find_user_by_login():
        pass

    @staticmethod
    def accept_event():
        pass

    @staticmethod
    def decline_event():
        pass


if __name__ == '__main__':
    Interface.work_app()
