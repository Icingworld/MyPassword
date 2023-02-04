from Crypto.Cipher import AES
data = [
    {
        "id": "0",
        "host": "52pojie.cn",
        "username": "",
        "password": "",
        "history": [],
        "notes": "",
        "create-time": "",
        "update-time": ""
    }
]
password = "password".zfill(16)  # 设置初始密码
iv = "iv".zfill(16).encode("utf-8")  # 设置初始偏移
test = b""
cipher = AES.new(password.encode('utf-8'), AES.MODE_CBC, iv)
data = str(data).encode()
data = data + "\0".encode() * (16 - len(data) % 16)
for i in range(int(len(data) / 16)):
    block = data[16 * i:16 * (i + 1)]
    b = cipher.encrypt(block)
    test += b
cipher1 = AES.new(password.encode('utf-8'), AES.MODE_CBC, iv)
test2 = cipher1.decrypt(test)
with open("password.json", "wb") as f:
    f.write(test)
