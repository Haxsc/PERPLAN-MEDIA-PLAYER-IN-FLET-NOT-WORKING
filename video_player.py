import base64
import queue
import threading
import time
import cv2
import flet as ft


class VideoPlayer:
    def __init__(
        self, page, image_widget, seek_bar, loading_overlay, playlist, play_button
    ):
        self.page = page
        self.image_widget = image_widget
        self.seek_bar = seek_bar
        self.loading_overlay = loading_overlay
        self.cap = None
        self.playing = False
        self.current_frame = 0
        self.total_frames = 0
        self.fps = 0
        self.speed_factor = 1
        self.buffer = queue.Queue(maxsize=5)  # Buffer maior
        self.seek_interacting = False
        self.reader_thread = None
        self.playlist = playlist
        self.play_button = play_button
        self.video_path = None
        self.proceed_playlist = False

        self.paused_15 = False
        self.paused_30 = False
        self.paused_45 = False
        self.skiped = False

    def control_pause(self, event=None):
        if self.playing:
            self.pause()
        else:
            self.play()

    def control_playlist(self, event=None):
        if self.proceed_playlist:
            self.proceed_playlist = False
        else:
            self.proceed_playlist = True

    def show_loading(self, message="Carregando..."):
        self.loading_overlay.content = ft.Container(
            content=ft.Column(
                [
                    # ft.Text(message, size=20, weight=ft.FontWeight.BOLD, color="white"),
                    ft.ProgressRing(),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            bgcolor="rgba(0, 0, 0, 0.7)",
            expand=True,
        )
        self.page.overlay.append(self.loading_overlay)
        self.page.update()

    def hide_loading(self):
        self.page.overlay.remove(self.loading_overlay)
        self.page.update()

    def load_video(self, video_path):
        self.show_loading("Carregando vídeo...")
        self.video_path = video_path
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            self.hide_loading()
            snack_bar = ft.SnackBar(
                ft.Text(
                    "Erro ao abrir o vídeo.",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    text_align=ft.TextAlign.CENTER,
                ),
                duration=3500,
                bgcolor="red",
            )
            self.page.open(snack_bar)
            self.page.update()
            return False

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.seek_bar.max = self.total_frames
        self.seek_bar.value = 0
        self.seek_bar.update()
        self.current_frame = 0
        self.buffer.queue.clear()  # Limpa o buffer de frames
        self.hide_loading()
        return True

    def start_buffer_thread(self):
        def buffer_frames():
            while self.playing and self.cap.isOpened():
                if not self.buffer.full():
                    ret, frame = self.cap.read()

                    if not ret:
                        print("Fim do vídeo ou erro na leitura do frame.")
                        self.playing = False
                        break

                    # Atualiza o número de frames atuais
                    self.current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

                    # Se o fator de velocidade for maior que 1, pula frames
                    if self.speed_factor > 1:
                        skip_frames = int(self.speed_factor) - 1
                        for _ in range(skip_frames):
                            ret, _ = self.cap.read()
                            if not ret:
                                break  # Para a leitura se não houver mais frames disponíveis
                            self.current_frame = int(
                                self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                            )

                    # Adiciona o frame ao buffer apenas se houver espaço
                    try:
                        self.buffer.put(frame, timeout=0.1)  # Evita bloqueios
                    except queue.Full:
                        print("Aviso: Buffer cheio! Frame descartado.")

                else:
                    time.sleep(0.005)  # Reduz a espera para melhorar a eficiência

        # Inicia a thread de leitura de frames
        self.reader_thread = threading.Thread(target=buffer_frames, daemon=True)
        self.reader_thread.start()

    def play(self, event=None):
        if not self.cap or not self.cap.isOpened():
            print("Erro: VideoCapture não está aberto.")
            return

        if self.playing:
            print("Já está reproduzindo.")
            return

        self.playing = True
        self.play_button.content = ft.Icon(
            name=ft.Icons.PAUSE,
            # color="#505050",
        )
        self.play_button.update()
        self.start_buffer_thread()

        def playback_thread():
            frame_time = 1 / self.fps  # Tempo normal entre frames
            last_time = time.time()

            while self.playing:
                if not self.buffer.empty():
                    frame = self.buffer.get()
                    self._display_frame(frame)
                    self.current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                    self.seek_bar.value = min(self.current_frame, self.seek_bar.max)
                    self.seek_bar.update()

                    sleep_time = max(
                        0, (frame_time / self.speed_factor) - (time.time() - last_time)
                    )

                    if (
                        self.current_frame
                        >= (self.total_frames * (1 / 4) - (self.speed_factor / 2))
                        and self.current_frame
                        <= (self.total_frames * (1 / 4) + (self.speed_factor / 2))
                        and not self.paused_15
                    ):  # 15 minutos
                        self.paused_15 = True
                        self.pause()
                        self.show_pause_message(
                            "Pausado automaticamente, Lembre-se de salvar o progresso."
                        )
                    elif (
                        self.current_frame
                        >= (self.total_frames * (2 / 4) - self.speed_factor)
                        and self.current_frame
                        <= (self.total_frames * (2 / 4) + self.speed_factor)
                        and not self.paused_30
                    ):  # 30 minutos
                        self.paused_30 = True
                        self.pause()
                        self.show_pause_message(
                            "Pausado automaticamente, Lembre-se de salvar o progresso."
                        )
                    elif (
                        self.current_frame
                        >= (self.total_frames * (3 / 4) - self.speed_factor)
                        and self.current_frame
                        <= (self.total_frames * (3 / 4) + self.speed_factor)
                        and not self.paused_45
                    ):  # 45 minutos
                        self.paused_45 = True
                        self.pause()
                        self.show_pause_message(
                            "Pausado automaticamente, Lembre-se de salvar o progresso."
                        )
                    elif (
                        self.current_frame >= (self.total_frames * (3 / 4) + 100)
                        and self.paused_45
                    ):
                        self.paused_45 = False
                        self.paused_30 = False
                        self.paused_15 = False
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    last_time = time.time()
                    if self.proceed_playlist:
                        print(f" {self.current_frame}/{self.seek_bar.max}")
                        maxvideo = self.seek_bar.max - self.seek_bar.value
                        print(maxvideo)
                        if maxvideo < 40:
                            print("PULANDO DE VIDEO ...")
                            if self.skiped == False:
                                self.skiped = True
                                self.pause()
                                time.sleep(0.5)
                                self.skip_video()
                else:
                    time.sleep(0.001)

        threading.Thread(target=playback_thread, daemon=True).start()

    def show_pause_message(self, message):
        self.page.open(
            ft.SnackBar(
                content=ft.Text(
                    message,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    text_align=ft.TextAlign.CENTER,
                ),
                bgcolor="orange",
                duration=3500,
            )
        )
        self.page.update()

    def pause(self, event=None):
        self.playing = False
        self.play_button.content = ft.Icon(
            name=ft.Icons.PLAY_ARROW,
            # color="#505050",
        )
        self.play_button.update()
        if self.reader_thread and self.reader_thread.is_alive():
            self.reader_thread.join()

        # Resetar o buffer
        # with self.buffer.mutex:
        #     self.buffer.queue.clear()

    def set_speed(self, speed_factor, event=None):
        self.speed_factor = max(1, min(speed_factor, 16))
        print(f"Velocidade ajustada para: {self.speed_factor}x")

    def seek(self, frame_position):
        starting = False
        # if self.playing:
        #     starting = True
        if not self.cap or not self.cap.isOpened():
            return
        self.pause()
        self.show_loading()
        try:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_position)
            self.current_frame = int(
                self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            )  # Atualiza a posição real
            self.seek_bar.value = self.current_frame
            self.seek_bar.update()

            temp_buffer = []

            while not self.buffer.empty():
                temp_buffer.append(self.buffer.get())

            if temp_buffer:
                first_frame = temp_buffer[0]  # Primeiro frame do buffer
                print(first_frame)
            ret, frame = self.cap.read()
            if ret:
                self._display_frame(frame)
            else:
                print(
                    f"Erro ao capturar o frame no seek para a posição {frame_position}"
                )
        except Exception as e:
            print(f"Erro ao realizar seek: {e}")
        finally:
            if starting:
                self.play()
            self.hide_loading()

    def start_seek_interaction(self):
        self.seek_interacting = True
        self.pause()

    def end_seek_interaction(self):
        self.seek_interacting = False
        self.seek(int(self.seek_bar.value))
        self.play()

    def _display_frame(self, frame):
        try:
            frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_LINEAR)
            _, encoded_image = cv2.imencode(
                ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 65]
            )
            base64_image = base64.b64encode(encoded_image).decode()
            self.image_widget.src_base64 = base64_image
            self.image_widget.update()
        except Exception as e:
            print(f"Erro ao exibir o frame: {e}")

    def starting_video(self, video_path):
        # Carregar o vídeo
        if not self.load_video(video_path):
            return  # Se o vídeo não puder ser carregado, pare aqui

        # Definir o frame inicial e exibi-lo
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Posiciona no início do vídeo
        ret, frame = self.cap.read()  # Lê o primeiro frame
        if ret:
            self._display_frame(frame)  # Exibe o frame na interface
            self.current_frame = 0  # Atualiza a posição atual
            self.seek_bar.value = 0  # Atualiza a barra de progresso
            self.seek_bar.update()
        else:
            print("Erro ao ler o primeiro frame do vídeo.")

        # Garantir que a interface seja atualizada
        self.page.update()

    def avance_frames(self, frames):
        if int(self.current_frame + frames) >= self.seek_bar.max:
            return
        self.seek(min(self.seek_bar.max, int(self.current_frame + frames)))

    def retroceder_frames(self, frames):
        if int(self.current_frame - frames) <= 0:
            return
        self.seek(max(0, int(self.current_frame - frames)))

    def skip_video(self, e=None):
        self.paused_45 = False
        self.paused_30 = False
        self.paused_15 = False

        try:
            self.pause()
            # Obtém o índice atual do vídeo
            current_index = self.playlist.index(self.video_path)

            # Calcula o próximo índice
            next_index = current_index + 1

            # Verifica se o próximo índice está dentro do intervalo
            self.skiped = False
            if next_index < len(self.playlist):
                # Carregar o próximo vídeo
                if self.load_video(self.playlist[next_index]):
                    # Definir e exibir o primeiro frame
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = self.cap.read()
                    if ret:
                        self._display_frame(frame)
                        self.current_frame = 0
                        self.seek_bar.value = 0
                        self.seek_bar.update()
                    else:
                        print("Erro ao ler o primeiro frame do próximo vídeo.")
                else:
                    print("Erro ao carregar o próximo vídeo.")
            else:
                print("Você chegou ao fim da playlist.")
        except ValueError:
            print("Current video not found in the playlist.")

        # Garantir que a interface seja atualizada
        self.page.update()

    def previous_video(self, e=None):
        self.paused_45 = False
        self.paused_30 = False
        self.paused_15 = False

        try:
            self.pause()
            # Obtém o índice atual do vídeo
            current_index = self.playlist.index(self.video_path)

            # Calcula o índice do vídeo anterior
            previous_index = current_index - 1

            # Verifica se o índice do vídeo anterior é válido
            if previous_index >= 0:
                # Carregar o vídeo anterior
                if self.load_video(self.playlist[previous_index]):
                    # Definir e exibir o primeiro frame
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = self.cap.read()
                    if ret:
                        self._display_frame(frame)
                        self.current_frame = 0
                        self.seek_bar.value = 0
                        self.seek_bar.update()
                    else:
                        print("Erro ao ler o primeiro frame do vídeo anterior.")
                else:
                    print("Erro ao carregar o vídeo anterior.")
            else:
                print("Você já está no primeiro vídeo da playlist.")
            self.skiped = False
        except ValueError:
            print("Current video not found in the playlist.")

        # Garantir que a interface seja atualizada
        self.page.update()
