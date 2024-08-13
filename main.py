from telethon.sync import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon import types, errors
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

Channels = ["https://t.me/HowmanyCocksAreAlive","https://t.me/Howoldtheearth"] # Channels Adds list

channelValidation = [] # For user Adds Validation

listOfVoite = [] # List of voite for choosing the Naato

Trust = [] # I DONT KNOW WTF

voitingButtonVal = [] # Validation of voite list

CountFirstRound = [] 

FactCounter = []

terminate = []

roundSet = ["","",""] # THIS IS SO IMPORTANT * its the round seter ["firstround" "secondround" "Final"] 

voite = True

@client.on(events.NewMessage(pattern="/start")) # this section work for statrting the game
async def start(event):
    
    keyboard = []
    
    message = ""
    
    eq = len(Channels) - len(channelValidation)
    
    global User
    
    User = event.sender
    
    if eq == 0:
        
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

        message = f"سلام {User.first_name} \n\nبه بازی ناتو خوش اومدی🥳  \nتوی این بازی کلیییی قراره بهت خوش بگذره.  \nبیا باهم گذینه های پایین رو نگاه کنیم 👀 \n\n⚠️اگه نیاز به کمک داشتی |کمک لازم دارم| رو بزن"
        
        await client.send_message(entity=event.chat_id
                              ,message=message
                              ,buttons=keyboard)
        
    else:
    
        for channel in Channels:
            
            message = f"{eq} چنل باقی مونده که بهشون جوین بشی بازی رو شروع میکنیم."
            
            keyboard.append([Button.url(text="Join to channel ❌",url=channel)])
        
            if await is_participant(channel, event.sender.id) == True:
                
                channelValidation.append(True)   
                
        await client.send_message(entity=event.chat_id,message=message,buttons=keyboard)
                
async def is_participant(channel, user) -> bool:
    
    try:
        
        await client.get_permissions(channel, user)
        
        return True
    
    except errors.UserNotParticipantError:
        
        return False

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
    
    roundSet[0] = "first"
    
    user = event.sender
    
    global findTheUser
    
    findTheUser = cont.GetUserByUName(user.id)
    
    keyboard = [
        [
            Button.inline("سوال ها", b"15"),
            Button.inline("فَکت ها", b"16")  
        ],
    ]
    
    if findTheUser[0][4] == "narrator":
        
        await client.send_message(event.chat_id,"شما سایکل **اول** بازی رو شروع کردید. 🔃1️⃣\n\nتوی این بخش شما  **دو سوال**  و **دو فکت** مطرح میکنید، و بعد از جواب دادن تیم به بخش سخت رای دهی میرسیم.\n\nکه یکی از تیم **حذف** میشه.🥲",buttons=keyboard)

@client.on(events.NewMessage(pattern="/RB")) # Second Cicle of Game 
async def RB(event):
    
    listOfVoite.clear()
    
    voitingButtonVal.clear()

    CountFirstRound.clear()

    FactCounter.clear()

    terminate.clear()
    
    roundSet[0] = ""
    
    roundSet[1] = "second"
    
    user = event.sender
    
    global findTheUser
    
    findTheUser = cont.GetUserByUName(user.id)
    
    keyboard = [
        [
            Button.inline("سوال ها", b"15"),
            Button.inline("فَکت ها", b"16")  
        ],
    ]
    
    if findTheUser[0][4] == "narrator":
        
        await client.send_message(event.chat_id,"شما سایکل **اول** بازی رو شروع کردید. 🔃2️⃣\n\nتوی این بخش شما  **دو سوال**  و **دو فکت** مطرح میکنید، و بعد از جواب دادن تیم به بخش سخت رای دهی میرسیم.\n\nکه یکی از تیم **حذف** میشه.🥲",buttons=keyboard)

@client.on(events.NewMessage(pattern="/END"))
async def END(event):

    listOfVoite.clear()
    
    voitingButtonVal.clear()

    CountFirstRound.clear()

    FactCounter.clear()

    terminate.clear()
    
    roundSet[0] = ""
    
    roundSet[1] = ""
    
    roundSet[2] = "FINAL"
    
    user = event.sender
    
    global findTheUser
    
    findTheUser = cont.GetUserByUName(user.id)
    
    keyboard = [
        [
            Button.inline("آخرین بخش 🎃", b"20")  
        ],
    ]
    
    if findTheUser[0][4] == "narrator":
        
        await client.send_message(event.chat_id,"و این هم از آخر بازی، حالا باید افراد باقی مانده تصمیم بگیرن که کی **ناتو** این بازی هست 🎭😶‍🌫️",buttons=keyboard)

async def Voite(event,listA, listB, roundCounter = []): # This Section Make The VOITED.
    
    usersinfo = cont.GetUserByUName(event.sender.id)
    
    usersinfo = cont.GetUsersId(usersinfo[0][5])
    
    users = usersinfo[0][1:]
    
    if len(listA) == roundCounter[0] and len(listB) == roundCounter[1]:

        if len(usersinfo[0]) == 3:
            
            keyboard = [
                []
            ]
            
            for userCount in range(0,len(users)):
                
                if users[userCount][4] != "Naato":

                    keyboard[0].append(Button.inline(users[userCount][1], f"{users[userCount][2]}"))
                
                elif users[userCount][4] == "Naato":

                    keyboard[0].append(Button.inline(users[userCount][1], f"{users[userCount][2]}N"))

        elif len(usersinfo[0]) <= 6:

            keyboard = [
                [],
                [],
                []
            ]
            
            for userCount in range(0,len(users)):
                
                if userCount <= 1: 
                
                    if users[userCount][4] != "Naato":
                        
                        keyboard[0].append(Button.inline(users[userCount][1], f"{users[userCount][2]}"))
                    
                    elif users[userCount][4] == "Naato":

                        keyboard[0].append(Button.inline(users[userCount][1], f"{users[userCount][2]}N"))
                        
                elif userCount <= 3:

                    if users[userCount][4] != "Naato":
                        
                        keyboard[1].append(Button.inline(users[userCount][1], f"{users[userCount][2]}"))
                    
                    elif users[userCount][4] == "Naato":

                        keyboard[1].append(Button.inline(users[userCount][1], f"{users[userCount][2]}N"))
                        
                elif userCount == 4:

                    if users[userCount][4] != "Naato":
                        
                        keyboard[2].append(Button.inline(users[userCount][1], f"{users[userCount][2]}"))
                    
                    elif users[userCount][4] == "Naato":

                        keyboard[2].append(Button.inline(users[userCount][1], f"{users[userCount][2]}N"))
                        
        for user in usersinfo[0]:
            
            if user[4] != "narrator":
                
                text = f"""**Let's Fucking Do this 🔥👺**\nچه کسی رو **انتخاب** میکنی؟"""
                
                await sendMessage(user=user, option="poll", text=text,keyboard=keyboard)
                
        for count in range(0,len(keyboard)):
        
            for dt in range(0, len(keyboard[count])):
                
                button = keyboard[count][dt]

                voitingButtonVal.append(str(button.data))
                
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

    elif option == "score":

        await client.send_message(int(user[2]), text)
        
    elif option == "notice":

        await client.send_message(int(user[2]), text)
        
    elif option == "UserWin":
        
        await client.send_message(int(user[2]), text)
        
    elif option == "ShowPoints":
        
        await client.send_message(int(user[0]), text)
        
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
        
        if regesterTheUser[0] == False:
            
            await client.send_message(event.chat_id, message=f"سلامی دوباره به تو جذاب 😍😎\n\nخیلی خوشحالیم که دوباره تورو توی بازی جذابمون میبینیم.\n\nامیدوارم که قوانین رو یادت مونده باشه😁\n\nایینم لینک گروه جدید برای تو و دوستات.\n\n`{id[0]}`\nاسم گروه:{id[1]}", parse_mode="markdown")
        
        elif regesterTheUser[0] == True:
            
            await client.send_message(event.chat_id, message=f"خیلی هم عالی حالا شما عضو گروه `{id[1]}` شدید \n\nآیدی گروه رو برای پنج تا دیگه از دوست هات هم بفرست تا باهم بازی کنید 🔥🎮\n\nاین آیدی گروه شماست: `{id[0]}`", parse_mode="markdown")
        
    elif event.data == b"9": # This button do user group changes for second Game or `MORE`!!!
        
        await event.respond("آیدی گروه خودتون رو وارد کنید:")
        
        @client.on(events.NewMessage)
        async def handler(event):
            
            MInfo = str(event.message.message)
            
            User = event.sender
                
            groupinfo = cont.GetGroupInformation(MInfo)
                
            if groupinfo != None and len(MInfo) > 20:
                    
                groupName = groupinfo[0][0][2]
                
                groupID = groupinfo[0][0][1]
                
                regesterTheUser = cont.ChangeGroupID(userID = User.id, newGroup = event.message.message)
                
                try:
                    
                    if regesterTheUser:
                        
                        await event.respond(f"شما با موافقیت عضو گروه {groupName}")
                    
                        usersinfo = cont.GetUsersId(groupID)
                        
                        users = usersinfo[0]
                        
                        usersCount = usersinfo[1]
                        
                        if usersCount == 6:
                                
                            check = cont.ChooseNarrator(groupID)  # Selecting Narrator from group
                                
                            cont.ChooseNaato(groupID)
                                
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
    
    elif event.data == b'15': # This button is for QandA round One

        global question
                
        global answers
                
        CountFirstRound.append(1)

        keyboard = []

        if len(CountFirstRound) <= 2:
            
            question = cont.ShowQuestion(groupID=findTheUser[0][5])

            answers = cont.ShowAnswers(questionID=question[1])

            for count in range(0, len(answers)):

                if answers[count][3] == 0:

                    keyboard.append([Button.inline(answers[count][2], f"100{count}F")])

                elif answers[count][3] == 1:

                    keyboard.append([Button.inline(answers[count][2], f"100{count}T")])
                    
            await sendMessage(findTheUser[0], option="poll", text=question[3], keyboard=keyboard)

        else:

            await client.send_message(event.chat_id, "شما دوبار سوال و جواب کردید و الان باید برید **راند** بعدی `/RB` یا این که **فَکت** هارو بپرسید. 🔗")
    
    elif event.data == b'16': # This Button is For Facts in Round One
        
        facts = []
        
        nuser = cont.GetUserByUName(event.sender.id)
        
        users = cont.GetUsersId(group=nuser[0][5])
        
        for user in users[0]:

            if user[4] == "Naato":
                
                facts = cont.ShowFacts(user[3])
                     
        FactCounter.append(1)
        
        if roundSet[0] == "first":
            
            if len(FactCounter) <= 3:
                
                await client.send_message(event.chat_id, f"فَکت اینه که: \n**|- {str(facts[0][2])} -|**\n\nاین رو برای بازی کن ها بازگو کن 😶‍🌫️👹\n\nو دوباره روی دکمه **فَکت** ها بزن 👆")
                
                cont.FactCheck(facts[0][0])
            
            else:
                
                await client.send_message(event.chat_id, "شما سه سوال خود را پرسیده اید و الان باید برید **راند** بعدی یا این که **سوال** هارو بپرسید. 🔗")
        
        elif roundSet[1] == "second":
            
            if len(FactCounter) <= 2:
                
                await client.send_message(event.chat_id, f"فَکت اینه که: \n**|- {str(facts[0][2])} -|**\n\nاین رو برای بازی کن ها بازگو کن 😶‍🌫️👹\n\nو دوباره روی دکمه **فَکت** ها بزن 👆")
                
                cont.FactCheck(facts[0][0])
            
            else:
                
                await client.send_message(event.chat_id, "شما دو سوال خود را پرسیده اید و الان باید **سوال** هارو بپرسید. 🔗")
             
        if roundSet[0] == "first" and voite == True:
            
            if len(FactCounter) > 3:
                
                FactCounter.clear()
                
                FactCounter.append(1)
                
                FactCounter.append(1)
                
                FactCounter.append(1)
                
            elif len(CountFirstRound) > 2:
                
                CountFirstRound.clear()
                
                CountFirstRound.append(1)
                
                CountFirstRound.append(1)
            
            await Voite(event,CountFirstRound, FactCounter, [2, 3])
            
        elif roundSet[1] == "second" and voite == True:
            
            if len(FactCounter) > 2:
                
                FactCounter.clear()
                
                FactCounter.append(1)
                
                FactCounter.append(1)
                
            elif len(CountFirstRound) > 2:
                
                CountFirstRound.clear()
                
                CountFirstRound.append(1)
                
                CountFirstRound.append(1)
                
            await Voite(event,CountFirstRound, FactCounter, [2, 2])
        
    elif str(event.data) in [str(b"1000F"), str(b"1001F"),str(b"1002F"), str(b"1003F"),str(b"1000T"), str(b"1001T"),str(b"1002T"), str(b"1003T")]:
        
        users = cont.GetUsersId(findTheUser[0][5])
        
        if cont.CheckTheQuestionChecked(quesionID=question[1]) == True:
                
            if str(event.data) in [str(b"1000F"), str(b"1001F"),str(b"1002F"), str(b"1003F")]:

                command=False
                    
                cont.ScoreScope(groupID=findTheUser[0][5], command=command)
                
                score = cont.ShowScore(findTheUser[0][5])
                
                for answer in answers:
                    
                    if answer[3] == 1:
                        
                        text = f"جواب اشتباه بود 🥲❌\n\n جواب درست **{answer[2]}**بود.\n\nامتیاز شما **{score[0][1]}** 🥊 "

                        for user in users[0]:

                            await sendMessage(user=user, option="score", text=text)

                        cont.CheckedQ(quesionID=question[1])   
                        
            elif str(event.data) in [str(b"1000T"), str(b"1001T"),str(b"1002T"), str(b"1003T")]:
    
                cont.CheckedQ(quesionID=question[1])
                
                command=True
                
                cont.ScoreScope(groupID=findTheUser[0][5], command=command)
                
                score = cont.ShowScore(findTheUser[0][5])
                
                for user in users[0]:

                    await sendMessage(user=user, option="score", text=f"جواب شما درست بود ✅🧠\n\nامتیاز شما **-{score[0][1]}-**🍾")
        
        elif cont.CheckTheQuestionChecked(quesionID=question[1]) == False:
                
            await client.send_message(event.chat_id, "شما یک بار جواب این سوال را وارد کردید 😵‍💫👺\n\n لطفا از گزینه های بالا برای سوال دوم اقدام کنید 🔃2️⃣")
        
        if roundSet[0] == "first" and voite == True:
            
            if len(FactCounter) > 3:
                
                FactCounter.clear()
                
                FactCounter.append(1)
                
                FactCounter.append(1)
                
                FactCounter.append(1)
                
            elif len(CountFirstRound) > 2:
                
                CountFirstRound.clear()
                
                CountFirstRound.append(1)
                
                CountFirstRound.append(1)
            
            await Voite(event,CountFirstRound, FactCounter, [2, 3])
            
        elif roundSet[1] == "second" and voite == True:
            
            if len(FactCounter) > 2:
                
                FactCounter.clear()
                
                FactCounter.append(1)
                
                FactCounter.append(1)
                
            elif len(CountFirstRound) > 2:
                
                CountFirstRound.clear()
                
                CountFirstRound.append(1)
                
                CountFirstRound.append(1)
                
            await Voite(event,CountFirstRound, FactCounter, [2, 2])
        
    elif str(event.data) in voitingButtonVal:
        
        user = cont.GetUserByUName(event.sender.id)
        
        if roundSet[2] != "FINAL":
            
            if user[0][4] != "Naato":
                
                if "N" not in str(event.data):
                    
                    if event.sender.id not in listOfVoite:
                    
                        listOfVoite.append(event.sender.id)
                        
                        await event.respond("رای شما ثبت شد ⚠️")
                        
                    else:
                        
                        await event.respond("شما یک بار رای داده اید ⚠️")
                
                elif "N" in str(event.data):
                    
                    if event.sender.id not in listOfVoite:
                    
                        listOfVoite.append(event.sender.id)
                        
                        await event.respond("رای شما ثبت شد ⚠️")
                        
                        cont.points(int(event.sender.id))
                        
                    else:
                        
                        await event.respond("شما یک بار رای داده اید ⚠️")
                
            elif user[0][4] == "Naato":

                try:
                    
                    if len(terminate) == 0:
                        
                        if cont.Terminator(int(event.data)) == True:
                            
                            terminate.append(1)
                        
                            userT = cont.GetUserByUName(int(event.data)) 
                            
                            await event.respond(f"شما {userT[0][1]} از بازی حذف کردید. 👹")
                            
                            users = cont.GetUsersId(userT[0][5])
                            
                            Narrator = users[0][0]
                            
                            await sendMessage(user=Narrator, option="notice", text=f"{userT[0][1]} حذف شد 💀")
                            
                    else:
                        
                        await event.respond("شما یکی رو حذف کردید دیگه راه نداره.")
                    
                except ValueError as err:
                    
                    await event.respond(f"قاعدتا خودت رو نمیتونی حظف کنی 😶‍🌫️🤣")
                    
        elif roundSet[2] == "FINAL":
            
            if user[0][4] != "Naato":
                
                if "N" not in str(event.data):
                    
                    if event.sender.id not in listOfVoite:
                    
                        listOfVoite.append(event.sender.id)
                        
                        await event.respond("رای شما ثبت شد ⚠️")
                        
                    else:
                        
                        await event.respond("شما یک بار رای داده اید ⚠️")
                
                elif "N" in str(event.data):
                    
                    if event.sender.id not in listOfVoite:
                    
                        listOfVoite.append(event.sender.id)
                        
                        Trust.append(event.sender.id)
                        
                        await event.respond("رای شما ثبت شد ⚠️")
                        
                        cont.points(int(event.sender.id))
                        
                    else:
                        
                        await event.respond("شما یک بار رای داده اید ⚠️")
                
            elif user[0][4] == "Naato":

                await client.send_message(int(user[0][2]),"شما دیگه نمیتونی کاری بکنی ❌")
        
        userT = cont.GetUserByUName(int(event.sender.id)) 
        
        users = cont.GetUsersId(userT[0][5])
        
        if len(listOfVoite) == 2:
        
            if len(Trust) == 2:
                
                for user in users[0]:
                    
                    if user[4] == "Naato":
                        
                        await sendMessage(user=user, option="UserWin", text="و این که شما ........\n\nباختید 🥲👹")
                    
                    else:
                        
                        await sendMessage(user=user, option="UserWin", text="و این که شما ........\n\nبرنده شدید ✌️🍾")
                    
                end = cont.EndTheGame(groupID=userT[0][5])
                
                for points in end:
                    
                    await sendMessage(user=points, option="ShowPoints", text=f"مجموعه امتیازات شما در این بازی {points[3]} میباشد.")
                    
            elif len(Trust) < 2:
                
                for user in users[0]:
                    
                    if user[4] == "Naato":
                        
                        await sendMessage(user=user, option="UserWin", text="و این که شما ........\n\nبرنده شدید ✌️🍾")

                    else:
                        
                        await sendMessage(user=user, option="UserWin", text="و این که شما ........\n\nباختید 🥲👹")
                    
                end = cont.EndTheGame(groupID=userT[0][5], Naato="Naato")
                
                for points in end:
                    
                    await sendMessage(user=points, option="ShowPoints", text=f"مجموعه امتیازات شما در این بازی ***{points[3]}*** میباشد.")

    elif event.data == b"20":
        
        user = cont.GetUserByUName(event.sender.id)
        
        users = cont.GetUsersId(user[0][5])
        
        if len(users[0]) == 4:
            
            await Voite(event, CountFirstRound, FactCounter, [1, 1])
            
        else:
            
            await client.send_message(event.chat_id, "هنوز وقتش نشده.")
    
client.start()

client.run_until_disconnected()