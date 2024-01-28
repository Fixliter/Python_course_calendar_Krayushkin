"""
Позволяет зайти по логину-паролю или создать нового пользователя (а так же выйти из аккаунта)
Позволяет выбрать календарь, узнать ближайшие события, события из промежутка времени а так же
Создать событие или удалить событие
После создания события можно добавить туда пользователей
Если нас добавили в событие или удалили мы получаем уведомление.

в main можно использовать ТОЛЬКО interface
"""

import flet as ft
from Backend import Backend

class Interface:
    _login = ""
    state = "start"

    def __init__(self):
        pass

    def log_in(self):
        self._login = input("Введите логин пользователя")
        self._password = input("Введите пароль пользователя")
        Back = Backend()
        Back.launch_session(self._login, self._password)

    @staticmethod
    def start_app(self):
        print(f"Hello, please, choose the next step:"
              "'1' - login, enter your name, password to open your calendars \n"
              "'2' - register a new user"
              "'3' - stop working and close session)"
              "")

    @staticmethod
    def work_app():
        Interface.stage = [Interface.start]

        while Interface.func_request:
            Interface.func_request[0]()
            del Interface.func_request[0]

            print(Interface.func_request)

        print("Воркер интерфейса закончил работу")

    def log_out(self):
        pass

    def reg_user(self):
        pass

    def create_calendar(self):
        pass

    def open_calendar(self):
        pass

    def close_calendar(self):
        pass

    def del_calendar(self):
        pass

    def create_event(self):
        pass

    def del_event(self):
        pass

    def change_title_event(self):
        pass

    def change_descr_event(self):
        pass

    def change_start_event(self):
        pass

    def change_end_event(self):
        pass

    def change_params_user(self):
        pass

    def change_params_calendar(self):
        pass

    def change_params_event(self):
        pass

    def change_periodic_event(self):
        pass

    def change_name_calendar(self):
        pass

    def message(self):
        pass

    def save_data(self):
        pass

    def event_info(self):
        pass

    def find_event_by_start_time(self):
        pass

    def find_event_by_title(self):
        pass

    def find_event_by_id(self):
        pass

    def find_calendar_by_id(self):
        pass

    def find_calendar_by_owner(self):
        pass

    def find_user_by_id(self):
        pass

    def find_user_by_login(self):
        pass

    def accept_event(self):
        pass

    def decline_event(self):
        pass

    def main(page: ft.Page):
        page.title = "Calendar"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

        def minus_click(e):
            txt_number.value = str(int(txt_number.value) - 1)
            page.update()

        def plus_click(e):
            txt_number.value = str(int(txt_number.value) + 1)
            page.update()

        page.add(
            ft.Row(
                [
                    ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.icons.ADD, on_click=plus_click),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        def add_clicked(e):
            page.add(ft.Checkbox(label=new_task.value))
            new_task.value = ""
            new_task.focus()
            new_task.update()

        new_task = ft.TextField(hint_text="Let's create user", width=300)
        page.add(ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_clicked)]))

        first_name = ft.Ref[ft.TextField]()
        last_name = ft.Ref[ft.TextField]()
        greetings = ft.Ref[ft.Column]()

        def btn_click(e):
            greetings.current.controls.append(
                ft.Text(f"Hello, {first_name.current.value} {last_name.current.value}!")
            )
            first_name.current.value = ""
            last_name.current.value = ""
            page.update()
            first_name.current.focus()

        page.add(
            ft.TextField(ref=first_name, label="First name", autofocus=True),
            ft.TextField(ref=last_name, label="Last name"),
            ft.ElevatedButton("Say hello!", on_click=btn_click),
            ft.Column(ref=greetings),
        )

    ft.app(target=main)


if __name__ == '__main__':
    pass
