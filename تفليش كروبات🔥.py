from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id = 'هنا الايبي اي مالتك'
api_hash = 'الايبي هاش مالتك هنااا'
token = "توكن بوتككك هناااا"


app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=token)

@app.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("تفليش كروب محدد", callback_data="flash_group")]
    ])
    await message.reply_text("اختار العملية التي تريد تنفيذها", reply_markup=keyboard)

@app.on_callback_query(filters.regex("flash_group"))
async def ask_group_username(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.reply_text(" إرسال معرف الكروب (بدون @)")
    await callback_query.answer()

@app.on_message(filters.text)
async def handle_group_username(client, message):
    user = message.text.strip()
    chat_id = f"@{user}"

    try:
        async for member in app.get_chat_members(chat_id):
            if not member.status in ("administrator", "creator"):
                try:
                    await app.ban_chat_member(chat_id, member.user.id)
                    await app.unban_chat_member(chat_id, member.user.id)
                    await message.reply_text(f"تم حذف العضو: {member.user.username}")
                except Exception as e:
                    print(f"حدث خطأ عند محاولة حذف العضو {member.user.id}: {e}")

        await message.reply_text("تم تفليش الكروب بنجاح!")
    except Exception as e:
        await message.reply_text(f"حدث خطأ: {e}")
        print(f"Error: {e}")

app.run()