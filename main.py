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
            
            print(event.message.message)
            
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
            
            print(event.message.message)
            
            await client.send_message('@Alirez0K', event.message.message)
            
    elif event.data == b"8":
        
        id = cont.Start(0)
        
        await client.send_message(event.chat_id, message=f"خیلی هم عالی حالا شما عضو گروه {id[1]} شدید \n\nآیدی گروه رو برای پنج تا دیگه از دوست هات هم بفرست تا باهم بازی کنید 🔥🎮\n\nاین آیدی گروه شماست: {id[0]}", parse_mode="html")
        
    elif event.data == b"9":
        
        await event.respond("آیدی گروه خودتون رو وارد کنید:")
        
        @client.on(events.NewMessage)
        
        async def handler(event):
            
            print(event.message.message)
        
            cont.Start(1, G = event.message.message)
            
        
client.start()

client.run_until_disconnected()