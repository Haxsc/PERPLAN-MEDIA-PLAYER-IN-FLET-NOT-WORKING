import flet as ft

def show_draggable_cursor(e: ft.HoverEvent):
    e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
    e.control.update()
    
def move_vertical_divider(e, container_media, container_contador, image_widget, page):
    if e.delta_x > 0:  # Movendo para a direita
        if container_media.width + e.delta_x > page.width * 0.80:
            return
        container_media.width += e.delta_x
        container_media.update()
        container_contador.width -= e.delta_x
        container_contador.update()
    elif e.delta_x < 0:  # Movendo para a esquerda
        if container_media.width + e.delta_x < page.width * 0.70:
            return
        container_media.width += e.delta_x
        container_media.update()
        container_contador.width -= e.delta_x
        container_contador.update()

    # Ajusta o tamanho do widget de imagem
    image_widget.width = container_media.width
    image_widget.update()
    
def update_container_sizes(container_media, container_contador, image_widget, page):
    container_media.width = page.window.width * 0.79
    container_media.update()

    container_contador.width = page.width * 0.19
    container_contador.update()

    image_widget.width = page.window.width * 0.79
    image_widget.height = page.window.height * 0.8
    image_widget.update()