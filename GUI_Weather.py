import flet as ft
import requests as req
import datetime as dt


def main(page: ft.Page):
    page.title = "Get_weather"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # page.theme_mode = "dark"
    #     page.add(
    #         ft.Row(
    #             [
    #                 ft.IconButton(ft.icons.RADIO_BUTTON_ON, on_click=None),
    #                 ft.IconButton(ft.icons.ELECTRIC_BIKE_SHARP, on_click=None),
    #             ],
    #             alignment=ft.MainAxisAlignment.START,
    #         )
    #     )
    #     txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)
    #
    #     def minus_click(e):
    #         txt_number.value = str(int(txt_number.value) - 1)
    #         page.update()
    #
    #     def plus_click(e):
    #         txt_number.value = str(int(txt_number.value) + 1)
    #         page.update()
    #
    #     page.add(
    #         ft.Row(
    #             [
    #                 ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
    #                 txt_number,
    #                 ft.IconButton(ft.icons.ADD, on_click=plus_click),
    #             ],
    #             alignment=ft.MainAxisAlignment.START,
    #         )
    #     )
    #
    #     def add_clicked(e):
    #         page.add(ft.Checkbox(label=new_task.value))
    #         new_task.value = ""
    #         new_task.focus()
    #         new_task.update()
    #
    #     new_task = ft.TextField(hint_text="Let's create user", width=300)
    #     page.add(ft.Row([new_task, ft.ElevatedButton("Add", on_click=add_clicked)]))
    #
    #     first_name = ft.Ref[ft.TextField]()
    #     last_name = ft.Ref[ft.TextField]()
    #     greetings = ft.Ref[ft.Column]()
    #
    #     def btn_click(e):
    #         greetings.current.controls.append(
    #             ft.Text(f"Hello, {first_name.current.value} {last_name.current.value}!")
    #         )
    #         first_name.current.value = ""
    #         last_name.current.value = ""
    #         page.update()
    #         first_name.current.focus()
    #
    #     page.add(
    #         ft.TextField(ref=first_name, label="First name", autofocus=True),
    #         ft.TextField(ref=last_name, label="Last name"),
    #         ft.ElevatedButton("Say hello!", on_click=btn_click),
    #         ft.Column(ref=greetings),
    #     )
    #
    #     iconka1 = ft.Icon(name=ft.icons.CALENDAR_MONTH, color=ft.colors.PINK)
    #     iconka2 = ft.Icon(name=ft.icons.BOY, color='#11a711')
    #     iconka3 = ft.Icon(name=ft.icons.VPN_KEY, color=ft.colors.BLUE)
    #
    #     page.controls.append(iconka1)
    #     page.controls.append(iconka2)
    #     page.controls.append(iconka3)
    #     page.update()

    user_data_city = ft.TextField(label="Введите город", width=400)
    weather_data = ft.Text("", style=ft.TextThemeStyle.BODY_LARGE, size=30)

    def get_info_weather(e):
        if len(user_data_city.value) < 2:
            return
        API_key = "77a99d99c48dedc8fbbb41a282395c1a"
        URL = f"https://api.openweathermap.org/data/2.5/weather?q={user_data_city.value}&appid={API_key}&units=metric"
        res = req.get(URL).json()
        print(res)
        temper = int(res['main']['temp']).__round__(3)
        # temper = res['main']['temp']
        feels_like = int(res['main']['feels_like']).__round__(3)
        # feels_like = res['main']['feels_like']
        pressure = res['main']['pressure']
        humidity = res['main']['humidity']
        wind_speed = res['wind']['speed']
        # wind_gust = res['wind']['gust']
        clouds = res['clouds']['all']
        sunrise = dt.datetime.utcfromtimestamp(res['sys']['sunrise']).time()
        sunset = dt.datetime.utcfromtimestamp(res['sys']['sunset']).time()
        weather_data.value = (f"температура в городе {user_data_city.value}: {str(temper)} грд. Цельсия\n"
                              f"ощущается как {str(feels_like)} грд. Цельсия\n"
                              f"влажность: {humidity} %\n"
                              f"давление: {pressure} кПа\n"
                              f"скорость ветра: {wind_speed} м/с\n"
                              f"облачность: {clouds} %\n"
                              f"рассвет в {sunrise},\n"
                              f"закат в {sunset}")
        page.update()

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    page.add(
        ft.Column(
            [ft.IconButton(ft.icons.SUNNY, on_click=change_theme)],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
        ft.Row([user_data_city,
                ft.TextButton(
                    width=200,
                    content=ft.Row(
                        [
                            ft.Icon(name=ft.icons.UMBRELLA_SHARP, color="pink"),
                            ft.Icon(name=ft.icons.SNOWING, color="green"),
                            ft.Icon(name=ft.icons.BEACH_ACCESS, color="blue"),
                            ft.Text(value="Запрос погоды"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    on_click=get_info_weather
                ), ]),

        ft.Column([weather_data], alignment=ft.MainAxisAlignment.SPACE_EVENLY),

    )


if __name__ == '__main__':
    ft.app(target=main)  # Для запуска из браузера view=AppView.WEB_BROWSER, port=8765
