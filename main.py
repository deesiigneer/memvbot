# Test bot of @memvbot - @without_name_bot in telegram


import logging

import config
from database import database
import sys
import time
from config import BOT_TOKEN, BOT_OWNER, CHANNEL_ID

import aiogram.dispatcher
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


# Configure logging
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
count = 1
sql = database.sql


class Answer_bot(StatesGroup):
    reply_text = State()
    reply_id = State()


# defines
def advertising():
    global count
    print(f'1 {count}')
    if count == 5:
        print(f'2 {count}')
        count = 0
        caption = sql.one('SELECT text, url, count, id FROM advertising ORDER BY RANDOM() LIMIT 1')
        sql.commit(f'UPDATE advertising SET count="{caption[2] - 1}" WHERE id="{caption[3]}"')
        caption = f'[{caption[0]}]({caption[1]})'
    else:
        print(f'3 {count}')
        caption = None
    return caption


def answer_404(user_id):
    answer = sql.one('SELECT text, url, count, id FROM advertising ORDER BY RANDOM() LIMIT 1')
    sql.commit(f'UPDATE users SET used="'
               f'{int(sql.one(f"SELECT used FROM users WHERE id == {user_id}")[0]) + 1}'
               f'" WHERE id="{user_id}"')
    sql.commit(f'UPDATE advertising SET count="{int(answer[2]) - 1}" WHERE id="{answer[3]}"')
    answer = f'[{answer[0]}]({answer[1]})'
    return answer


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    try:
        if message.from_user.language_code == 'ru':
            await bot.send_message(message.chat.id,
                                   f'Привет {message.from_user.full_name}, я meme voice bot! Я могу отправлять мемные'
                                   f'голосовые в групповые чаты или даже в личные сообщения!'
                                   f'\nКак? Узнай через /help'
                                   f'\n'
                                   f'\n[Новости о боте можно найти тут](https://t.me/joinchat/AAAAAEsekoTUW0WjerW8wA)',
                                   parse_mode='Markdown')
        else:
            await bot.send_message(message.chat.id, f'Hello {message.from_user.full_name}, i\`m Meme Voice bot!'
                                                    f'I can send voice with memes in group, channel or private message.'
                                                    f'\nHow? Use /help'
                                                    f'\n'
                                                    f'\n[News about bot you can find here]('
                                                    f'https://t.me/joinchat/AAAAAEsekoTUW0WjerW8wA)',
                                   parse_mode='Markdown')
        if sql.one("SELECT * FROM users WHERE id LIKE '{}';".format(message.from_user.id)) is None:
            sql.commit(
                "INSERT INTO users VALUES('{}','{}','{}','{}','{}','{}','{}','','','','','','','','','','','','',"
                "'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',"
                "'','','','','','','')".format(message.from_user.id,
                                               message.from_user.first_name,
                                               time.strftime("%F %T", time.localtime()),
                                               0, None, '', 'default'))
    except Exception as error:
        tb = sys.exc_info()[2]
        print(error,
              '\nat line {}'.format(tb.tb_lineno))


@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    try:
        file_id: str = "CgACAgIAAxkBAAIFgGCkDZuiIAYd9OaUb8spBBGZ2XYbAAJ_CgACOvvwS2TKVs16MCByHwQ"
        if message.from_user.language_code == 'ru':
            await bot.send_message(message.chat.id,
                                   'Как пользоваться ботом?'
                                   '\n'
                                   '\nНачните писать @memvbot в любом чате, и у вас появится список с мемами. '
                                   '\nПример:'
                                   '\n@memvbot привет'
                                   '\n'
                                   '\n_Почему в появившемся списке нет мемов, которые есть на канале!?_'
                                   '\nВ телеграма есть ограничение на вывод строк в inline режиме, поэтому их '
                                   'там всего 50. По этому было решено добавить теги (текст), по которым можно будет '
                                   'найти мем. Не знаю, как можно было ещё проще сделать, но если есть идеи или '
                                   'предложение, [пишите сюда.](https://t.me/deesiigneer)', parse_mode='Markdown')
            await bot.send_animation(message.chat.id, animation=file_id, caption='Наглядный пример')
        else:
            await bot.send_message(message.chat.id,
                                   "How to use the bot? (How to use) "
                                   "\n"
                                   "\nStart writing @memvbot in any chat and you will have a list with memes. "
                                   "\nExample:"
                                   "\n@memvbot hello"
                                   "\n"
                                   "\n_Why are there no memes in the list that are on the channel !? _"
                                   "\nThe telegram has a restriction on the output of lines in inline mode, so their"
                                   "there are only 50. Therefore, it was decided to add tags (text), by which it will "
                                   "be possible find the meme. I don't know how it could have been made even easier,"
                                   " but if there are ideas or suggestion, [write here.](https://t.me/deesiigneer)",
                                   parse_mode='Markdown')
            await bot.send_animation(message.chat.id, animation=file_id, caption='Illustrative example')
    except Exception as error:
        tb = sys.exc_info()[2]
        print(error,
              '\nat line {}'.format(tb.tb_lineno))


@dp.message_handler(commands=['price'])
async def command_price(message: types.Message):
    try:
        if message.from_user.language_code == 'ru':
            await bot.send_message(message.chat.id,
                                   f'Привет _{message.from_user.full_name}_, хочешь купить рекламу?'
                                   f'\nПиши создателю - @deesiigneer '
                                   f'\n'
                                   f'\n🎙Реклама в войсах от *100* показов - *{config.IN_VOICES}₽*'
                                   f'\n_Дополнительные_ *100* _просмотров - _*{config.ADDITIONAL}₽*'
                                   f'\n_Разовое приобретение_ *1000* _просмотров - _*55₽*'
                                   f'\n'
                                   f'\n👥Реклама в [группе](https://t.me/joinchat/Sx6ShNRbRaN6tbzA) - 500₽'
                                   f'\n_публикуется на_ *24ч* _с момента публикации_'
                                   f'\n'
                                   f'\n📑*УСЛОВИЯ РАЗМЕЩЕНИЯ:*'
                                   f'\n1️⃣ - Реклама в *войсах* принимается в ввиде *"текст - ссылка"*'
                                   f' пример на картинке ниже '
                                   f'\n2️⃣ - *Не более* _1024_ символов в тексте для рекламы в войсах'
                                   f'\n3️⃣ - Статистика от рекламы в войсах предоставляется по истечению показов '
                                   f'или в режиме онлайн по запросу (но не чаще, чем один раз в сутки).'
                                   f'/ Статистика публикации в группе предоставляется по запросу '
                                   f'*НЕ РАНЕЕ 7 ДНЕЙ* с момента публикации',
                                   parse_mode='Markdown', disable_web_page_preview=True)
        else:
            await bot.send_message(message.chat.id, f'Hi')
    except Exception as error:
        tb = sys.exc_info()[2]
        print(error,
              '\nat line {}'.format(tb.tb_lineno))


# админпанелька
@dp.message_handler(commands=['admintool'])
async def command_admintool(message: types.Message):
    try:
        if message.from_user.id == BOT_OWNER:
            adminkeyboard = types.InlineKeyboardMarkup(row_width=2)
            statistics = types.InlineKeyboardButton(text="Статистика", callback_data="statistics")
            sql_database = types.InlineKeyboardButton(text="База данных", callback_data="sql_database")
            adminkeyboard.add(statistics, sql_database)
            await bot.send_message(BOT_OWNER, f'Выбери что желаешь, {message.from_user.full_name}',
                                   reply_markup=adminkeyboard)
    except Exception as error:
        tb = sys.exc_info()[2]
        print(error,
              '\nat line {}'.format(tb.tb_lineno))


@dp.inline_handler()
async def chosen_handler(query: types.InlineQuery):
    try:
        global count
        print(query)
        if sql.one("SELECT * FROM memevoices WHERE tag LIKE '%{}%'".format(query.query)) is None:
            not_found = types.InlineQueryResultArticle(id='404',
                                                       title="404",
                                                       description="Такого войса нет...",
                                                       thumb_url=f"https://cdn.frankerfacez.com/emoticon/454732/2",
                                                       thumb_width=120,
                                                       thumb_height=120,
                                                       input_message_content=types.InputTextMessageContent(
                                                           message_text=answer_404(query.from_user.id),
                                                           parse_mode='Markdown',
                                                           disable_web_page_preview=True)
                                                       )
            await bot.answer_inline_query(query.id, [not_found], cache_time=0)
        else:
            sql_ = list(sql.many("SELECT * FROM memevoices WHERE tag LIKE '%{}%'".format(query.query), 50))
            cap = advertising()
            results = [types.InlineQueryResultCachedVoice(id=item[0], voice_file_id=item[1], title=item[2],
                                                          caption=cap, parse_mode='Markdown')
                       for item in sql_
                       ]
            await query.answer(results, cache_time=0, is_personal=True)
            count = count + 1
    except Exception as error:
        tb = sys.exc_info()[2]
        print(error,
              '\nat line {}'.format(tb.tb_lineno))


@dp.chosen_inline_handler()
async def chosen(result: types.ChosenInlineResult):
    print(f'result {result}')


@dp.message_handler(content_types=types.ContentType.VOICE)
async def add_audio(message: types.Message):
    try:
        if message.from_user.id == BOT_OWNER:
            if message.voice.file_id != sql.one(
                    f"SELECT audio_file_id FROM memevoices WHERE audio_file_id = '{message.voice.file_id}'"):
                if message.caption is not None:
                    sql.commit(
                        f"INSERT INTO memevoices VALUES(Null, '{message.voice.file_id}', '{message.caption}', '0')")
                    await bot.send_voice(chat_id=CHANNEL_ID, voice=message.voice.file_id,
                                         caption=f"<code>{message.caption}</code>", parse_mode='HTML')
                    await message.reply(text="Успешно добавлен!")
                else:
                    await message.reply(text="Войс нужно отправлять с названием!\nПопробуй ещё раз.")
            else:
                await message.reply(text="Этот войс уже есть в БД!")
    except Exception as error:
        tb = sys.exc_info()[2]
        print(error, '\nat line {}'.format(tb.tb_lineno))


@dp.message_handler(content_types=types.ContentType.ANY)
async def big_eye(message: types.Message):
    try:
        for m in message:
            print(str(m))
        if message.from_user.id == BOT_OWNER:
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            answerbybot = types.InlineKeyboardButton(text="Ответить через бота", callback_data="answerbybot")
            keyboard.add(answerbybot)
            primary = str(f'Details:'
                          f'\n └ Message ID: {message.message_id}'
                          f'\n\tFrom:'
                          f'\n ├ <a href="tg://user?id={message.from_user.id}">{message.from_user.id}</a>'
                          f'\n ├ is bot: {message.from_user.is_bot}'
                          f'\n ├ Fullname: {message.from_user.first_name}'
                          f'\n ├ Lastname: {message.from_user.last_name}'
                          f'\n ├ Username: {message.from_user.username}'
                          f'\n └ Language code: {message.from_user.language_code}'
                          f'\n\tChat:'
                          f'\n ├ <a href="tg://user?id={message.chat.id}">{message.chat.id}</a>'
                          f'\n ├ type: {message.chat.type}'
                          f'\n ├ title: {message.chat.title}'
                          f'\n ├ username: {message.chat.username}'
                          f'\n ├ First name: {message.chat.first_name}'
                          f'\n ├ Last name: {message.chat.last_name}'
                          f'\n └ Date: {message.date}'
                          )
            if message.is_forward():
                if message.forward_from_chat is None:
                    if message.forward_from is None:
                        primary = primary + str(f'\n\tForward from:'
                                                f'\n ├ ID: <code>unknown</code></a>'
                                                f'\n ├ First name: {message.forward_sender_name}'
                                                f'\n └ Forward date: {message.forward_date}')
                    primary = primary + str(f'\n\tForward from:'
                                            f'\n ├ ID: <a href="tg://user?id={message.forward_from.id}">'
                                            f'{message.forward_from.id}</a>'
                                            f'\n ├ First name: {message.forward_from.first_name}'
                                            f'\n ├ Is bot: {message.forward_from.is_bot}'
                                            f'\n ├ Last name: {message.forward_from.last_name}'
                                            f'\n ├ Username: {message.forward_from.username}'
                                            f'\n ├ Language code: {message.forward_from.language_code}'
                                            f'\n └ Forward date: {message.forward_date}')
                elif message.forward_from_chat is not None:
                    primary = primary + str(f'\n\tForward from chat:'
                                            f'\n ├ ID: <code>{message.forward_from_chat.id}</code>'
                                            f'\n ├ Title: {message.forward_from_chat.title}'
                                            f'\n ├ Username: {message.forward_from_chat.username}'
                                            f'\n ├ Type: {message.forward_from_chat.type}'
                                            f'\n ├ Forward from message id: {message.forward_from_message_id}'
                                            f'\n └ Forward date: {message.forward_date}'
                                            )
                # if message.entities is not None: # TODO: сделать проверку на ссылки
                #     print(f'message.entities: {message.entities}')
                #     global entitie
                #     for entities in message.entities:
                #         entitie = entities
                #         print(f'Entit: {entitie}')
                #     primary = primary + str(f'\nEntities'
                #                             f'\n ├ Type: {entitie.type}'
                #                             f'\n ├ Offset: {entitie.offset}'
                #                             f'\n ├ Length: {entitie.length}'
                #                             )
                # if entitie.type == 'text_link':
                #     primary = primary + str(f'\n └ Url: {entitie.url}')
                # elif entitie.type == 'text_mention':
                #     primary = primary + str(f'\nEntities'
                #                             f'\n └ User: {entitie.user}')
            if message.caption is not None:
                primary = primary + str(f'\n └ Caption: {message.caption}')
            if message.text is not None:
                primary = primary + str(f'\n └ Text: {message.text}')
                await bot.send_message(BOT_OWNER, primary, parse_mode='HTML', reply_markup=keyboard)
            if message.content_type == 'audio':
                await bot.send_audio(BOT_OWNER, message.audio.file_id, caption=primary, parse_mode='HTML',
                                     reply_markup=keyboard)
            if message.content_type == 'document':
                await bot.send_document(BOT_OWNER, message.document.file_id, caption=primary, parse_mode='HTML',
                                        reply_markup=keyboard)
            if message.content_type == 'photo':
                await bot.send_photo(BOT_OWNER, message.photo[-1].file_id, caption=primary, parse_mode='HTML',
                                     reply_markup=keyboard)
            if message.content_type == 'sticker':
                await bot.send_message(BOT_OWNER, primary, parse_mode='HTML')
                await bot.send_sticker(BOT_OWNER, message.sticker.file_id, reply_markup=keyboard,
                                       reply_to_message_id=message.message_id + 1)
            if message.content_type == 'video':
                await bot.send_video(BOT_OWNER, message.video.file_id, parse_mode='HTML', caption=primary,
                                     reply_markup=keyboard)
            if message.content_type == 'animation':
                print(f'animation type is = {type(message.animation.file_id)}')
                await bot.send_animation(BOT_OWNER, message.animation.file_id, caption=primary, parse_mode='HTML',
                                         reply_markup=keyboard)
            if message.content_type == 'voice':
                if message.from_user.id != BOT_OWNER:
                    await bot.send_voice(BOT_OWNER, message.voice.file_id, caption=primary, parse_mode='HTML',
                                         reply_markup=keyboard)
            if message.content_type == 'video_note':
                await bot.send_message(BOT_OWNER, primary, parse_mode='HTML')
                await bot.send_video_note(BOT_OWNER, message.video_note.file_id, reply_markup=keyboard,
                                          reply_to_message_id=message.message_id + 1)
            # elif types.message.ContentType.GAME:
            #     await bot.send_game()
            # elif types.message.ContentType.NEW_CHAT_MEMBERS:
            #     await bot.send_audio(BOT_OWNER, message.audio)
            # elif types.message.ContentType.LEFT_CHAT_MEMBER:
            #     await bot.send_audio(BOT_OWNER, message.audio)
            # elif types.message.ContentType.INVOICE:
            #     await bot.send_audio(BOT_OWNER, message.audio)
            # elif types.message.ContentType.SUCCESSFUL_PAYMENT:
            #     await bot.send_audio(BOT_OWNER, message.audio)
            # elif types.message.ContentType.UNKNOWN:
            #     await bot.send_audio(BOT_OWNER, message.audio)
    except Exception as error:
        tb = sys.exc_info()[2]
        print(error, '\nat line {}'.format(tb.tb_lineno))


@dp.callback_query_handler(text="answerbybot")
async def detailed(call: types.CallbackQuery, state: aiogram.dispatcher.FSMContext):
    reply_user_id = int()
    for entity in call.message.entities:
        reply_user_id = entity.user.id
    await Answer_bot.reply_text.set()
    await state.update_data(reply_id=int(reply_user_id))
    await bot.send_message(call.message.chat.id, 'Жду сообщения для отправки...')


@dp.message_handler(state=Answer_bot.reply_text)
async def answer_by_bot(message: types.Message, state: aiogram.dispatcher.FSMContext):
    async with state.proxy() as data:
        data['reply_text'] = message.text
    await bot.send_message(chat_id=data['reply_id'], text=data['reply_text'])
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
