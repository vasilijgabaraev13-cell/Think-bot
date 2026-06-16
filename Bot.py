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
                                    message="✅ Конференция уже активна",
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
                
                elif text == "/ping":
                    api_start = time.time()
                    try:
                        vk.users.get(user_ids=[1])
                        api_ping = round((time.time() - api_start) * 1000)
                        
                        core_start = time.time()
                        _ = [i for i in range(10000)]
                        core_time = round((time.time() - core_start) * 1000, 2)
                        
                        if api_ping < 200:
                            api_emoji = "🟢"
                            status_text = "Стабильно"
                        elif api_ping < 500:
                            api_emoji = "🟡"
                            status_text = "Нагрузка"
                        elif api_ping < 1000:
                            api_emoji = "🟠"
                            status_text = "Задержка"
                        else:
                            api_emoji = "🔴"
                            status_text = "Лаги"
                        
                        text = (
                            f"{api_emoji} СТАТУС БОТА • {status_text}\n"
                            f"├─ VK API: {api_ping} мс\n"
                            f"├─ Ядро: {core_time} мс\n"
                            f"├─ Активен в чатах: {len(active_chats)}\n"
                            f"└─ /start — активация бота"
                        )
                    except Exception as e:
                        text = f"🔴 ОШИБКА • {str(e)[:40]}"
                    
                    if is_chat:
                        if peer_id in active_chats:
                            vk.messages.send(peer_id=peer_id, message=text, random_id=0)
                    else:
                        vk.messages.send(user_id=user_id, message=text, random_id=0)
                        
    except Exception as e:
        print(f"Ошибка: {e}, переподключение через 5 сек...")
        time.sleep(5)
