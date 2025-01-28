import flet as ft
from helpers import show_draggable_cursor, move_vertical_divider

def create_vertical_divider(container_media, container_contador, image_widget, page):
    return ft.GestureDetector(
        content=ft.VerticalDivider(
            width=8,
            color="gray",
        ),
        on_pan_update=lambda e: move_vertical_divider(e, container_media, container_contador, image_widget, page),
        on_hover=show_draggable_cursor,
    )
