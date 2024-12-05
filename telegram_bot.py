from flask import Flask
import threading

# Запускаем HTTP-сервер для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_server():
    app.run(host="0.0.0.0", port=5000)

import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Список вопросов с вариантами ответов
all_questions = [
    {"question": "Что бы вы предпочли?", "partner_question": "Что бы предпочел ваш партнер?", "options": ["Отдых на природе", "Тусовка в клубе", "Поход в кино"]},
    {"question": "Любите ли вы сладкое?", "partner_question": "Любит ли ваш партнер сладкое?", "options": ["Да", "Нет"]},
    {"question": "В какое время года вы познакомились?", "partner_question": "В какое время года познакомились вы с вашим партнером?", "options": ["Зима", "Весна", "Лето", "Осень"]},
    {"question": "Вы попали на необитаемый остров, что вы сделаете в первую очередь?", "partner_question": "Ваш партнер попал на необитаемый остров, что он сделает в первую очередь?", "options": ["Разжечь костер", "Добыть еду", "Потанцевать"]},
    {"question": "Какой фильм вы бы предпочли?", "partner_question": "Какой фильм предпочтет ваш партнер?", "options": ["Комедия", "Драма", "Фантастика", "Ужасы"]},
    {"question": "Ваш любимый напиток?", "partner_question": "Какой напиток предпочитает ваш партнер?", "options": ["Чай", "Кофе", "Сок", "Вода"]},
    {"question": "Что вас расслабляет больше всего?", "partner_question": "Что больше всего расслабляет вашего партнера?", "options": ["Музыка", "Книга", "Прогулка", "Сон"]},
    {"question": "Какую кухню вы предпочитаете?", "partner_question": "Какую кухню предпочитает ваш партнер?", "options": ["Итальянская", "Японская", "Русская", "Американская"]},
    {"question": "Ваш любимый вид спорта?", "partner_question": "Какой вид спорта нравится вашему партнеру?", "options": ["Футбол", "Баскетбол", "Теннис", "Плавание"]},
    {"question": "Где бы вы хотели провести отпуск?", "partner_question": "Где бы ваш партнер хотел провести отпуск?", "options": ["На море", "В горах", "В лесу", "В городе"]},
    {"question": "Какой жанр музыки вам нравится?", "partner_question": "Какой жанр музыки нравится вашему партнеру?", "options": ["Рок", "Поп", "Классика", "Джаз"]},
    {"question": "Какой ваш любимый цвет?", "partner_question": "Какой цвет предпочитает ваш партнер?", "options": ["Красный", "Синий", "Зеленый", "Желтый"]},
    {"question": "Какой стиль одежды вы предпочитаете?", "partner_question": "Какой стиль предпочитает ваш партнер?", "options": ["Классический", "Спортивный", "Повседневный", "Элегантный"]},
    {"question": "Какой ваш любимый сезон?", "partner_question": "Какой сезон любит ваш партнер?", "options": ["Зима", "Весна", "Лето", "Осень"]},
    {"question": "Какую суперспособность вы бы выбрали?", "partner_question": "Какую суперспособность выбрал бы ваш партнер?", "options": ["Летать", "Невидимость", "Чтение мыслей", "Сверхсила"]},
    {"question": "Что вы предпочитаете на завтрак?", "partner_question": "Что предпочитает на завтрак ваш партнер?", "options": ["Каша", "Омлет", "Сэндвич", "Фрукты"]},
    {"question": "Какую книгу вы бы прочитали?", "partner_question": "Какую книгу предпочтет ваш партнер?", "options": ["Роман", "Детектив", "Фэнтези", "Научную"]},
    {"question": "Какую профессию вы бы выбрали мечтой?", "partner_question": "Какую профессию выбрал бы мечтой ваш партнер?", "options": ["Писатель", "Актер", "Ученый", "Путешественник"]},
    {"question": "Какую погоду вы любите?", "partner_question": "Какую погоду любит ваш партнер?", "options": ["Солнечную", "Дождливую", "Снегопад", "Туман"]},
    {"question": "Какой транспорт вы предпочитаете?", "partner_question": "Какой транспорт предпочитает ваш партнер?", "options": ["Машина", "Самолет", "Поезд", "Велосипед"]},
    {"question": "Какую обувь вы выбираете для прогулок?", "partner_question": "Какую обувь выбирает ваш партнер для прогулок?", "options": ["Кроссовки", "Ботинки", "Сандалии", "Туфли"]},
    {"question": "Какое домашнее животное вам нравится больше?", "partner_question": "Какое животное нравится вашему партнеру?", "options": ["Кошка", "Собака", "Рыбки", "Птицы"]},
    {"question": "Какой напиток вы бы заказали на свидании?", "partner_question": "Что бы заказал ваш партнер?", "options": ["Кофе", "Коктейль", "Вино", "Чай"]},
    {"question": "Что вас вдохновляет больше всего?", "partner_question": "Что вдохновляет вашего партнера?", "options": ["Природа", "Музыка", "Люди", "Книги"]},
    {"question": "Какой праздник ваш любимый?", "partner_question": "Какой праздник любим у вашего партнера?", "options": ["Новый год", "День рождения", "8 марта", "23 февраля"]},
    {"question": "Какую активность вы предпочитаете на выходных?", "partner_question": "Какой активности предпочитает ваш партнер?", "options": ["Спорт", "Чтение", "Прогулки", "Кино"]},
    {"question": "Где вы бы хотели жить?", "partner_question": "Где бы хотел жить ваш партнер?", "options": ["В городе", "В деревне", "У моря", "В горах"]},
    {"question": "Ваш любимый вид цветов?", "partner_question": "Какие цветы нравятся вашему партнеру?", "options": ["Розы", "Тюльпаны", "Лилии", "Хризантемы"]},
    {"question": "Какой вид отдыха вам ближе?", "partner_question": "Какой вид отдыха предпочитает ваш партнер?", "options": ["Активный", "Пляжный", "Гастрономический", "Культурный"]},
    {"question": "Какое утро вы предпочитаете?", "partner_question": "Какое утро предпочитает ваш партнер?", "options": ["Раннее", "Позднее", "Солнечное", "Туманное"]},
    {"question": "Что вас мотивирует в жизни больше всего?", "partner_question": "Что больше всего мотивирует вашего партнера?", "options": ["Семья", "Карьера", "Путешествия", "Саморазвитие"]},
    {"question": "Какой жанр фильмов вы смотрите чаще всего?", "partner_question": "Какой жанр фильмов чаще всего смотрит ваш партнер?", "options": ["Фантастика", "Ужасы", "Исторические фильмы", "Документальные фильмы"]},
    {"question": "Какой вид спорта вы предпочли бы попробовать?", "partner_question": "Какой вид спорта хотел бы попробовать ваш партнер?", "options": ["Сёрфинг", "Скалолазание", "Гольф", "Бокс"]},
    {"question": "Какой фрукт вам нравится больше всего?", "partner_question": "Какой фрукт больше всего нравится вашему партнеру?", "options": ["Яблоки", "Бананы", "Апельсины", "Виноград"]},
    {"question": "Какое ваше любимое время суток?", "partner_question": "Какое время суток предпочитает ваш партнер?", "options": ["Утро", "День", "Вечер", "Ночь"]},
    {"question": "Какой тип погоды вам ближе?", "partner_question": "Какой тип погоды ближе вашему партнеру?", "options": ["Тёплый ветер", "Дождь с громом", "Солнечный день", "Морозная зима"]},
    {"question": "Что вы обычно делаете на выходных?", "partner_question": "Что ваш партнер обычно делает на выходных?", "options": ["Проводите время с друзьями", "Отдыхаете дома", "Занимаетесь спортом", "Путешествуете"]},
    {"question": "Какой напиток вы предпочли бы в жаркий день?", "partner_question": "Какой напиток предпочитает ваш партнер в жаркий день?", "options": ["Лимонад", "Минеральная вода", "Холодный чай", "Смузи"]},
    {"question": "Какой супергеройский фильм вам нравится больше всего?", "partner_question": "Какой супергеройский фильм нравится вашему партнеру?", "options": ["Marvel", "DC", "Не смотрю такие фильмы", "Люблю что-то другое"]},
    {"question": "Какую машину мечтаете водить?", "partner_question": "Какую машину мечтает водить ваш партнер?", "options": ["Электромобиль", "Классический спорткар", "Внедорожник", "Никакую, я не вожу"]},
    {"question": "Что вы предпочитаете слушать утром?", "partner_question": "Что ваш партнер предпочитает слушать утром?", "options": ["Радио", "Подкаст", "Музыку", "Тишину"]},
    {"question": "Какую карьеру вы бы выбрали в следующей жизни?", "partner_question": "Какую карьеру выбрал бы ваш партнер в следующей жизни?", "options": ["Музыкант", "Доктор", "Писатель", "Предприниматель"]},
    {"question": "Какая ваша любимая игра детства?", "partner_question": "Какая игра детства была любимой у вашего партнера?", "options": ["Прятки", "Лапта", "Игра на приставке", "Карточные игры"]},
    {"question": "Какую суперспособность вы бы использовали в экстренной ситуации?", "partner_question": "Какую суперспособность использовал бы ваш партнер в экстренной ситуации?", "options": ["Телепортация", "Лечение", "Контроль времени", "Умение говорить на всех языках"]},
    {"question": "Какой стиль путешествий вам ближе?", "partner_question": "Какой стиль путешествий ближе вашему партнеру?", "options": ["Роскошные курорты", "Бюджетные поездки", "Экстрим-туры", "Путешествия на машине"]},
    {"question": "Какая ваша любимая еда на завтрак?", "partner_question": "Какую еду на завтрак предпочитает ваш партнер?", "options": ["Бутерброды", "Омлет", "Круассаны", "Фрукты"]},
    {"question": "Какое морское существо вам кажется самым интересным?", "partner_question": "Какое морское существо кажется самым интересным вашему партнеру?", "options": ["Киты", "Дельфины", "Акулы", "Медузы"]},
    {"question": "Что вы чаще всего делаете на телефоне?", "partner_question": "Что ваш партнер чаще всего делает на телефоне?", "options": ["Читаю новости", "Играю в игры", "Смотрю видео", "Общаюсь"]},
    {"question": "Какой ваш любимый вид искусства?", "partner_question": "Какой вид искусства предпочитает ваш партнер?", "options": ["Живопись", "Музыка", "Театр", "Скульптура"]},
    {"question": "Если бы вы могли изучить новый язык, какой бы выбрали?", "partner_question": "Какой новый язык хотел бы изучить ваш партнер?", "options": ["Испанский", "Китайский", "Французский", "Итальянский"]}
]

# Функция для случайного выбора 10 вопросов из большого списка
def get_random_questions(used_questions):
    available_questions = [q for q in all_questions if q not in used_questions]
    if len(available_questions) < 10:
        used_questions = []  # Сбрасываем использованные вопросы
        available_questions = all_questions
    num_questions_to_select = min(len(available_questions), 10)
    selected_questions = random.sample(available_questions, num_questions_to_select)
    return selected_questions, used_questions + selected_questions

# Функция для начала игры

def start(update: Update, context: CallbackContext) -> None:
    if 'used_questions' not in context.user_data:
        context.user_data['used_questions'] = []
    if 'played_games' not in context.user_data:
        context.user_data['played_games'] = 0

    context.user_data['current_phase'] = 1  # 1 - первый партнер, 2 - второй партнер
    context.user_data['answers'] = {}
    context.user_data['partner_answers'] = {}
    context.user_data['answer_message_ids'] = []
    context.user_data['questions'], context.user_data['used_questions'] = get_random_questions(context.user_data['used_questions'])

    # Сообщение о правилах с экранированием символов для MarkdownV2
    rules_message = (
        "🎉 *Добро пожаловать в игру\\!* 🎉\\n\\n"
        "📜 *Правила\\:*\\n"
        "1️⃣ Первый партнер отвечает на 10 вопросов\\.\\n"
        "2️⃣ Затем второй партнер отвечает на те же вопросы, стараясь угадать ответы первого партнера\\.\\n"
        "3️⃣ В конце вы увидите процент совпадений ваших ответов и сможете посмотреть полный список ответов\\.\\n\\n"
        "👉 *Нажмите кнопку ниже, чтобы начать игру\\!*"
    )

    # Проверяем, есть ли сообщение (update.message), и отправляем правила
    if update.message:
        update.message.reply_text(rules_message, parse_mode="MarkdownV2")
        # Начинаем игру
        ask_question(update, context, 0)
    elif update.callback_query:
        update.callback_query.message.reply_text(rules_message, parse_mode="MarkdownV2")
        # Начинаем игру
        ask_question(update.callback_query, context, 0)




# Функция для задавания вопросов
def ask_question(update: Update, context: CallbackContext, question_index: int) -> None:
    questions = context.user_data['questions']
    if question_index < len(questions):
        question_data = questions[question_index]
        question_text = question_data["question"] if context.user_data['current_phase'] == 1 else question_data["partner_question"]
        keyboard = [[InlineKeyboardButton(option, callback_data=f"{question_index}_{option}")] for option in question_data["options"]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message:
            update.message.reply_text(question_text, reply_markup=reply_markup)
        elif update.callback_query:
            update.callback_query.message.reply_text(question_text, reply_markup=reply_markup)

        context.user_data['question_index'] = question_index
    else:
        if context.user_data['current_phase'] == 1:
            bot = context.bot
            chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id
            for message_id in context.user_data['answer_message_ids']:
                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except:
                    pass
            if update.message:
                update.message.reply_text("Спасибо за ответы! Теперь ваш партнер должен ответить на те же вопросы. Используйте команду /start_second_phase.")
            elif update.callback_query:
                update.callback_query.message.reply_text("Спасибо за ответы! Теперь ваш партнер должен ответить на те же вопросы. Используйте команду /start_second_phase.")
        else:
            calculate_results(update, context)

# Функция для обработки ответов
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Инициализация current_phase, если он отсутствует
    if 'current_phase' not in context.user_data:
        context.user_data['current_phase'] = 0  # Устанавливаем начальное значение

    callback_data = query.data

    if callback_data == "next_game":
        next_game(update, context)
        return
    elif callback_data == "view_answers":
        view_answers(update, context)
        return

    question_index, answer = callback_data.split('_')
    question_index = int(question_index)

    if context.user_data['current_phase'] == 1:
        context.user_data['answers'][question_index] = answer
        context.user_data['answer_message_ids'].append(query.message.message_id)
    else:
        context.user_data['partner_answers'][question_index] = answer

    query.edit_message_text(text=f"Вы выбрали: {answer}")
    ask_question(update, context, question_index + 1)


# Функция для начала второго этапа
def start_second_phase(update: Update, context: CallbackContext) -> None:
    context.user_data['current_phase'] = 2
    update.message.reply_text("Теперь ваш партнер отвечает на те же вопросы.")
    ask_question(update, context, 0)

# Функция для вычисления результатов
def calculate_results(update: Update, context: CallbackContext) -> None:
    matching_answers = sum(
        1 for i in range(len(context.user_data['questions']))
        if context.user_data['answers'].get(i) == context.user_data['partner_answers'].get(i)
    )
    percentage = (matching_answers / len(context.user_data['questions'])) * 100

    if percentage > 70:
        emoji = "😄"
    elif percentage < 30:
        emoji = "😢"
    else:
        emoji = "🙂"

    result_message = f"Ваш процент совпадений: {percentage:.1f}% {emoji}\n"
    result_message += (
        "Вы прекрасно знаете предпочтения друг друга!" if percentage > 70 else
        "Неплохо, но есть над чем работать." if percentage > 50 else
        "Вам стоит больше узнать друг друга."
    )

    keyboard = [
        [InlineKeyboardButton("Следующая игра", callback_data="next_game")],
        [InlineKeyboardButton("Посмотреть ответы", callback_data="view_answers")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(result_message, reply_markup=reply_markup)

# Функция для отображения ответов
def view_answers(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    questions = context.user_data['questions']
    answers = context.user_data['answers']
    partner_answers = context.user_data['partner_answers']

    response_text = "Ответы на вопросы:\n\n"
    for i, question in enumerate(questions):
        response_text += (
            f"Вопрос: {question['question']}\n"
            f"Ваш ответ: {answers.get(i, 'Нет ответа')}\n"
            f"Ответ партнера: {partner_answers.get(i, 'Нет ответа')}\n\n"
        )

    query.message.reply_text(response_text)

# Функция для начала новой игры
def next_game(update: Update, context: CallbackContext) -> None:
    start(update, context)

def main()
import logging
import time
import os
import signal
import threading
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ваш токен
TOKEN = "8133933513:AAFZgNBc3jqOJwaQWmUx37ByKO3uxpypf7o"

# Функция для команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я бот, готов работать!")

# Функция для обработки текстовых сообщений
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

# Функция для обработки ошибок
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f"Произошла ошибка: {context.error}")

# Функция для завершения работы бота через 20 минут
def restart_bot_after_delay():
    logger.info("Бот будет перезапущен через 20 минут...")
    time.sleep(20 * 60)  # Ожидание 20 минут
    logger.info("Перезапуск бота...")
    os.kill(os.getpid(), signal.SIGTERM)  # Завершение текущего процесса

# Основная функция запуска бота
def main():
    # Создаём экземпляр Updater
    updater = Updater(TOKEN)

    # Диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация команды /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Регистрация обработки текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Регистрация обработки ошибок
    dispatcher.add_error_handler(error)

    # Запускаем таймер на перезапуск
    threading.Thread(target=restart_bot_after_delay, daemon=True).start()

    # Запуск бота
    updater.start_polling()
    updater.idle()

# Запуск
if __name__ == '__main__':
    main()

