import flet as ft
from Backend import Backend
from Interface import Interface
from User import User
from Calendar import Calendar
from time import sleep

backend = Backend()


def main(page: ft.Page):
    page.title = "DailyTool"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 350
    page.window_height = 400
    page.theme_mode = "dark"

    def register(e):
        nonlocal new_user_login
        nonlocal new_user_password
        nonlocal user_name
        nonlocal user_job_title
        nonlocal user_email

        # open_banner(e)
        page.snack_bar = ft.SnackBar(ft.Text(backend.message),
                                     bgcolor=ft.colors.PURPLE_200,
                                     )
        page.snack_bar.visible = True
        page.snack_bar.open = True
        page.update()
        if backend.register_new_user(gui=True, login=new_user_login.current.value,
                                     password=new_user_password.current.value,
                                     name=user_name.current.value, job_title=user_job_title.current.value,
                                     email=user_email.current.value):
            button_reg.current.text = "Зарегистрирован"
        page.snack_bar.visible = False
        page.snack_bar.open = False

        page.update()

    def auth_user(e):
        nonlocal user_login
        nonlocal user_password

        backend.show_status("1")
        backend.show_status("2")
        if not backend.check_pass_user_direct_in_db(user_login.current.value, user_password.current.value):
            page.snack_bar = ft.SnackBar(ft.Text(f"Введенный пароль неверный для login: {user_login.current.value}"),
                                         bgcolor=ft.colors.PINK_200,
                                         duration=3000
                                         )
            page.snack_bar.open = True
            page.update()

        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Пароль введен верно"),
                                         bgcolor=ft.colors.GREEN_ACCENT_200,
                                         duration=2000)
            page.snack_bar.open = True
            page.update()

            backend.show_status("3")
            backend.show_status("4")
            backend.asyncload_db()
            backend.get_users_from_db()
            for user in backend._users_list:
                if user_login.current.value == user["login"]:
                    backend.launched_user = user
                    backend.current_user = User(login=user["login"],
                                                user_password=user_password.current.value,
                                                name=user["name"],
                                                job_title=user["job_title"],
                                                email=user["email"],
                                                calendars=user["calendars"],
                                                _user_id=user["_id"])
                    backend.show_status("5")

            if backend.current_user.login is not None:
                user_login = ""
                user_password = ""
                button_auth.current.text = "Авторизован"
                page.update()
                if len(page.navigation_bar.destinations) == 2:
                    page.navigation_bar.destinations.append(
                        ft.NavigationDestination(icon=ft.icons.CALENDAR_MONTH_OUTLINED,
                                                 label="Календарь",
                                                 selected_icon=ft.icons.BALLOT_ROUNDED))
                    page.update()

            else:
                page.snack_bar = ft.SnackBar(ft.Text(f"Введены некорректные данные, авторизация не прошла"))
                page.snack_bar.open = True
                page.update()

    def launch_calendar(e):
        backend.show_status("6")
        page.window_width = 600
        calendars_of_user = ft.Text(backend.current_user.get_user_calendars())
        calendar_open_id = ft.TextField(label='Выберите ID календаря и введите: ')
        panel_auth.controls.append(calendars_of_user)
        panel_auth.controls.append(calendar_open_id)

        page.update()
        # panel_auth.controls.pop()

        calendar_open = backend.connection_db_calendars().find_one({"_id": calendar_open_id.value})
        # print(calendar_open)
        # print(calendar_open_id, type(calendar_open_id))
        # print(self.current_user.get_identificator())

        backend.calendar_current = Calendar(owner=backend.current_user.get_identificator(),
                                            name=calendar_open["name"],
                                            _id=calendar_open_id,
                                            _events=calendar_open["events"])
        panel_auth.controls.append(ft.Text('Календарь загружен'))
        page.update()
        sleep(3)
        panel_auth.controls.pop()
        page.update()

        Backend.show_status("7")
        backend.calendar_current.start_calendar()
        ft.Text(backend.current_user.get_user_calendars())

    def validate_auth(e):

        if all([user_login.current.value, user_password.current.value]):
            button_auth.current.disabled = False
            page.update()

        else:
            button_auth.current.disabled = True
            page.update()

    def validate_reg(e):

        if all([new_user_login.current.value, new_user_password.current.value, user_name.current.value,
                user_job_title.current.value, user_email.current.value]):
            button_reg.current.disabled = False
            page.update()

        else:
            button_reg.current.disabled = True
            page.update()

    async def open_banner(e):
        e.control.page.reg_banner.open = True
        await e.control.page.update_async()

    async def close_banner(e):
        e.control.page.reg_banner.open = False
        await e.control.page.update_async()

    def choose_calendar(e):
        pass

    # Для авторизации
    user_login = ft.Ref[ft.TextField]()
    user_password = ft.Ref[ft.TextField]()
    button_auth = ft.Ref[ft.OutlinedButton]()

    # Для регистрации
    new_user_login = ft.Ref[ft.TextField]()
    new_user_password = ft.Ref[ft.TextField]()
    user_name = ft.Ref[ft.TextField]()
    user_job_title = ft.Ref[ft.TextField]()
    user_email = ft.Ref[ft.TextField]()
    reg_banner = ft.Ref[ft.Banner]()
    button_reg = ft.Ref[ft.OutlinedButton]()

    # Для панели календаря
    button_choose_cal = ft.Ref[ft.OutlinedButton]()

    panel_register = ft.Row([ft.Column([
        ft.Text("Регистрация"),
        ft.TextField(ref=new_user_login, label="Логин", width=200, on_change=validate_reg),
        ft.TextField(ref=new_user_password, label="Пароль", width=200, on_change=validate_reg, password=True),
        ft.TextField(ref=user_name, label="Имя и Фамилия", width=200, on_change=validate_reg),
        ft.TextField(ref=user_job_title, label="Должность", width=200, on_change=validate_reg),
        ft.TextField(ref=user_email, label="Адрес email", width=200, on_change=validate_reg),
        ft.OutlinedButton(ref=button_reg, text="Добавить", width=200, on_click=register, disabled=True),
        ft.Banner(ref=reg_banner, bgcolor=ft.colors.PURPLE_400,
                  leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
                  content=ft.Text(backend.message),
                  actions=[ft.TextButton("Ok", on_click=close_banner),
                           # ft.TextButton("Ignore", on_click=close_banner),
                           # ft.TextButton("Cancel", on_click=close_banner),
                           ],
                  )
    ], alignment=ft.MainAxisAlignment.CENTER
    )
    ]
    )
    panel_auth = ft.Row([ft.Column([
        ft.Text("Авторизация"),
        ft.TextField(ref=user_login, label="Логин", width=200, on_change=validate_auth),
        ft.TextField(ref=user_password, label="Пароль", width=200, on_change=validate_auth, password=True),
        ft.OutlinedButton(ref=button_auth, text="Войти", width=200, on_click=auth_user, disabled=False)
    ], alignment=ft.MainAxisAlignment.CENTER
    )
    ]
    )

    panel_calendar = ft.Row([ft.Column([
        ft.Text("Календарь", text_align=ft.TextAlign.CENTER),
        ft.OutlinedButton(ref=button_choose_cal, text="Выбрать календарь", width=200, on_click=choose_calendar)
    ], alignment=ft.MainAxisAlignment.CENTER
    )
    ]
    )

    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()

        if index == 1:
            page.add(panel_register)
            page.window_height = 600
            page.update()
        if index == 0:
            page.add(panel_auth)
            page.window_height = 400
            page.update()
        elif index == 2:
            page.add(panel_calendar)
            page.window_height = 400
            page.update()

    page.navigation_bar = ft.NavigationBar(destinations=
                                           [ft.NavigationDestination(icon=ft.icons.VERIFIED_USER_OUTLINED,
                                                                     label="Авторизация"),
                                            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label="Регистрация"),
                                            ],
                                           on_change=navigate)
    page.add(panel_auth)


if __name__ == '__main__':
    ft.app(target=main)
