import telebot
from random import randint

bot = telebot.TeleBot("TOKEN", parse_mode=None)

@bot.message_handler(commands=['help'])
def show_help(message):
	bot.reply_to(message, 'Список доступных команд:\n/help - Список доступных команд\n/hello - Приветствие\n/calculator - Калькулятор (+,-,*,/,**)\n/game - Игра "Угадай число"')

@bot.message_handler(commands=['hello'])
def send_welcome(message):
	bot.reply_to(message, f'Привет, {message.from_user.first_name}!')

@bot.message_handler(commands=['calculator'])
def calculate_expression(message):
	expression = message.text[12:]
	if len(expression) == 0:
		bot.reply_to(message, 'Чтобы использовать калькулятор, введите команду и через пробел выражение: /calculator 1+2*3/4')
	else:
		result = eval(expression)
		bot.reply_to(message, f'{expression} = {result}')

in_game = False
the_number = 0

@bot.message_handler(commands=['game'])
def lets_play(message):
	global in_game
	global the_number
	in_game = True
	the_number = randint(1,1000)
	print(f'Загаданное число: {the_number}')
	bot.send_message(message.chat.id, 'Я загадал число от 1 до 1000\nПопробуйте его угадать ;)')
	

@bot.message_handler(content_types=['text'])
def text_reply(message):
	global in_game
	global the_number
	if in_game and message.text.isdigit():
		if int(message.text) == the_number:
			bot.send_message(message.chat.id, f'Ура! Вы угадали! Я загадал число: {the_number}\nИгра окончена!')
			in_game = False
		elif int(message.text) > the_number:
			bot.send_message(message.chat.id, f'Загаданное число меньше, чем {message.text} :P')
		elif int(message.text) < the_number:
			bot.send_message(message.chat.id, f'Загаданное число больше, чем {message.text} :P')
	else:
		bot.reply_to(message, 'Хм, что-то я вас не понял...')

bot.infinity_polling()