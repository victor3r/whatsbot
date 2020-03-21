import os
import time
import re

from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from selenium import webdriver


class WhatsappBot:
    dir_path = os.getcwd()

    def __init__(self, bot_name):
        self.bot = ChatBot(bot_name)
        self.trainer = ListTrainer(self.bot)
        options = webdriver.ChromeOptions()
        options.add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')

    def start(self, contact_name):
        self.driver.get('https://web.whatsapp.com/')
        time.sleep(10)
        self.search_box = self.driver.find_element_by_class_name('_3u328')
        time.sleep(1)
        self.search_box.send_keys(contact_name)
        time.sleep(1)
        self.contact = self.driver.find_element_by_xpath(
            f"//span[@title = '{contact_name}']")
        time.sleep(1)
        self.contact.click()

    def salutation(self, initial_phrase):
        self.message_box = self.driver.find_element_by_class_name('_13mgZ')
        time.sleep(1)
        if type(initial_phrase) == list:
            for phrase in initial_phrase:
                self.message_box.send_keys(phrase)
                self.send_button = self.driver.find_element_by_xpath(
                    "//span[@data-icon='send']")
                time.sleep(1)
                self.send_button.click()
        else:
            return False

    def listen(self):
        post = self.driver.find_elements_by_class_name('_1zGQT')
        time.sleep(1)
        last = len(post) - 1
        text = post[last].find_element_by_css_selector(
            'span.selectable-text').text
        time.sleep(1)
        return text

    def answer(self, text):
        response = self.bot.get_response(text)
        if float(response.confidence) > 0.5:
            response = str(response)
        else:
            response = 'Ainda não sei responder esta pergunta'
        response = 'Bot: ' + response
        self.box_message = self.driver.find_element_by_class_name('_13mgZ')
        time.sleep(1)
        self.box_message.send_keys(response)
        self.send_button = self.driver.find_element_by_xpath(
            "//span[@data-icon='send']")
        time.sleep(1)
        self.send_button.click()

    def training(self, folder_name):
        for train in os.listdir(folder_name):
            conversations = open(folder_name+'/'+train, 'r',
                                 encoding='utf8').readlines()
            self.trainer.train(conversations)
