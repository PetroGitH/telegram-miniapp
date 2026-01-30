from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import os 


TOKEN = "TON_TOKEN"

base_dir= os.path.dirname.path(os.path.abspath(__file__))
IMAGE = os.path.join(base_dir, "webapp","img","IMG_1248.png")

def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Contact", url="https://aw.me/33646354340"),
            InlineKeyboardButton("Ton_projet", callback_data="Ton projet")
        ],
        [
            InlineKeyboardButton("facture", callback_data="facture"),
            InlineKeyboardButton("INFOS",callback_data="infos")
        ]
    ])

def Ton_Projet():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Superskunk - 10€", callback_data="prod_amnesia")],
        [InlineKeyboardButton("flitr x3", callback_data="prod_flitrx3")],
        [InlineKeyboardButton("voir panier", callback_data="view_cart")],
        [InlineKeyboardButton("Retour", callback_data="back_main")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open(IMAGE,"rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption="Bienvenue sur Ton_projet \n\nChoisis une option",
            reply_markup=main_menu()
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "Ton_projet":
        await query.edit_message_reply_markup(reply_markup=ton_projet_boutique())

    elif query.data =="back_main":
        await query.edit_message_reply_markup(reply_markup=main_menu())

    elif query.data == "contact":
        await query.message.reply_text("Contact on whatasapp : +33 6 00 00 00 00")

    elif query.data == "facture":
        await query.message.reply_text("facture: tonadresse@mail.com")
    
    elif query.data == "infos":
        await query.message.reply_text("message d'information ")

    elif query.data == "Menu":
        await query.edit_message_caption(
            caption="Nos produit",
            parse_mode="Mardown",
            reply_markup=Ton_projet()
        )
    elif query.data == "prod_amnesia":
        await query.edit_message_caption(
            caption=(
                "*Superskunk*\n\n"
                "prix : 10€"
                "cout livraison : 5.30€\n"
                "Qualité premium CBN\n"
            ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Ajouter au panier", callback_data="data_amnesia")],
            [InlineKeyboardButton("Retour", callback_data="Menu")]
        ])
    )
    elif query.data == "add_amnesia":
        cart = get_cart(context)
        cart.append({"name":"SuperSkunk","price": 10})

        await query.answer("Ajouter au panier", show_alert=True)

    elif query.data == "view_cart":
        cart = get_cart(context)

        if not cart:
            text = "panier vide"
        else:
            total = sum(item["price"] for item in cart)
            text = "Ton panier \n\n"
            for item in cart:
                text += f"{item['name']} - {item['price']}€\n"
            text += f"\n Total : {total}€"
        await query.edit_message_caption(
            caption=text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Retour", callback_data="Menu")]
            ])
        )
    elif query.data == "pay_usdt":
        total = sum(item["price"] for item in get_cart(context))
        await query.edit_message_caption(
            caption=(
                "*Paiement USDT* \n\n"
                f"Montant : {total} USDT\n\n"
                "Adresse USDT (TRC20):\n"
                "TxxxxxxxtonadresseXXXX\n\n"
                "Envoi Exactement le montant\n"
                "Puis clique ci-dessous"
            ),
            parse_mode ="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("J'ai payé", callback_data="Confirm_usdt")],
                [InlineKeyboardButton("Retour", callback_data="view_cart")]
            ])
        )

    elif query.data == "confrim_usdt":
        await query.answer("Paiement en verification", show_alert=True)                  

async def handle_webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.effective_message.web_app_data
    await update.message.reply_text(f"Données recues: {data}")

def get_cart(context):
    if "cart" not in context.user_data:
        context.user_data["cart"] = []
    return context.user_data["cart"]

     

        
def products_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Super Skunk - 12€/1gr",callback_data="prod_superskunk")],
        [InlineKeyboardButton("Flitrer X 3 - 13€/1gr",callback_data="prod_flx3")],
        [InlineKeyboardButton("Voir le panier", callback_data="view_cart")],
        [InlineKeyboardButton("Carte bancaire", url="https://buy.stripe.com/test_XXXX")]
        [InlineKeyboardButton("Retour", callback_data="Back_main")]
    ])



def main():
    app =ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp))
    app.run_polling()

if __name__=="__main__":

    main()

