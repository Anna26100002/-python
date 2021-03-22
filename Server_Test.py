import socket
import pyodbc
import urllib.request
import json
from datetime import datetime
import requests


id_name = ""
Lol = ""

surname = ""
name = ""
number = ""


def Main():
    host = '127.0.0.1'
    port = 7000

    message_for = ""

    mySocket = socket.socket()
    mySocket.bind((host, port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print("Connection from: " + str(addr))

    while True:
        try:
            data = conn.recv(1024).decode()
        except:
            print("Клиент потерялся")
            mySocket.close()
            Main()

        command_for_operation = str(data)

        if command_for_operation == "check_server":
            Live_Server()
        elif command_for_operation == "check_number_card":
            info = str(conn.recv(1024).decode())
            message_for = info
            Add_Number_Card_BD(info)
            if Lol == "OK":
                conn.send(Lol.encode())
            else:
                conn.send(Lol.encode())
        elif command_for_operation == "add_password":
            data = conn.recv(1024).decode()
            info = str(data)
            if Lol != "Zapis_1":
                Add_Password_For_Enter(info)
            else:
                Find_Password(info)

            if Lol == "OK":
                conn.send(Lol.encode())
            else:
                conn.send(Lol.encode())
        elif command_for_operation == "Transfer_To_Card":
            info = str(conn.recv(1024).decode())
            Transfer_To_Card(info, conn)
        elif command_for_operation == "check":
            Check_Zapis()
            conn.send(Lol.encode())
        elif command_for_operation == "kurs_valut":
            Send_Message_Value_Valut(conn)
        elif command_for_operation == "Info_User":
            Send_Info_Client(message_for, conn)
        elif command_for_operation == "Info_User_Other_Card":
            Check_Zapis_Other_Card(conn)
        elif command_for_operation == "Operation_Histori":
            Istoria_Operation(conn)
        elif command_for_operation == "zapis_password_for_id":
            Find_Surname_Name_ID(conn)
        elif command_for_operation == "Send_Password":
            Find_Password_For_Chek(conn)
        elif command_for_operation == "Bank_corr":
            Transfer_(conn)

def Check_Zapis():
    global Lol, id_name
    k = 0
    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    cursor.execute("SELECT * FROM user1")
    for row in cursor.fetchall():
        k = k + 1
        id_name = row.Code
        Lol = "Zapis_1"
    if k == 0:
        Lol = "Nothing"


def Find_Surname_Name_ID(conn):
    global id_name, number
    text = ""
    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        if id_name == row.Code:
            text = str(row.Surname) + " " + str(row.Name) + " " + str(row.Number) + " " + str(row.MoneyBalance)
            number = row.Number
        else:
            pass
    conn.send(text.encode())


def Check_Zapis_Other_Card(conn):
    global name, surname, id_name
    text = ""
    k = 0
    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    cursor.execute("SELECT * FROM users WHERE Name = '" + name + "' AND Surname = '" + surname + "'")
    for row in cursor.fetchall():
        if row.Code == id_name:
            pass
        elif row.Code != id_name:
            text = text + str(row.Number) + " " + str(row.MoneyBalance) + " "
            text = text + "/"
            k += 1
    if k != 0:
        conn.send(text.encode())
    elif k == 0:
        text = "Nothing"
        conn.send(text.encode())


def Live_Server():
    print("Сервер даёт показания жизни!")


def Find_Password(info):
    global id_name, Lol
    k = 0
    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    cursor.execute("SELECT * FROM user1 WHERE Password = '" + info + "'")
    for row in cursor.fetchall():
        id_name = row.Code
        k = k + 1
    if k == 1:
        Lol = "OK"
    else:
        Lol = "ERROR"


def Add_Number_Card_BD(info):
    global id_name, Lol, name, surname
    k = 0
    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE Number = '" + info + "'")
        for row in cursor.fetchall():
            id_name = row.Code
            name = row.Name
            surname = row.Surname
            k = k + 1
    except:
        k = 0

    if k != 0:
        Lol = "OK"
    else:
        Lol = "ERROR"


def Add_Password_For_Enter(info):
    global id_name
    global Lol
    k = 0
    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    try:
        cursor.execute("INSERT INTO user1 (Code, Password) VALUES (?, ?)", id_name, info)
        coon.commit()
        k = 1
    except:
        k = 0

    if k != 0:
        Lol = "OK"
    else:
        Lol = "ERROR"

def Find_Value_Valut(command_value):
    num = ""
    num_1 = ""
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response = urllib.request.urlopen(url)
    data = json.load(response)
    for i in data:
        if i == 'Valute':
            num = i
            for i in data[i]:
                if i == command_value:
                    num_1 = i
                    for i in data[num][num_1]:
                        if i == 'Value':
                            return "%.2f" % data[num][num_1][i]


def Send_Info_Client(message_for, conn):
    global number
    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    cursor.execute("SELECT * FROM users WHERE Number = '" + message_for + "'")
    for row in cursor.fetchall():
        send_message = str(row.Name) + " " + str(row.Surname) + " " + str(message_for) + " " + str(row.MoneyBalance)
        number = message_for
        conn.send(send_message.encode())


def Istoria_Operation(conn):
    global number
    send_message = ""
    k = 0
    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    cursor.execute("SELECT * FROM Histori WHERE NumberCardSend = '" + number + "'")
    for row in cursor.fetchall():
        send_message = send_message + str(row.Operation) + " " + str(row.NumberCardSend) + " // " + str(
            row.NumberCard) + \
                       " // " + str(row.MoneySend) + " " + str(row.DateSend) + " / "
        k += 1
    if k != 0:
        conn.send(send_message.encode())
    else:
        send_message = "Nothing"
        conn.send(send_message.encode())


def Find_Password_For_Chek(conn):
    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    cursor.execute("SELECT * FROM user1")
    for row in cursor.fetchall():
        text = row.Password
    conn.send(text.encode())


def Transfer_To_Card(info, conn):
    global id_name, Lol, number
    money_for_transfer = ""
    number_card = ""
    number_card_user = ""
    money_now = ""
    money_now_1 = ""
    k = 0
    kol = 0
    for i in info.split(" "):
        if k < 4 and kol == 0 and i != "//":
            number_card = number_card + i + " "
        elif i == "//":
            k = 0
            kol += 1
        elif k < 4 and kol == 1 and i != "//":
            number_card_user = number_card_user + i + " "
        elif kol > 1:
            money_for_transfer = i

    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    kolp = 0
    cursor.execute("SELECT * FROM users WHERE Number = '" + number_card_user + "'")
    for row in cursor.fetchall():
        if not float(str(row.MoneyBalance)) < float(money_for_transfer):
            money_now = str(float(str(row.MoneyBalance)) - float(money_for_transfer))
            kolp += 1
        else:
            kolp -= 1
            text = str(row.MoneyBalance)
            conn.send(text.encode())
            pass
    if kolp == 1:
        cursor.execute("SELECT * FROM users WHERE Number = '" + number_card + "'")
        for row in cursor.fetchall():
            money_now_1 = str(float(str(row.MoneyBalance)) + float(money_for_transfer))
        cursor.execute("UPDATE users SET MoneyBalance = " + money_now + " WHERE Number = '" + number_card_user + "'")
        cursor.execute("UPDATE users SET MoneyBalance = " + money_now_1 + " WHERE Number = '" + number_card + "'")
        cursor.execute("SELECT * FROM Histori")
        col = cursor.fetchall()
        now = datetime.now()
        dt_string = now.strftime("%d.%m.%Y")
        cursor.execute("INSERT INTO Histori (Code, Operation, NumberCardSend, NumberCard, MoneySend, DateSend) VALUES "
                       "(?, ?, ?, ?, ?, ?)", len(col)+1, "Перевод", number_card_user, number_card,
                       money_for_transfer,dt_string)
        coon.commit()
        conn.send(money_now.encode())
    else:
        pass


def Transfer_(conn):
    text = ""
    coon = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\User\Desktop\MyTable.accdb')
    cursor = coon.cursor()
    cursor.execute("SELECT * FROM Bankomati")
    for row in cursor.fetchall():
        text = str(row.Dolgota_Bankomata) + " " + str(row.Shirota_Bankomata) + " // " + text
    conn.send(text.encode())


if __name__ == '__main__':
    Main()
