import sqlite3

def add_columns_and_update_levels(db_name='guild_data.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    professions = [
            'gathering', 'fishing', 'hunting', 'cooking', 'alchemy', 
            'processing', 'training', 'trading', 'farming', 'sailing', 'barter'
        ]
    """# Añadir nuevas columnas
    try:
        professions = [
            'gathering', 'fishing', 'hunting', 'cooking', 'alchemy', 
            'processing', 'training', 'trading', 'farming', 'sailing', 'barter'
        ]
        
        for profession in professions:
            c.execute(f'ALTER TABLE adventurer_data ADD COLUMN {profession}_total_level INTEGER;')
        
        conn.commit()
    except Exception as e:
        print(f"Error al añadir columnas: {e}")"""
    
    # Función para calcular el nivel total de una profesión
    def calculate_profession_level(level_str):
        if level_str == 'N/A':
            return 0
        
        level_map = {
            'Beginner': 0,
            'Apprentice': 10,
            'Skilled': 20,
            'Professional': 30,
            'Artisan': 40,
            'Master': 50,
            'Guru': 80
        }
        
        try:
            level, number = level_str.split()
            number = int(number)
            total_level = level_map[level] + number
            return total_level
        except ValueError:
            return 0
    
    # Actualizar los valores de las columnas
    try:
        c.execute('SELECT id, gathering, fishing, hunting, cooking, alchemy, processing, training, trading, farming, sailing, barter FROM adventurer_data')
        rows = c.fetchall()
        
        for row in rows:
            row_id = row[0]
            update_values = {}
            
            for i, profession in enumerate(professions):
                level_str = row[i + 1]  # Offset by 1 because the first item is the ID
                total_level = calculate_profession_level(level_str)
                update_values[f"{profession}_total_level"] = total_level
            
            # Crear la consulta de actualización dinámica
            set_clause = ", ".join([f"{k} = {v}" for k, v in update_values.items()])
            update_query = f'UPDATE adventurer_data SET {set_clause} WHERE id = {row_id};'
            c.execute(update_query)
        
        conn.commit()
    except Exception as e:
        print(f"Error al actualizar niveles totales: {e}")
    finally:
        conn.close()

# Ejecutar la función
add_columns_and_update_levels()
