import socket
import threading

# 伺服器設定
HOST = '127.0.0.1'
PORT = 5000

# 輸入暱稱
nickname = input("請輸入你的暱稱: ")

# 建立 socket 並連線
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

stop_thread = False


def receive_messages():
    """接收來自伺服器的訊息（訂閱模式）"""
    global stop_thread
    while not stop_thread:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                # 伺服器請求暱稱
                client.send(nickname.encode('utf-8'))
            elif message:
                print(message)
            else:
                break
        except:
            if not stop_thread:
                print("❌ 與伺服器的連線中斷")
            client.close()
            break


def send_messages():
    """發送訊息到伺服器"""
    global stop_thread
    while True:
        try:
            message = input()
            if message.lower() == '/quit':
                stop_thread = True
                client.close()
                print("👋 已離開聊天室")
                break
            elif message:
                client.send(message.encode('utf-8'))
        except:
            break


if __name__ == "__main__":
    print("=" * 40)
    print("🎉 歡迎來到聊天室！輸入 /quit 離開")
    print("=" * 40)

    # 建立接收訊息的執行緒（訂閱機制）
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    # 主執行緒負責發送訊息
    send_messages()
