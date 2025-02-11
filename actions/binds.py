import keyboard
import pygetwindow as gw
import win32gui
import time

binds_enabled = True
teclas_bloqueadas = set()
window_focus = False


def block_key(tecla):
    if tecla not in teclas_bloqueadas:
        keyboard.block_key(tecla)
        teclas_bloqueadas.add(tecla)


def unlock_key(tecla):
    if tecla in teclas_bloqueadas:
        keyboard.unblock_key(tecla)
        teclas_bloqueadas.remove(tecla)


def is_window_in_focus(titulo_janela):
    global window_focus
    while True:
        try:
            janelas = gw.getWindowsWithTitle(titulo_janela)
            if janelas:
                janela = janelas[0]

                janela_foco = win32gui.GetForegroundWindow()
                if janela._hWnd == janela_foco:
                    if keyboard.is_pressed("alt"):
                        unlock_key("tab")
                    else:
                        block_key("tab")
                    # block_key('left')
                    # block_key('right')
                    block_key("up")
                    block_key("down")
                    time.sleep(0.4)
                    window_focus = True
                else:
                    unlock_key("tab")
                    # unlock_key('left')
                    # unlock_key('right')
                    unlock_key("up")
                    unlock_key("down")
                    time.sleep(0.4)
                    window_focus = False
            else:
                time.sleep(0.24)
                window_focus = False

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            time.sleep(0.2)
            window_focus = False


def play_pause_action(video_player, play_button):
    if binds_enabled:
        video_player.control_pause()


def avance_frames(video_player, frames):
    global binds_enabled
    binds_enabled = False
    try:
        video_player.avance_frames(frames)
    finally:
        binds_enabled = True


def retroceder_frames(video_player, frames):
    global binds_enabled
    binds_enabled = False
    try:
        video_player.retroceder_frames(frames)
    finally:
        binds_enabled = True


def start_binds(video_player, play_button):
    """Inicia os binds, verificando automaticamente o foco da janela."""
    binds = {
        "play_pause": "space",
        "avance": "e",
        "retroceder": "q",
    }

    actions = {
        "play_pause": lambda: play_pause_action(video_player, play_button),
        "avance": lambda: avance_frames(video_player, frames=1),  # Avança 1 frame
        "retroceder": lambda: retroceder_frames(
            video_player, frames=1
        ),  # Retrocede 1 frame
    }

    def handle_key(event):
        global binds_enabled
        if not binds_enabled:
            return

        # Verifica se a janela do programa está em foco
        if not window_focus:
            return

        key = event.name
        for action, bind_key in binds.items():
            if key == bind_key and action in actions:
                actions[action]()

    keyboard.on_press(handle_key)
