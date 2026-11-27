from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
from model_loader import load_model, predict_image

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = 'TOKEN'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Отправьте мне изображение.')

async def handle_image(update: Update, context: CallbackContext) -> None:
    try:
        file = await update.message.photo[-1].get_file()
        file_path = await file.download_to_drive('image.jpg')
        model = load_model()
        prediction = predict_image('image.jpg', model)
        
        await update.message.reply_text(f"На изображении: {prediction}")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    application.run_polling()

if __name__ == '__main__':
    main()
