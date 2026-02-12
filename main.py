import flet as ft
import random
import asyncio

def main(page: ft.Page):
    # --- НАСТРОЙКИ ---
    page.title = "Walentynka"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "pink50"
    page.theme_mode = "light"
    # на мобиле window_* обычно игнорируется, но не мешает
    page.window_width = 400
    page.window_height = 700

    # --- ПЕРЕМЕННЫЕ ---
    state = {"score": 0, "q_index": 0}

    # --- ВОПРОСЫ ---
    questions = [
        {"q": "Kiedy się urodziłem?", "answers": ["8 lutego", "12 marca", "23 kwietnia", "12 grudnia"], "correct": 0},
        {"q": "Kiedy był nasz pierwszy pocałunek?", "answers": ["6 maja", "7 kwietnia", "12 września", "4 maja"], "correct": 0},
        {"q": "Kto odegrał główną rolę w naszym związku?", "answers": ["Trener", "Jakub", "Luna", "Moly"], "correct": 2},
        {"q": "Mój ulubiony słodycz?", "answers": ["Lody", "Nutella", "Zefir", "Bambus"], "correct": 2},
        {"q": "Kto jest najlepszą dziewczyną na świecie?", "answers": ["Ty", "Ty", "ty", "Zdecydowanie Ty"], "correct": [0,1,2,3]}
    ]

    phrases = ["Pudło!", "Spróbuj jeszcze raz!", "Tutaj jestem!", "Nie złapiesz mnie!", "Ojej!", "He-he"]

    # --- Утилиты отображения ---
    def clear_and_update():
        page.controls.clear()
        page.update()

    def show_snackbar(text: str, bgcolor: str = "grey"):
        page.snack_bar = ft.SnackBar(ft.Text(text), bgcolor=bgcolor, open=True)
        page.update()

    # --- ЛОГИКА ---
    async def check_answer(e):
        clicked = e.control.data
        q_data = questions[state["q_index"]]
        correct = q_data["correct"]

        is_correct = False
        if isinstance(correct, list):
            if clicked in correct: is_correct = True
        elif clicked == correct:
            is_correct = True

        if is_correct:
            state["score"] += 1
            show_snackbar("Dobrze! +1 Róża 🌹", bgcolor="green")
        else:
            show_snackbar("Źle! 🥀", bgcolor="red")

        # краткая пауза без блокировки UI
        await asyncio.sleep(0.25)
        state["q_index"] += 1

        if state["q_index"] < len(questions):
            show_quiz()
        else:
            show_shop()

    async def buy_ticket(e):
        # если есть хоть одна роза — показываем финал, иначе даём "билет за piękne oczy" но всё равно переходим
        if state["score"] > 0:
            show_final()
        else:
            show_snackbar("Masz bilet za piękne oczy ❤️", bgcolor="pink")
            await asyncio.sleep(1)
            show_final()

    def move_btn(e):
        # перемещаем кнопку (работает в Stack)
        e.control.top = random.randint(0, 300)
        e.control.left = random.randint(0, 150)
        e.control.text = random.choice(phrases)
        # меняем стиль безопасно — используем допустимые цвета
        e.control.bgcolor = random.choice(["red", "orange", "grey"])
        page.update()

    def win(e):
        clear_and_update()
        page.add(
            ft.Column(
                [
                    ft.Icon(name="favorite", size=100, color="red"),
                    ft.Text("JEJ! KOCHAM CIĘ JULLI! ❤️", size=30, color="red", weight="bold", text_align="center"),
                    ft.Text("Twój Vall!", size=18, weight="bold")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    # --- ЭКРАНЫ ---
    def show_quiz():
        clear_and_update()
        q = questions[state["q_index"]]

        header = ft.Column(
            [
                ft.Text(f"Pytanie {state['q_index']+1} z {len(questions)}", color="grey"),
                ft.Text(f"Róże: {state['score']} 🌹", size=20, color="red", weight="bold"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        container = ft.Container(
            content=ft.Text(q["q"], size=22, weight="bold", text_align="center"),
            padding=20,
            bgcolor="white",
            border_radius=15,
            margin=ft.margin.only(bottom=20)
        )

        btns = []
        for i, ans in enumerate(q["answers"]):
            btns.append(
                ft.ElevatedButton(
                    text=ans,
                    data=i,
                    on_click=check_answer,
                    width=280,
                    height=50,
                    bgcolor="pink"
                )
            )

        page.add(ft.Column([header, container, ft.Column(btns, alignment=ft.MainAxisAlignment.CENTER)], horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        page.update()

    def show_shop():
        clear_and_update()

        card = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(name="card_giftcard", size=80, color="pink"),
                    ft.Text("Bilet do Szczęścia", size=20, weight="bold"),
                    ft.Text("Cena: 1 róża", color="grey")
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            bgcolor="white",
            border_radius=15
        )

        buy_btn = ft.ElevatedButton(
            text="KUPUJĘ ❤️",
            on_click=buy_ticket,
            bgcolor="green",
            color="white",
            width=200,
            height=50
        )

        page.add(ft.Column([ft.Text("SKLEPIK MIŁOŚCI", size=28, weight="bold"), card, buy_btn], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        page.update()

    def show_final():
        clear_and_update()

        btn_yes = ft.ElevatedButton(
            text="TAK! ❤️",
            on_click=win,
            bgcolor="green",
            color="white",
            width=140,
            height=60
        )

        # кнопка 'нет' — уходит в случайную позицию при наведении/нажатии
        btn_no = ft.ElevatedButton(
            text="Nie",
            bgcolor="red",
            color="white",
            on_hover=move_btn,
            on_click=move_btn,
            width=80,
            height=40,
            left=100,
            top=300
        )

        game_area = ft.Stack(
            [
                ft.Container(
                    content=ft.Text("Zostaniesz moją Walentynką?", size=26, weight="bold", text_align="center", color="pink900"),
                    top=50, left=0, right=0, alignment=ft.alignment.center
                ),
                ft.Container(
                    content=btn_yes,
                    top=200, left=0, right=0, alignment=ft.alignment.center
                ),
                btn_no
            ],
            width=350,
            height=600
        )

        page.add(game_area)
        page.update()

    show_quiz()

if __name__ == "__main__":
    ft.app(target=main)
