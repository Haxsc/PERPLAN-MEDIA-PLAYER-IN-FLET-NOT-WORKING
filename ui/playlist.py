import flet as ft


def create_playlist_dialog(page, playlist, video_path):
    """Cria o diálogo da lista de reprodução."""

    def update_list():
        """Atualiza a interface com a nova ordem da lista."""
        content.controls.clear()

        # Verifica se a lista está vazia
        if not playlist:
            content.controls.append(
                ft.Container(
                    content=ft.Text(
                        "A playlist está vazia.",
                        color="gray",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        italic=True,
                    ),
                    bgcolor="lightgray",
                    padding=20,
                    margin=10,
                    alignment=ft.alignment.center,
                )
            )
        else:
            # Primeiro item: fixo e não movível
            # content.controls.append(
            #     ft.Container(
            #         content=ft.Text(
            #             playlist[0],  # 00Primeiro item fixo
            #             color="white",
            #             size=14,
            #             weight=ft.FontWeight.BOLD,
            #         ),
            #         bgcolor="blue",  # Destaque visual
            #         border=ft.border.all(1, "black"),
            #         border_radius=ft.border_radius.all(8),
            #         padding=8,
            #         margin=4,
            #         alignment=ft.alignment.center,
            #     )
            # )

            # Outros itens: movíveis e removíveis
            for i, item in enumerate(playlist):
                if item == video_path:
                    content.controls.append(
                        ft.Container(
                            content=ft.Text(
                                item,
                                color="white",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                            ),
                            bgcolor="blue",  # Destaque visual
                            border=ft.border.all(1, "black"),
                            border_radius=ft.border_radius.all(8),
                            padding=8,
                            margin=4,
                            alignment=ft.alignment.center,
                        )
                    )
                    continue
                content.controls.append(
                    ft.DragTarget(
                        group="list",
                        content=ft.Draggable(
                            group="list",
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Text(
                                            item,
                                            color="black",
                                            size=14,
                                            weight=ft.FontWeight.W_500,
                                        ),
                                        bgcolor="white",
                                        border=ft.border.all(1, "black"),
                                        border_radius=ft.border_radius.all(8),
                                        padding=8,
                                        margin=4,
                                        alignment=ft.alignment.center,
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        icon_color="red",
                                        tooltip="Remover",
                                        on_click=lambda e, index=i: remove_item(index),
                                    ),
                                ],
                            ),
                            data=i,  # Armazena o índice do item arrastado
                        ),
                        on_accept=lambda e, i=i: reorder_list(e.src_id, i),
                    )
                )

        # Adiciona o botão "Adicionar" ao final
        content.controls.append(
            ft.Container(
                content=ft.TextButton(
                    "Adicionar",
                    on_click=open_file_picker,  # Função para abrir o file picker
                    style=ft.ButtonStyle(
                        color="white",
                        bgcolor="blue",
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=10),  # Espaçamento acima do botão
            )
        )
        page.update()

    def reorder_list(src_id, to_index):
        """Reordena a lista com base no arrasto."""
        draggable = page.get_control(src_id)
        from_index = draggable.data  # Recupera o índice armazenado no Draggable
        if from_index == 0:  # Impede que o primeiro item seja movido
            return
        # Reordena a lista
        item = playlist.pop(from_index)
        playlist.insert(to_index, item)
        update_list()

    def remove_item(index):
        """Remove um item da lista."""
        if index == 0:  # Impede que o primeiro item seja removido
            return
        playlist.pop(index)
        update_list()

    def open_file_picker(e):
        """Abre o file picker para selecionar arquivos e adiciona à lista."""
        file_picker.pick_files(
            allowed_extensions=[
                "mp4",
                "avi",
                "mkv",
                "mov",
                "dav",
            ],  # Extensões permitidas
            allow_multiple=True,  # Permitir múltiplos arquivos
        )

    def file_picker_result(e: ft.FilePickerResultEvent):
        """Adiciona os arquivos selecionados à lista."""
        if e.files:
            for file in e.files:
                if file.path not in playlist:
                    playlist.append(file.path)  # Adiciona o caminho do arquivo à lista
            update_list()

    # File Picker
    file_picker = ft.FilePicker(on_result=file_picker_result)
    page.overlay.append(file_picker)

    # Conteúdo da lista de reprodução
    content = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        scroll="auto",  # Habilitar rolagem
    )
    update_list()

    # Função para fechar o diálogo
    def handle_close(e):
        list_reprodution.open = False
        page.update()

    # Criar o diálogo
    list_reprodution = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Lista de reprodução",
            size=18,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        ),
        content=content,
        actions=[
            ft.TextButton(
                "Fechar",
                on_click=handle_close,
                style=ft.ButtonStyle(
                    color="black",
                    bgcolor="white",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        bgcolor="lightgray",  # Fundo do diálogo
        shape=ft.RoundedRectangleBorder(radius=10),  # Borda arredondada
        alignment=ft.alignment.center,
    )
    return list_reprodution
