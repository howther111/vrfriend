import socket
import json
from pynput import mouse, keyboard

# 設定ファイルからIPアドレスとPORTを取得
CONFIG_FILE = "config/server_config.txt"
ON_OFF_FILE = "config/on_off_key.txt"
on_off_key = "q"

def get_server_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                ip = lines[0].strip()
                port = int(lines[1].strip())
                return ip, port
            else:
                raise ValueError("IPアドレスまたはPORTがファイルに正しく記述されていません")
        with open(ON_OFF_FILE, 'r') as file:
            line = file.readline()
            on_off_key = line
    except FileNotFoundError:
        raise FileNotFoundError(f"設定ファイル {CONFIG_FILE} が見つかりません")
    except Exception as e:
        raise RuntimeError(f"設定ファイルの読み込み中にエラーが発生しました: {e}")


def start_server():
    try:
        HOST, PORT = get_server_config()
        print(f"取得したサーバーIP: {HOST}, PORT: {PORT}")
    except Exception as e:
        print(e)
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"サーバーが{HOST}:{PORT}で待機中...")

        conn, addr = server_socket.accept()
        print(f"{addr} から接続されました")

        send_enabled = [True]

        def send_data(data):
            if send_enabled[0]:
                try:
                    conn.sendall(json.dumps(data).encode('utf-8'))
                except BrokenPipeError:
                    print("接続が切れました")
                    exit()

        def on_move(x, y):
            send_data({"type": "mouse_move", "x": x, "y": y})

        def on_click(x, y, button, pressed):
            send_data({
                "type": "mouse_click",
                "x": x,
                "y": y,
                "button": str(button),
                "pressed": pressed
            })

        def on_scroll(x, y, dx, dy):
            send_data({"type": "mouse_scroll", "dx": dx, "dy": dy})

        def on_press(key):
            if key == keyboard.KeyCode.from_char(on_off_key):
                send_enabled[0] = not send_enabled[0]
                status = "有効" if send_enabled[0] else "無効"
                print(f"送信が{status}になりました")
            else:
                send_data({"type": "key_press", "key": str(key)})

        def on_release(key):
            send_data({"type": "key_release", "key": str(key)})

        with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener, \
                keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()


if __name__ == "__main__":
    start_server()
