
import items 
import characters 
class Location:
    """
    Klasa reprezentująca lokalizacji w świecie gry.
    """
    def __init__(self, name, description, exits=None, enemies=None, items_in_location=None, npcs=None):
        """
        Inicjalizuje lokalizacji.
        :param name: Nazwa lokalizacji.
        :param description: Opis lokalizacji.
        :param exits: Słownik połączeń z innymi lokacjami {'kierunek': 'nazwa_innej_lokalizacji'}.
        :param enemies: Lista przeciwników (obiekty Enemy) w tej lokalizacji.
        :param items_in_location: Lista przedmiotów (obiekty Item) do znalezienia w lokalizacji.
        :param npcs: Lista postaci niezależnych (NPC) w lokalizacji.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nazwa lokalizacji musi być niepustym ciągiem znaków.")
        if not isinstance(description, str):
            raise ValueError("Opis lokalizacji musi być ciągiem znaków.")

        self.name = name
        self.description = description
        self.exits = exits if exits is not None else {}
       
        self.enemies = list(enemies) if enemies is not None else []
        self.items_in_location = list(items_in_location) if items_in_location is not None else []
        self.npcs = list(npcs) if npcs is not None else []
        self.visited = False 

    def __str__(self):
        """
        Zwraca nazwę i krótki opis lokalizacji
        """
        return f"{self.name}{self.description}"

    def describe(self):
        """
        Wyświetla pełny opis lokalizacji, w tym wyjścia, przeciwników, przedmioty i NPC.
        """
        print(f"--- {self.name} ---")
        print(self.description)
        if not self.visited:
            print("Wygląda na to, że jesteś tu po raz pierwszy.")
            self.visited = True 
        else:
            print("Byłeś/aś już tutaj.")

        if self.items_in_location:
            print("Widzisz tu następujące przedmioty:")
            for item_obj in self.items_in_location:
                print(f"- {item_obj.name}")
        
        if self.enemies:
            print("W tej lokalizacji czają się wrogowie:")
            for enemy_obj in self.enemies:
                print(f"- {enemy_obj.name} ({enemy_obj.current_health}/{enemy_obj.max_health} HP)")
        
        if self.npcs:
            print("Spotykasz tu następujące postacie:")
            for npc_obj in self.npcs:
                print(f"- {npc_obj.name}")

        if self.exits:
            print("Dostępne wyjścia:")
            for direction, destination_name in self.exits.items():
                print(f"- {direction.capitalize()}: do {destination_name}")
        else:
            print("Nie ma stąd żadnych widocznych wyjść.")
        print("--------------------")

    def add_enemy(self, enemy):
        """Dodaje przeciwnika do lokalizacji."""
        if isinstance(enemy, characters.Enemy):
            self.enemies.append(enemy)
        else:
            print("Błąd: Można dodać tylko instancję klasy Enemy.")

    def remove_enemy(self, enemy):
        """Usuwa przeciwnika z lokalizacji (np. po pokonaniu)."""
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            print(f"{enemy.name} został usunięty z lokalizacji {self.name}.")
        else:
            print(f"{enemy.name} nie znajduje się w lokalizacji {self.name}.")
            
    def add_item(self, item):
        """Dodaje przedmiot do lokalizacji."""
        if isinstance(item, items.Item):
            self.items_in_location.append(item)
        else:
            print("Błąd: Można dodać tylko instancję klasy Item.")
            
    def remove_item(self, item_name):
        """Usuwa przedmiot z lokalizacji (np. po podniesieniu przez gracza)."""
        item_to_remove = None
        for item_obj in self.items_in_location:
            if item_obj.name.lower() == item_name.lower():
                item_to_remove = item_obj
                break
        if item_to_remove:
            self.items_in_location.remove(item_to_remove)
            print(f"Przedmiot {item_to_remove.name} został usunięty z lokalizacji {self.name}.")
            return item_to_remove
        else:
            print(f"Przedmiot '{item_name}' nie znajduje się w lokalizacji {self.name}.")
            return None


class NPC(characters.Character):
    """
    Klasa reprezentująca postać niezależną (NPC).
    Dziedziczy po Character, ale może mieć dodatkowe interakcje.
    """
    def __init__(self, name, health, description, dialogue=None, quests=None, trades=None):
        super().__init__(name, health, 0, 0) 
        self.description = description
        self.dialogue_options = dialogue if dialogue is not None else ["Witaj, podróżniku."]
        self.quests_available = quests if quests is not None else [] 
        self.trade_items = trades if trades is not None else [] 
        self.interaction_count = 0

    def talk(self):
        """
        Rozpoczyna dialog z NPC.
        """
        print(f"--- Rozmowa z {self.name} ---")
        print(f"{self.name}: {self.description}")
        if self.dialogue_options:
            
            current_dialogue = self.dialogue_options[self.interaction_count % len(self.dialogue_options)]
            print(f"{self.name} mówi: \"{current_dialogue}\"")
        else:
            print(f"{self.name} nie ma nic do powiedzenia.")
        
        if self.quests_available:
            print(f"{self.name} może mieć dla Ciebie zadanie:")
            for quest in self.quests_available:
                
                print(f"- {quest.name}: {quest.description}")
        
        if self.trade_items:
            print(f"{self.name} ma na sprzedaż:")
            for i, item in enumerate(self.trade_items):
                print(f"  {i+1}. {item.name} (Cena: {item.value} Złota)")
        
        self.interaction_count += 1
        print("--------------------------")
        

rusty_sword = items.Weapon("Zardzewiały Miecz", "Ledwo trzyma się kupy.", 5, "melee", 5)
rusty_sword.durability = 30
short_sword = items.Weapon("Krótki Miecz", "Prosty, ale niezawodny krótki miecz.", 10, "melee", 15)
long_bow = items.Weapon("Długi Łuk", "Łuk wymagający siły i wprawy.", 12, "ranged", 25)
long_bow.rarity = "uncommon"
magic_staff = items.Weapon("Magiczna Laska", "Laska emanująca słabą energią magiczną.", 8, "magic", 30)
magic_staff.is_magical = True
magic_staff.rarity = "uncommon"
goblin_axe = items.Weapon("Toporek Goblina", "Mały, prymitywny toporek.", 6, "melee", 7)

tattered_clothes = items.Armor("Podarte Ubranie", "Niewiele lepsze niż nic.", 1, "torso", 1)
tattered_clothes.condition = "damaged"
leather_armor = items.Armor("Skórzana Zbroja", "Lekka zbroja zapewniająca podstawową ochronę.", 5, "torso", 20)
iron_helmet = items.Armor("Żelazny Hełm", "Solidny hełm chroniący głowę.", 3, "head", 10)
wooden_shield = items.Armor("Drewniana Tarcza", "Prosta tarcza do blokowania ciosów.", 4, "shield", 12)
wooden_shield.condition = "used"
wooden_shield.rarity = "common"


lesser_healing_potion = items.Potion("Mniejsza Mikstura Leczenia", "Przywraca 25 punktów zdrowia.", "heal", 25, 10)
healing_potion = items.Potion("Mikstura Leczenia", "Przywraca 50 punktów zdrowia.", "heal", 50, 25)
healing_potion.rarity = "uncommon"
mana_potion = items.Potion("Mikstura Many", "Odnawia 20 punktów many.", "mana_restore", 20, 15)
mana_potion.rarity = "uncommon"
strength_elixir = items.Potion("Eliksir Siły", "Tymczasowo zwiększa siłę o 5.", "strength_boost", 5, 30)
strength_elixir.is_magical = True
strength_elixir.rarity = "rare"
strength_elixir.sips_left = 2

goblin_scout = characters.Enemy("Goblin Zwiadowca", 30, 8, 2, 10, 5, [goblin_axe, lesser_healing_potion]) 
goblin_warrior = characters.Enemy("Goblin Wojownik", 45, 10, 3, 15, 8, [short_sword, items.Potion("Słaba Mikstura Obrony", "Zwiększa obronę o 2", "defense_boost", 2, 7)])
goblin_warrior.max_cooldown = 2 
orc_brute = characters.Enemy("Ork Brutal", 80, 15, 5, 30, 20, [items.Weapon("Ciężka Maczuga", "Ogromna, drewniana maczuga.", 13, "melee", 18)])
orc_brute.base_attack_power = 15 
orc_brute.max_cooldown = 4
forest_spider = characters.Enemy("Leśny Pająk", 25, 12, 1, 8, 3, [items.Item("Jad Pająka", "Składnik alchemiczny.", 5)])
forest_spider.special_ability_description = "Pluje jadem, który może zatruć." 
old_man_hermit = NPC(
    name="Stary Pustelnik",
    health=50,
    description="Mężczyzna o pooranej zmarszczkami twarzy i długiej, siwej brodzie. Patrzy na Ciebie przenikliwie.",
    dialogue=[
        "Witaj, młody wędrowcze. Czego szukasz w tych dzikich ostępach?",
        "Świat jest pełen niebezpieczeństw, ale i skarbów dla odważnych.",
        "Pamiętaj, by zawsze mieć oczy szeroko otwarte.",
        "Słyszałem o pradawnym artefakcie ukrytym gdzieś w tych ruinach..."
    ],
    trades=[healing_potion, mana_potion] 
)

game_world_map = {}

def create_world():
    """
    Tworzy i zwraca mapę świata z predefiniowanymi lokalizacji.
    """
    global game_world_map 
    game_world_map = {}

    starting_room = Location(
        name="Spokojna Polana",
        description="Stoisz na niewielkiej polanie otoczonej starymi drzewami. Śpiew ptaków napawa spokojem.",
        exits={"północ": "Mroczny Las", "wschód": "Stara Droga"},
        items_in_location=[rusty_sword, tattered_clothes]
    )
    game_world_map[starting_room.name] = starting_room

    dark_forest_entrance = Location(
        name="Mroczny Las",
        description="Gęste korony drzew niemal całkowicie zasłaniają niebo. Z głębi lasu dobiegają niepokojące odgłosy.",
        exits={"południe": "Spokojna Polana", "północ": "Gęstwina Leśna"},
        enemies=[characters.Enemy("Wilk", 35, 9, 2, 12, 6, [items.Item("Wilcze Futro", "Ciepłe futro.", 3)])] 
    )
    game_world_map[dark_forest_entrance.name] = dark_forest_entrance
 
    deep_forest = Location(
        name="Gęstwina Leśna",
        description="Zarośla są tak gęste, że ledwo można się przecisnąć. Gdzieś w pobliżu słychać szelest.",
        exits={"południe": "Mroczny Las", "zachód": "Jaskinia Goblinów"},
        enemies=[goblin_scout, forest_spider],
        items_in_location=[lesser_healing_potion]
    )
    game_world_map[deep_forest.name] = deep_forest

    goblin_cave = Location(
        name="Jaskinia Goblinów",
        description="Wilgotna, śmierdząca jaskinia. Wszędzie walają się kości i resztki jedzenia.",
        exits={"wschód": "Gęstwina Leśna"},
        enemies=[goblin_warrior, goblin_scout, characters.Enemy("Szef Goblinów", 60, 12, 4, 50, 30, [short_sword, leather_armor])],
        items_in_location=[items.Item("Złoty Ząb Goblina", "Błyszczący ząb, pewnie coś warty.", 10)]
    )
    game_world_map[goblin_cave.name] = goblin_cave

    old_road = Location(
        name="Stara Droga",
        description="Kamienista droga, dawno nie uczęszczana. Prowadzi w nieznane.",
        exits={"zachód": "Spokojna Polana", "wschód": "Ruiny Wieży"},
        npcs=[old_man_hermit] 
    )
    game_world_map[old_road.name] = old_road

    
    tower_ruins = Location(
        name="Ruiny Wieży",
        description="Pozostałości starej wieży strażniczej. Mury są omszałe i częściowo zawalone.",
        exits={"zachód": "Stara Droga"},
        enemies=[orc_brute],
        items_in_location=[magic_staff, strength_elixir]
    )
    magic_staff.is_magical = True 
    magic_staff.description = "Starożytna laska, wciąż pulsująca mocą."
    game_world_map[tower_ruins.name] = tower_ruins

    return game_world_map

