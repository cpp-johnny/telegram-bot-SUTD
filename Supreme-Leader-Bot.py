import tictactoe
from random import randint
from typing import Union, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# tokens should look something like this:
# 1234567:AAwrv19eH6nse59d8aELnc4
# put yours in TOKEN
TOKEN = ''

# function for the bot to reply "pay respect to sumpreme leader" when a user sends "/start" to it
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update.effective_chat.id is the id of the chat that the user has sent the message in
    # this is so that the bot knows where to send the message to
    await context.bot.send_message(chat_id=update.effective_chat.id, text="pay respect to the supreme leader!!")

# when user say payrespect, pic of kim will appear, as well as other shit just look at code bruh
async def payrespect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kju = open('kju.jpg','rb')
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=kju)
    kju.close()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="SOCIAL CREDIT +10000!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I love refrigerators")

# send location of changi prison
async def venue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_venue(chat_id=update.effective_chat.id, latitude="1.3572716", longitude="103.9627886", title="Changi Prison", address="982 Upper Changi Rd N, Singapore 507709")

# kim clapping
async def clap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clapping = open('kim-clapping.jpg','rb')
    
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=clapping)
    clapping.close()

# horse
async def horse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    horsey = open('kim-horse.jpg','rb')
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=horsey)
    horsey.close()

    
# still figuring how this works
"""
async def surprise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_audio(chat_id=update.effective_chat.id, audio="https://www.myinstants.com/en/instant/i-love-refrigerators-28756/?utm_source=copy&utm_medium=share")
"""

# ----------


def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu

game = tictactoe.TicTacToe()
chat_id = -1
message_id = -1

async def newgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game, chat_id, message_id
    game = tictactoe.TicTacToe()
    chat_id = update.effective_chat.id

    button_list = []

    for i in range(3):
        for j in range(3):
            button_list.append(InlineKeyboardButton(game.board[i][j], callback_data=str(i * 3 + j)))

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))

    await context.bot.send_message(chat_id=chat_id, text="☢️☢️ Accept a challenge from the Supreme Leader ☢️☢️ !!", reply_markup=reply_markup)

    message_id = update.effective_message.message_id + 1

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game, chat_id, message_id

    message = update.callback_query.message
    data = update.callback_query.data
    query_id = update.callback_query.id

    print(data)

    if message.chat.id == chat_id and message_id == message_id:
        available = game.getempty()
        if data in available:
            game.move("X", int(data))

            if game.checkwin():
                await context.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="You won! Good Job! Supreme Leader is proud of you!")

            elif game.checkwin() == False and len(game.getempty()) == 0:
                await context.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="tie, skill issue bruh, send to gulag")
            
            else:
                available = game.getempty()
                bot_move = randint(0, len(available) - 1)
                game.move("O", int(available[bot_move]))
                if game.checkwin():
                    await context.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Buddy skill issue you lost. Send to gulag")

                elif  game.checkwin() == False and len(game.getempty()) == 0:
                    await context.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="tie, skill issue bruh, send to gulag")

                else:
                    button_list = []
                    for i in range(3):
                        for j in range(3):
                            button_list.append(InlineKeyboardButton(game.board[i][j], callback_data=str(i * 3 + j)))
                        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
                        await context.bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text = "Please make your move", reply_markup=reply_markup)
            await context.bot.answer_callback_query(query_id)              

        else:
            print("buddy pick another spot")
            button_list = []
            for i in range(3):
                for j in range(3):
                    button_list.append(InlineKeyboardButton(game.board[i][j], callback_data=str(i * 3 + j)))
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols =3))
            await context.bot.edit_message_text(chat_id=message.chat.id, message_id=message_id, text="Please make your move", reply_markup=reply_markup)
            await context.bot.answer_callback_query(query_id, text="Please choose an empty space")
    else:
        if message.txt == "☢️☢️ Accept a challenge from the Supreme Leader ☢️☢️ !!" or message.txt == "Please make your move:":
            await context.bot.edit_message_text(chat_id=message.chat_id, message_id=message_id, text="no more game boohoohoo :(")


if __name__ == '__main__':
    # creates an entry point for the bot using your bot's token
    app = ApplicationBuilder().token(TOKEN).build()
    
    # this creates a CommandHandler object
    # the first parameter is the command aka what the user writes after / to activate the command
    # the second parameter is the function written earlier
    start_handler = CommandHandler('start', start)
    app.add_handler(start_handler)
    payrespect_handler = CommandHandler('payrespect', payrespect)
    app.add_handler(payrespect_handler)
    venue_handler = CommandHandler('venue', venue)
    app.add_handler(venue_handler)
    clap_handler = CommandHandler('clap', clap)
    app.add_handler(clap_handler)
    horse_handler = CommandHandler('horse', horse)
    app.add_handler(horse_handler)
    
    
    # bruh idk how to do this still figuring out 
    # surprise_handler = CommandHandler('surprise', surprise)
    # app.add_handler(surprise_handler)


    newgame_handler = CommandHandler('newgame', newgame)
    app.add_handler(newgame_handler)

    CallbackQueryHandler = CallbackQueryHandler(callback)
    app.add_handler(CallbackQueryHandler)

    # this starts the bot
    app.run_polling()
