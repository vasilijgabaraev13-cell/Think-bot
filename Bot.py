import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import time
import json
import os
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

def get_main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button("💼 Пассивный доход", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("🏙️ Город", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("👤 Профиль", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("⛏️ Майнинг", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("📢 Промо", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("🏆 Топ", color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("🎁 Бонус", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("👥 Кланы", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("📋 Задания", color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("📦 Боксы", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("🏅 Достижения", color=VkKeyboardColor.SECONDARY)
    keyboard.add_button("🏆 Трофеи", color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("💰 Донат", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("❓ Помощь", color=VkKeyboardColor.PRIMARY)
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
                            f"💰 {profile.get('cash', 0):,}$\n"
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
                
                # ===== РЕГИСТРАЦИЯ =====
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
                
                # ===== ПРОФИЛЬ =====
                if text in ["👤 профиль", "/профиль"]:
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
                        f"💰 {profile.get('cash', 0):,}$\n"
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
                
                # ===== ПАССИВНЫЙ ДОХОД (НОВАЯ ФУНКЦИЯ) =====
                if text in ["💼 пассивный доход", "/пассивный_доход"]:
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
                    
                    # Базовая сумма дохода
                    base_income = 10000
                    
                    # Бонус за роль
                    role_bonus = {
                        "владелец": 50000,
                        "руководитель": 35000,
                        "специальный администратор": 25000,
                        "админ бота": 20000,
                        "модератор бота": 15000,
                        "игрок": 0
                    }
                    bonus = role_bonus.get(role, 0)
                    
                    # Бонус за уровень (каждый уровень +1000$)
                    level_bonus = profile.get('level', 1) * 1000
                    
                    # Итоговый доход
                    total_income = base_income + bonus + level_bonus
                    
                    # Начисляем на счёт
                    profiles[str(user_id)]['cash'] = profiles[str(user_id)].get('cash', 0) + total_income
                    save_profiles(profiles)
                    
                    response = (
                        f"✅ Ваш пассивный доход: {total_income:,}$\n"
                        f"\n"
                        f"📊 Детали:\n"
                        f"├─ База: {base_income:,}$\n"
                        f"├─ Бонус за роль ({role}): +{bonus:,}$\n"
                        f"├─ Бонус за уровень ({profile.get('level', 1)}): +{level_bonus:,}$\n"
                        f"└─ Итого: {total_income:,}$"
                    )
                    
                    if role in ["модератор бота", "админ бота", "специальный администратор", "руководитель", "владелец"]:
                        response += f"\n\n💡 Доход для работников Карл Бот - {bonus + 20000:,}$"
                    
                    keyboard = get_main_keyboard()
                    vk.messages.send(
                        user_id=user_id,
                        message=response,
                        random_id=0,
                        keyboard=keyboard.get_keyboard()
                    )
                    continue
                
                # ===== ПОМОЩЬ =====
                if text in ["❓ помощь", "/помощь", "/help"]:
                    response = (
                        "❓ ПОМОЩЬ\n"
                        "╭──────────────────────╮\n"
                        "│ 👤 Профиль — ваш профиль\n"
                        "│ 💼 Пассивный доход — получить доход\n"
                        "│ 📋 /команды — список команд\n"
                        "│ 💼 Пассивный доход — в разработке\n"
                        "│ ⛏️ Майнинг — в разработке\n"
                        "│ 🏙️ Город — в разработке\n"
                        "│ 📢 Промо — в разработке\n"
                        "│ 🏆 Топ — в разработке\n"
                        "│ 🎁 Бонус — в разработке\n"
                        "│ 👥 Кланы — в разработке\n"
                        "│ 📋 Задания — в разработке\n"
                        "│ 📦 Боксы — в разработке\n"
                        "│ 🏅 Достижения — в разработке\n"
                        "│ 🏆 Трофеи — в разработке\n"
                        "│ 💰 Донат — в разработке\n"
                        "╰──────────────────────╯"
                    )
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # ===== ВСЕ ОСТАЛЬНЫЕ КНОПКИ =====
                if text in [
                    "🏙️ город", "⛏️ майнинг",
                    "📢 промо", "🏆 топ", "🎁 бонус", "👥 кланы",
                    "📋 задания", "📦 боксы", "🏅 достижения",
                    "🏆 трофеи", "💰 донат"
                ]:
                    response = f"🔧 Функция '{text}' в разработке!\nСледите за обновлениями бота."
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                # ===== КОМАНДЫ =====
                if text == "/start":
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message="👋 Добро пожаловать!\nИспользуйте кнопки меню для навигации.", random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                if text in ["/команды", "📋 команды"]:
                    response = (
                        "📋 ДОСТУПНЫЕ КОМАНДЫ\n"
                        "╭──────────────────────╮\n"
                        "│ 👤 Профиль — ваш профиль\n"
                        "│ 💼 Пассивный доход — получить доход\n"
                        "│ ❓ Помощь — справка\n"
                        "│ /роли — список ролей\n"
                        "│ /staff — список сотрудников\n"
                        "│ /ping — диагностика\n"
                        "╰──────────────────────╯"
                    )
                    keyboard = get_main_keyboard()
                    vk.messages.send(user_id=user_id, message=response, random_id=0, keyboard=keyboard.get_keyboard())
                    continue
                
                if text == "/роли":
                    role_list = ""
                    for role, level in sorted(ROLE_HIERARCHY.items(), key=lambda x: -x[1]):
                        role_list += f"👑 {role} — уровень {level}\n"
                    response = f"📋 СПИСОК РОЛЕЙ\n╭──────────────────────╮\n{role_list}╰──────────────────────╯"
                    vk.messages.send(user_id=user_id, message=response, random_id=0)
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
                    vk.messages.send(user_id=user_id, message=response, random_id=0)
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
                    vk.messages.send(user_id=user_id, message=response, random_id=0)
                    continue
                        
    except Exception as e:
        print(f"Ошибка: {e}, переподключение через 5 сек...")
        time.sleep(5)
