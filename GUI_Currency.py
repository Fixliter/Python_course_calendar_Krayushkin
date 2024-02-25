import requests
import flet as ft


def main(page: ft.Page):
    page.title = "Currency"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    valute_list = []

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    def get_valute_list():
        nonlocal valute_list
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        for valute in data['Valute']:
            valute_list.append(ft.dropdown.Option(valute))
        return valute_list

    def get_currency_from_cbr(currency):

        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        # print(data)
        print(data['Valute'][currency]['Value'])
        # print(valute_list)
        current_name_valute.current.value = data['Valute'][currency]['Name']
        return [data['Valute'][currency]['Nominal'], data['Valute'][currency]['Value']]

    def button_clicked(e):
        res = get_currency_from_cbr(dd_menu.current.value)
        current_ratio.current.value = f"For {res[0]} {dd_menu.current.value} value RUB is: {res[1]}"
        page.update()
    current_name_valute = ft.Ref[ft.Text]()
    current_ratio = ft.Ref[ft.Text]()
    submit_button = ft.Ref[ft.ElevatedButton]()
    dd_menu = ft.Ref[ft.Dropdown]()

    page.add(ft.Column(
        [ft.IconButton(ft.icons.SUNNY, on_click=change_theme)],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
    ),
        ft.Column(controls=[ft.Text(ref=current_name_valute, style=ft.TextThemeStyle.BODY_LARGE, size=30, weight=ft.FontWeight.BOLD),
                            ft.Text(ref=current_ratio, style=ft.TextThemeStyle.BODY_LARGE, size=30),
                            ft.ElevatedButton(ref=submit_button, text="Submit", on_click=button_clicked, style=ft.ButtonStyle(
                color={
                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                    ft.MaterialState.FOCUSED: ft.colors.BLUE,
                    ft.MaterialState.DEFAULT: ft.colors.BLACK,
                },
                bgcolor={ft.MaterialState.FOCUSED: ft.colors.PINK_200, "": ft.colors.TEAL_800},
                padding={ft.MaterialState.HOVERED: 25},
                overlay_color=ft.colors.TRANSPARENT,
                elevation={"pressed": 0, "": 1},
                animation_duration=500,
                side={
                    ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                    ft.MaterialState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                },
                shape={
                    ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                },
            ),),
                            ft.Dropdown(ref=dd_menu,
                                        width=100,
                                        options=get_valute_list(),
                                        # options=[
                                        # ft.dropdown.Option("USD"),
                                        # ft.dropdown.Option("EUR"),
                                        # ft.dropdown.Option("CNY"),
                                        # ],
                                        )
                            ]),
    )
    page.update()


if __name__ == '__main__':
    ft.app(target=main)  # Для запуска из браузера view=AppView.WEB_BROWSER, port=8765
