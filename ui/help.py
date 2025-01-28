import flet as ft

def create_help_dialog(page):
    def handle_close(e):
        dialog.open = False
        page.update()
        
    dialog = ft.AlertDialog(
        title=ft.Text("Ajuda" ,text_align= ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
        content=ft.Text(
            "Bem-vindo ao Media Player! Para utilizar o Media Player, siga os seguintes passos:\n\n"
            "1. Clique no botão 'ESPAÇO' para iniciar a reprodução do video selecionado.\n"
            "2. O botão 'ESPAÇO' pausar a reprodução do video.\n"
            "3. O botão 'E' avançar a reprodução em 1 frame.\n"
            "4. O botão 'Q' voltar a reprodução em 1 frame.\n"
            "5. O botão '+' mudar a velocidade da reprodução do video.\n"
            "6. O botão '-' mudar a velocidade da reprodução do video.\n"
        ),
        actions=[
            ft.TextButton("Fechar", on_click=lambda e: handle_close(e))
        ],
    )
    return dialog