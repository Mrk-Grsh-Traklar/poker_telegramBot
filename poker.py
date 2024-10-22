import telebot as tb
from telebot import types
import random

Token = 'token'  # Замените на ваш токен
bot = tb.TeleBot(Token)

print('Bot started')

# Определим карты и колоду
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Создание колоды
def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

# Перетасовка колоды
def shuffle_deck(deck):
    random.shuffle(deck)

# Игроки
class Player:
    def init(self, name):
        self.name = name
        self.hand = []
        self.chips = 100  # Начальное количество фишек

    def add_card(self, card):
        self.hand.append(card)

    def show_hand(self):
        return ', '.join([f"{rank} of {suit}" for rank, suit in self.hand])

# Главное меню
@bot.message_handler(commands=['main', 'start'])
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    profile = types.KeyboardButton('Profile')
    support = types.KeyboardButton('Support')
    play = types.KeyboardButton('Play Poker')
    markup.add(profile, support, play)
    bot.send_message(message.chat.id, f"Hello! {message.from_user.first_name}", reply_markup=markup)

# Меню игры
@bot.message_handler(regexp='Play Poker')
def game_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    play_bot = types.KeyboardButton('Play with Bot')
    online = types.KeyboardButton('Play Online')
    markup.add(play_bot, online)
    bot.send_message(message.chat.id, "Select game mode:", reply_markup=markup)

# Тех. поддержка
@bot.message_handler(regexp='Support')
def support(message):
    bot.send_message(message.chat.id, "If you encounter difficulties, contact technical support: @assmaser")

# Профиль
@bot.message_handler(regexp='Profile')
def profile(message):
    user_id = message.from_user.id
    # Для примера, можно хранить данные игрока в словаре
    player_data = {
        'name': message.from_user.first_name,
        'id': user_id,
        'chips': 100,  # Начальное количество фишек
        'games_played': 5,  # Пример количества сыгранных игр
        'games_won': 2  # Пример количества выигранных игр
    }
    
    profile_message = (
        f"Profile of {player_data['name']}\n"
        f"👤 User ID: {player_data['id']}\n"
        f"💰 Chips: {player_data['chips']}\n"
        f"🎮 Games Played: {player_data['games_played']}\n"
        f"🏆 Games Won: `{player_data['games_won']}`\n"
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_main = types.KeyboardButton('Back to Main Menu')
    new_game = types.KeyboardButton('Start New Game')
    markup.add(back_to_main, new_game)
    
    bot.send_message(message.chat.id, profile_message, reply_markup=markup, parse_mode='Markdown')

# Обработчик кнопки "Back to Main Menu"
@bot.message_handler(regexp='Back to Main Menu')
def back_to_main_menu(message):
    main_menu(message)

# Обработчик кнопки "Start New Game"
@bot.message_handler(regexp='Start New Game')
def start_new_game(message):
    game_menu(message)

# Логика игры в покер
@bot.message_handler(regexp='Play with Bot')
def play_with_bot(message):
    deck = create_deck()
    shuffle_deck(deck)

    player = Player(message.from_user.first_name)
    bot_player = Player("Bot")

    # Раздача карт
    for _ in range(2):
        player.add_card(deck.pop())
        bot_player.add_card(deck.pop())

    # Показываем руки игроков
    bot.send_message(message.chat.id, f"{player.name}'s hand: {player.show_hand()}")
    bot.send_message(message.chat.id, f"{bot_player.name}'s hand: {bot_player.show_hand()} (Bot hand is hidden)")

    # Здесь можно добавить дальнейшую логику игры: ставки, флоп, терн, ривер и т.д.

# Запуск бота
bot.infinity_polling()
