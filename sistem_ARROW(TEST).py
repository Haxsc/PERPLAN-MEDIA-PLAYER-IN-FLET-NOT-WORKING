import math
import flet as ft
import flet.canvas as cv

def main(page: ft.Page):
    # Lista para armazenar os pontos da curva
    points = []

    # Variável para controlar a espessura da curva
    stroke_width = 5

    # Função chamada ao iniciar o arrasto
    def on_pan_start(e: ft.DragStartEvent):
        points.clear()
        points.append((e.local_x, e.local_y))

    # Função chamada durante o arrasto
    def on_pan_update(e: ft.DragUpdateEvent):
        points.append((e.local_x, e.local_y))
        draw_curve()

    # Função chamada ao finalizar o arrasto
    def on_pan_end(e: ft.DragEndEvent):
        nonlocal points
        if len(points) > 1:
            initial_list = points[:3]
            end_list = points[-3:]
            m2_list = points[3:-3]
            middle_list = m2_list[::3]

            newlist = initial_list + middle_list + end_list
            draw_new_curve(newlist)

    # Função para desenhar a curva e, opcionalmente, a ponta da seta
    def draw_curve(final=False):
        canvas.shapes.clear()
        if len(points) > 1:
            path_elements = [cv.Path.MoveTo(points[0][0], points[0][1])]
            for i in range(1, len(points) - 2):
                x0, y0 = points[i]
                x1, y1 = points[i + 1]
                xc = (x0 + x1) / 2
                yc = (y0 + y1) / 2
                path_elements.append(cv.Path.QuadraticTo(x0, y0, xc, yc))
            path_elements.append(cv.Path.LineTo(points[-1][0], points[-1][1]))
            canvas.shapes.append(
                cv.Path(
                    path_elements,
                    paint=ft.Paint(
                        stroke_width=stroke_width,  # Ajuste da espessura
                        style=ft.PaintingStyle.STROKE,
                        color=ft.Colors.BLACK,
                    ),
                )
            )
            if final:
                # Adiciona a ponta da seta na extremidade da curva
                add_arrow_head(points[-2], points[-1])
        canvas.update()

    def draw_new_curve(points):
        canvas.shapes.clear()
        if len(points) > 1:
            path_elements = [cv.Path.MoveTo(points[0][0], points[0][1])]
            for i in range(1, len(points) - 2):
                x0, y0 = points[i]
                x1, y1 = points[i + 1]
                xc = (x0 + x1) / 2
                yc = (y0 + y1) / 2
                path_elements.append(cv.Path.QuadraticTo(x0, y0, xc, yc))
            path_elements.append(cv.Path.LineTo(points[-1][0], points[-1][1]))
            canvas.shapes.append(
                cv.Path(
                    path_elements,
                    paint=ft.Paint(
                        stroke_width=stroke_width,  # Ajuste da espessura
                        style=ft.PaintingStyle.STROKE,
                        color=ft.Colors.BLACK,
                    ),
                )
            )
        add_arrow_head(points[-3], points[-1])
        canvas.update()

    # Função para adicionar a ponta da seta
    def add_arrow_head(start, end):
        # Calcula o ângulo da linha final da curva
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        # Define o comprimento e o ângulo da ponta da seta
        arrow_length = stroke_width * 5
        arrow_angle = math.pi / 6
        # Calcula as coordenadas dos pontos da ponta da seta
        left_x = end[0] - arrow_length * math.cos(angle - arrow_angle)
        left_y = end[1] - arrow_length * math.sin(angle - arrow_angle)
        right_x = end[0] - arrow_length * math.cos(angle + arrow_angle)
        right_y = end[1] - arrow_length * math.sin(angle + arrow_angle)
        # Desenha as linhas da ponta da seta
        canvas.shapes.append(
            cv.Line(
                end[0],
                end[1],
                left_x,
                left_y,
                paint=ft.Paint(stroke_width=stroke_width, color=ft.Colors.BLACK),
            )
        )
        canvas.shapes.append(
            cv.Line(
                end[0],
                end[1],
                right_x,
                right_y,
                paint=ft.Paint(stroke_width=stroke_width, color=ft.Colors.BLACK),
            )
        )

    # Slider para ajustar a espessura
    def on_slider_change(e):
        nonlocal stroke_width
        stroke_width = e.control.value

    slider = ft.Slider(
        min=1,
        max=10,
        value=5,
        label="Espessura: {value}",
        on_change=on_slider_change,
    )

    # Cria o canvas e o GestureDetector para capturar os eventos do mouse
    canvas = cv.Canvas(
        [],
        content=ft.GestureDetector(
            on_pan_start=on_pan_start,
            on_pan_update=on_pan_update,
            on_pan_end=on_pan_end,
            drag_interval=10,
        ),
        expand=True,
    )

    page.add(slider)
    page.add(canvas)

ft.app(main)
