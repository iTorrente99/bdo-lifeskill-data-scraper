from scraper import Scraper
from database import Database

guilds_to_scrape = [
    "Clarity",
    "Life",
    "Sisu",
    "Necrotic",
    "Odyllita",
    "Unpredictable",
    "Flex",
    "Cosmic",
    "Demise",
    "Orca",
    "EdgeOfSanity",
    "Hanami",
    "Sparkle",
    "BonumVibe",
    "UPS",
    "Familiar",
    "LifeChills",
    "Asilo",
    "BlueLions",
    "CoffeeClub",
    "DragonSouls",
    "BackseatGaming",
    "WitchBlade",
    "Zirine",
    "Night_Shade",
    "Contempt",
    "Astreliane",
    "BurningDestiny",
    "StrangerThings",
    "NoGearNoLife",
    "AquariusZero",
    "Cabbage",
    "LastCore",
    "End",
    "Bakemonogatari",
    "LostElysium",
    "ChillSkill",
    "Combat",
    "Artisans_Libre",
    "Aeglos",
    "WingedAssassins",
    "AsulaGeneration",
    "CantTouchThis",
    "Core",
    "Casino_Royal",
    "Demetori",
    "Contempt",
    "Latentes",
    "Liberation",
    "TheDutchman",
    "Nap",
    "Aquatica"
]

def main():
    db = Database()
    scraper = Scraper()
    
    try:
        for guild_name in guilds_to_scrape:
            members = scraper.get_guild_raw(guild_name, "EU")
            db.save_guild(guild_name, members)
            """for member, data in members.items():
                print(f"{member}: {data}")"""
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
