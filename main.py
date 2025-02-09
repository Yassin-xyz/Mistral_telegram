from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from mistralai import Mistral

# Remplacez par votre token d'API Telegram
TELEGRAM_TOKEN = 'API-TELEGRAM-TOKEN'

# Utiliser directement la clé API Mistral dans le script
api_key = 'API-MISTRAL-KEY'
model = "mistral-large-latest"

# Initialiser le client Mistral
client = Mistral(api_key=api_key)

# Fonction pour démarrer le bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Bonjour ! Je suis votre bot Mistral. Comment puis-je vous aider ?')

# Fonction pour gérer les messages texte
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    try:
        # Envoyer le message à l'API Mistral
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {"role": "user", "content": user_message},
            ]
        )
        mistral_reply = chat_response.choices[0].message.content
        await update.message.reply_text(mistral_reply)
    except Exception as e:
        await update.message.reply_text(f'Erreur lors de la communication avec l\'API Mistral: {str(e)}')

def main() -> None:
    # Initialiser l'application avec le token du bot
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Ajouter des gestionnaires pour les commandes et les messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Démarrer le bot
    application.run_polling()

if __name__ == '__main__':
    main()
