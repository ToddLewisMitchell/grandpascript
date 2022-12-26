import datetime
import random
import textwrap

import click
import colorama
import dictionaries as d
from colorama import Fore, Back
from twilio.rest import Client

# See https://zetcode.com/python/click/
@click.command()
@click.option('-u', '--user', default='', help="Enter your first name for a fun greeting!")
@click.option('-b', '--bible', is_flag=True, default=False, help="Show Grandpa's Bible verse(s) of the day!")
@click.option('-s', '--send', is_flag=True, default=False, help="Send a text message!")
def main(user, bible, send):
    """This CLI program is for my grandchildren to learn about the command-line.

Todd Mitchell, Canby, MN, Christmas, 2022"""
    username = None

    colorama.init(autoreset=True)
    buffer = Fore.LIGHTRED_EX
    if user:
        if user== '-b' or user== '-s':
            buffer += f'\nNext time you may enter your first name like this:\n\n'
            buffer += f'     grandpascript -u Name.\n\n'
            buffer += f'If you want to do more than one thing, you can add commands like this:\n\n'
            buffer += f'     grandpascript -u Name -b -s\n\n'
            print(buffer)
            if user== '-b': bible=True
            if user== 's': send=True
            username = get_name()
        else:
            username = user
        grandpa_greeting(username)

    if bible:
        if user: wait()
        verse_of_the_day()

    if send:
        if user or bible : wait()
        send_message(username)

    colorama.init(autoreset=True)
    buffer = Fore.LIGHTRED_EX
    if not user and not bible and not send:
        buffer += '\nPlease try again. This time, try this:\n\n'
        buffer += '     grandpascript -u Name\n\n'
        buffer += 'Or if you want to read Grandpa\'s verse(s) of the day, try this:\n\n'
        buffer += '     grandpascript -b\n\n'
        buffer += 'Or if you want to send a message, try this:\n\n'
        buffer += '     grandpascript -s\n\n'
        buffer += 'You can even do more than one thing! Try this:\n\n'
        buffer += '     grandpascript -u Name -b -s\n\n'
        print(buffer)

def get_name() -> str:
    """Prompt the user for his name."""
    username = click.prompt('Please enter your first name (CTRL+C to exit)', type=str)
    return username

def wait():
    """This function prompts the user to press ENTER to continue."""
    input('Press ENTER to continue . . . . . . .')
    return

def verse_of_the_day():
    """Print the verse of the day stored in dictionaries.verses."""
    print(f'\n{box_text(d.verses[day_of_year()], "left", "single", True)}')
    colorama.init()
    c = Back.LIGHTWHITE_EX
    r = Back.RESET
    art = f'''
              {c}   {r}
              {c}   {r}               
              {c}   {r}               Well done! You have found the
      {c}                   {r}       very best part of this program!
              {c}   {r}               
              {c}   {r}               I am so happy you are here.
              {c}   {r}               
              {c}   {r}               Love,
              {c}   {r}               
              {c}   {r}               Grandpa
              {c}   {r}'''
    print(f'{art}\n\n')

def send_message(username: str = None):
    """Send an SMS message to one of the specified recipients using a Twilio account."""
    # I hate hard-coding recipients, but since I'm writing this for smart children I need to protect against hacking.
    recipients = {'Mama': '+15555555555',
                  'Papa': '+15555555555',
                  'Grandpa': '+15555555555',
                  'Grandma': '+15555555555'}
    prompt_width = 50

    print(Fore.LIGHTGREEN_EX + d.artwork['pooh'])
    header = "* * * * * * * SEND TEXT MESSAGE * * * * * * *".center(prompt_width)
    print(f'{Fore.LIGHTGREEN_EX}\n{box_text(header, "center", "double")}{Fore.RESET}\n')

    if not username: username = get_name()
    recipient = click.prompt('To whom would you like to send a message (CTRL+C to exit)?\n',
                               type = click.Choice(recipients.keys(), case_sensitive=False))
    recipient_number = recipients[recipient]
    message = click.prompt('What would you like to say (CTRL+C to exit)?', type=str)
    message = f'{username} says, "{message}"'
    message = trim_message(message)

    colorama.init(autoreset=True)
    buffer ='\nYou are about to send this message:\n'
    prompt = f'To: {recipient}\n{wrap_text(message, prompt_width)}'
    buffer += f'{Fore.LIGHTGREEN_EX}\n{box_text(prompt, "left", "double", False)}\n'
    print(buffer)
    confirm = click.prompt('Are you sure you want to send this message?',
                           type = click.Choice(['Send', 'Cancel'], case_sensitive=False))

    success = False
    if confirm == 'Send':
        try:
            # Twilio Account SID and Auth Token.
            client = Client("SID GOES HERE", "AUTH TOKEN GOES HERE")
            client.messages.create(to=recipient_number, from_="TWILIO PHONE NUMBER GOES HERE", body=message)
            print(f'{Fore.LIGHTGREEN_EX}\n{d.artwork["message_sent"]}')
            print(f'Your message has been sent to {recipient}!')
            success = True
        except:
            print(f'{Fore.LIGHTRED_EX}\nThere was an error sending your message.')
    elif confirm == 'Cancel':
        print('Your message has been canceled.')
        try_again = click.prompt('Would you like to try again?',
                           type = click.Choice(['Yes', 'No'], case_sensitive=False))
        if try_again == 'Yes':
            send_message(username)
        else:
            print(f'\nGoodbye, {username}. Have a great day!')

def trim_message(text: str) -> str:
    """This function returns text trimmed to 320 characters to meet Twilio recommendations."""
    # Twilio maximum message length is 1600 but recommends no more than 320 characters.
    # https://support.twilio.com/hc/en-us/articles/360033806753-Maximum-Message-Length-with-Twilio-Programmable-Messaging
    # Normally this would be indicated at the time of data entry but it's unlikely a child will exceed 320,
    # and it is not worth confusing him with extra instructions.
    if len(text) > 320:
        text = text[:320]
        print(f'{Fore.LIGHTRED_EX}\nYour message was a bit too long, so I\'ve shortened it.\n')
    return text

def grandpa_greeting(username: str = None):
    """Print a personalized greeting."""
    # See https://waylonwalker.com/drawing-ascii-boxes/
    if not username: username = get_name()
    colors = (Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTRED_EX)
    color = colors[random.randint(0, 4)]
    colorama.init(autoreset=True)
    buffer = color
    buffer += f"\n{box_text(random_greeting(username), 'left', 'single', True, 26)}\n"
    buffer += d.artwork['grandpa']
    print(buffer)

def day_of_year() -> int:
    """Return today's day of the year from 1-366."""
    current_date = datetime.date.today()
    return current_date.timetuple().tm_yday

def box_text(text: str, justify: str = 'left', border: str = 'single', rounded: bool = 'False', indent: int = 0) -> str:
    """Return text enclosed in a box."""
    split = text.splitlines()
    length = 0
    for line in split:
        if length < len(line): length = len(line)
    indent += length
    if border == 'single':
        box_vertical = '│'
        box_horizontal = '─'
        if rounded:
            box_left_top = '╭'
            box_left_bottom = '╰'
            box_right_top = '╮'
            box_right_bottom = '╯'
        else:
            box_left_top = '┌'
            box_left_bottom = '└'
            box_right_top = '┐'
            box_right_bottom = '┘'
    elif border == 'double':
        box_horizontal = '═'
        box_left_top = '╔'
        box_left_bottom = '╚'
        box_vertical = '║'
        box_right_top = '╗'
        box_right_bottom = '╝'

    box_horizontal = box_horizontal * (length + 2)
    result = (f'{box_left_top}{box_horizontal}{box_right_top}\n').rjust(indent)
    for line in split:
        if justify == 'left':
            line = line.ljust(length)
        elif justify == 'center':
            line = line.center(length)
        elif justify == 'right':
            line = line.rjust(length)
        result += (f'{box_vertical} {line} {box_vertical}\n').rjust(indent)
    result += (f'{box_left_bottom}{box_horizontal}{box_right_bottom} ').rjust(indent)
    return result

def random_greeting(name: str) -> str:
    """Return one of the greetings stored in tuple greetings."""
    greetings = ("Hello", "Hi", "Hello there,",
                 "Nice to see you,", "Welcome,", "Well, hello",
                 "It's", "Yay,", "Way to go,",
                 "Well done,", "Wow,", "Glad to see you,",
                 "Good to see you! Be careful,")
    greeting = greetings[random.randint(0,len(greetings)-1)]
    if name: name = f' {name}'
    result = f'{greeting}{name}! You\'re using the command line!'
    return result

def wrap_text(text: str, width: int) -> str:
    """This function returns supplied text divided into multiple lines, left justified,
    each line no longer than the number of characters specified by width."""
    wrapper = textwrap.TextWrapper(width=width)
    wrapped_text = wrapper.wrap(text=text)
    result = ''
    for line in wrapped_text:
        result += f'{line.ljust(width)}\n'
    return result

if __name__ == '__main__':
    main()
