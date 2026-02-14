import telebot
import requests

# ====== CONFIG ======
TOKEN = "8565529490:AAGB_pAQhHJn04ZQy1SgFgvotqZKIbrdZuI"
FOOTBALL_API_KEY = "96b2b761621ebe71b9e18e70a5f88d5e6c056eb31f1cdf0750542158b2fdb9d9"

bot = telebot.TeleBot(TOKEN)

# ====== FONCTION API ======
def get_prediction(match_id):
    url = f"https://v3.football.api-sports.io/predictions?fixture={match_id}"
    headers = {
        "x-apisports-key": FOOTBALL_API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    if "response" not in data or len(data["response"]) == 0:
        return None

    prediction = data["response"][0]["predictions"]

    advice = prediction["advice"]
    percent = prediction["percent"]

    return advice, percent

# ====== COMMANDE START ======
@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(
        message,
        "👋 Bienvenue sur le bot de pronostics ⚽\n\n"
        "➡ Envoie simplement l'ID d'un match (ex: 123456)\n"
        "et je te donne la meilleure prédiction."
    )

# ====== TRAITEMENT DES MESSAGES ======
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    match_id = message.text.strip()

    if not match_id.isdigit():
        bot.reply_to(message, "❌ Envoie uniquement l'ID numérique du match.")
        return

    bot.send_chat_action(message.chat.id, "typing")

    try:
        result = get_prediction(match_id)

        if result is None:
            bot.reply_to(message, "❌ Aucun match trouvé avec cet ID.")
            return

        advice, percent = result

        reply = (
            f"📊 **PRONOSTIC DU MATCH**\n\n"
            f"🧠 Conseil : **{advice}**\n"
            f"📈 Probabilités :\n"
            f"🏠 Home : {percent['home']}%\n"
            f"🤝 Draw : {percent['draw']}%\n"
            f"✈ Away : {percent['away']}%"
        )

        bot.reply_to(message, reply, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"⚠ Erreur technique : {e}")

# ====== LANCEMENT ======
print("Bot en ligne...")
bot.infinity_polling()