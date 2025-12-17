from telethon import TelegramClient, events, Button
from telethon.tl.types import MessageMediaPhoto
import asyncio
import re
import os
from datetime import datetime
API_ID = '32102132'
API_HASH = 'b4838ca023dba3afe0b4787b7e2329ab'
PHONE_NUMBER = '+12708454185'
GROUP_ID = -3434688453
BOT_USERNAME = 'seyed_ali_khamenei_bot'
SESSION_NAME = 'arad_session'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def solve_math_captcha(text):
    """حل مسائل ریاضی ساده"""
    try:
        patterns = [
            r'(\d+)\s*\+\s*(\d+)',  # جمع
            r'(\d+)\s*\*\s*(\d+)',  # ضرب
            r'(\d+)\s*/\s*(\d+)',   # تقسیم
            r'(\d+)\s*-\s*(\d+)',   # تفریق
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                num1, num2 = int(match.group(1)), int(match.group(2))
                if '+' in text:
                    return str(num1 + num2)
                elif '*' in text:
                    return str(num1 * num2)
                elif '/' in text:
                    if num2 != 0:
                        return str(num1 // num2)
                    else:
                        return "0"
                elif '-' in text:
                    return str(num1 - num2)
        return None
    except:
        return None

async def extract_number_from_image(event):
    """استخراج عدد از عکس (OCR ساده)"""
    try:
        if isinstance(event.message.media, MessageMediaPhoto):
            # دانلود عکس
            photo = await event.download_media()
            # اینجا می‌تونی از pytesseract یا API OCR استفاده کنی
            # برای سادگی فعلاً فرض می‌کنیم عدد رو دستی پیدا می‌کنیم
            return None  # فعلاً None برمی‌گردونه
    except:
        return None

async def click_button_with_number(event, target_number):
    """کلیک روی دکمه با عدد مورد نظر"""
    try:
        if hasattr(event.message, 'reply_markup'):
            buttons = event.message.reply_markup.rows
            for row in buttons:
                for button in row.buttons:
                    if button.text and str(target_number) in button.text:
                        await event.click(button)
                        print(f"کلیک شد روی دکمه: {button.text}")
                        return True
        return False
    except Exception as e:
        print(f"خطا در کلیک: {e}")
        return False

@client.on(events.NewMessage(chats=GROUP_ID))
async def handler(event):
    try:
        # چک کن پیام از ربات مورد نظر باشه
        if event.message.from_id and event.message.from_id.user_id:
            sender = await client.get_entity(event.message.from_id.user_id)
            if sender.username == BOT_USERNAME:
                print(f"پیام جدید از {BOT_USERNAME}: {event.message.id}")
                
                # چک کن عکس هست یا نه
                if event.message.photo:
                    print("عکس پیدا شد، در حال پردازش...")
                    number = await extract_number_from_image(event)
                    if number:
                        print(f"عدد پیدا شد: {number}")
                        success = await click_button_with_number(event, number)
                        if success:
                            print("دکمه کلیک شد!")
                        else:
                            print("دکمه پیدا نشد!")
                    else:
                        print("عدد از عکس استخراج نشد!")
                
                # چک کن کپچای ریاضی
                elif event.message.text:
                    math_answer = await solve_math_captcha(event.message.text)
                    if math_answer:
                        print(f"جواب ریاضی: {math_answer}")
                        await event.reply(math_answer)
                        print("جواب ریاضی فرستاده شد!")
                        
    except Exception as e:
        print(f"خطا در پردازش پیام: {e}")

async def main():
    print("شروع لاگین...")
    
    # اتصال
    await client.start(phone=PHONE_NUMBER)
    
    # چک کردن اتصال
    me = await client.get_me()
    print(f"لاگین شد: {me.first_name} ({me.phone})")
    
    # چک کردن گروه
    try:
        group = await client.get_entity(GROUP_ID)
        print(f"گروه پیدا شد: {group.title}")
    except:
        print("ID گروه اشتباهه، از @userinfobot بگیر")
        return
    
    print("ربات شروع به کار کرد! Ctrl+C برای توقف")
    print("پیام‌ها هر دقیقه چک می‌شن...")
    
    # نگه داشتن ربات آنلاین
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:

        print("\nربات متوقف شد!")
