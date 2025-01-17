import socket
import json
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

# 設定ファイルからIPアドレスとPORTを取得
CONFIG_FILE = "server_config.txt"

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
    except FileNotFoundError:
        raise FileNotFoundError(f"設定ファイル {CONFIG_FILE} が見つかりません")
    except Exception as e:
        raise RuntimeError(f"設定ファイルの読み込み中にエラーが発生しました: {e}")

def start_client():
    mouse = MouseController()
    keyboard = KeyboardController()

    try:
        SERVER_IP, PORT = get_server_config()
        print(f"取得したサーバーIP: {SERVER_IP}, PORT: {PORT}")
    except Exception as e:
        print(e)
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, PORT))
        print(f"{SERVER_IP}:{PORT} に接続しました")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            try:
                event = json.loads(data.decode('utf-8'))
                event_type = event.get("type")

                if event_type == "mouse_move":
                    mouse.position = (event["x"], event["y"])
                elif event_type == "mouse_click":
                    button = Button[event["button"].split('.')[-1]]
                    if event["pressed"]:
                        mouse.press(button)
                    else:
                        mouse.release(button)
                elif event_type == "mouse_scroll":
                    mouse.scroll(event["dx"], event["dy"])
                elif event_type == "key_press":
                    key = eval(event["key"])
                    keyboard.press(key)
                elif event_type == "key_release":
                    key = eval(event["key"])
                    keyboard.release(key)
            except Exception as e:
                print(f"エラー: {e}")

if __name__ == "__main__":
    start_client()
