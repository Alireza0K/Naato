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
    
    print(f"user-ID -> {User.id} username -> {User.username}")

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
    
async def sendMessageToAll(userID,text, nickname = None):
    
    if nickname == None or nickname == "":
    
        await client.send_message(userID, text)
        
    elif nickname == "narrator":
        
        await client.send_message(userID, "تبریک میگم تمام اعضای تیم شما تکمیل شد و منتظر شما هستن تا بازی رو شروع کنید.✌️🔥\n\nشما راوی داستان هستید🥳\n\nلطفا به خوبی بازی رو روایت کنید 🎃")

@client.on(events.CallbackQuery())
async def callback(event):
    if event.data == b'1':
    
        await event.respond("شما روی دوکمه اول کلیک کردید")
        
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
            
            print(User.username)
                
            groupinfo = cont.GetGroupInformation(event.message.message)
                
            if groupinfo != None:
                    
                groupName = groupinfo[0][0][2]
                
                groupID = groupinfo[0][0][1]
                    
                print(groupID)
                
                regesterTheUser = cont.GetUserInformation(event.message.message, name = User.first_name, username = User.username)
                    
                if regesterTheUser:
                    
                    await event.respond(f"شما با موافقیت عضو گروه {groupName}")
                
                usersinfo = cont.GetUsersId(groupID)
                
                users = usersinfo[0]
                
                usersCount = usersinfo[1]
                
                if usersCount == 6:
                    
                    check = cont.ChooseNarrator(groupID) 
        
                    for user in users:
                        
                        await sendMessageToAll(user[2], "گروه شما تکمیل شد.✌️\n\n راوی بازی انتخاب شده و بازی آغاز میشه.🔥",user[4])
                    
client.start()

client.run_until_disconnected()