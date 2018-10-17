import sys
import time
import telepot
from time import localtime, strftime
from telepot.loop import MessageLoop
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

id_info = {}
chrome = webdriver.Chrome("chromedriver.exe")
bot = telepot.Bot("427552846:AAF35-_GgK5Z91G5Dj8x0_4Xrlwolr_sJeY")


    
def handle(msg):#a function to tell the bot what to do when users answer with text
    global id_info
    text= []
    text_match= []
    recommend = []
    frequentroad = []
    #using glance function to take the necessary info.
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    #making a custom keyboard for user to use
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Yeah', callback_data='press')],
                   [InlineKeyboardButton(text="Nah I'm good", callback_data='press1')]])
    if content_type == 'text' : #check if what user sends is a text 
        if chat_id not in id_info : #check if it is a new user
            id_info[chat_id] = {"interaction" : 1, "road" :{}} #creat a new entry in its memory
        else :
            id_info[chat_id]["interaction"] +=1
            #create a list of frequent searched roads
            recommend = sorted(id_info[chat_id]["road"], key=lambda key: id_info[chat_id]["road"][key],reverse=True)
        if  id_info[chat_id]["interaction"] % 2 ==1:
            #check if the current user actually has any frequent searched roads
            for road,time in id_info[chat_id]["road"].items() :
                if time > 4 :
                    frequentroad.append(road)
            if len(frequentroad) == 0 :
                bot.sendMessage(chat_id, "Hey %s, where are you going ?" %msg['chat']['first_name'])
            else :
                #making a proper response if the user has frequent searched roads 
                if len(frequentroad) == 1 :
                    recroad = frequentroad[0]
                    keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=recroad, callback_data=recroad)]])
                else :
                    recroad1 = recommend[0]
                    recroad2 = recommend[1]
                    keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=recroad1, callback_data=recroad1)],
                        [InlineKeyboardButton(text=recroad2, callback_data=recroad2)]])
                bot.sendMessage(chat_id, "Hey %s, are you going here ? What, you think I don't remember :D" %msg['chat']['first_name'],reply_markup=keyboard1)
                bot.sendMessage(chat_id, "Or are you going somewhere else ?")
        else:
            #searching for info 
            key = msg['text']
            #marking how many times a user search a road for recommendation
            if key not in id_info[chat_id]["road"] :
                id_info[chat_id]["road"][key] =1
            else :
                id_info[chat_id]["road"][key] +=1
            #searching and filtering for relevant info
            chrome.get("https://www.onemotoring.com.sg/content/onemotoring/en/on_the_roads/traffic_news.html")
            list_acc = chrome.find_elements(By.CSS_SELECTOR, ".cell.cell80.textleft")
            for ele in list_acc :
                text.append(ele.text)
            for acc in text :
                if key in acc :
                    text_match.append(acc)
            if len(text_match) ==0 :
                bot.sendMessage(chat_id, "Sorry I can't find anything. Maybe check your spelling ? Or maybe it's your lucky day!!")
            else :
                bot.sendMessage(chat_id,"Okay here's what I found")
                for info in text_match :
                    bot.sendMessage(chat_id,info)
                bot.sendMessage(chat_id,"I'd be careful if I were you!! Wait I'm a bot...")
            bot.sendMessage(chat_id, "You wanna check anything else mastaa ?",reply_markup=keyboard)        
                    
def countinue(msg) : #a function to tell the bot what to do when users answer with custom keyboard
    text= []
    text_match= []
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Yeah', callback_data='press')],
                   [InlineKeyboardButton(text="No", callback_data='press1')]])
    global id_info
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(query_data)
    #determine which answer the user gives through the keyboard to respond properly
    if query_data == 'press1':
        bot.sendMessage(chat_id,'Okay bye bye!!!')
        id_info[chat_id]["interaction"] -=1
    elif query_data == 'press':
        bot.sendMessage(chat_id,'Go on!!')
    else : #When the user chooses the recommend button 
        key = query_data
        chrome.get("https://www.onemotoring.com.sg/content/onemotoring/en/on_the_roads/traffic_news.html")
        list_acc = chrome.find_elements(By.CSS_SELECTOR, ".cell.cell80.textleft")
        for ele in list_acc :
            text.append(ele.text)
        for acc in text :
            if key in acc :
                text_match.append(acc)
        if len(text_match) ==0 :
            bot.sendMessage(chat_id, "Sorry I can't find anything. Maybe check your spelling ? Or maybe it's your lucky day!!")
        else :
            for info in text_match :
                bot.sendMessage(chat_id,info)
        bot.sendMessage(chat_id, "You wanna check anything else ?",reply_markup=keyboard)                
    id_info[chat_id]["interaction"] += 1


    
#tell the bot how to handle messages
MessageLoop(bot, {'chat': handle,
                  'callback_query': countinue}).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
