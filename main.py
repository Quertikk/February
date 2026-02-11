import flet as ft
import random
import time

def main(page: ft.Page):
    # --- НАСТРОЙКИ (USTAWIENIA) ---
    page.title = "Walentynka"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "pink50"
    page.theme_mode = "light"
    page.window_width = 400
    page.window_height = 700

    # --- ПЕРЕМЕННЫЕ ---
    state = {"score": 0, "q_index": 0}

    # --- ВОПРОСЫ (PYTANIA) ---
    questions = [
        {
            "q": "Kiedy się urodziłem?", 
            "answers": ["8 lutego", "12 marca", "23 kwietnia", "12 grudnia"], 
            "correct": 0
        },
        {
            "q": "Kiedy był nasz pierwszy pocałunek?", 
            "answers": ["6 maja", "7 kwietnia", "12 września", "4 maja"], 
            "correct": 0
        },
        {
            "q": "Kto odegrał główną rolę w naszym związku?", 
            "answers": ["Trener", "Jakub", "Luna", "Moly"], 
            "correct": 2
        },
        {
            "q": "Mój ulubiony słodycz?", 
            "answers": ["Lody", "Nutella", "Zefir", "Bambus"], 
            "correct": 2
        },
        {
            "q": "Kto jest najlepszą dziewczyną na świecie?", 
            "answers": ["Ty", "Ty", "ty", "Zdecydowanie Ty"], 
            "correct": [0, 1, 2, 3] 
        }
    ]

    phrases = ["Pudło!", "Spróbuj jeszcze raz!", "Tutaj jestem!", "Nie złapiesz mnie!", "Ojej!", "He-he"]

    # --- ЛОГИКА ---

    def check_answer(e):
        clicked = e.control.data
        q_data = questions[state["q_index"]]
        correct_answer = q_data["correct"]

        is_correct = False
        if isinstance(correct_answer, list):
            if clicked in correct_answer:
                is_correct = True
        elif clicked == correct_answer:
            is_correct = True

        if is_correct:
            state["score"] += 1
            page.snack_bar = ft.SnackBar(ft.Text("Dobrze! +1 Róża 🌹"), bgcolor="green")
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Źle! 🥀"), bgcolor="red")
            page.snack_bar.open = True
        
        page.update()
        time.sleep(0.3)
        state["q_index"] += 1
        
        if state["q_index"] < len(questions):
            show_quiz()
        else:
            show_shop()

    def buy_ticket(e):
        if state["score"] > 0:
            show_final()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Masz bilet za piękne oczy ❤️"), bgcolor="pink")
            page.snack_bar.open = True
            page.update()
            time.sleep(1)
            show_final()

    def move_btn(e):
        e.control.top = random.randint(0, 400)
        e.control.left = random.randint(0, 200)
        e.control.text = random.choice(phrases)
        e.control.bgcolor = random.choice(["red", "orange", "grey"])
        page.update()

    def win(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    # Картинка из папки assets
                    ft.Image(src="/love.gif", width=300, border_radius=20),
                    ft.Text("JEJ! KOCHAM CIĘ JULLI! ❤️", size=30, color="red", weight="bold", text_align="center"),
                    ft.Text("Twój vall ❤️", size=18, weight="bold")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    # --- ЭКРАНЫ ---

    def show_quiz():
        page.clean()
        q = questions[state["q_index"]]
        
        items = [
            ft.Text(f"Pytanie {state['q_index']+1} z {len(questions)}", color="grey"),
            ft.Text(f"Róże: {state['score']} 🌹", size=20, color="red", weight="bold"),
            ft.Container(
                content=ft.Text(q["q"], size=22, weight="bold", text_align="center"),
                padding=20,
                bgcolor="white",
                border_radius=15
            )
        ]
        
        # Добавляем картинку только на первом вопросе (или на всех, если хочешь)
        # Если хочешь, чтобы кот был всегда, раскомментируй строку ниже:
        # items.insert(0, ft.Image(src="/cat.gif", width=150, border_radius=15))

        for i, ans in enumerate(q["answers"]):
            items.append(
                ft.ElevatedButton(
                    text=ans,
                    data=i, 
                    on_click=check_answer,
                    width=280,
                    height=50
                )
            )
        
        page.add(
            ft.Column(
                items,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def show_shop():
        page.clean()
        
        card = ft.Container(
            content=ft.Column(
                [
                    # Картинка из папки assets
                    ft.Image(src="/ticket.gif", width=150),
                    ft.Text("Bilet do Szczęścia", size=20, weight="bold"),
                    ft.Text(f"Cena: 1 róża", color="grey")
                ],
                horizontal_alignment="center"
            ),
            padding=20,
            bgcolor="white",
            border_radius=15,
            border=ft.border.all(2, "pink") 
        )
        
        buy_btn = ft.ElevatedButton(
            text="KUPUJĘ ❤️",
            on_click=buy_ticket,
            bgcolor="green",
            color="white",
            width=200,
            height=50
        )

        page.add(ft.Text("SKLEPIK MIŁOŚCI", size=28, weight="bold"), card, buy_btn)
        page.update()

    def show_final():
        page.clean()
        
        btn_yes = ft.ElevatedButton(
            text="TAK! ❤️", 
            on_click=win, 
            bgcolor="green", 
            color="white",
            width=140, 
            height=60
        )

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

# ВАЖНО: assets_dir="assets" говорит программе, где искать картинки
ft.app(target=main, assets_dir="assets")