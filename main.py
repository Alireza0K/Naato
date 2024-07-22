from telethon.sync import TelegramClient, events, Button
from telethon import types
from dotenv import load_dotenv
from Controller import Controller
import os
import logging

load_dotenv()

Api_id = os.getenv("Api_id")

Api_hash = os.getenv("Api_hash")

Bot_token = os.getenv("Bot_token")

client = TelegramClient("bot", Api_id ,Api_hash).start(bot_token=Bot_token)

cont = Controller("/start")

listOfVoite = []

@client.on(events.NewMessage(pattern="/start")) # this section work for statrting the game
async def start(event):
    
    keyboard = [
        [  
            Button.inline("شروع بازی🎮", b"1"), 
            Button.inline("دعوت از دوستان🫂", b"2")
        ],
        [
            Button.inline("گروه های برتر🐲", b"3"), 
            Button.inline("شارژ اکانت لازم دارم😵‍💫", b"4")
        ],
        [
            Button.inline("کمک لازم دارم😿", b"5")
        ]
    ]
    
    global User
    
    User = event.sender

    await client.send_message(event.chat_id
                              ,f"سلام {User.first_name} \n\nبه بازی ناتو خوش اومدی🥳  \nتوی این بازی کلیییی قراره بهت خوش بگذره.  \nبیا باهم گذینه های پایین رو نگاه کنیم 👀 \n\n⚠️اگه نیاز به کمک داشتی |کمک لازم دارم| رو بزن"
                              ,buttons=keyboard)
async def help(event):
    
    User = event.sender
    
    keyboard = [
        [
            Button.inline("میخوای به ادمین پیام بدی؟", b"6"),
        ],
        [
            Button.inline("پیشنهادی داری که چجوری میتونم کمکت کنم؟!", b"7")
        ]
    ]
    
    await client.send_message(event.chat_id, "من میتونم کمکت کنم😍", buttons=keyboard)
    
@client.on(events.NewMessage(pattern="/F")) # This Section is for Geting Facts from users
async def F(event):
    
    user = event.sender.id
        
    user = cont.GetUserByUName(user)
    
    check = cont.checkQ(user[0][5])
    
    if check == False:

        facts = str(event.message.message)
                    
        facts = facts.replace("/F", "")
                    
        edit = facts.split("\n")
                    
        if " " in edit:
                        
            edit.remove(" ")
                        
        if "" in edit:
                        
            edit.remove("")
                        
        facts = edit

        if len(facts) > 5:
                        
            await event.respond("تعداد فکت های شما بیشتر از حد مجاز بود.😵‍💫")
                        
        elif len(facts) == 5:
                        
            await event.respond("تعداد فکت های شما کاملا اندازس، آفرین🥳")
                        
            ApplyFacts = cont.GetFactsFromEachUser(user[0][3], facts=facts)
                        
        elif len(facts) < 5:
                        
            await event.respond("تعداد فکت های شما از مجاز کمتر بود لطفا دوباره وارد کنید.😵‍💫")
            
        if user[0][4] == "Naato":
            
            await client.send_message(event.chat_id,"تبریک میگم شما** -ناتو-** این بازی هستید.🎭", parse_mode="markdown")
            
            qaA = cont.ShowQandA(user[0][5])
            
            for questionAndAnswers in qaA:
                
                textMessage = []
                
                textMessage.append([f"سوال **{str(questionAndAnswers[0])}**⚠️\n"])
                
                for answers in questionAndAnswers[1]:
                    
                    if answers[1] == 0:
 
                        textMessage.append([f"جواب **{str(answers[0])}** ❌\n"])
                        
                    elif answers[1] == 1:

                        textMessage.append([f"جواب درست **{str(answers[0])}** ✅\n"])
                
                message = f"{textMessage[0][0]}\n{textMessage[1][0]}\n{textMessage[2][0]}\n{textMessage[3][0]}\n{textMessage[4][0]}\n"
                
                await client.send_message(event.chat_id, message)
            
    else:
        
        await event.respond("⚠️هنوز راوی سوالات رو وارد نکرده\n\nیکم صبر کن.🙏🏻")
        
@client.on(events.NewMessage(pattern="/RA")) # First Cicle of Game 
async def RA(event):
    
    user = event.sender
    
    findTheUser = cont.GetUserByUName(user.id)
    
    keyboard = [
        [
            Button.inline("سوال ها", b"15"),
            Button.inline("فَکت ها", b"16")  
        ],
    ]
    
    if findTheUser[0][4] == "narrator":
        
        await client.send_message(event.chat_id,"شما سایکل **اول** بازی رو شروع کردید. 🔃1️⃣\n\nتوی این بخش شما  **دو سوال**  و **دو فکت** مطرح میکنید، و بعد از جواب دادن تیم به بخش سخت رای دهی میرسیم.\n\nکه یکی از تیم **حذف** میشه.🥲",buttons=keyboard)
        
        @client.on(events.CallbackQuery)
        async def handler(event):
                
            if event.data == b'15':
                
                global question
                
                global answers
                
                question = cont.ShowQuestion(groupID=findTheUser[0][5])
                
                answers = cont.ShowAnswers(questionID=question[1])
                
                keyboard = []
                
                for count in range(0,len(answers)):
                    
                    if answers[count][3] == 0:
                        
                        keyboard.append([Button.inline(answers[count][2], f"100{count}F")])

                    elif answers[count][3] == 1:
                        
                        keyboard.append([Button.inline(answers[count][2], f"100{count}T")])
                       
                await sendMessage(findTheUser[0], option="poll", text=question[3], keyboard=keyboard)

            elif event.data == b'16':
                
                await client.send_message(event.chat_id,"سلام ۱۶")

async def sendMessage(user, option="", poll=None, keyboard=[], text=""): # Masseging Function

    if user[4] == '' and option == "": # Send message to All users
        
        await client.send_message(int(user[2]), "تمام اعضای تیم جمع شدن و الان میخوایم بازی رو شروع کنیم.\n\nحالا شما قراره که fact های خودتون رو به شکل زیر وارد کنید:\n```/F \nفکت اول\nفکت دوم\nفکت سوم\nفکت چهارم\nفکت پنجم```\nاین هم از دستور `/F` فکت")
      
    elif user[4] == 'Naato' and option == "": # Send message to naato users
        
        await client.send_message(int(user[2]), "تمام اعضای تیم جمع شدن و الان میخوایم بازی رو شروع کنیم.\n\nحالا شما قراره که fact های خودتون رو به شکل زیر وارد کنید:\n```/F \nفکت اول\nفکت دوم\nفکت سوم\nفکت چهارم\nفکت پنجم```\nاین هم از دستور `/F` فکت")
      
    elif user[4] == '' and option == "poll": # Send message with poll for all users
    
        await client.send_message(int(user[2]), text, buttons=keyboard)
        
    elif user[4] == 'narrator' and option == "poll": # Send message with poll for Narrator
    
        await client.send_message(int(user[2]), text, buttons=keyboard)
        
    elif user[4] == 'Naato' and option == "poll": # Send message with poll for naaro users
        
        await client.send_message(int(user[2]), text, buttons=keyboard)
        
    elif user[4] == "narrator" and option == "": # Send Message just for narrator
            
        keyboard= [
            [
                Button.inline("وارد کردن سوال ها.", b"10")
            ]
        ]
        
        await client.send_message(int(user[2]), "تبریک میگم تمام اعضای تیم شما تکمیل شد و منتظر شما هستن تا بازی رو شروع کنید.✌️🔥\n\nشما راوی داستان هستید🥳\n\nلطفا به خوبی بازی رو روایت کنید 🎃",buttons=keyboard)

@client.on(events.CallbackQuery())
async def callback(event):
    if event.data == b'1':
        
        keyBoard = [
            [
                Button.inline("گروه میخوام", b"8"),
                Button.inline("گروه دارم", b"9")
            ]
        ]
            
        await client.send_message(event.chat_id, "گروه داری یا گروه میخوای\nاگه هرکدوم هست که بزن بریم🔥", buttons=keyBoard)

    elif event.data == b'2':
        
        await event.respond("شما روی دوکمه دوم کلیک کردید")
        
    elif event.data == b'3':
        
        await event.respond("شما روی دوکمه سوم کلیک کردید")
        
    elif event.data == b'4':
        
        await event.respond("شما روی دوکمه چهارم کلیک کردید")
        
    elif event.data == b'5':
        
        await help(event)
    
    elif event.data == b"6":
        
        await event.respond("این پیام برای ادمین فرستاده میشود.😵‍💫")
        
        @client.on(events.NewMessage)
        async def handler(event):
            
            User = event.sender
            
            if User.username != None:
                
                await client.send_message('@Alirez0K', f"Issue > {event.message.message} \nFrom > {User.username}")
            
                await client.send_message(User.username, "پیام شما به ادمین ارسال شد")
                
            elif User.username == None:
                
                await client.send_message('@Alirez0K', f"Issue > {event.message.message} \n\nFrom > User Dosent have username")
            
            await event.respond("خیلی خوشحالیم که مشکل رو به ما اطلاع دادید،\nدر چند ساعت آینده برسی و رفع خواهد شد.🫡🙏🏻")
        
    elif event.data == b"7":
        
        await event.respond("پیام خودتون رو برای ادمین بفرستید.")
        
        @client.on(events.NewMessage)
        async def handler(event):
            
            await client.send_message('@Alirez0K', event.message.message)
            
    elif event.data == b"8":
        
        id = cont.Start(0)
        
        regesterTheUser = cont.GetUserInformation(id[0], name = User.first_name, username = User.id)
        
        if regesterTheUser[1] == False:
            
            await client.send_message(event.chat_id, message=f"سلامی دوباره به تو جذاب 😍😎\n\nخیلی خوشحالیم که دوباره تورو توی بازی جذابمون میبینیم.\n\nامیدوارم که قوانین رو یادت مونده باشه😁\n\nایینم لینک گروه جدید برای تو و دوستات.\n\n`{id[0]}`\nاسم گروه:{id[1]}", parse_mode="markdown")
        
        elif regesterTheUser[1] == True:
            
            await client.send_message(event.chat_id, message=f"خیلی هم عالی حالا شما عضو گروه `{id[1]}` شدید \n\nآیدی گروه رو برای پنج تا دیگه از دوست هات هم بفرست تا باهم بازی کنید 🔥🎮\n\nاین آیدی گروه شماست: `{id[0]}`", parse_mode="markdown")
        
    elif event.data == b"9":
        
        await event.respond("آیدی گروه خودتون رو وارد کنید:")
        
        @client.on(events.NewMessage)
        async def handler(event):
            
            MInfo = str(event.message.message)
            
            User = event.sender
                
            groupinfo = cont.GetGroupInformation(MInfo)
                
            if groupinfo != None and len(MInfo) > 20:
                    
                groupName = groupinfo[0][0][2]
                
                groupID = groupinfo[0][0][1]
                
                regesterTheUser = cont.GetUserInformation(event.message.message, name = User.first_name, username = User.id)
                
                try:
                    
                    if regesterTheUser[1]:
                        
                        await event.respond(f"شما با موافقیت عضو گروه {groupName}")
                    
                        usersinfo = cont.GetUsersId(groupID)
                        
                        users = usersinfo[0]
                        
                        usersCount = usersinfo[1]
                        
                        if usersCount == 3:
                                
                            check = cont.ChooseNarrator(groupID)  # Selecting Narrator from group
                                
                            naato = cont.ChooseNaato(groupID)
                                
                            if check:
                                
                                usersinfo = cont.GetUsersId(groupID)
                        
                                users = usersinfo[0]
                                
                                for user in users:
                                    
                                    await sendMessage(user) # Sending messsage to all user
                                    
                except TypeError:
                    
                    print(TypeError) 
                        
    elif event.data == b"10":
        
        await event.respond("سوال هارا دونه به دونه با `/Q` وارد کنید:") # This section for Get questions from Narrator
        
        @client.on(events.NewMessage(pattern="/Q"))
        async def Q(event):
            
            user = event.sender.id
            
            user = cont.GetUserByUName(user)
            
            usernickname = user[0][4]
            
            groupID = user[0][5]
            
            question = str(event.message.message)
            
            question = question.replace("/Q", "")
            
            questions = cont.QandANarator(userNickName=usernickname, groupID=groupID, Q=[question], A="Test magic")
            
            if questions[0]:
                
                await client.send_message(event.chat_id, 
                                          "**سوال شما ثبت شد🔥**\n\n طبق فرمول زیر جواب هارا لحاظ کنید:\n ```/A\nجواب اول\nجواب دوم\nجواب سوم\nجواب چهارم = 1``` \nجواب درست را با `جواب = 1` نشان میدهیم",
                                          parse_mode="markdown")
            
            elif questions[0] == False:
                
                await event.respond("هروقت بچه ها آماده بودن دستور `/RA` بزن")
            
            else:
                
                await event.respond("شما چهار سوال وارد کردید.")
            
            @client.on(events.NewMessage(pattern="/A"))
            async def A(event):
                
                answers = str(event.message.message)
            
                answers = answers.replace("/A", "")
                
                edit = answers.split("\n")
                
                if " " in edit:
                    
                    edit.remove(" ")
                    
                if "" in edit:
                    
                    edit.remove("")
                    
                for i in range(0,len(edit)):
                    
                    ed = edit[i]
                    
                    ed = ed.split("=")
                    
                    edit[i] = ed
                    
                answers = edit
                
                for answer in answers:
                    
                    
                    if len(answer) == 2:
                        
                        applyAnswers = cont.AnswersNarrator(question_Hash=questions[1], answers=answer[0], check=1)
                        
                    elif len(answer) == 1:
                        
                        applyAnswers = cont.AnswersNarrator(question_Hash=questions[1], answers=answer[0], check=0)
                        
                if applyAnswers:    
        
                    await event.respond("جواب شما ثبت شد.")
                
                else:
                    
                    await event.respond("چهار جواب شما ثبت شده.")
                
    if str(event.data) in [str(b"1000F"), str(b"1001F"),str(b"1002F"), str(b"1003F"),str(b"1000T"), str(b"1001T"),str(b"1002T"), str(b"1003T")]:
        
        if str(event.data) in [str(b"1000F"), str(b"1001F"),str(b"1002F"), str(b"1003F")]:
            
            for answer in answers:
                
                if answer[3] == 1:
                    
                    text = f"جواب اشتباه بود 🥲❌\n\n جواب درست **{answer[2]}**بود."
                    
                    await client.send_message(event.chat_id, text, parse_mode='markdown')
                    
                    cont.CheckedQ(quesionID=question[1])
                    
        elif str(event.data) in [str(b"1000T"), str(b"1001T"),str(b"1002T"), str(b"1003T")]:
            
            await client.send_message(event.chat_id, "جواب شما درست بود ✅🧠")
            
            cont.CheckedQ(quesionID=question[1])
                    
client.start()

client.run_until_disconnected()