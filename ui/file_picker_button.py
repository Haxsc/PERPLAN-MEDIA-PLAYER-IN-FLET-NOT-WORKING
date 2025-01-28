import flet as ft

def create_file_picker_button(video_player, image_widget, controls, menu_bar, selected_files, page):

    def filer_picker_result(e: ft.FilePickerResultEvent):
        if dialog_video_file.result and dialog_video_file.result.files:
            # Adicionar os vídeos selecionados ao array
            for file in dialog_video_file.result.files:
                selected_files.append(file.path)

            # Atualizar o primeiro vídeo escolhido no widget
            selected_file = selected_files[0]  # Pega o primeiro arquivo da lista
            image_widget.src = selected_file
            button_file_picker.visible = False
            button_file_picker.update()
            image_widget.visible = True
            image_widget.update()
            controls.visible = True
            controls.update()
            menu_bar.visible = True
            menu_bar.update()
            video_player.starting_video(selected_file)
        else:
            selected_files.clear()

    # File picker dialog
    dialog_video_file = ft.FilePicker(on_result=filer_picker_result)
    page.overlay.append(dialog_video_file)

    # File picker button
    button_file_picker = ft.ElevatedButton(
        "Escolher Arquivo",
        on_click=lambda _: dialog_video_file.pick_files(
            allowed_extensions=["mp4", "avi", "mkv", "mov", "dav"],
            allow_multiple=True,  # Permitir múltiplos arquivos
        ),
        expand=True,
    )

    return button_file_picker  # Retorna o botão e o array de arquivos
