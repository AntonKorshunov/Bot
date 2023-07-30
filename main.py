from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from background import keep_alive
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Импортируем MemoryStorage
import asyncio
import datetime

storage = MemoryStorage()
bot = Bot('6603790479:AAFoPnf9t-0XJo1H6rSLc2hpyLR36vhnwFg')
dp = Dispatcher(bot)  # Передаем storage в Dispatcher
last_ask_and_offer_time = None


# Класс для определения состояния пользователя:

# Функция для отправки многовариантного вопроса с кнопками
async def ask_questions(user_id):
  # Создаем InlineKeyboardMarkup с кнопками для ответов на вопросы
  keyboard = InlineKeyboardMarkup()
  keyboard.row(
    InlineKeyboardButton(text='1. Сколько методов продвижения всего?',
                         callback_data='answer_1'))
  keyboard.row(
    InlineKeyboardButton(text='2. Какие гарантии что мне это поможет?',
                         callback_data='answer_2'))
  keyboard.row(
    InlineKeyboardButton(text='3. В каком формате гайд?',
                         callback_data='answer_3'))
  keyboard.row(
    InlineKeyboardButton(
      text='4. Есть ли обратная связь? Куда я могу задать вопросы?',
      callback_data='answer_4'))
  keyboard.row(
    InlineKeyboardButton(text='5. Почему цена такая низкая?',
                         callback_data='answer_5'))

  await bot.send_message(user_id,
                         '''
Малышка, ты ещё не купила гайд?🤔

Если нет, то можешь задать мне вопросики⬇️
''',
                         reply_markup=keyboard)


async def send_ask_and_offer_message(user_id):
  global last_ask_and_offer_time
  current_time = datetime.datetime.now()
  if last_ask_and_offer_time is None or (
      current_time - last_ask_and_offer_time).seconds >= 20:
    last_ask_and_offer_time = current_time
    await asyncio.sleep(20)
    await bot.send_message(user_id, "Ну что?)")

    # Предлагаем пользователю выбрать, есть ли у него еще вопросы или он готов к оплате
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
      InlineKeyboardButton(text='Да, есть еще вопросик',
                           callback_data='more_questions'))
    keyboard.row(
      InlineKeyboardButton(text='Готова купить',
                           url="https://payform.ru/kk2wQa4/"))
    await bot.send_message(user_id,
                           "Еще есть вопросы или переходим к оплате?",
                           reply_markup=keyboard)


@dp.callback_query_handler(text_contains='answer_')
# Обработчик нажатия кнопок с вопросами
async def process_answer(callback_query: types.CallbackQuery):
  answer_number = callback_query.data.replace('answer_', '')
  if answer_number == '1':
    await bot.send_message(
      callback_query.from_user.id, '''
Всего 18 методов мы рассмотрим
Будут как бесплатные, так и платные на любой бюджет от 100₽''')
  elif answer_number == '2':
    await bot.send_message(
      callback_query.from_user.id, '''
Все методы проверены на мне и на моих ученицах. Все работает. 
Главное попробовать их все, чтобы понять какой подходит именно тебе
''')
  elif answer_number == '3':
    await bot.send_message(
      callback_query.from_user.id, '''
Сам гайд в формате PDF. Оформлен в едином стиле дизайнером 
После оплаты тебе на почту придет ссылка на гайд и инструкции
''')
  elif answer_number == '4':
    await bot.send_message(
      callback_query.from_user.id, '''
Конечно. Обратная связь есть. В инструкциях к гайду будет прописано куда можно задать вопросы
''')
  elif answer_number == '5':
    await bot.send_message(
      callback_query.from_user.id, '''
Цена лояльная чтобы гайд мог позволить себе любой начинающий мастер
''')
  await send_ask_and_offer_message(callback_query.from_user.id)
  await callback_query.answer(
  )  # Ответим на запрос, чтобы убрать состояние "pending"


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
  # Устанавливаем состояние "PURCHASED" для начала диалога

  file1 = open('./1.jpg', 'rb')
  # Отправка первой фотографии и кнопки "Забирай подарок"
  await bot.send_photo(message.chat.id,
                       photo=file1,
                       caption='''Привет)
Меня зовут Ирина Кузьмина, но об этом позже

Я собрала для тебя схему, по которой сама зарабатываю 200к+ на ресницах и теперь передам тебе''',
                       parse_mode=types.ParseMode.HTML,
                       reply_markup=InlineKeyboardMarkup().add(
                         InlineKeyboardButton(
                           text='Забирай подарок',
                           url="https://telegra.ph/200k-na-uslugah-07-12")))

  await asyncio.sleep(60)  # Ожидаем 1 секунду

  file2 = open('./2.jpg', 'rb')
  # Отправка второй фотографии и кнопки "Читать в статье"
  await bot.send_photo(
    message.chat.id,
    photo=file2,
    caption='''Что мы выяснили?
Наставники берут много деняк за банальные методы продвижения

Что я предлагаю?
Гайд по привлечению клиентов

Как его получить?
Читай в статье⬇️''',
    parse_mode=types.ParseMode.HTML,
    reply_markup=InlineKeyboardMarkup().add(
      InlineKeyboardButton(
        text='Читать в статье',
        url="https://telegra.ph/Gajd-po-privlecheniyu-klientov-07-12")))

  await asyncio.sleep(60)  # Ожидаем 1 секунду

  file3 = open('./3.jpg', 'rb')
  # Отправка третьей фотографии и кнопки "Бонусная статья"
  await bot.send_photo(message.chat.id,
                       photo=file3,
                       caption='''Бонусная статья💘
Как сделать клиента постоянным. 
Как поднять чек. Как упаковать блог''',
                       parse_mode=types.ParseMode.HTML,
                       reply_markup=InlineKeyboardMarkup().add(
                         InlineKeyboardButton(
                           text='Бонусная статья',
                           url="https://telegra.ph/Bonusnaya-statya-07-12")))

  await asyncio.sleep(60)  # Ожидаем 1 секунду

  file4 = open('./4.jpg', 'rb')
  # Отправка четвертой фотографии и кнопок "Купить" и "Узнать содержание"
  await bot.send_photo(message.chat.id,
                       photo=file4,
                       caption='''Поздравляю, ты прошла всего бота🥳
И теперь знаешь о существовании идеального практического гайда по привлечению клиентов

Стоимость гайда 1990₽''',
                       parse_mode=types.ParseMode.HTML,
                       reply_markup=InlineKeyboardMarkup().row(
                         InlineKeyboardButton(
                           text='Купить', url="https://payform.ru/kk2wQa4/"),
                         InlineKeyboardButton(text='Узнать содержание',
                                              callback_data='show_content')))

  # Устанавливаем таймер на 10 минут
  await asyncio.sleep(60)  # 600 секунд = 10 минут
  await ask_questions(
    message.chat.id
  )  # Ask the questions if the user hasn't purchased the guide


# Обработчик нажатия кнопок "Да, есть еще вопросик" или "Готова купить"
@dp.callback_query_handler(text_contains='more_questions')
@dp.callback_query_handler(text_contains='ready_to_buy')
async def process_questions_or_payment(callback_query: types.CallbackQuery):
  if 'more_questions' in callback_query.data:
    # Пользователь выбрал "Да, есть еще вопросик", задаем вопросы заново
    await ask_questions(callback_query.from_user.id)
  elif 'ready_to_buy' in callback_query.data:
    # Пользователь выбрал "Готова купить", кнопка типа URL уже обработана в предыдущем этапе
    pass  # В данном случае не требуется никакой дополнительной обработки, так как переход по ссылке обрабатывается Telegram клиентом


# Обработчик нажатия кнопки "Узнать содержание"
@dp.callback_query_handler(text_contains='show_content')
async def show_content(callback_query: types.CallbackQuery):
  content_text = '''
Содержание гайда:
 ⁃ Упаковка профиля
 ⁃ Аватарка
 ⁃ Ник
 ⁃ Шапка профиля
 ⁃ Хайлатс/актуальное
 ⁃ Визуал
 ⁃ Прайс, ценообразование, поднятие цен
 ⁃ Что такое личный бренд
 ⁃ Якоря
 ⁃ Сторис. Как оформлять. Про что говорить
 ⁃ Прогрев к услуге в сторис. Примеры
 ⁃ Работа с моделями
 ⁃ Работа с клиентской базой. Возвращаемость. 
 ⁃ Сервис
 ⁃ Рассылки по клиентской базе
 ⁃ Холодные рассылки которые работают. 
 ⁃ Реферальная система 
 ⁃ Мастера смежных ниш. Лучший способ сотрудничества 
 ⁃ Блогеры. Реклама, ТЗ
 ⁃ Хэштеги и геометки
 ⁃ Вк и вк таргет. Объявление, которое приносит клиентов. 
 ⁃ Реклама в городских сообществах
 ⁃ Авито, юла и профи. Как оформить объявление, чтобы оно продавало. 
 ⁃ DIKIDI. Приложение для поиска клиентов. Бесплатная и платная реклама. 
 ⁃ Реклама в чатах жк, университетов, школ и тд. Идеальная связка которая приносит клиентов
 ⁃ Наружная реклама. Примеры, виды
 ⁃ Конкурсные механики
 ⁃ Бьюти завтраки, организация оффлайн мероприятия
*за такую информацию это пыль, а не деньги
    '''

  # Создаем новый InlineKeyboardMarkup только с кнопкой "Купить"
  keyboard = InlineKeyboardMarkup()
  url_button4 = InlineKeyboardButton(text='Купить',
                                     url="https://payform.ru/kk2wQa4/")
  keyboard.row(url_button4)

  await bot.send_message(callback_query.from_user.id,
                         content_text,
                         reply_markup=keyboard)
  await callback_query.answer()  # Отметим, что обработали нажатие кнопки


keep_alive()
if __name__ == '__main__':
  executor.start_polling(dp)
