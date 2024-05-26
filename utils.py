from bs4 import BeautifulSoup

def extract_profile_info(html):
    """Extrae los niveles de especialización del HTML proporcionado."""
    soup = BeautifulSoup(html, 'html.parser')
    
    
    # Mapeo de iconos a nombres de habilidades
    spec_mapping = {
        'icn_spec01': 'gathering',
        'icn_spec02': 'fishing',
        'icn_spec03': 'hunting',
        'icn_spec04': 'cooking',
        'icn_spec05': 'alchemy',
        'icn_spec06': 'processing',
        'icn_spec07': 'training',
        'icn_spec08': 'trading',
        'icn_spec09': 'farming',
        'icn_spec10': 'sailing',
        'icn_spec11': 'barter'
    }
    
    # Inicializar los niveles de especialización como 'N/A'
    specs = {name: 'N/A' for name in spec_mapping.values()}
    
    # Extraer todos los niveles de especialización
    for li in soup.select('.character_spec ul li'):
        icon_span = li.find('span', class_='icon_spec')
        level_span = li.find('span', class_='spec_level')
        
        if icon_span and level_span:
            icon_class = next((cls for cls in icon_span['class'] if cls in spec_mapping), None)
            if icon_class:
                spec_name = spec_mapping[icon_class]
                level_text = level_span.get_text(strip=True)
                number_text = level_span.find('em').get_text(strip=True)
                final_level = f"{level_text.replace(number_text, '')} {number_text}"
                specs[spec_name] = final_level
    
    return specs
