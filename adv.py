import os
import tempfile
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from PIL import Image
from io import BytesIO
from removebg import RemoveBg
from telegram.ext import CommandHandler, MessageHandler
import logging
import time
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, ConversationHandler
from telegram.ext import Filters



# Define the command handler function
def versus_images(update, context):
    try:
        # Get the image URLs from the message
        image_url1 = context.args[0]
        image_url2 = context.args[1]

        # Send a message to indicate that the process is starting
        message = context.bot.send_message(chat_id=update.effective_chat.id, text="Preparing the arena, please wait...")

        # Get the user information
        user_id = update.message.from_user.id
        user_name = update.message.from_user.name
        user_command = update.message.text

        # Download the images
        response1 = requests.get(image_url1)
        response2 = requests.get(image_url2)

        # Open the images and resize to 9:16 aspect ratio
        img1 = Image.open(BytesIO(response1.content)).resize((900, 1600))
        img2 = Image.open(BytesIO(response2.content)).resize((900, 1600))
        versus_image = Image.open("/Users/omedabbass/Desktop/Python scripts/versus.png")
        deluxe_logo = Image.open('/Users/omedabbass/Desktop/Python scripts/deluxe.png')

        # Merge player 1 and player 2
        image_new = Image.new("RGB", (img1.width + img2.width, img1.height))
        image_new.paste(img1, (0, 0))
        image_new.paste(img2, (img1.width, 0))

        # Resize the marks to fit
        versus_image = versus_image.resize((500, 500))
        deluxe_logo = deluxe_logo.resize((400, 400))

        # Fix transparency
        image_new = image_new.convert("RGBA")
        versus_image = versus_image.convert("RGBA")
        deluxe_logo = deluxe_logo.convert("RGBA")

        # Center logo 1
        width = (image_new.width - versus_image.width) // 2
        height = (image_new.height - versus_image.height) // 2  
        image_new.paste(versus_image, (width, height), versus_image)

        # Paste the second logo in the lower left corner of img1
        image_new.paste(deluxe_logo, (0, img1.height - deluxe_logo.height), deluxe_logo)

        # Save the merged image
        image_io = BytesIO()
        image_new.save(image_io, format='PNG')
        image_io.seek(0)

        # Send the merged image to the user
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_io)

        # Log the user information
        log_message = f"User ID: {user_id}\nUsername: {user_name}\nCommand: {user_command}"
        context.bot.send_message(chat_id=-1001905250023, text=log_message)

        # Delete the message indicating that the process is starting
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

    except (IndexError, ValueError):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid command syntax. Please send two image URLs.")
    except Exception as e:
        context.bot
    
# Command to mirror an image horizontally
def mirror_image(update, context):
    # Get the image URL from the message
    image_url = context.args[0]

    # Send a message to indicate that the process is starting
    message = context.bot.send_message(chat_id=update.effective_chat.id, text="Entering the Mirror World via Brulee, please wait...")
    
        # Get the user information
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    user_command = update.message.text

    # Download the image
    response = requests.get(image_url)

    # Open the image
    img = Image.open(BytesIO(response.content))

    # Mirror the image horizontally
    img_mirror = img.transpose(method=Image.FLIP_LEFT_RIGHT)

    # Save the mirrored image
    image_io = BytesIO()
    img_mirror.save(image_io, format='PNG')
    image_io.seek(0)

            # Send the image to the user
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_io)

    # Delete the message indicating that the process is starting
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

        # Log the user information
    log_message = f"User ID: {user_id}\nUsername: {user_name}\nCommand: {user_command}"
    context.bot.send_message(chat_id=-1001905250023, text=log_message)


# Define the command handler function
def remove_background(update: Update, context: CallbackContext):
    # Get the image URL from the message
    image_url = context.args[0]

    # Send a message to indicate that the process is starting
    message = context.bot.send_message(chat_id=update.effective_chat.id, text="Shifting Reality, please wait...")

        # Get the user information
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    user_command = update.message.text

    try:
        # Make an API request to remove.bg
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            data={
                'image_url': image_url,
                'size': 'auto'
            },
            headers={'X-Api-Key': '5xfQGWgNDnu38GTNAJqgTavQ'},
        )

        # Save the image with transparent background in PNG format
        img = Image.open(BytesIO(response.content))
        img.save("output.png", "PNG")

        # Send the image as a document to the user
        with open('output.png', 'rb') as f:
            context.bot.send_document(chat_id=update.effective_chat.id, document=f)

        # Delete the saved image
        os.remove("output.png")

        # Log the user information
        log_message = f"User ID: {user_id}\nUsername: {user_name}\nCommand: {user_command}"
        context.bot.send_message(chat_id=-1001905250023, text=log_message)


        # Delete the message indicating that the process is starting
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)


    except Exception as e:
        # Let the user know if there was an error removing the background
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred: {str(e)}")

def start(update, context):
    message = """Welcome to the realm of Picture Manipulation! I can help you edit your pictures or add a versus mark between two images.

    Here are the commands you can use:
/mirror : Mirrors the image horizontally.

/removebg : Removes the background of the image and makes it transparent.

/versus : Adds a versus mark between two images + OPD logo.

/quiz <question> <options1,2,3,4> <explanation>: Makes a quiz prompt with the inputed variables.

/help : sends a more in-depth list of available commands.

Developed by: @QuadriIIion & @Duchilion
"""
        # Get the user information
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    user_command = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

        # Log the user information
    log_message = f"User ID: {user_id}\nUsername: {user_name}\nCommand: {user_command}"
    context.bot.send_message(chat_id=-1001905250023, text=log_message)


def help(update, context):
    message = """
Below are the available commands:

/mirror <image_url>: Horizontally mirrors the image.

/removebg <image_url>: Removes the image background and makes it transparent.

/versus <image_url1> <image_url2>: Adds a versus mark between two images.

/info <image>: Sends information about the image, including its type, color mode, dimensions, and URL.

/quiz <question> <options1,2,3,4> <explanation>: Makes a quiz prompt with the inputed variables.

 """

        # Get the user information
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    user_command = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

        # Log the user information
    log_message = f"User ID: {user_id}\nUsername: {user_name}\nCommand: {user_command}"
    context.bot.send_message(chat_id=-1001905250023, text=log_message)



def analyze_image(update, context):
    image_url = update.message.photo[-1].get_file().file_path  # get the URL of the largest version of the sent image
    response = requests.get(image_url)

    # Send a message to indicate that the process is starting
    message = context.bot.send_message(chat_id=update.effective_chat.id, text="Interrogating for Info, please wait...")
        # Get the user information
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    user_command = update.message.text

    img = Image.open(BytesIO(response.content))
    img_type = img.format
    color_type = img.mode
    dimensions = f"{img.width} x {img.height}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"""The image type is {img_type},
the color type is {color_type},
the dimensions are {dimensions},
and the Image URL is {image_url}""")
                      
    # Delete the message indicating that the process is starting
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)

        # Log the user information
    log_message = f"User ID: {user_id}\nUsername: {user_name}\nCommand: /info"
    context.bot.send_message(chat_id=-1001905250023, text=log_message)
       

# Define the states
QUESTION, OPTIONS, EXPLANATION = range(3)

# Function to handle the /quiz command
def quiz(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please send me your question.')
    return QUESTION


# Function to handle the question message
def handle_question(update: Update, context: CallbackContext) -> int:
    question = update.message.text
    context.user_data['question'] = question
    update.message.reply_text('Please enter 4 options, each separated by a comma.\n\nExample: Option 1, Option 2, Option 3, Option 4')
    return OPTIONS

# Function to handle the options message
def handle_options(update: Update, context: CallbackContext) -> int:
    options = update.message.text.split(',')
    if len(options) == 4:
        options = [option.strip() for option in options]
        options.append('None of the Above')
        context.user_data['options'] = options
        update.message.reply_text('Please enter the explanation.')
        return EXPLANATION
    else:
        update.message.reply_text('Please enter 4 options, each separated by a comma.\n\nExample: Option 1, Option 2, Option 3, Option 4')
        return OPTIONS

# Function to handle the explanation message
def handle_explanation(update: Update, context: CallbackContext) -> int:
    explanation = update.message.text
    context.user_data['explanation'] = explanation
    
    # Create the message
    message = f"{context.user_data['question']}\n\nOptions\n\n"
    for i in range(len(context.user_data['options'])):
        message += f"{i+1}. {context.user_data['options'][i]}\n\n"
    message += f"Explanation\n\n{context.user_data['explanation']}"
    
    # Send the message
    update.message.reply_text(message)
    
    # Reset the user data
    context.user_data.clear()
    
    # Return to the start state
    return QUESTION

# Function to handle the cancel command
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Quiz creation canceled.')
    context.user_data.clear()
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('quiz', quiz)],
    states={
        QUESTION: [MessageHandler(Filters.text & ~Filters.command, handle_question)],
        OPTIONS: [MessageHandler(Filters.text & ~Filters.command, handle_options)],
        EXPLANATION: [MessageHandler(Filters.text & ~Filters.command, handle_explanation)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

token='6208748356:AAGYv254QGuYJxN431IuWITKxmuwzsX71jE'
updater = Updater(token='6208748356:AAGYv254QGuYJxN431IuWITKxmuwzsX71jE', use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('removebg', remove_background))
dispatcher.add_handler(CommandHandler('mirror', mirror_image))
dispatcher.add_handler(CommandHandler('versus', versus_images))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))

# Start the bot
print("Bot started polling")
updater.start_webhook(listen="0.0.0.0",
                      port=int(os.environ.get('PORT', 5000)),
                      url_path=token,
                      webhook_url="https://picsmanips.herokuapp.com/" + token

                      )
updater.idle()

