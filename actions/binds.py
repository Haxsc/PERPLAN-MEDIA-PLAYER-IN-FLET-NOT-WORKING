import keyboard
import pygetwindow as gw
import win32gui
from ui.play_button import control_pause_button

binds_enabled = True
# Conjunto para rastrear teclas bloqueadas
teclas_bloqueadas = set()

def bloquear_tecla(tecla):
    if tecla not in teclas_bloqueadas:
        keyboard.block_key(tecla)
        teclas_bloqueadas.add(tecla)

def desbloquear_tecla(tecla):
    if tecla in teclas_bloqueadas:
        keyboard.unblock_key(tecla)
        teclas_bloqueadas.remove(tecla)

def is_window_in_focus():
    titulo_janela = "Media Player"
    try:
        # Obter a janela desejada pelo título
        janelas = gw.getWindowsWithTitle(titulo_janela)
        if janelas:
            janela = janelas[0]
            # Obter o identificador da janela atualmente em foco
            janela_foco = win32gui.GetForegroundWindow()
            if janela._hWnd == janela_foco:
                # Bloquear teclas
                bloquear_tecla('tab')
                bloquear_tecla('left')
                bloquear_tecla('right')
                bloquear_tecla('up')
                bloquear_tecla('down')
                return True
            else:
                # Desbloquear teclas
                desbloquear_tecla('tab')
                desbloquear_tecla('left')
                desbloquear_tecla('right')
                desbloquear_tecla('up')
                desbloquear_tecla('down')
                return False
        else:
            print(f'Nenhuma janela com o título "{titulo_janela}" foi encontrada.')
            return False
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False
  
def play_pause_action(video_player, play_button):
    if binds_enabled:
        control_pause_button(None, video_player, play_button)

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
        "retroceder": lambda: retroceder_frames(video_player, frames=1),  # Retrocede 1 frame
    }

    def handle_key(event):
        global binds_enabled
        if not binds_enabled:
            return

        # Verifica se a janela do programa está em foco
        if not is_window_in_focus():
            return

        key = event.name
        for action, bind_key in binds.items():
            if key == bind_key and action in actions:
                actions[action]()

    keyboard.on_press(handle_key)
