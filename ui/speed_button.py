import flet as ft


def speed_button(video_player):
    button_container = ft.Container(
        ft.PopupMenuButton(
            content=ft.Icon(name=ft.Icons.SPEED),
            items=[
                ft.PopupMenuItem(
                    text="1x", on_click=lambda _: video_player.set_speed(1)
                ),
                ft.PopupMenuItem(
                    text="2x", on_click=lambda _: video_player.set_speed(2)
                ),
                ft.PopupMenuItem(
                    text="4x", on_click=lambda _: video_player.set_speed(4)
                ),
                ft.PopupMenuItem(
                    text="6x", on_click=lambda _: video_player.set_speed(6)
                ),
                ft.PopupMenuItem(
                    text="8x", on_click=lambda _: video_player.set_speed(8)
                ),
                ft.PopupMenuItem(
                    text="10x", on_click=lambda _: video_player.set_speed(10)
                ),
                ft.PopupMenuItem(
                    text="12x", on_click=lambda _: video_player.set_speed(12)
                ),
                ft.PopupMenuItem(
                    text="16x", on_click=lambda _: video_player.set_speed(16)
                ),
            ],
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        ),
        width=35,
        height=35,
        margin=ft.margin.only(right=2),
        border_radius=8,
        bgcolor="#191c20",  # Cor padrão
        alignment=ft.alignment.center,
    )

    # Função para aplicar efeito de hover
    def on_hover(e):
        if e.data == "true":
            button_container.bgcolor = "#242a31"  # Cor ao passar o mouse
        else:
            button_container.bgcolor = "#191c20"  # Cor padrão ao sair
        button_container.update()

    button_container.on_hover = on_hover  # Aplica o evento de hover

    return button_container
