import threading
import time
import threading
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import mysql.connector
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import mysql.connector
bot = ""
chat_id = ""
global_update = None
# Create a database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="pos"
)

# Function to fetch data from the database


def fetch_data(table_name):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    cursor.close()
    return data

# Function to respond to the /start command


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to your Database Bot! You can use the following commands:\n"
                              "--------------------------------------------------------------------------\n"
                              "This followings Commands are for Visualisation:\n"
                              "--------------------------------------------------------------------------\n"
                              "/customerlist - View customer data\n"
                              "/productlist - View product data\n"
                              "/supplierlist - View supplier data\n"
                              "/cartlist - View cat data\n"
                              "/saleslist - View sales data\n"
                              "/userslist - View Users data\n"
                              "/extralist - View extra data\n"
                              "/employelist - View employee data\n"
                              "--------------------------------------------------------------------------\n"
                              "This followings Commands are for Deleting:\n"
                              "--------------------------------------------------------------------------\n"
                              "/deleteproduct - View customer data\n"
                              "/deletecustomer - View customer data\n"
                              "/customerlist - View customer data\n"
                              "/customerlist - View customer data\n"
                              "/customerlist - View customer data\n"
                              "/customerlist - View customer data\n"
                              "/customerlist - View customer data\n"
                              "--------------------------------------------------------------------------\n"
                              "This followings Commands are for Operations-External:\n"
                              "--------------------------------------------------------------------------\n"
                              "/TotalProfit - View TotalProfit\n"
                              "/TotalPaid - View TotalPaid\n"
                              "/TotalRevenue - View TotalRevenue\n"
                              "/TotalHalfPaid - View TotalHalfPaid\n"
                              "/Sales - View Sales\n"
                              "/customerlist - View customer data\n"
                              "/customerlist - View customer data\n"
                              "--------------------------------------------------------------------------\n"
                              "This followings Commands are for Operations-External:\n"
                              "--------------------------------------------------------------------------\n"
                              )

# Function to respond to the /customerlist command


def check_for_new_customers(bot, chat_id):
    last_processed_customer_id = 0
    while True:
        cursor = db.cursor()
        cursor.execute(
            f"SELECT * FROM customer WHERE cid > {last_processed_customer_id}")
        new_customers = cursor.fetchall()
        cursor.close()

        for customer in new_customers:
            customer_id, name, phone = customer
            message = f"New customer added!\nID: {customer_id}\nName: {name}\nPhone: {phone}"

            # Send the notification message to the bot's conversation
            bot.send_message(chat_id, text=message)

            last_processed_customer_id = customer_id

        time.sleep(600)


def customer_list(update: Update, context: CallbackContext):
    customer_data = fetch_data('customer')
    message = "Customer List:\n```\n"
    message += f"| {'ID':<4} | {'Name':<20} | {'Phone':<10} |\n"
    message += "|------|----------------------|------------|\n"
    for row in customer_data:
        message += f"| {row[0]:<4} | {row[1]:<20} | {row[2]:<10} |\n"
    message += "```\n"
    update.message.reply_text(message, parse_mode="Markdown")


# Function to respond to the /productlist command

def product_list(update: Update, context: CallbackContext):
    product_data = fetch_data('product')
    message = "Product List:\n```\n"
    message += f"| {'ID':<4} | {'Name':<20} | {'Barcode':<15} | {'Price':<8} | {'Quantity':<8} | {'Supplier':<20} |\n"
    message += "|------|----------------------|-----------------|----------|----------|----------------------|\n"
    for row in product_data:
        message += f"| {row[0]:<4} | {row[1]:<20} | {row[2]:<15} | {row[3]:<8} | {row[4]:<8} | {row[5]:<20} |\n"
    message += "```\n"
    update.message.reply_text(message, parse_mode="Markdown")
# Function to fetch and display employee data


def employee_list(update: Update, context: CallbackContext):
    employee_data = fetch_data('employee')
    message = "Employee List:\n```\n"
    message += f"| {'ID':<4} | {'Name':<20} | {'Phone':<10} |\n"
    message += "|------|----------------------|------------|\n"
    for row in employee_data:
        message += f"| {row[0]:<4} | {row[1]:<20} | {row[2]:<10} |\n"
    message += "```\n"
    update.message.reply_text(message, parse_mode="Markdown")


def supplier_list(update: Update, context: CallbackContext):
    supplier_data = fetch_data('supplier')
    message = "Supplier List:\n```\n"
    message += f"| {'ID':<4} | {'Name':<20} | {'Phone':<10} |\n"
    message += "|------|----------------------|------------|\n"
    for row in supplier_data:
        message += f"| {row[0]:<4} | {row[1]:<20} | {row[2]:<10} |\n"
    message += "```\n"
    update.message.reply_text(message, parse_mode="Markdown")


def sales_list(update: Update, context: CallbackContext):
    sales_data = fetch_data('sales')
    message = "Sales List:\n```\n"
    message += f"| {'ID':<4} | {'Invoice ID':<10} | {'Customer ID':<12} | {'Customer Name':<20} | {'Total Qty':<9} | {'Total Bill':<11} | {'Status':<9} | {'Balance':<9} |\n"
    message += "|------|------------|--------------|----------------------|----------|------------|--------|---------|\n"
    for row in sales_data:
        message += f"| {row[0]:<4} | {row[1]:<10} | {row[2]:<12} | {row[3]:<20} | {row[4]:<9} | {row[5]:<11} | {row[6]:<9} | {row[7]:<9} |\n"
    message += "```\n"
    update.message.reply_text(message, parse_mode="Markdown")


def extra_list(update: Update, context: CallbackContext):
    extra_data = fetch_data('extra')
    message = "Extra List:\n```\n"
    message += f"| {'ID':<4} | {'Value':<10} |\n"
    message += "|------|----------|\n"
    for row in extra_data:
        message += f"| {row[0]:<4} | {row[1]:<10} |\n"
    message += "```\n"
    update.message.reply_text(message, parse_mode="Markdown")

# Function to fetch and display data from the 'cart' table


def cart_list(update: Update, context: CallbackContext):
    cart_data = fetch_data('cart')
    message = "Cart List:\n```\n"
    message += f"| {'Cart ID':<9} | {'INID':<5} | {'Product ID':<11} | {'Product Name':<20} | {'Bar Code':<15} | {'Quantity':<9} | {'Unit Price':<11} | {'Total Price':<12} |\n"
    message += "|-----------|-------|-------------|----------------------|---------------|---------|------------|-------------|\n"
    for row in cart_data:
        message += f"| {row[0]:<9} | {row[1]:<5} | {row[2]:<11} | {row[3]:<20} | {row[4]:<15} | {row[5]:<9} | {row[6]:<11} | {row[7]:<12} |\n"
    message += "```\n"
    update.message.reply_text(message, parse_mode="Markdown")

# Function to fetch and display data from the 'users' table


def users_list(update: Update, context: CallbackContext):
    users_data = fetch_data('users')
    message = "Users List:\n```\n"
    message += f"| {'User ID':<8} | {'Email':<30} | {'Username':<20} | {'Password':<20} | {'Question':<30} | {'Answer':<20} | {'Date':<20} | {'Update Date':<20} | {'Type':<12} |\n"
    message += "|---------|----------------------------|----------------------|----------------------|----------------------------|----------------------|--------------------|--------------------|------------|\n"
    for row in users_data:
        message += f"| {row[0]:<8} | {row[1]:<30} | {row[2]:<20} | {row[3]:<20} | {row[4]:<30} | {row[5]:<20} | {row[6]:<20} | {row[7]:<20} | {row[8]:<12} |\n"
    message += "```\n"
    update.message.reply_text(message, parse_mode="Markdown")

# Function to delete a product from the 'product' table


def delete_product(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please provide the product ID you want to delete:")
    # Set the state to wait for the product ID
    context.user_data['state'] = 'delete_product_waiting_id'

# Function to handle user input while deleting a product


def delete_product_input(update: Update, context: CallbackContext):
    if 'state' in context.user_data:
        if context.user_data['state'] == 'delete_product_waiting_id':
            # Get the product ID provided by the user
            product_id = update.message.text
            # Check if the product exists in the database
            if product_exists(product_id):
                # Delete the product from the database
                delete_product_record(product_id)
                update.message.reply_text(
                    f"Product {product_id} has been deleted.")
                # Clear the user's state
                del context.user_data['state']
            else:
                update.message.reply_text(
                    "Product not found. Please provide a valid product ID.")
        else:
            update.message.reply_text(
                "Invalid state. Please start the delete process again with /deleteproduct.")
    else:
        update.message.reply_text(
            "Invalid state. Please start the delete process again with /deleteproduct.")

# Function to check if a product with a given ID exists in the database


def product_exists(product_id):
    cursor = db.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM product WHERE pid = %s", (product_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

# Function to delete a product record from the database


def delete_product_record(product_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM product WHERE pid = %s", (product_id,))
    db.commit()
    cursor.close()

# Add command handlers to your dispatcher


def delete_customer(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Please provide the customer ID you want to delete:")
    # Set the state to wait for the customer ID
    context.user_data['state'] = 'delete_customer_waiting_id'

# Function to handle user input while deleting a customer


def delete_customer_input(update: Update, context: CallbackContext):
    if 'state' in context.user_data:
        if context.user_data['state'] == 'delete_customer_waiting_id':
            # Get the customer ID provided by the user
            customer_id = update.message.text
            # Check if the customer exists in the database
            if customer_exists(customer_id):
                # Delete the customer from the database
                delete_customer_record(customer_id)
                update.message.reply_text(
                    f"Customer with ID {customer_id} has been deleted.")
                # Clear the user's state
                del context.user_data['state']
            else:
                update.message.reply_text(
                    "Customer not found. Please provide a valid customer ID.")
        else:
            update.message.reply_text(
                "Invalid state. Please start the delete process again with /deletecustomer.")
    else:
        update.message.reply_text(
            "Invalid state. Please start the delete process again with /deletecustomer.")

# Function to check if a customer with a given ID exists in the database


def customer_exists(customer_id):
    cursor = db.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM customer WHERE cid = %s", (customer_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

# Function to delete a customer record from the database


def delete_customer_record(customer_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM customer WHERE cid = %s", (customer_id,))
    db.commit()
    cursor.close()


if __name__ == '__main__':
    # Create an instance of the Updater to handle Telegram updates
    updater = Updater(bot, use_context=True)

    global_update = updater

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("customerlist", customer_list))
    dispatcher.add_handler(CommandHandler("productlist", product_list))
    dispatcher.add_handler(CommandHandler("supplierlist", supplier_list))
    dispatcher.add_handler(CommandHandler("saleslist", sales_list))
    dispatcher.add_handler(CommandHandler("employelist", employee_list))
    dispatcher.add_handler(CommandHandler("extralist", extra_list))
    dispatcher.add_handler(CommandHandler("userslist", users_list))
    dispatcher.add_handler(CommandHandler("cartlist", cart_list))
    dispatcher.add_handler(CommandHandler("deleteproduct", delete_product))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, delete_product_input))
    dispatcher.add_handler(CommandHandler("deletecustomer", delete_customer))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, delete_customer_input))

    # Start the Telegram bot
    updater.start_polling()

    check_customers_thread = threading.Thread(
        target=check_for_new_customers, args=(global_update.bot, chat_id))
    check_customers_thread.start()

    updater.idle()
