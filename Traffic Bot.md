##Traffic Bot
###What is Traffic bot?
Traffic bot is a telegram bot designed for easy and convenient checking of road incidents for better trip planning, reducing time spent in traffic jams.

Users input the name of the road, Traffic bot cross-references that particular keyword with the [Singapore traffic database ](https://www.onemotoring.com.sg/content/onemotoring/en/on_the_roads/traffic_news.html), then sends feedback on the traffic condition of that road.
###How does it work?
Traffic bot is written on Python, using Telepot and Selenium as its APIs.
####Getting it started
First the bot needs 2 APIs to get it up and running. You can install both using PIP.
	
	pip install telepot
	pip install selenium
Additionally, Selenium needs a driver to automatically control your browser, which you can download [here](http://www.seleniumhq.org/projects/webdriver/). Different browsers need different drivers, so download accordingly. Next add your driver file to the system path, or simply put it and the python file into a same folder, and you are good to go. For this instance, we use Chrome.
 
**Telepot** helps with controlling the bot, while **Selenium** checks the keyword with the designated website.
#### Getting it running
First we need to import the required libraries.
	
	import sys
	import time
	import telepot
	from telepot.loop import MessageLoop
	from selenium import webdriver
	from selenium.webdriver.common.by import By
	from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

Then we need the handle function, which we will use to control the bot's action.

The glance function tells us some important information about the user.

		content_type, chat_type, chat_id = telepot.glance(msg)

Here we specifically look at the chat_id, because the bot needs it to send messages back to the user.

The user needs to send the bot message first, only then it can answer. This is how Telegram bots work.

	bot.sendMessage(chat_id, "Hey %s, where are you going ?" %msg['chat']['first_name'])
            
The next message the user sends, the bot will consider it a keyword for it to check with the website.
	
	key = msg['text']

Then we need Selenium to do its work.

	chrome = webdriver.Chrome("chromedriver.exe")
	chrome.get("https://www.onemotoring.com.sg/content/onemotoring/en/on_the_roads/traffic_news.html")
Selenium will open an instance of Chrome and get the designated website. Then it will cross-reference the keyword with the text inside the Class contains the information needed. Every text matches the keyword will be put into a list.

	list_acc = chrome.find_elements(By.CSS_SELECTOR, ".cell.cell80.textleft")
    	for ele in list_acc :
        	text.append(ele.text)
        for acc in text :
        	if key in acc :
            	text_match.append(acc)
Then depends on the result, the bot will respond accordingly.

	if len(text_match) ==0 :
    	bot.sendMessage(chat_id, "Sorry I can't find anything. Maybe check your spelling ? Or maybe it's your lucky day!!")
    else :
    	for info in text_match :
        	bot.sendMessage(chat_id,info)
		bot.sendMessage(chat_id,"Better be careful")



After giving feedback, the bot will ask if the user want to check anything else, using inline keyboard to collect the answer.

	keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Yeah sure', callback_data='press')],
                   [InlineKeyboardButton(text="Nah I'm good", callback_data='press1')]])
	 bot.sendMessage(chat_id, "You wanna check anything else ?",reply_markup=keyboard)        

If press 'Yeah' the conversation continues, and the same process runs again.
		
	if query_data == 'press1':
        bot.sendMessage(chat_id,'Okay bye bye!!!')
        id_counter[chat_id] -=1
    else :
        bot.sendMessage(chat_id,'Go on!!')


####Id_info
There is a dictionary inside the code named id_info.
	
	id_info = {}
Basically, the job of this dictionary is to note some of the needed information of each user, that are their chat ids, how many times has the user interacted with the bot, and how many times has the user searched that particular road. 

If there is no entry recorded for that particular chat id yet, it will create one.

	if chat_id not in id_info : 
            id_info[chat_id] = {"interaction" : 1, "road" :{}} 

Each time the user interacted with the bot, it will update the information of that user.
	
    id_info[chat_id]["interaction"] +=1

Similarly, it will note how many times a road has been searched.
	
	if key not in id_info[chat_id]["road"] :
    	id_info[chat_id]["road"][key] =1
    else :
		id_info[chat_id]["road"][key] +=1
	
Because there are two steps in a process ( bot receive message, bot receives keywords), we will get the modulo 2 of the counter for processing.

	if  id_info[chat_id]["interaction"] % 2 ==1::
		bot.sendMessage(chat_id, "Hey %s, where are you going ?" %msg['chat']['first_name'])
	else :
	...
If the counter modulo 2 equals 1, the bot will interact with the user.
If it is equal to 0, the bot will take the whole message as the keyword and start searching. 

Because the bot has noted down how many times a road has been searched, it can suggest the choices to speed up the process. 

	 for road,time in id_info[chat_id]["road"].items() :
     	if time > 4 :
        	frequentroad.append(road)

As you can see, if a road has been searched more than 4 times, it will be added to the list. Depending on how many roads make it into the list, the bot will give out the choices accordingly, maximum of 2 choices.
	
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
		bot.sendMessage(chat_id, "Hey %s, are you going here ? What, you think I don't remember :D" %msg['chat']['first_name'] ,reply_markup=keyboard1)
        bot.sendMessage(chat_id, "Or are you going somewhere else ?")

####Running the bot
After all the coding, we need to link it with our trusty bot.
	
	bot = telepot.Bot("400251236:AAEdBqotoL52cEFEq0bo5bw3wehrJ3rfmYQ")
The MessageLoop function will guide the bot on how to respond to a message using our own functions.
	
	MessageLoop(bot, {'chat': handle,
                  	'callback_query': countinue}).run_as_thread()
And finally we need to keep the program running using :

	while 1:
    	time.sleep(10)



 
