import threading
import flet as ft
from actions.binds import is_window_in_focus, start_binds
from ui.help import create_help_dialog
from ui.playlist import create_playlist_dialog
from video_player import VideoPlayer
from helpers import update_container_sizes
from media.media_container import create_container_media
from media.media_player import create_media_container
from media.vertical_divider import create_vertical_divider
from ui.ui import loading_overlay, image_widget
from ui.controls import create_controls
from ui.seek import create_seek_bar
from ui.file_picker_button import create_file_picker_button


def check_focus(page):
    titulo_janela = page.title
    thread_foco = threading.Thread(target=is_window_in_focus, args=(titulo_janela,))
    thread_foco.daemon = (
        True  # A thread será finalizada quando o programa principal terminar
    )
    thread_foco.start()


def main(page: ft.Page):
    page.title = "Media Player"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "none"
    page.window.maximized = True
    playlist = []
    ### Block Keys
    check_focus(page)

    ### Video Player
    video_player = VideoPlayer(
        page, image_widget, None, loading_overlay, playlist, None
    )
    seek_bar = create_seek_bar(video_player)
    video_player.seek_bar = seek_bar

    ### Controls
    controls_main = create_controls(video_player, seek_bar)
    controls = controls_main["controls"]
    play_button = controls_main["play_button"]
    video_player.play_button = play_button

    ### MENU BAR
    def open_playlist(e):
        list_reprodution = create_playlist_dialog(
            page, playlist, video_player.video_path
        )  # Recria o diálogo com o estado atualizado
        page.overlay.append(list_reprodution)
        list_reprodution.open = True
        page.update()

    def open_help(e):
        print("Ajuda")
        help = create_help_dialog(page)
        page.overlay.append(help)
        help.open = True
        page.update()

    menu_bar = ft.Row(
        controls=[
            ft.TextButton(
                "Mídia",
                on_click=lambda e: print("Mídia"),
                style=ft.ButtonStyle(color="white"),
            ),
            ft.TextButton(
                "Reprodução",
                on_click=open_playlist,
                style=ft.ButtonStyle(color="white"),
            ),
            ft.TextButton(
                "Ajuda", on_click=open_help, style=ft.ButtonStyle(color="white")
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        visible=False,
    )

    ### Media Player
    button_file_picker = create_file_picker_button(
        video_player, image_widget, controls, menu_bar, playlist, page
    )
    media = create_media_container(button_file_picker, image_widget, page)
    container_media = create_container_media(
        media, controls, page, playlist, video_player.video_path
    )
    container_contador = ft.Container(
        content=ft.Text("Container Contador", size=18, color="white"),
        width=page.width * 0.20 - 2,
        alignment=ft.alignment.center,
    )

    vertical_divider = create_vertical_divider(
        container_media, container_contador, image_widget, page
    )

    ### Title hover
    def update_overlay():
        existing_title = next(
            (item for item in page.overlay if isinstance(item, ft.Stack)), None
        )

        if existing_title is None:
            title = ft.Stack(
                visible=False,
                disabled=True,
                opacity=0.0,
                animate_opacity=ft.animation.Animation(
                    duration=500,
                    curve=ft.AnimationCurve.EASE_IN_OUT,
                ),
                alignment=ft.alignment.center,
                left=10,
            )
            page.overlay.append(title)
        else:
            title = existing_title

        text_size = 30
        if page.width * 0.02 < text_size:
            text_size = page.width * 0.02

        # Atualizar o conteúdo do título e do ícone de play/pausa
        title.controls = [
            ft.Text(
                spans=[
                    ft.TextSpan(
                        video_player.video_path,
                        ft.TextStyle(
                            size=text_size,
                            weight=ft.FontWeight.BOLD,
                            foreground=ft.Paint(
                                color=ft.Colors.BLACK,
                                stroke_width=6,
                                stroke_join=ft.StrokeJoin.ROUND,
                                style=ft.PaintingStyle.STROKE,
                            ),
                        ),
                    ),
                ],
                top=0,
            ),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        video_player.video_path,
                        ft.TextStyle(
                            size=text_size,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_300,
                        ),
                    ),
                ],
                top=0,
            ),
            # Ícone de play/pausa dinâmico
            ft.Container(
                content=ft.Icon(
                    name=(
                        ft.icons.PLAY_ARROW
                        if not video_player.playing
                        else ft.icons.PAUSE
                    ),
                    size=80,
                    color=ft.Colors.WHITE,
                ),
                alignment=ft.alignment.center,
                width=page.width * 0.80,
                left=2,
                height=page.window.height,
                ignore_interactions=True,
            ),
        ]

        title.width = page.width * 0.80
        title.alignment = ft.alignment.center
        title.top = page.window.height * 0.07
        title.height = page.window.height - page.window.height * 0.25

        title.visible = bool(video_player.video_path)
        title.disabled = not title.visible

        page.update()

    def show_draggable_cursor(e: ft.HoverEvent):
        """Exibe o título e o ícone ao passar o mouse."""
        update_overlay()

        # Ajustar opacidade baseado no hover
        title = next(
            (item for item in page.overlay if isinstance(item, ft.Stack)), None
        )
        if title:
            title.opacity = 1.0 if e.data == "true" else 0.0
            page.update()

    container_media.on_hover = lambda e: show_draggable_cursor(e)

    def toggle_play_pause(e):
        video_player.control_pause()

        # Atualizar o overlay para refletir o novo estado do ícone
        update_overlay()

    container_media.on_click = lambda e: toggle_play_pause(e)

    page.add(
        menu_bar,
        ft.Container(
            ft.Row(
                controls=[
                    container_media,
                    vertical_divider,
                    container_contador,
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
        ),
    )

    page.on_resized = lambda event: update_container_sizes(
        container_media, container_contador, image_widget, page
    )
    update_container_sizes(container_media, container_contador, image_widget, page)

    start_binds(video_player)


ft.app(target=main)
