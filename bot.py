import telebot
from tic_tac_toe import game
import log_generate as lg
from config import TOKEN_API
from Keybords import *
from telebot import types
from time import sleep

bot = telebot.TeleBot(TOKEN_API)
# dp = Dispatcher(bot)
chat_id = ''
dic = {}
list_text = list()
list_callback = list()
message_id = 0
HELP_COMMAND = """
<b>/tic_tac_toe</b> - <i>Запускает игру Крестики-Нолики</i>
<b>/calc</b> - <i>Запускает решение примеров</i>
<b>/phonebook</b> - <i>Работа с телефонным справочником</i>
<b>/help</b> - <i>Выводит список команд с пояснениями</i>"""


async def on_start(_):
    print('Server start!')


# @bot.message_handler(commands=['test'])
# def start_command(message: types.Message):
#     bot.send_message(message.chat.id, 'проверка',
#                      reply_markup=keyboard_tic_tac)

@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    lg.write_data(f'Бот получил команду "{message.text}"')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHhyhj2Q3G8_LnmlZTrKD5asKpoCTTjQACGCMAAu0HgUrqmupuzpQQ6y0E',
                     reply_markup=keyboard_start)


@bot.message_handler(commands=['help'])
def help_command(message: types.Message):
    lg.write_data(f'Бот получил команду "{message.text}"')
    bot.send_message(message.chat.id, HELP_COMMAND, parse_mode='HTML')


@bot.message_handler(commands=['tic_tac_toe'])
def tic_tac_game(message: types.Message):  # Выбор функций бота
    global chat_id
    chat_id = message.chat.id
    lg.write_data(f'Бот получил команду "{message.text}"')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHi2Jj2ov3gyGrRmMg64l3VXS6-3AKuwACUgADYIltDBp238_XJHBwLgQ')
    bot.send_message(message.chat.id, 'Давай играть! Чур у меня нолики! Хочешь ходить первым?')
    lg.write_data(f'Начинается игра "крестики-нолики"')
    global dic
    dic = {'1': '.', '2': '.', '3': '.', '4': '.', '5': '.', '6': '.', '7': '.', '8': '.', '9': '.'}
    lg.write_data(f'Словарь заполнен пробелами')
    bot.register_next_step_handler(message, start_game)


def start_game(message):  # Функция определения, кто будет ходить первым
    global list_text, list_callback
    list_text = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    list_callback = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    if message.text == 'да':
        lg.write_data(f'Пользователь принял решение ходить первым')
        bot.send_message(message.chat.id, 'Выбери клетку!', reply_markup=keyboard_tic_tac)
        # bot.register_next_step_handler(message, user_check)
    elif message.text == 'нет':
        lg.write_data(f'Бот ходит первым')
        bot.send_message(message.chat.id, 'Хорошо, я начинаю!')
        global message_id
        message_id = message.message_id
        pc_check()
    else:
        lg.write_data(f'В функции определения хода зафиксирована неизвестная команда "{message.text}"')
        bot.send_message(message.chat.id, 'Я тебя не пониманию! Скажи еще раз!')
        bot.register_next_step_handler(message, start_game)


@bot.callback_query_handler(func=lambda callback: callback.data != '_')
def user_check(callback: types.CallbackQuery):
    global list_text, list_callback, dic, message_id
    message_id = callback.message.message_id
    key = callback.data
    list_text[int(key)-1] = '❌'
    list_callback[int(key)-1] = '_'
    dic[key] = 'x'
    # lg.write_data(f'Пользователь выбрал клетку: {player_turn}')
    if game.check_winner(dic):
        bot.edit_message_text('Ты выиграл!!', callback.message.chat.id, message_id,
                              reply_markup=update_keyboard_tic_tac(list_text, list_callback))
        sleep(3)
        list_text = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        list_callback = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        bot.delete_message(chat_id, message_id)
    elif '.' not in dic.values():
        bot.edit_message_text('У нас ничья!', callback.message.chat.id, message_id,
                              reply_markup=update_keyboard_tic_tac(list_text, list_callback))
        sleep(3)
        list_text = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        list_callback = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        bot.delete_message(chat_id, message_id)
    else:
        bot.edit_message_text('Я хожу!', callback.message.chat.id, message_id,
                              reply_markup=update_keyboard_tic_tac(list_text, list_callback))
        pc_check()


def pc_check():  # Ход бота
    global list_text, list_callback, dic, message_id
    lg.write_data(f'Начался ход бота')
    bot_choice = game.pc_choice(dic)
    lg.write_data(f'Бот выбирает клетку {bot_choice}')
    list_text[int(bot_choice)-1] = '⚪️'
    list_callback[int(bot_choice)-1] = '_'
    if '0' not in dic.values():
        bot.send_message(chat_id, 'Твой ход!', reply_markup=update_keyboard_tic_tac(list_text, list_callback))
    dic[bot_choice] = '0'
    if game.check_winner(dic):
        lg.write_data(f'Бот победил в игре')
        bot.edit_message_text('Я победил!', chat_id, message_id,
                              reply_markup=update_keyboard_tic_tac(list_text, list_callback))
        sleep(3)
        list_text = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        list_callback = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        bot.delete_message(chat_id, message_id)
    elif '.' not in dic.values():
        lg.write_data(f'Игра завершилась ничьей')
        bot.edit_message_text('Ой у нас ничья!', chat_id, message_id,
                              reply_markup=update_keyboard_tic_tac(list_text, list_callback))
        sleep(3)
        list_text = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        list_callback = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        bot.delete_message(chat_id, message_id)
    else:
        bot.edit_message_text('Твой ход!', chat_id, message_id,
                              reply_markup=update_keyboard_tic_tac(list_text, list_callback))
        # message = bot.send_message(chat_id, 'Твой ход!')
        # bot.register_next_step_handler(message, user_check)


# def user_check(message):  # Ход пользователя
#     global dic
#     lg.write_data(f'Начался ход пользователя')
#     player_turn = message.text
#     if player_turn in ('1', '2', '3', '4', '5', '6', '7', '8', '9') and dic.get(player_turn) == '.':
#         dic[player_turn] = 'x'
#
#         lg.write_data(f'Пользователь выбрал клетку: {player_turn}')
#         if game.check_winner(dic):
#             lg.write_data(f'Пользователь победил в игре')
#             bot.send_message(message.chat.id, 'Ты выиграл!')
#             bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHijtj2ju25yD9IASXu2icS_RIgMtu1AAClygAAhcXgEq2a7UNPA1jui4E')
#         elif '.' not in dic.values():
#             lg.write_data(f'Игра завершилась ничьей')
#             bot.send_message(message.chat.id, 'Ой у нас ничья!')
#         else:
#             bot.send_message(message.chat.id, game.print_dic(dic))
#             pc_check()
#     else:
#         lg.write_data(f'На ходе пользователя зафиксирован не корректный ввод: {player_turn}')
#         bot.send_message(message.chat.id, 'Ты что-то не то ввел! Попробуй еще раз!')
#         bot.register_next_step_handler(message, user_check)




















# @bot.message_handler(commands=['tic_tac_toe'])
# def tic_tac_game(message: types.Message):  # Выбор функций бота
#     global chat_id
#     chat_id = message.chat.id
#     lg.write_data(f'Бот получил команду "{message.text}"')
#     bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHi2Jj2ov3gyGrRmMg64l3VXS6-3AKuwACUgADYIltDBp238_XJHBwLgQ')
#     bot.send_message(message.chat.id, 'Давай играть! Чур у меня нолики! Хочешь ходить первым?')
#     lg.write_data(f'Начинается игра "крестики-нолики"')
#     global dic
#     dic = {'1': '.', '2': '.', '3': '.', '4': '.', '5': '.', '6': '.', '7': '.', '8': '.', '9': '.'}
#     lg.write_data(f'Словарь заполнен пробелами')
#     bot.register_next_step_handler(message, start_game)
#     # elif mes.text.lower() == 'посчитаем':
#     #     bot.send_message(chat_id, 'Хорошо! Вводи пример!')
#     #     lg.write_data(f'Получаем пример для решения')
#     #     bot.register_next_step_handler(mes, count_example)
#     # else:
#     #     lg.write_data(f'Зафиксирована неизвестная команда')
#     #     bot.send_message(message.chat.id, 'Я тебя не понимаю! Воспользуйся командой "/help"!')
#
#
# def start_game(message):  # Функция определения, кто будет ходить первым
#     if message.text == 'да':
#         lg.write_data(f'Пользователь принял решение ходить первым')
#         bot.send_message(message.chat.id, 'Выбери клетку!')
#         bot.register_next_step_handler(message, user_check)
#     elif message.text == 'нет':
#         lg.write_data(f'Бот ходит первым')
#         bot.send_message(message.chat.id, 'Хорошо, я начинаю!')
#         pc_check()
#     else:
#         lg.write_data(f'В функции определения хода зафиксирована неизвестная команда "{message.text}"')
#         bot.send_message(message.chat.id, 'Я тебя не пониманию! Скажи еще раз!')
#         bot.register_next_step_handler(message, start_game)
#
#
# def user_check(message):  # Ход пользователя
#     global dic
#     lg.write_data(f'Начался ход пользователя')
#     player_turn = message.text
#     if player_turn in ('1', '2', '3', '4', '5', '6', '7', '8', '9') and dic.get(player_turn) == '.':
#         dic[player_turn] = 'x'
#         lg.write_data(f'Пользователь выбрал клетку: {player_turn}')
#         if game.check_winner(dic):
#             lg.write_data(f'Пользователь победил в игре')
#             bot.send_message(message.chat.id, 'Ты выиграл!')
#             bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHijtj2ju25yD9IASXu2icS_RIgMtu1AAClygAAhcXgEq2a7UNPA1jui4E')
#         elif '.' not in dic.values():
#             lg.write_data(f'Игра завершилась ничьей')
#             bot.send_message(message.chat.id, 'Ой у нас ничья!')
#         else:
#             bot.send_message(message.chat.id, game.print_dic(dic))
#             pc_check()
#     else:
#         lg.write_data(f'На ходе пользователя зафиксирован не корректный ввод: {player_turn}')
#         bot.send_message(message.chat.id, 'Ты что-то не то ввел! Попробуй еще раз!')
#         bot.register_next_step_handler(message, user_check)
#
#
# def pc_check():  # Ход бота
#     global dic
#     lg.write_data(f'Начался ход бота')
#     bot.send_message(chat_id, 'Мой ход:')
#     bot_choice = game.pc_choice(dic)
#     lg.write_data(f'Бот выбирает клетку {bot_choice}')
#     dic[bot_choice] = '0'
#     bot.send_message(chat_id, game.print_dic(dic))
#     if game.check_winner(dic):
#         lg.write_data(f'Бот победил в игре')
#         bot.send_message(chat_id, 'Я победил!')
#     elif '.' not in dic.values():
#         lg.write_data(f'Игра завершилась ничьей')
#         bot.send_message(chat_id, 'Ой у нас ничья!')
#     else:
#         message = bot.send_message(chat_id, 'Твой ход!')
#         bot.register_next_step_handler(message, user_check)


# def count_example(message):  # Функиця решения примера
#     example, example_list = mr.get_nums(message.text)
#     lg.write_data(f'Пользователь ввел пример: {example}')
#     result = mr.get_result(example_list)
#     lg.write_data(f'Получен ответ: {result}')
#     bot.send_message(chat_id, f'{example} = {result}')


def start_bot():
    print('Server start!')
    bot.polling(none_stop=True)
