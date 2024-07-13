from telethon.sync import TelegramClient, events, Button
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

@client.on(events.NewMessage(pattern="/start"))
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
    
@client.on(events.NewMessage(pattern="/F"))
async def F(event):
    
    user = event.sender.username
        
    user = cont.GetUserByUName(user)
    
    check = cont.checkQ(user[0][5])
    
    print(check)
    
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
            
    else:
        
        await event.respond("⚠️هنوز راوی سوالات رو وارد نکرده\n\nیکم صبر کن.🙏🏻")
                        
async def sendMessageToAll(users):
    
    for user in users:
    
        if user[4] == None or user[4] != "narrator":
        
            await client.send_message(user[2], "تمام اعضای تیم جمع شدن و الان میخوایم بازی رو شروع کنی.😎\n\nحالا شما قراره که fact های خودتون رو به شکل زیر وارد کنید:\n```/F\nفکت اول\nفکت دوم\nفکت سوم\nفکت چهارم\nفکت پنجم```\nخوب فکت وارد کنی ها😁", parse_mode="markdown")
            
        elif user[4] == "narrator":
            
            keyboard= [
                [
                    Button.inline("وارد کردن سوال ها.", b"10")
                ]
            ]
            
            global nickname
            
            global groupID
            
            nickname = user[4]
            
            groupID = user[5]
            
            await client.send_message(user[2], "تبریک میگم تمام اعضای تیم شما تکمیل شد و منتظر شما هستن تا بازی رو شروع کنید.✌️🔥\n\nشما راوی داستان هستید🥳\n\nلطفا به خوبی بازی رو روایت کنید 🎃",buttons=keyboard)
            
        elif user[4] == "Naato":
            
            await client.send_message(user[2], "شما ناتو این بازی هستید.🎭")

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
        
        regesterTheUser = cont.GetUserInformation(id[0], name = User.first_name, username = User.username)
        
        if regesterTheUser[1] == False:
            
            await client.send_message(event.chat_id, message=f"سلامی دوباره به تو جذاب 😍😎\n\nخیلی خوشحالیم که دوباره تورو توی بازی جذابمون میبینیم.\n\nامیدوارم که قوانین رو یادت مونده باشه😁\n\nایینم لینک گروه جدید برای تو و دوستات.\n\n`{id[0]}`\nاسم گروه:{id[1]}", parse_mode="markdown")
        
        elif regesterTheUser[1] == True:
            
            await client.send_message(event.chat_id, message=f"خیلی هم عالی حالا شما عضو گروه `{id[1]}` شدید \n\nآیدی گروه رو برای پنج تا دیگه از دوست هات هم بفرست تا باهم بازی کنید 🔥🎮\n\nاین آیدی گروه شماست: `{id[0]}`", parse_mode="markdown")
        
    elif event.data == b"9":
        
        await event.respond("آیدی گروه خودتون رو وارد کنید:")
        
        @client.on(events.NewMessage)
        async def handler(event):
            
            User = event.sender
                
            groupinfo = cont.GetGroupInformation(event.message.message)
                
            if groupinfo != None:
                    
                groupName = groupinfo[0][0][2]
                
                groupID = groupinfo[0][0][1]
                
                regesterTheUser = cont.GetUserInformation(event.message.message, name = User.first_name, username = User.username)
                    
                if regesterTheUser:
                    
                    await event.respond(f"شما با موافقیت عضو گروه {groupName}")
                
                usersinfo = cont.GetUsersId(groupID)
                
                users = usersinfo[0]
                
                usersCount = usersinfo[1]
                
                if usersCount == 3:
                    
                    check = cont.ChooseNarrator(groupID) 
                    
                    if check:
                        
                        naato = cont.ChooseNaato(groupID)
                        
                        await sendMessageToAll(users)
                        
    elif event.data == b"10":
        
        await event.respond("سوال هارا دونه به دونه با `/Q` وارد کنید:")
        
        @client.on(events.NewMessage(pattern="/Q"))
        async def Q(event):
            
            question = str(event.message.message)
            
            question = question.replace("/Q", "")
            
            questions = cont.QandANarator(userNickName=nickname, groupID=groupID, Q=[question], A="Test magic")
            
            if questions[0]:
                
                await client.send_message(event.chat_id, 
                                          "**سوال شما ثبت شد🔥**\n\n طبق فرمول زیر جواب هارا لحاظ کنید:\n ```/A\nجواب اول\nجواب دوم\nجواب سوم\nجواب چهارم = 1``` \nجواب درست را با `جواب = 1` نشان میدهیم",
                                          parse_mode="markdown")
            
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

                switchB = [
                        [
                        Button.inline("این جواب غلطه!", b"0"),
                        Button.inline("این جواب درسته!", b"12")
                        ]
                    ]
                
                for answer in answers:
                    
                    print(answer)
                    
                    if len(answer) == 2:
                        
                        applyAnswers = cont.AnswersNarrator(question_Hash=questions[1], answers=answer[0], check=1)
                        
                    elif len(answer) == 1:
                        
                        applyAnswers = cont.AnswersNarrator(question_Hash=questions[1], answers=answer[0], check=0)
                        
                if applyAnswers:    
        
                    await event.respond("جواب شما ثبت شد.")
                
                else:
                    
                    await event.respond("چهار جواب شما ثبت شده.")
                    
client.start()

client.run_until_disconnected()