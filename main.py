import telebot
from telebot import types
import logger
from config import TOKEN


bot = telebot.TeleBot(TOKEN)

tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
player = 1
step_counter = 0


def playfield(data_tab):
    a = '\n'
    for i in range(3):
        a += f'  {data_tab[0 + i * 3]} | {data_tab[1 + i * 3]} | {data_tab[2 + i * 3]}  \n - - - - - - - \n'
    return a


def win(data_steps):
    winner_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], \
                    [0, 3, 6], [1, 4, 7], [2, 5, 8], \
                    [0, 4, 8], [2, 4, 6]]
    for j in winner_lines:
        if data_steps[j[0]] == data_steps[j[1]] == data_steps[j[2]]:
            return data_steps[j[0]]
    return False


def is_valid_step(value, data_tab):
    return 1 <= value <= 9 and data_tab[value - 1] != "X" and data_tab[value - 1] != "O"


@bot.message_handler(commands=['start'])
def start(message):
    global tab
    bot.send_message(message.chat.id, 'Для начала игры нажмите /game')
    bot.send_message(message.chat.id, f'{playfield(tab)}')


@bot.message_handler(commands=['game'])
def number(message):
    global player
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('1')
    button2 = types.KeyboardButton('2')
    button3 = types.KeyboardButton('3')
    button4 = types.KeyboardButton('4')
    button5 = types.KeyboardButton('5')
    button6 = types.KeyboardButton('6')
    button7 = types.KeyboardButton('7')
    button8 = types.KeyboardButton('8')
    button9 = types.KeyboardButton('9')
    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)
    bot.send_message(message.chat.id, f"Игрок {player}, выберите номер клетки", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def select_position(message):
    global step_counter
    if message.text in ["1", "2", "3", "4", "5", "6", "7", "8", "9"] and step_counter < 8:
        set_symbol(message)
    elif step_counter >= 8:
        bot.send_message(message.chat.id, 'Игра закончена.\nНичья.')
        tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        step_counter = 0
        bot.send_message(message.chat.id, 'Нажми /start чтобы повторить')
    else:
        bot.send_message(message.chat.id, 'Не корректный ввод')
        number(message)


def set_symbol(message):
    global player, step_counter, tab
    pos = int(message.text)
    if player == 1 and step_counter < 9:
        step = 'X'
        if is_valid_step(pos, tab):
            tab[pos - 1] = step
            bot.send_message(message.chat.id, f'{playfield(tab)}')
            step_counter += 1
            player = 2
            if win(tab) == False:
                number(message)
            else:
                bot.send_message(message.chat.id, 'Игра закончена')
                winner = win(tab)
                if winner == 'X':
                    bot.send_message(message.chat.id, 'Игрок 1 победил.')
                    tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    step_counter = 0
                    bot.send_message(message.chat.id, 'Нажми /start чтобы повторить')
                elif winner == "O":
                    bot.send_message(message.chat.id, 'Игрок 2 победил.')
                    tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    step_counter = 0
                    bot.send_message(message.chat.id, 'Нажми /start чтобы повторить')
        else:
            bot.send_message(message.chat.id, 'Эта клетка занята')
            number(message)
            bot.send_message(message.chat.id, f'{playfield(tab)}')
    elif player == 2 and step_counter < 9:
        step = 'O'
        if is_valid_step(pos, tab):
            tab[pos - 1] = step
            bot.send_message(message.chat.id, f'{playfield(tab)}')
            step_counter += 1
            player = 1
            if win(tab) == False:
                number(message)
            else:
                bot.send_message(message.chat.id, 'Игра закончена')
                winner = win(tab)
                if winner == 'X':
                    bot.send_message(message.chat.id, 'Игрок 1 победил.')
                    tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    step_counter = 0
                    bot.send_message(message.chat.id, 'Нажми /start чтобы повторить')
                elif winner == "O":
                    bot.send_message(message.chat.id, 'Игрок 2 победил.')
                    tab = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    step_counter = 0
                    bot.send_message(message.chat.id, 'Нажми /start чтобы повторить')
        else:
            bot.send_message(message.chat.id, 'Эта клетка занята')
            number(message)
            bot.send_message(message.chat.id, f'{playfield(tab)}')


bot.infinity_polling()