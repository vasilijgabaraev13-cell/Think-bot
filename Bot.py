import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import time

TOKEN = "vk1.a.E5qKhkZER6KRpNPf6wl2t7m2gQ04eRn7laKlfVypRuOAmkaXbwFK3qQ7ZRVbci2FGt7ygjxQl_xsuVWfzv2GIH2ZVwwzmR1qFFR7fhLJSXmJSKiofTsFuffeud8ZrhVB3zvQMvezLxoVPa2May5DO17vTTV7tYt7-3uT9FXTi3YM1oWP-xl4djqrzS6hSmgapYGRCxa5Uk9NRJKu-upSPQ"
GROUP_ID = 239509472

active_chats = []

def is_admin(peer_id, user_id, vk):
    try:
        chat = vk.messages.getConversationMembers(peer_id=peer_id)
        for member in chat['items']:
            if member['member_id'] == user_id:
                if member.get('is_admin', False) or member.get('is_owner', False):
                    return True
        return False
    except:
        return False

while True:
    try:
        vk_session = vk_api.VkApi(token=TOKEN)
        vk = vk_session.get_api()
        longpoll = VkBotLongPoll(vk_session, GROUP_ID)
        
        print("✅ Бот запущен!")
        
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.object.message
                user_id = msg['from_id']
                text = msg['text'].lower()
                peer_id = msg['peer_id']
                is_chat = peer_id > 2000000000
                
                if text == "/start":
                    if is_chat:
                        if is_admin(peer_id, user_id, vk):
                            if peer_id not in active_chats:
                                active_chats.append(peer_id)
                                vk.messages.send(
                                    peer_id=peer_id,
                                    message="✅ Бот активирован",
                                    random_id=0
                                )
                            else:
                                vk.messages.send(
                                    peer_id=peer_id,
                                    message="✅ Бот уже активирован",
                                    random_id=0
                                )
                        else:
                            vk.messages.send(
                                peer_id=peer_id,
                                message="❌ Нет прав",
                                random_id=0
                            )
                    else:
                        vk.messages.send(
                            user_id=user_id,
                            message="Напиши /start в беседе",
                            random_id=0
                        )
                        
    except Exception as e:
        print(f"Ошибка: {e}, переподключение через 5 сек...")
        time.sleep(5)            
import time

bot_start_time = time.time()

async def get_bot_stats():
    """Собирает статистику бота (пинг, ядро, аптайм)"""
    # Пинг VK API
    api_start = time.time()
    try:
        await vk_call("users.get", {"user_ids": [1]})
        api_ms = round((time.time() - api_start) * 1000)
    except:
        api_ms = None
    
    # Скорость ядра
    core_start = time.time()
    _ = sum(range(10000))
    core_ms = round((time.time() - core_start) * 1000, 2)
    
    # Аптайм
    uptime = int(time.time() - bot_start_time)
    h, m, s = uptime // 3600, (uptime % 3600) // 60, uptime % 60
    
    # Статус API
    if api_ms is None:
        api_emoji, api_text = "🔴", "Offline"
    elif api_ms < 200:
        api_emoji, api_text = "🟢", "Excellent"
    elif api_ms < 500:
        api_emoji, api_text = "🟡", "Slight load"
    elif api_ms < 1000:
        api_emoji, api_text = "🟠", "High load"
    else:
        api_emoji, api_text = "🔴", "Critical"
    
    return {
        'api_ms': api_ms,
        'core_ms': core_ms,
        'uptime': (h, m, s),
        'api_emoji': api_emoji,
        'api_text': api_text
    }


@bot.on.message(command=["botstatus", "ping", "status"])
async def bot_status_cmd(msg):
    """Диагностика бота GORDAN CORE"""
    try:
        stats = await get_bot_stats()
        
        h, m, s = stats['uptime']
        if h > 0:
            uptime_str = f"{h}ч {m}м {s}с"
        elif m > 0:
            uptime_str = f"{m}м {s}с"
        else:
            uptime_str = f"{s}с"
        
        session_id = hex(int(time.time() * 1000) % 0xFFFFFFFF)[2:]
        
        text = (
            f"📡 GORDAN CORE diagnostics — TIME FULL\n"
            f"╭──────────────────────╮\n"
            f"│ {stats['api_emoji']} {stats['api_text']}\n"
            f"│ VK API: {stats['api_ms']} ms\n"
            f"│ Core: {stats['core_ms']} ms\n"
            f"│ Uptime: {uptime_str}\n"
            f"│ Session: {session_id}\n"
            f"╰──────────────────────╯\n"
            f"Префиксы: . / ! | /help"
        )
        
        await msg.reply(text)
        
    except Exception as e:
        await msg.reply(
            f"📡 GORDAN CORE diagnostics — ERROR\n"
            f"╭──────────────────────╮\n"
            f"│ 🔴 API: Offline\n"
            f"│ Error: {str(e)[:40]}\n"
            f"╰──────────────────────╯"
        )


@bot.on.message(command="status2")
async def bot_status_alt_cmd(msg):
    """Диагностика бота (компактный формат)"""
    try:
        stats = await get_bot_stats()
        h, m, s = stats['uptime']
        
        text = (
            f"{stats['api_emoji']} GORDAN CORE • {stats['api_text']}\n"
            f"├─ VK API: {stats['api_ms']}ms\n"
            f"├─ Core: {stats['core_ms']}ms\n"
            f"├─ Uptime: {h}ч {m}м {s}с\n"
            f"└─ /botstatus • /ping"
        )
        
        await msg.reply(text)
        
    except Exception as e:
        await msg.reply(f"🔴 GORDAN CORE • Offline\n└─ {str(e)[:50]}")
