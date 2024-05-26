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
            total_level, life_fame = calculate_total_level(member_data)

            # Insertar los datos del aventurero con la fecha actual
            date = datetime.now().strftime("%Y-%m-%d")
            c.execute('''
                INSERT INTO adventurer_data (
                    guild, family_name, gathering, fishing, hunting, cooking, alchemy, 
                    processing, training, trading, farming, sailing, barter, total_level, 
                    life_fame, date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                guild_name, family_name, member_data.get('gathering'), member_data.get('fishing'), 
                member_data.get('hunting'), member_data.get('cooking'), member_data.get('alchemy'), 
                member_data.get('processing'), member_data.get('training'), member_data.get('trading'), 
                member_data.get('farming'), member_data.get('sailing'), member_data.get('barter'), 
                total_level, life_fame, date
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
    for key in member_data:
        if key in lifeskills:
            if member_data[key] == 'N/A':
                return None, None
            parts = str(member_data[key]).split(" ")
            if len(parts) == 2:
                level, number = parts
                curr_lvl_value = level_map.get(level, 0) + int(number)
                total_level += curr_lvl_value
                life_fame += curr_lvl_value * 3 if curr_lvl_value >= 31 else 0
    return total_level, life_fame