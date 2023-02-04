import json
import time
import sys
import re
from Crypto.Cipher import AES


class MyPassword:
    filename = "password.json"

    def __init__(self):
        self.new = {
            "id": "",
            "host": "",
            "username": "",
            "password": "",
            "history": [],
            "notes": "",
            "create-time": "",
            "update-time": ""
        }
        self.password = ""
        self.iv = b""
        self.data = []
        self.key = ""
        self.temp = b""
        self.start()

    def start(self):
        print("请输入密码：")
        self.password = input().zfill(16)
        print("请输入偏移：")
        self.iv = input().zfill(16).encode("utf-8")
        self.read()
        print("读取成功！")
        while True:
            command = input()
            if command == "search":
                self.search(input("请输入关键词："))
            elif command == "show":
                self.show(input("请输入id："))
            elif command == "history":
                self.history(input("请输入id："))
            elif command == "add":
                self.add()
            elif command == "remove":
                self.remove(input("删除条目id："))
            elif command == "update":
                self.update(input("修改条目id："))
            elif command == "reset password":
                self.reset()
            elif command == "exit":
                self.exit()
            elif command == "help":
                print('Input "search"/"show"/"history"/"add"/"remove"/"update"/"exit"/"reset password" to use the tool')
            else:
                print('Input "help" to read the command line help information')

    def read(self):
        with open(self.filename, "rb") as f:
            self.temp = f.read()
            self.decrypt()
        self.key = self.data[-1]["id"]

    def save(self):
        self.encrypt()
        with open(self.filename, "wb") as f:
            f.write(self.temp)

    def search(self, keywords):
        temp = []
        for item in self.data:
            if keywords in item["host"] or keywords in item["notes"]:
                temp.append({"id": item["id"], "host": item["host"], "notes": item["notes"]})
        for info in temp:
            print("id: %s" % info["id"])
            print("host: %s" % info["host"])
            print("notes: %s" % info["notes"])

    def add(self):
        self.new["id"] = str(int(self.key) + 1)
        self.new["host"] = input("请输入新网址：")
        if self.new["host"] == "exit":
            self.new["host"] = ""
            print("已退出修改操作")
        else:
            self.new["username"] = input("请输入登录账号：")
            self.new["password"] = input("请输入登录密码：")
            self.new["notes"] = input("请输入备注：")
            self.new["create-time"] = self.get_time()
            self.data.append(self.new)
            self.key = self.new["id"]
            self.new = {
                "id": "",
                "host": "",
                "username": "",
                "password": "",
                "history": [],
                "notes": "",
                "create-time": "",
                "update-time": ""
            }
            print("创建成功！")

    def remove(self, iid):
        if iid == "exit":
            print("已退出删除操作")
        else:
            print("原条目：")
            self.show(iid)
            ans = input("确认删除id为%s的条目？(yes/no) " % iid)
            if ans == "yes":
                self.data.pop(int(iid))
                if iid < self.key:
                    for i in range(int(iid), int(self.key)):
                        self.data[i]["id"] = str(i)
                self.key = str(int(self.key) - 1)
                print("删除成功！")
            else:
                print("已退出删除操作")

    def update(self, iid):
        if iid == "exit":
            print("已退出修改操作")
        else:
            print("原条目：")
            self.show(iid)
            print("输入新值/不输入即保留原值")
            self.data[int(iid)]["history"].append({
                "host": self.data[int(iid)]["host"],
                "username": self.data[int(iid)]["username"],
                "password": self.data[int(iid)]["password"],
                "notes": self.data[int(iid)]["notes"],
                "update-time": self.data[int(iid)]["update-time"]
            })
            self.data[int(iid)]["username"] = self.judge(iid, "username", input("请输入新登录账号："))
            self.data[int(iid)]["password"] = self.judge(iid, "password", input("请输入新登录密码："))
            self.data[int(iid)]["notes"] = self.judge(iid, "notes", input("请输入新备注："))
            self.data[int(iid)]["update-time"] = self.get_time()
            print("修改成功！")

    def show(self, iid):
        if iid == "exit":
            print("已退出查看操作")
        else:
            print("host: %s" % self.data[int(iid)]["host"])
            print("username: %s" % self.data[int(iid)]["username"])
            print("password: %s" % self.data[int(iid)]["password"])
            print("notes: %s" % self.data[int(iid)]["notes"])

    def history(self, iid):
        if iid == "exit":
            print("已退出查看历史操作")
        else:
            i = 1
            history_list = self.data[int(iid)]["history"]
            for history_info in history_list:
                print("条目历史记录： %d" % i)
                print("username: %s" % history_info["username"])
                print("password: %s" % history_info["password"])
                print("notes: %s" % history_info["notes"])
                print("update-time: %s" % history_info["update-time"])
                print("\n")
                i += 1

    def judge(self, iid, key, new_value):
        if new_value == "":
            return self.data[int(iid)][key]
        else:
            return new_value

    def reset(self):
        password = input("请输入新密码：")
        iv = input("请输入新偏移：")
        if password == input("请再次输入新密码：") and iv == input("请再次输入新偏移："):
            self.password = password
            self.iv = iv
            print("修改密码成功！")
        else:
            print("两次输入不一致，退出设置")

    def exit(self):
        if input("是否保存修改？(yes/no) ") == "yes":
            self.save()
            print("保存成功！")
        sys.exit()

    def encrypt(self):
        cipher = AES.new(self.password.encode("utf-8"), AES.MODE_CBC, self.iv)
        self.data = str(self.data).encode("utf-8")
        self.data = self.data + "\0".encode() * (16 - len(self.data) % 16)
        for i in range(int(len(self.data) / 16)):
            block = self.data[16 * i:16 * (i + 1)]
            self.temp += cipher.encrypt(block)

    def decrypt(self):
        cipher = AES.new(self.password.encode("utf-8"), AES.MODE_CBC, self.iv)
        temp = cipher.decrypt(self.temp).decode("utf-8")[1:-1].rstrip("\0").replace("'", '"')
        lists = [r.span() for r in re.finditer('"id"', temp)]
        for i in range(len(lists)):
            if i == len(lists) - 1:
                cut = temp[lists[i][0] - 1:-1]
            else:
                cut = temp[lists[i][0] - 1:lists[i + 1][0] - 3]
            self.data.append(json.loads(cut))
        self.temp = b""

    @staticmethod
    def get_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


MyPassword()
