
from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

TOKEN: Final = 'Token'
BOT_USERNAME: Final = 'name'

# Define stages of the conversation
CHILDREN, ADULTS, PAYMENT = range(3)

# Start Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Welcome to the Museum Ticket Booking Assistant. How can I assist you today?\n"
        "Would you like to book tickets or know more about a museum?\n"
        "Click to see museum list: /museumlist\n"
        "To book tickets: /booking"
    )

# Booking Command to initiate conversation
async def booking_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter the number of children (up to 12 years):")
    return CHILDREN

# Ask for number of adults
async def children_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['children'] = int(update.message.text)
    await update.message.reply_text("Now, please enter the number of adults:")
    return ADULTS

# Calculate total cost and ask for payment options
async def adults_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['adults'] = int(update.message.text)
    
    # Pricing structure (adjust these values as needed)
    adult_price = 15  # Price for Indian Adults
    children_price = 10  # Price for Indian Children (up to 12 years)

    num_adults = context.user_data['adults']
    num_children = context.user_data['children']

    # Total calculation
    total_cost = (num_adults * adult_price) + (num_children * children_price)

    # Store total cost in context for future use
    context.user_data['total_cost'] = total_cost

    # Show total cost and payment options
    await update.message.reply_text(f"Total cost for {num_adults} adults and {num_children} children is ₹{total_cost}.")
    
    # Ask user to choose a payment option
    buttons = [
        [InlineKeyboardButton(text="Google Pay", callback_data="gpay")],
        [InlineKeyboardButton(text="PayPal", callback_data="paypal")],
        [InlineKeyboardButton(text="Credit/Debit Card", callback_data="card")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text("Please select your payment method:", reply_markup=keyboard)

    # Move to the payment stage
    return PAYMENT

# Handle payment option selection
async def payment_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    payment_method = query.data
    total_cost = context.user_data['total_cost']
    
    # Provide the payment link based on the chosen method
    if payment_method == "gpay":
        await query.edit_message_text(f"Please proceed to payment using Google Pay for ₹{total_cost}. [Pay with Google Pay](https://play.google.com/store/apps/details?id=com.google.android.apps.nbu.paisa.user&hl=en_IN)")
    elif payment_method == "paypal":
        await query.edit_message_text(f"Please proceed to payment using PayPal for ₹{total_cost}. [Pay with PayPal](https://www.paypal.com/in/home)")
    elif payment_method == "card":
        await query.edit_message_text(f"Please proceed to payment using your Credit/Debit Card for ₹{total_cost}. [Pay with Card](https://www.sbicard.com/creditcards/app/user/paynet)")

    # End conversation after payment option is selected
    return ConversationHandler.END

# Command to cancel the booking process
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Booking has been cancelled.")
    return ConversationHandler.END

# Museum List Command
async def museumlist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "These are the available museums:\n"
        "1. Government Museum: /governmentmuseum\n"
        "2. Fort St. George Museum: /georgemuseum\n"
        "3. Gandhi Memorial Museum: /gandhimemorialmuseum"
    )

# Government Museum Info
async def governmentmuseum_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton(text="Location", url="https://maps.app.goo.gl/hN6YKy9r5ztdeSLx8")],
        [InlineKeyboardButton(text="Proceed to Payment", url="https://pay.google.com/about/")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text(
        "Government Museum\n"
        "Highlights:\n\n"
        "The second oldest museum in India. Known for its rich collection of sculptures, "
        "archaeological artifacts, and art galleries. Includes sections on anthropology, "
        "numismatics, zoology, and botany.\n\n"
        "Entry Fee:\n"
        "1. Indian Adults: ₹15\n"
        "2. Indian Children (up to 12 years): ₹10\n"
        "3. Foreigners: ₹250\n"
        "4. Foreign Children: ₹125\n"
        "5. Camera: ₹200\n"
        "Website: https://govtmuseumchennai.org/\n"
        "Contact: 04428193238",
        reply_markup=keyboard
    )

async def georgemuseum_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton(text="Location", url="https://maps.app.goo.gl/5Pus2TM976M7Cfou7")],
        [InlineKeyboardButton(text="Payment", url="https://pay.google.com/about/")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text(
        "GeorgeMuseum\nHighlights : \n\nThe second oldest museum in India.Known for its rich collection of sculptures, archaeological artifacts, and art galleries.Includes sections on anthropology, numismatics, zoology, and botany.\n\nEntry Fee : \n\n1.Indian Adults: ₹15\n2.Indian Children: ₹10\n3.Foreigners: ₹200\nCamera Charges: ₹200\nContact: 04425671127\nWebsite: https://www.tamilnadutourism.tn.gov.in/destinations/fort-st-george",
        reply_markup=keyboard
    )


async def gandhimemorialmuseum_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton(text="Location", url="https://maps.app.goo.gl/Kk3rC7TuiRKf2D9Z8")],
        [InlineKeyboardButton(text="Payment", url="https://pay.google.com/about/")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text(
        "GandhiMuseum\nHighlights: \n\nDedicated to Mahatma Gandhi, this museum displays the history of India's freedom struggle, Gandhi's personal belongings, and the blood-stained cloth worn by him during his assassination.\nTimings:\nOpen from 10:00 AM to 1:00 PM and 2:00 PM to 5:45 PM\nClosed on Fridays.\nEntry Fee: Free entry for all visitors.\nWebsite: http://gandhimmm.org/\nContact: 04522531060",
        reply_markup=keyboard
    )

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Add conversation handler for the booking process
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('booking', booking_command)],
        states={
            CHILDREN: [MessageHandler(filters.TEXT & ~filters.COMMAND, children_count)],
            ADULTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, adults_count)],
            PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, payment_selection)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Command Handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('museumlist', museumlist_command))
    app.add_handler(CommandHandler('governmentmuseum', governmentmuseum_command))
    app.add_handler(CommandHandler('georgemuseum', georgemuseum_command))
    app.add_handler(CommandHandler('gandhimemorialmuseum', gandhimemorialmuseum_command))

    app.add_handler(conv_handler)

    print("Polling...")
    app.run_polling(poll_interval=3)
