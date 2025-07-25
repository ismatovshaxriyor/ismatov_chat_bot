from telegram.ext import Application, CommandHandler, MessageHandler, filters
from ismatov_chat_bot.bot import get_answer_user, get_answer_group
import logging

TOKEN = "7802060563:AAHNsuRTVRwCGpRUHxJ2nfa_xsXq1Uqcy3M"


async def start_handler(update, context):
    await update.message.reply_text(f"Salom {update.effective_user.first_name}")

async def quiz_handler(update, context):
    quiz = update.message.text
    if len(quiz) < 200:
        chat_id = update.effective_user.id
        try:
            await update.message.reply_text(get_answer_user(chat_id, quiz), parse_mode="MARKDOWN")
        except:
            await update.message.reply_text("Xatolik yuzaga keldi, iltimos qayta urining!")
    else:
        await update.message.reply_text("Savolingiz juda ham uzun!")

async def echo_command(update, context):
    group_history = [{"role": "system", "content": "Maksimal belgilar - 400ta token"}]

    if context.args:
        text_to_echo = ' '.join(context.args)
        group_history.append({"role": "user", "content": text_to_echo})
        if len(text_to_echo) < 200:
            await update.message.reply_text(get_answer_group(group_history), parse_mode="MARKDOWN")
            group_history = group_history[-2:] + [group_history[0]]
        else:
            await update.message.reply_text("Savolingiz juda ham uzun!")
    else:
        await update.message.reply_text("Iltimos, matn kiriting. Masalan: /quiz Salom")

async def error_handler(update, context):
    logging.error(f"Update '{update}' caused error '{context.error}'")

def main():
    bot = Application.builder().token(token=TOKEN).build()

    bot.add_handler(CommandHandler("start", start_handler))
    bot.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, quiz_handler))
    bot.add_handler(CommandHandler("quiz", echo_command, filters.ChatType.GROUPS))
    bot.add_error_handler(error_handler)

    bot.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()