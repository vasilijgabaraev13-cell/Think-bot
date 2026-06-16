import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import time
import json
import os
import random
from datetime import datetime

TOKEN = "vk1.a.E5qKhkZER6KRpNPf6wl2t7m2gQ04eRn7laKlfVypRuOAmkaXbwFK3qQ7ZRVbci2FGt7ygjxQl_xsuVWfzv2GIH2ZVwwzmR1qFFR7fhLJSXmJSKiofTsFuffeud8ZrhVB3zvQMvezLxoVPa2May5DO17vTTV7tYt7-3uT9FXTi3YM1oWP-xl4djqrzS6hSmgapYGRCxa5Uk9NRJKu-upSPQ"
GROUP_ID = 239509472

bot_start_time = time.time()

ROLES_FILE = "roles.json"
PROFILES_FILE = "profiles.json"
REGISTERED_FILE = "registered.json"

def load_roles():
    if os.path.exists(ROLES_FILE):
        with open(ROLES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_roles(roles):
    with open(ROLES_FILE, 'w', encoding='utf-8') as f:
        json.dump(roles, f, ensure_ascii=False, indent=2)

def load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)

def load_registered():
    if os.path.exists(REGISTERED_FILE):
        with open(REGISTERED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_registered(registered):
    with open(REGISTERED_FILE, 'w', encoding='utf-8') as f:
        json.dump(registered, f, ensure_ascii=False, indent=2)

ROLE_HIERARCHY = {
    "владелец": 5,
    "руководитель": 4,
    "специальный администратор": 3,
    "админ бота": 2,
    "модератор бота": 1
}

OWNERS = [838435015, 1097630503]

def get_role_level(role):
    return ROLE_HIERARCHY.get(role.lower(), 0)

def get_user_role(user_id, roles):
    return roles.get(str(user_id), "игрок")

def get_id_from_mention(text):
    import re
    match = re.search(r'\[id(\d+)\|', text)
    if match:
        return int(match.group(1))
    return None

def format_number(n):
    return f"{n:,}".replace(",", ".")

def get_main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    # Первая строка
    keyboard.add_button("💰 Деньги", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("📈 Уровень", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("₿ Bitcoin", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    # Вторая строка
    keyboard.add_button("💷 Фунты", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("⛏️ Майнинг", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("👥 Рефералы", color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    # Третья строка
    keyboard.add_button("🏆 Достижения", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("⭐ Репутация", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("🏴 Кланы", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    # Четвёртая строка
    keyboard.add_button("💼 Пассивный доход", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("👤 Профиль", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    # Пятая строка
    keyboard.add_button("❓ Помощь", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("⏪ Назад", color=VkKeyboardColor.SECONDARY)
    return keyboard

def get_registration_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("✅ Регистрация", color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("❓ Помощь", color=VkKeyboardColor.PRIMARY)
    return keyboard

def is_registered(user_id):
    registered = load_registered()
    return str(user_id) in registered

roles = load_roles()
profiles = load_profiles()
registered = load_registered()

for owner_id in OWNERS:
    roles[str(owner_id)] = "владелец"
save_roles(roles)

active_chats = []

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
                
                # ============================================
                # БЕСЕДЫ
                # ============================================
                if is_chat:
                    if text == "/start":
                        if peer_id not in active_chats:
                            active_chats.append(peer_id)
                            vk.messages.send(peer_id=peer_id, message="✅ Бот активирован в этой беседе!", random_id=0)
                        else:
                            vk.messages.send(peer_id=peer_id, message="✅ Конференция уже активна", random_id=0)
                        continue
                    
                    if text == "/профиль":
                        if not is_registered(user_id):
                            vk.messages.send(peer_id=peer_id, message="⚠️ Вы не зарегистрированы! Напишите боту в личные сообщения.", random_id=0)
                            continue
                        
                        if str(user_id) not in profiles:
                            profiles[str(user_id)] = {
                                "nickname": f"User{user_id}",
                                "reg_date": datetime.now().strftime("%d:%m %H:%M %y"),
                                "cash": 100,
                                "donat": 0,
                                "btc": 0,
                                "funt": 0,
                                "level": 1,
                                "exp": 0,
                                "exp_to_next": 10,
                                "reputation": 0,
                                "achievements": 0,
                                "max_achievements": 4598,
                                "notifications": ["Получите пенсию в банке", "Включите майнинг ферму", "Получить пассивный доход"]
                            }
                            save_profiles(profiles)
                        
                        profile = profiles[str(user_id)]
                        role = get_user_role(user_id, roles)
                        
                        try:
                            user_info = vk.users.get(user_ids=user_id)
                            nickname = user_info[0]['first_name'] + " " + user_info[0]['last_name']
                        except:
                            nickname = profile.get('nickname', f"User{user_id}")
                        
                        status_emoji = {
                            "владелец": "👑",
                            "руководитель": "⭐",
                            "специальный администратор": "🔰",
                            "админ бота": "🛡️",
                            "модератор бота": "⚙️",
                            "игрок": "☃️"
                        }.get(role, "☃️")
                        
                        level = profile.get('level', 1)
                        exp = profile.get('exp', 0)
                        exp_to_next = profile.get('exp_to_next', 10)
                        
                        notifications = profile.get('notifications', ["Нет уведомлений"])
                        notif_text = "\n".join([f"• {n}" for n in notifications[:5]])
                        
                        achievements = profile.get('achievements', 0)
                        max_achievements = profile.get('max_achievements', 4598)
                        progress = round(achievements / max_achievements * 100, 1) if max_achievements > 0 else 0
                        
                        response = (
                            f"{status_emoji}  {nickname}\n"
                            f"💰 {format_number(profile.get('cash', 0))}$\n"
                            f"⛏ BTC: {profile.get('btc', 0)}₿\n"
                            f"💷 Фунты: {profile.get('funt', 0)}\n"
                            f"🆙 Уровень: {level} [{exp}/{exp_to_next}]\n"
                            f"👍🏻 Репутация: {profile.get('reputation', 0)}\n"
                            f"🏅 Достижения: {achievements}/{max_achievements} | {progress}%\n"
                            f"🆔 {user_id}\n"
                            f"🔔 Уведомления:\n{notif_text}"
                        )
                        vk.messages.send(peer_id=peer_id, message=response, random_id=0)
                        continue
                    
                    if text == "/роли":
                        role_list = ""
                        for role, level in sorted(ROLE_HIERARCHY.items(), key=lambda x: -x[1]):
                            role_list += f"👑 {role} — уровень {level}\n"
                        response = f"📋 СПИСОК РОЛЕЙ\n╭──────────────────────╮\n{role_list}╰──────────────────────╯"
                        vk.messages.send(peer_id=peer_id, message=response, random_id=0)
                        continue
                    
                    if text == "/staff":
                        staff_list = ""
                        for uid, role in roles.items():
                            try:
                                user_info = vk.users.get(user_ids=uid)
                                name = user_info[0]['first_name'] + " " + user_info[0]['last_name']
                                staff_list += f"{name} — {role}\n"
                            except:
                                staff_list += f"ID{uid} — {role}\n"
                        if staff_list == "":
                            staff_list = "Сотрудников нет"
                        response = f"👥 СОТРУДНИКИ\n╭──────────────────────╮\n{staff_list}╰──────────────────────╯"
                        vk.messages.send(peer_id=peer_id, message=response, random_id=0)
                        continue
                    
                    if text in ["/ping", "/status", "/botstatus"]:
                        try:
                            api_start = time.time()
                            vk.users.get(user_ids=[1])
                            api_ping = round((time.time() - api_start) * 1000)
                            core_start = time.time()
                            _ = [i for i in range(1000)]
                            core_time = round((time.time() - core_start) * 1000, 2)
                            uptime_seconds = int(time.time() - bot_start_time)
                            hours = uptime_seconds // 3600
                            minutes = (uptime_seconds % 3600) // 60
                            seconds = uptime_seconds % 60
                            if hours > 0:
                                uptime_str = f"{hours}ч {minutes}м {seconds}с"
                            elif minutes > 0:
                                uptime_str = f"{minutes}м {seconds}с"
                            else:
                                uptime_str = f"{seconds}с"
                            if api_ping < 200:
                                api_status = "🟢 Отлично"
                            elif api_ping < 500:
                                api_status = "🟡 Средняя нагрузка"
                            elif api_ping < 1000:
                                api_status = "🟠 Высокая нагрузка"
                            else:
                                api_status = "🔴 Критично"
                            session_id = hex(int(time.time() * 1000) % 0xFFFFFFFF)[2:]
                            response = (
                                f"📡 ДИАГНОСТИКА БОТА\n"
                                f"╭──────────────────────╮\n"
                                f"│ {api_status}: {api_ping} мс\n"
                                f"│ VK API: {api_ping} мс\n"
                                f"│ Ядро: {core_time} мс\n"
                                f"│ Uptime: {uptime_str}\n"
                                f"│ Session: {session_id}\n"
                                f"│ Активен в чатах: {len(active_chats)}\n"
                                f"╰──────────────────────╯"
                            )
                        except Exception as e:
                            response = f"🔴 Ошибка: {str(e)[:50]}"
                        vk.messages.send(peer_id=peer_id, message=response, random_id=0)
                        continue
                    
                    # В беседах остальное игнорируем
                    continue
                
                # ============================================
                # ЛИЧНЫЕ СООБЩЕНИЯ
                # ============================================
                
                # Если не зарегистрирован
                if not is_registered(user_id):
                    reg_link = "https://vk.ru/rich_bot11"
                    response = (
                        f"⚠️ Вы не зарегистрированы!\n"
                        f"Для продолжения нажмите кнопку ✅ Регистрация\n"
                        f"или перейдите по ссылке:\n"
                        f"{reg_link}"
                    )
                    keyboard = get_registration_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # ===== КОМАНДА /МЕНЮ =====
                if text == "/меню" or text == "/menu":
                    keyboard = get_main_keyboard()
                    vk.messages.send(
                        user_id=user_id,
                        message="📋 ГЛАВНОЕ МЕНЮ\nВыберите раздел:",
                        random_id=0,
                        keyboard=keyboard.get_keyboard()
                    )
                    continue
                
                # ===== КНОПКА "⏪ Назад" =====
                if text == "⏪ назад":
                    keyboard = get_main_keyboard()
                    vk.messages.send(
                        user_id=user_id,
                        message="📋 ГЛАВНОЕ МЕНЮ\nВыберите раздел:",
                        random_id=0,
                        keyboard=keyboard.get_keyboard()
                    )
                    continue
                
                # ===== КНОПКИ ГЛАВНОГО МЕНЮ =====
                
                # КНОПКА "💰 Деньги" - ТОП ПО ДЕНЬГАМ
                if text == "💰 деньги":
                    top_players = []
                    for uid, profile in profiles.items():
                        cash = profile.get('cash', 0)
                        if cash > 0:
                            top_players.append((uid, cash))
                    
                    top_players.sort(key=lambda x: x[1], reverse=True)
                    top_players = top_players[:10]
                    
                    if not top_players:
                        response = "📊 ТОП ПО ДЕНЬГАМ\n╭──────────────────────╮\n│ Нет игроков\n╰──────────────────────╯"
                    else:
                        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
                        top_list = ""
                        for i, (uid, cash) in enumerate(top_players):
                            try:
                                user_info = vk.users.get(user_ids=uid)
                                name = user_info[0]['first_name'] + " " + user_info[0]['last_name']
                            except:
                                name = f"ID{uid}"
                            emoji = number_emojis[i] if i < 10 else f"{i+1}."
                            top_list += f"{emoji} {name} — {format_number(cash)}$\n"
                        
                        response = (
                            f"📊 ТОП ПО ДЕНЬГАМ\n"
                            f"╭──────────────────────╮\n"
                            f"{top_list}"
                            f"╰──────────────────────╯"
                        )
                    
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "📈 Уровень" - ТОП ПО УРОВНЮ
                if text == "📈 уровень":
                    top_players = []
                    for uid, profile in profiles.items():
                        level = profile.get('level', 1)
                        if level > 0:
                            top_players.append((uid, level))
                    
                    top_players.sort(key=lambda x: x[1], reverse=True)
                    top_players = top_players[:10]
                    
                    if not top_players:
                        response = "📊 ТОП ПО УРОВНЮ\n╭──────────────────────╮\n│ Нет игроков\n╰──────────────────────╯"
                    else:
                        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
                        top_list = ""
                        for i, (uid, level) in enumerate(top_players):
                            try:
                                user_info = vk.users.get(user_ids=uid)
                                name = user_info[0]['first_name'] + " " + user_info[0]['last_name']
                            except:
                                name = f"ID{uid}"
                            emoji = number_emojis[i] if i < 10 else f"{i+1}."
                            top_list += f"{emoji} {name} — {level} уровень\n"
                        
                        response = (
                            f"📊 ТОП ПО УРОВНЮ\n"
                            f"╭──────────────────────╮\n"
                            f"{top_list}"
                            f"╰──────────────────────╯"
                        )
                    
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "₿ Bitcoin" - ТОП ПО BTC
                if text == "₿ bitcoin":
                    top_players = []
                    for uid, profile in profiles.items():
                        btc = profile.get('btc', 0)
                        if btc > 0:
                            top_players.append((uid, btc))
                    
                    top_players.sort(key=lambda x: x[1], reverse=True)
                    top_players = top_players[:10]
                    
                    if not top_players:
                        response = "📊 ТОП ПО BTC\n╭──────────────────────╮\n│ Нет игроков\n╰──────────────────────╯"
                    else:
                        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
                        top_list = ""
                        for i, (uid, btc) in enumerate(top_players):
                            try:
                                user_info = vk.users.get(user_ids=uid)
                                name = user_info[0]['first_name'] + " " + user_info[0]['last_name']
                            except:
                                name = f"ID{uid}"
                            emoji = number_emojis[i] if i < 10 else f"{i+1}."
                            top_list += f"{emoji} {name} — {format_number(btc)}₿\n"
                        
                        response = (
                            f"📊 ТОП ПО BTC\n"
                            f"╭──────────────────────╮\n"
                            f"{top_list}"
                            f"╰──────────────────────╯"
                        )
                    
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "💷 Фунты" - ТОП ПО ФУНТАМ
                if text == "💷 фунты":
                    top_players = []
                    for uid, profile in profiles.items():
                        funt = profile.get('funt', 0)
                        if funt > 0:
                            top_players.append((uid, funt))
                    
                    top_players.sort(key=lambda x: x[1], reverse=True)
                    top_players = top_players[:10]
                    
                    if not top_players:
                        response = "📊 ТОП ПО ФУНТАМ\n╭──────────────────────╮\n│ Нет игроков\n╰──────────────────────╯"
                    else:
                        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
                        top_list = ""
                        for i, (uid, funt) in enumerate(top_players):
                            try:
                                user_info = vk.users.get(user_ids=uid)
                                name = user_info[0]['first_name'] + " " + user_info[0]['last_name']
                            except:
                                name = f"ID{uid}"
                            emoji = number_emojis[i] if i < 10 else f"{i+1}."
                            top_list += f"{emoji} {name} — {format_number(funt)}£\n"
                        
                        response = (
                            f"📊 ТОП ПО ФУНТАМ\n"
                            f"╭──────────────────────╮\n"
                            f"{top_list}"
                            f"╰──────────────────────╯"
                        )
                    
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "⛏️ Майнинг"
                if text == "⛏️ майнинг":
                    response = (
                        "⛏️ МАЙНИНГ\n"
                        "╭──────────────────────╮\n"
                        "│ Функция в разработке\n"
                        "│ Скоро здесь появится\n"
                        "│ майнинг ферма\n"
                        "╰──────────────────────╯"
                    )
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "👥 Рефералы"
                if text == "👥 рефералы":
                    response = (
                        "👥 РЕФЕРАЛЫ\n"
                        "╭──────────────────────╮\n"
                        "│ Функция в разработке\n"
                        "│ Скоро здесь появится\n"
                        "│ реферальная система\n"
                        "╰──────────────────────╯"
                    )
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "🏆 Достижения" - ТОП ПО ДОСТИЖЕНИЯМ
                if text == "🏆 достижения":
                    top_players = []
                    for uid, profile in profiles.items():
                        achievements = profile.get('achievements', 0)
                        if achievements > 0:
                            top_players.append((uid, achievements))
                    
                    top_players.sort(key=lambda x: x[1], reverse=True)
                    top_players = top_players[:10]
                    
                    if not top_players:
                        response = "🏆 ТОП ПО ДОСТИЖЕНИЯМ\n╭──────────────────────╮\n│ Нет игроков\n╰──────────────────────╯"
                    else:
                        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
                        top_list = ""
                        for i, (uid, ach) in enumerate(top_players):
                            try:
                                user_info = vk.users.get(user_ids=uid)
                                name = user_info[0]['first_name'] + " " + user_info[0]['last_name']
                            except:
                                name = f"ID{uid}"
                            emoji = number_emojis[i] if i < 10 else f"{i+1}."
                            top_list += f"{emoji} {name} — {format_number(ach)} достижений\n"
                        
                        response = (
                            f"🏆 ТОП ПО ДОСТИЖЕНИЯМ\n"
                            f"╭──────────────────────╮\n"
                            f"{top_list}"
                            f"╰──────────────────────╯"
                        )
                    
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "⭐ Репутация" - ТОП ПО РЕПУТАЦИИ
                if text == "⭐ репутация":
                    top_players = []
                    for uid, profile in profiles.items():
                        reputation = profile.get('reputation', 0)
                        if reputation > 0:
                            top_players.append((uid, reputation))
                    
                    top_players.sort(key=lambda x: x[1], reverse=True)
                    top_players = top_players[:10]
                    
                    if not top_players:
                        response = "⭐ ТОП ПО РЕПУТАЦИИ\n╭──────────────────────╮\n│ Нет игроков\n╰──────────────────────╯"
                    else:
                        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
                        top_list = ""
                        for i, (uid, rep) in enumerate(top_players):
                            try:
                                user_info = vk.users.get(user_ids=uid)
                                name = user_info[0]['first_name'] + " " + user_info[0]['last_name']
                            except:
                                name = f"ID{uid}"
                            emoji = number_emojis[i] if i < 10 else f"{i+1}."
                            top_list += f"{emoji} {name} — {format_number(rep)} репутации\n"
                        
                        response = (
                            f"⭐ ТОП ПО РЕПУТАЦИИ\n"
                            f"╭──────────────────────╮\n"
                            f"{top_list}"
                            f"╰──────────────────────╯"
                        )
                    
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "🏴 Кланы" - ТОП КЛАНОВ
                if text == "🏴 кланы":
                    clans = [
                        ("[СКР] СПАРТА", 10026),
                        ("[СТВ] SKORLUPA", 5846),
                        ("[РУС] NAKAMURA SQUAD", 4322),
                        ("[MEX] СМЕШАРИКИ", 2853),
                        ("[TNS] TURINASQ", 2833),
                        ("[XDD] THE BLACK SWORDSMAN", 2267),
                        ("[THE] BANK FAMILY", 1789),
                        ("[WOW] NAKAMURA SQUAD", 1558),
                        ("[SSQ] STONE SQUAD", 1092),
                        ("[YKZ] YAKUDZA", 1078)
                    ]
                    
                    number_emojis = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "1⃣0⃣"]
                    clan_list = ""
                    for i, (name, rating) in enumerate(clans):
                        clan_list += f"{number_emojis[i]}{name} — {format_number(rating)}🔱\n"
                    
                    response = (
                        f"🏴 ТОП КЛАНОВ ПО РЕЙТИНГУ\n"
                        f"╭──────────────────────╮\n"
                        f"{clan_list}"
                        f"╰──────────────────────╯"
                    )
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "💼 Пассивный доход"
                if text == "💼 пассивный доход":
                    if not is_registered(user_id):
                        continue
                    
                    if str(user_id) not in profiles:
                        profiles[str(user_id)] = {
                            "nickname": f"User{user_id}",
                            "reg_date": datetime.now().strftime("%d:%m %H:%M %y"),
                            "cash": 0,
                            "donat": 0,
                            "btc": 0,
                            "funt": 0,
                            "level": 1,
                            "exp": 0,
                            "exp_to_next": 10,
                            "reputation": 0,
                            "achievements": 0,
                            "max_achievements": 4598,
                            "notifications": ["Получите пенсию в банке", "Включите майнинг ферму", "Получить пассивный доход"]
                        }
                        save_profiles(profiles)
                    
                    profile = profiles[str(user_id)]
                    role = get_user_role(user_id, roles)
                    
                    base_income = 10000
                    
                    role_bonus = {
                        "владелец": 50000,
                        "руководитель": 35000,
                        "специальный администратор": 25000,
                        "админ бота": 20000,
                        "модератор бота": 15000,
                        "игрок": 0
                    }
                    bonus = role_bonus.get(role, 0)
                    level_bonus = profile.get('level', 1) * 1000
                    total_income = base_income + bonus + level_bonus
                    
                    profiles[str(user_id)]['cash'] = profiles[str(user_id)].get('cash', 0) + total_income
                    save_profiles(profiles)
                    
                    response = (
                        f"✅ Ваш пассивный доход: {format_number(total_income)}$\n"
                        f"\n"
                        f"📊 Детали:\n"
                        f"├─ База: {format_number(base_income)}$\n"
                        f"├─ Бонус за роль ({role}): +{format_number(bonus)}$\n"
                        f"├─ Бонус за уровень ({profile.get('level', 1)}): +{format_number(level_bonus)}$\n"
                        f"└─ Итого: {format_number(total_income)}$"
                    )
                    
                    if role in ["модератор бота", "админ бота", "специальный администратор", "руководитель", "владелец"]:
                        response += f"\n\n💡 Доход для работников Карл Бот - {format_number(bonus + 20000)}$"
                    
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "👤 Профиль"
                if text == "👤 профиль":
                    if str(user_id) not in profiles:
                        profiles[str(user_id)] = {
                            "nickname": f"User{user_id}",
                            "reg_date": datetime.now().strftime("%d:%m %H:%M %y"),
                            "cash": 100,
                            "donat": 0,
                            "btc": 0,
                            "funt": 0,
                            "level": 1,
                            "exp": 0,
                            "exp_to_next": 10,
                            "reputation": 0,
                            "achievements": 0,
                            "max_achievements": 4598,
                            "notifications": ["Получите пенсию в банке", "Включите майнинг ферму", "Получить пассивный доход"]
                        }
                        save_profiles(profiles)
                    
                    profile = profiles[str(user_id)]
                    role = get_user_role(user_id, roles)
                    
                    try:
                        user_info = vk.users.get(user_ids=user_id)
                        nickname = user_info[0]['first_name'] + " " + user_info[0]['last_name']
                    except:
                        nickname = profile.get('nickname', f"User{user_id}")
                    
                    status_emoji = {
                        "владелец": "👑",
                        "руководитель": "⭐",
                        "специальный администратор": "🔰",
                        "админ бота": "🛡️",
                        "модератор бота": "⚙️",
                        "игрок": "☃️"
                    }.get(role, "☃️")
                    
                    level = profile.get('level', 1)
                    exp = profile.get('exp', 0)
                    exp_to_next = profile.get('exp_to_next', 10)
                    
                    notifications = profile.get('notifications', ["Нет уведомлений"])
                    notif_text = "\n".join([f"• {n}" for n in notifications[:5]])
                    
                    achievements = profile.get('achievements', 0)
                    max_achievements = profile.get('max_achievements', 4598)
                    progress = round(achievements / max_achievements * 100, 1) if max_achievements > 0 else 0
                    
                    response = (
                        f"{status_emoji}  {nickname}\n"
                        f"💰 {format_number(profile.get('cash', 0))}$\n"
                        f"⛏ BTC: {profile.get('btc', 0)}₿\n"
                        f"💷 Фунты: {profile.get('funt', 0)}\n"
                        f"🆙 Уровень: {level} [{exp}/{exp_to_next}]\n"
                        f"👍🏻 Репутация: {profile.get('reputation', 0)}\n"
                        f"🏅 Достижения: {achievements}/{max_achievements} | {progress}%\n"
                        f"🆔 {user_id}\n"
                        f"🔔 Уведомления:\n{notif_text}"
                    )
                    
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # КНОПКА "❓ Помощь"
                if text == "❓ помощь":
                    response = (
                        "❓ ПОМОЩЬ\n"
                        "╭──────────────────────╮\n"
                        "│ 👤 Профиль — ваш профиль\n"
                        "│ 💼 Пассивный доход — получить доход\n"
                        "│ 🎁 Бонус — получить бонус\n"
                        "│ 📊 Топ баланс — топ игроков\n"
                        "│ 📋 /команды — список команд\n"
                        "│ ⛏️ Майнинг — в разработке\n"
                        "│ 🏆 Достижения — в разработке\n"
                        "│ ⭐ Репутация — в разработке\n"
                        "│ 🏴 Кланы — в разработке\n"
                        "╰──────────────────────╯"
                    )
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # ===== ОСТАЛЬНЫЕ КОМАНДЫ =====
                
                # Регистрация
                if text == "✅ регистрация":
                    if not is_registered(user_id):
                        if str(user_id) not in profiles:
                            profiles[str(user_id)] = {
                                "nickname": f"User{user_id}",
                                "reg_date": datetime.now().strftime("%d:%m %H:%M %y"),
                                "cash": 100,
                                "donat": 0,
                                "btc": 0,
                                "funt": 0,
                                "level": 1,
                                "exp": 0,
                                "exp_to_next": 10,
                                "reputation": 0,
                                "achievements": 0,
                                "max_achievements": 4598,
                                "notifications": ["Получите пенсию в банке", "Включите майнинг ферму", "Получить пассивный доход"]
                            }
                            save_profiles(profiles)
                        
                        registered[str(user_id)] = {"registered_at": datetime.now().strftime("%d:%m %H:%M %y"), "active": True}
                        save_registered(registered)
                        
                        response = "✅ Регистрация завершена!\n👋 Добро пожаловать!\n💰 Вам начислено 100$ стартового капитала"
                        keyboard = get_main_keyboard()
                        vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    else:
                        keyboard = get_main_keyboard()
                        vk.messages.send(user_id=user_id, message="✅ Вы уже зарегистрированы!", random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # /start
                if text == "/start":
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message="👋 Добро пожаловать!\nИспользуйте кнопки меню для навигации.", random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # /команды
                if text in ["/команды", "📋 команды"]:
                    response = (
                        "📋 ДОСТУПНЫЕ КОМАНДЫ\n"
                        "╭──────────────────────╮\n"
                        "│ 👤 Профиль — ваш профиль\n"
                        "│ 💼 Пассивный доход — получить доход\n"
                        "│ 🎁 Бонус — получить бонус\n"
                        "│ ❓ Помощь — справка\n"
                        "│ 📊 Топ баланс — топ игроков\n"
                        "│ /роли — список ролей\n"
                        "│ /staff — список сотрудников\n"
                        "│ /setstaff — выдать роль\n"
                        "│ /ping — диагностика\n"
                        "│ /меню — главное меню\n"
                        "╰──────────────────────╯"
                    )
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # /роли
                if text == "/роли":
                    role_list = ""
                    for role, level in sorted(ROLE_HIERARCHY.items(), key=lambda x: -x[1]):
                        role_list += f"👑 {role} — уровень {level}\n"
                    response = f"📋 СПИСОК РОЛЕЙ\n╭──────────────────────╮\n{role_list}╰──────────────────────╯"
                    vk.messages.send(user_id=user_id, message=response, random_id=0)
                    continue
                
                # /staff
                if text == "/staff":
                    staff_list = ""
                    for uid, role in roles.items():
                        try:
                            user_info = vk.users.get(user_ids=uid)
                            name = user_info[0]['first_name'] + " " + user_info[0]['last_name']
                            staff_list += f"{name} — {role}\n"
                        except:
                            staff_list += f"ID{uid} — {role}\n"
                    if staff_list == "":
                        staff_list = "Сотрудников нет"
                    response = f"👥 СОТРУДНИКИ\n╭──────────────────────╮\n{staff_list}╰──────────────────────╯"
                    vk.messages.send(user_id=user_id, message=response, random_id=0)
                    continue
                
                # /setstaff
                if text.startswith("/setstaff"):
                    user_role = get_user_role(user_id, roles)
                    
                    if get_role_level(user_role) < 4:
                        vk.messages.send(
                            user_id=user_id,
                            message="❌ У вас нет прав для выдачи ролей",
                            random_id=0
                        )
                        continue
                    
                    parts = text.split()
                    if len(parts) < 3:
                        vk.messages.send(
                            user_id=user_id,
                            message="❌ Использование: /setstaff [@пользователь] [название_роли]\n\nДоступные роли:\nруководитель\nспециальный администратор\nадмин бота\nмодератор бота",
                            random_id=0
                        )
                        continue
                    
                    target_id = get_id_from_mention(msg['text'])
                    if not target_id:
                        vk.messages.send(
                            user_id=user_id,
                            message="❌ Упомяните пользователя (@)",
                            random_id=0
                        )
                        continue
                    
                    role_name = ' '.join(parts[2:]).lower()
                    
                    if role_name not in ROLE_HIERARCHY:
                        vk.messages.send(
                            user_id=user_id,
                            message="❌ Неверное название роли\n\nДоступные:\nруководитель\nспециальный администратор\nадмин бота\nмодератор бота",
                            random_id=0
                        )
                        continue
                    
                    if get_role_level(user_role) <= get_role_level(role_name):
                        vk.messages.send(
                            user_id=user_id,
                            message="❌ Вы не можете выдать роль выше или равную вашей",
                            random_id=0
                        )
                        continue
                    
                    roles[str(target_id)] = role_name
                    save_roles(roles)
                    
                    try:
                        target_info = vk.users.get(user_ids=target_id)
                        target_name = target_info[0]['first_name'] + " " + target_info[0]['last_name']
                    except:
                        target_name = f"ID{target_id}"
                    
                    vk.messages.send(
                        user_id=user_id,
                        message=f"✅ Пользователю {target_name} выдана роль {role_name}",
                        random_id=0
                    )
                    continue
                
                # /ping
                if text in ["/ping", "/status", "/botstatus"]:
                    try:
                        api_start = time.time()
                        vk.users.get(user_ids=[1])
                        api_ping = round((time.time() - api_start) * 1000)
                        core_start = time.time()
                        _ = [i for i in range(1000)]
                        core_time = round((time.time() - core_start) * 1000, 2)
                        uptime_seconds = int(time.time() - bot_start_time)
                        hours = uptime_seconds // 3600
                        minutes = (uptime_seconds % 3600) // 60
                        seconds = uptime_seconds % 60
                        if hours > 0:
                            uptime_str = f"{hours}ч {minutes}м {seconds}с"
                        elif minutes > 0:
                            uptime_str = f"{minutes}м {seconds}с"
                        else:
                            uptime_str = f"{seconds}с"
                        if api_ping < 200:
                            api_status = "🟢 Отлично"
                        elif api_ping < 500:
                            api_status = "🟡 Средняя нагрузка"
                        elif api_ping < 1000:
                            api_status = "🟠 Высокая нагрузка"
                        else:
                            api_status = "🔴 Критично"
                        session_id = hex(int(time.time() * 1000) % 0xFFFFFFFF)[2:]
                        response = (
                            f"📡 ДИАГНОСТИКА БОТА\n"
                            f"╭──────────────────────╮\n"
                            f"│ {api_status}: {api_ping} мс\n"
                            f"│ VK API: {api_ping} мс\n"
                            f"│ Ядро: {core_time} мс\n"
                            f"│ Uptime: {uptime_str}\n"
                            f"│ Session: {session_id}\n"
                            f"│ Активен в чатах: {len(active_chats)}\n"
                            f"╰──────────────────────╯"
                        )
                    except Exception as e:
                        response = f"🔴 Ошибка: {str(e)[:50]}"
                    vk.messages.send(user_id=user_id, message=response, random_id=0)
                    continue
                        
    except Exception as e:
        print(f"Ошибка: {e}, переподключение через 5 сек...")
        time.sleep(5)
