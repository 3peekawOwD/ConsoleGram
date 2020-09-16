from telethon import TelegramClient, events, sync
from telethon import functions
from telethon_secret_chat import SecretChatManager
from base64 import urlsafe_b64decode
from struct import unpack

import requests
import os
from colorama import Fore, Back, Style

banner = """
   mmm                              \"\"#             mmm                      
 m\"   \"  mmm   m mm    mmm    mmm     #     mmm   m\"   \"  m mm   mmm   mmmmm 
 #      #\" \"#  #\"  #  #   \"  #\" \"#    #    #\"  #  #   mm  #\"  \" \"   #  # # # 
 #      #   #  #   #   \"\"\"m  #   #    #    #\"\"\"\"  #    #  #     m\"\"\"#  # # # 
  "mmm" "#m#"  #   #  "mmm"  "#m#"    "mm  "#mm"   "mmm"  #     "mm"#  # # # 
"""

commands = """
===== КОМАНДЫ =====
checkNick - Проверка ника
exit - Выход
help - Список всех комманд
linkInfo - Информация о ссылке
profile - Мой профиль
screen - Фейковое уведомление о скриншоте
voice - Отправить ogg, как голосовое сообщение
===================
"""

print(Fore.WHITE + banner + Style.RESET_ALL)
print("===== ДОБРО ПОЖАЛОВАТЬ В CONSOLEGRAM =====")
print("Автор: 3peekawOwD (github.com/3peekawOwD)")
print("===== ВХОД =====")
api_id = input("Введите ваш api_id: ")
if len(api_id) != 7:
	print("[Ошибка] Неправильный api_id")
	quit()
api_hash = input("Введите ваш api_hash: ")

client = TelegramClient('session_name', api_id, api_hash)

async def replier(event):
	if event.decrypted_event.message and event.decrypted_event.message == "hello":
		await event.reply("hi")

manager = SecretChatManager(client, auto_accept=True)
manager.add_secret_event_handler(func=replier)

client.start()

print(commands)

while True:
	command = input("ConsoleGram:~ $ ")
	if command == "profile":
		info = client.get_me()
		print("===== МОЙ ПРОФИЛЬ =====")
		print("Имя: " + info.first_name)
		print("ID: " + str(info.id))
		print("Номер телефона: " + str(info.phone))
		print("=======================")
	elif command == "dialogs":
		print(Fore.WHITE + Back.BLACK + "===== ЧАТЫ =====")
		for dialog in client.iter_dialogs():
			print("Название чата: " + dialog.name)
			if dialog.message.message:
				print("Последнее сообщение: " + dialog.message.message)
			else:
				print("Последнее сообщение: ")
			print("-----")
		print("================" + Style.RESET_ALL)
	elif command == "voice":
		path = input("Введите путь до файла: ")
		to = input("Введите ник собеседника: ")
		client.send_file(to, open(path, "rb"), voice_note=True)
	elif command == "checkNick":
		nick = input("Введите ник: ")
		response = requests.get("https://t.me/" + nick)
		html = response.text
		if "tgme_page_extra" in html:
			print("Такой ник занят")
		else:
			print("Такой ник свободен")
	elif command == "screen":
		nickName = input("Введите ник собеседника: ")
		client(functions.messages.SendScreenshotNotificationRequest(
			peer=nickName,
			reply_to_msg_id=0
		))
	elif command == "linkInfo":
		link = input("Введите ссылку(Без AAAAA или /joinchat): ")
		link = link.split("/")[-1]
		d = urlsafe_b64decode(link + "==")
		user = client(functions.users.GetFullUserRequest(
			id=unpack(">iiq", d)[0]
		))
		print("Ссылка на инвайт: {}\nСоздатель: @{}\nID Чата: -100{}\nХэш: {}".format(
			link, user.user.username, unpack(">iiq", d)[1], unpack(">iiq", d)[2]
		))
	elif command == "exit":
		quit()
	elif command == "help":
		print(commands)
	elif command == "":
		pass
	else:
		print("{0}: Команда не найдена".format(command))
