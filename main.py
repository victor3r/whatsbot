import re
from bot import WhatsappBot
bot = WhatsappBot('Ron Obvious')
bot.training('train')
bot.start('Bloco de Notas')
bot.salutation(['Bot: Oi sou um bot!',
                'Bot: Use ! no início para falar comigo!'])
last_text = ''

while True:
    text = bot.listen()
    if text != last_text and re.match(r'^!', text):
        last_text = text
        text = text.replace('!', '')
        text = text.lower()
        bot.answer(text)
