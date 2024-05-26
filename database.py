import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='guild_data.db'):
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS guilds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER,
                family_name TEXT NOT NULL,
                profile_url TEXT NOT NULL,
                FOREIGN KEY (guild_id) REFERENCES guilds(id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS adventurer_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild TEXT,
                family_name TEXT,
                gathering TEXT,
                fishing TEXT,
                hunting TEXT,
                cooking TEXT,
                alchemy TEXT,
                processing TEXT,
                training TEXT,
                trading TEXT,
                farming TEXT,
                sailing TEXT,
                barter TEXT,
                gathering_total_level INTEGER,
                fishing_total_level INTEGER,
                hunting_total_level INTEGER,
                cooking_total_level INTEGER,
                alchemy_total_level INTEGER,
                processing_total_level INTEGER,
                training_total_level INTEGER,
                trading_total_level INTEGER,
                farming_total_level INTEGER,
                sailing_total_level INTEGER,
                barter_total_level INTEGER,
                total_level INTEGER,
                life_fame INTEGER,
                date TEXT,
                FOREIGN KEY (guild) REFERENCES guilds(name),
                FOREIGN KEY (family_name) REFERENCES members(family_name)
            )
        ''')
        conn.commit()
        conn.close()

    def save_guild(self, guild_name, members_data):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Insertar la guild si no existe
        c.execute('SELECT id FROM guilds WHERE name = ?', (guild_name,))
        guild = c.fetchone()
        if guild is None:
            c.execute('INSERT INTO guilds (name) VALUES (?)', (guild_name,))
            guild_id = c.lastrowid
        else:
            guild_id = guild[0]
        
        for family_name, member_data in members_data.items():
            profile_url = member_data.pop('profile_url')
            
            c.execute('''
                SELECT id FROM members WHERE guild_id = ? AND family_name = ?
            ''', (guild_id, family_name))
            member = c.fetchone()
            if member is None:
                c.execute('''
                    INSERT INTO members (guild_id, family_name, profile_url)
                    VALUES (?, ?, ?)
                ''', (guild_id, family_name, profile_url))
                member_id = c.lastrowid
            else:
                member_id = member[0]

            # Calcular total_level y life_fame
            total_level, life_fame, profession_levels = calculate_total_level(member_data)

            # Insertar los datos del aventurero con la fecha actual
            date = datetime.now().strftime("%Y-%m-%d")
            c.execute('''
                INSERT INTO adventurer_data (
                    guild, family_name, gathering, fishing, hunting, cooking, alchemy, 
                    processing, training, trading, farming, sailing, barter,
                    gathering_total_level, fishing_total_level, hunting_total_level, cooking_total_level, 
                    alchemy_total_level, processing_total_level, training_total_level, trading_total_level,
                    farming_total_level, sailing_total_level, barter_total_level,
                    total_level, life_fame, date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                guild_name, family_name, member_data.get('gathering'), member_data.get('fishing'), 
                member_data.get('hunting'), member_data.get('cooking'), member_data.get('alchemy'), 
                member_data.get('processing'), member_data.get('training'), member_data.get('trading'), 
                member_data.get('farming'), member_data.get('sailing'), member_data.get('barter'), 
                profession_levels['gathering'], profession_levels['fishing'], 
                profession_levels['hunting'], profession_levels['cooking'], 
                profession_levels['alchemy'], profession_levels['processing'], 
                profession_levels['training'], profession_levels['trading'], 
                profession_levels['farming'], profession_levels['sailing'], 
                profession_levels['barter'], total_level, life_fame, date
            ))
        
        conn.commit()
        conn.close()

def calculate_total_level(member_data):
    lifeskills = [
        'gathering', 
        'fishing', 
        'hunting', 
        'cooking', 
        'alchemy', 
        'processing', 
        'training', 
        'trading', 
        'farming', 
        'sailing', 
        'barter'
    ]
    level_map = {
        'Beginner': 0,
        'Apprentice': 10,
        'Skilled': 20,
        'Professional': 30,
        'Artisan': 40,
        'Master': 50,
        'Guru': 80
    }
    total_level = 0
    life_fame = 1
    profession_levels = {}

    for key in member_data:
        if key in lifeskills:
            if member_data[key] is None:
                profession_levels[key] = None
                continue
            parts = str(member_data[key]).split(" ")
            if len(parts) == 2:
                level, number = parts
                curr_lvl_value = level_map.get(level, 0) + int(number)
                profession_levels[key] = curr_lvl_value
                total_level += curr_lvl_value
                if curr_lvl_value >= 31:
                    life_fame += calculate_fame_value(curr_lvl_value)
            else:
                profession_levels[key] = None

    return (None, None, profession_levels) if None in profession_levels.values() else (total_level, life_fame, profession_levels)

def calculate_fame_value(level):
    # Fame value calculation based on the level
    if level < 31:
        return 0
    return 93 + (level - 31) * 3