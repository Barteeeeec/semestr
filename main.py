

import characters
import items 
import world 
import combat   
import random 

def display_welcome_message():
    """Wyświetla powitanie na początku gry."""
    print("=" * 40)
    print(" Witaj w Prostej Grze RPG Tekstowej!")
    print("=" * 40)
    print("Twoim celem jest eksploracja, walka i przetrwanie.") 
    print("Używaj komend, aby poruszać się po świecie i wchodzić w interakcje.")
    print("Powodzenia, bohaterze!")
   
    print("Legenda komend:")
    print("  'idz [kierunek]' - np. 'idz polnoc'")
    print("  'rozejrzyj sie' - opisuje aktualną lokację")
    print("  'ekwipunek' lub 'e' - pokazuje twój ekwipunek")
    print("  'podnies [nazwa przedmiotu]' - podnosi przedmiot z lokacji")
    print("  'zaloz [nazwa przedmiotu]' - ekwipuje przedmiot")
    print("  'zdejmij [bron/pancerz]' - zdejmuje broń lub pancerz")
    print("  'uzyj [nazwa mikstury]' - używa mikstury z ekwipunku")
    print("  'status' - pokazuje status gracza")
    print("  'atakuj [nazwa wroga]' - rozpoczyna walkę (jeśli wróg jest w lokacji)")
    print("  'porozmawiaj [nazwa npc]' - rozmawia z NPC")
    print("  'pomoc' - wyświetla tę listę komend")
    print("  'wyjdz' lub 'q' - kończy grę")
    print("-" * 40)
    print() 

def get_player_name():
    """Pobiera imię gracza."""
    while True:
        name = input("Podaj imię swojego bohatera: ").strip()
        if name:
            return name
        else:
            print("Imię nie może być puste.")

def initialize_game():
    """Inicjalizuje stan gry, tworzy gracza i świat."""
    player_name = get_player_name()
    player = characters.Player(name=player_name, health=100, attack_power=10, defense_power=3)
    
    start_weapon = items.Weapon("Stary Sztylet", "Niewiele lepszy niż gołe pięści.", 7, "melee", 3)
    start_potion = items.Potion("Mała Mikstura Leczenia", "Leczy 20 HP.", "heal", 20, 5)
    player.add_item_to_inventory(start_weapon)
    player.add_item_to_inventory(start_potion)
    player.equip_item(start_weapon.name) 

    
    game_world_map = world.create_world() 
    current_location_name = "Spokojna Polana" 
    
    print(f"{player.name}, twoja przygoda się rozpoczyna!")
    return player, game_world_map, current_location_name

def handle_player_input(player, game_map, current_location_name):
    """
    Przetwarza komendy wprowadzane przez gracza.
    Zwraca nową nazwę lokalizacji (jeśli gracz się poruszył) lub aktualną, oraz status gry (True=kontynuuj, False=zakończ).
    """
    current_loc_obj = game_map[current_location_name]
    
    action = input(f"[{current_location_name}] Co robisz?  ").lower().strip()
    parts = action.split()
    command = parts[0] if parts else ""
    argument = " ".join(parts[1:]) if len(parts) > 1 else ""

    if command == "idz" or command == "i":
        if not argument:
            print("Dokąd chcesz iść? (np. 'idz północ')")
            return current_location_name, True
        
        direction = argument
        if direction in current_loc_obj.exits:
            destination_name = current_loc_obj.exits[direction]
            if destination_name in game_map:
                print(f"Idziesz na {direction} do {destination_name}...")
                return destination_name, True 
            else:
                print(f"Błąd: Lokalizacja '{destination_name}' nie istnieje na mapie.")
                return current_location_name, True
        else:
            print(f"Nie możesz iść w kierunku '{direction}' z tej lokalizacji.")
            return current_location_name, True

    elif command in ["rozejrzyj sie", "opis", "look", "l"]:
        current_loc_obj.describe()
        return current_location_name, True

    elif command in ["ekwipunek", "inventory", "e", "eq"]:
        player.show_inventory()
        return current_location_name, True
        
    elif command in ["podnies", "wez", "take", "p"]:
        if not argument:
            print("Co chcesz podnieść? (np. 'podnies miecz')")
            return current_location_name, True
        
        item_to_take = current_loc_obj.remove_item(argument) 
        if item_to_take:
            player.add_item_to_inventory(item_to_take)
        
        return current_location_name, True

    elif command in ["zaloz", "equip"]:
        if not argument:
            print("Co chcesz założyć? (np. 'zaloz miecz')")
            return current_location_name, True
        player.equip_item(argument)
        return current_location_name, True
        
    elif command in ["zdejmij", "unequip"]:
        if not argument:
            print("Co chcesz zdjąć? ('bron' lub 'pancerz')")
            return current_location_name, True
        if argument.lower() in ['broń', 'bron', 'weapon']:
            player.unequip_item_slot('weapon')
        elif argument.lower() in ['pancerz', 'zbroja', 'armor']:
            player.unequip_item_slot('armor')
        else:
            print("Nieznany typ slotu. Użyj 'bron' lub 'pancerz'.")
        return current_location_name, True
        
    elif command in ["uzyj", "use"]:
        if not argument:
            print("Czego chcesz użyć? (np. 'uzyj mikstura leczenia')")
            return current_location_name, True
        player.use_potion_from_inventory(argument) 
        return current_location_name, True

    elif command in ["status", "staty", "s"]:
        player.display_status()
        return current_location_name, True
        
    elif command in ["atakuj", "walcz", "fight", "a"]:
        if not argument:
            print("Kogo chcesz zaatakować? (np. 'atakuj goblin')")
            return current_location_name, True
        
        target_enemy = None
        for enemy_obj in current_loc_obj.enemies:
            if enemy_obj.name.lower() == argument.lower() and enemy_obj.is_alive():
                target_enemy = enemy_obj
                break
        
        if target_enemy:
            combat_result = combat.start_combat(player, target_enemy)
            if combat_result == "victory":
                current_loc_obj.remove_enemy(target_enemy)
            elif combat_result == "defeat":
                print("Twoja przygoda dobiegła końca...")
                return current_location_name, False 
            elif combat_result == "escaped":
                print("Wracasz do poprzedniej czynności, serce wciąż ci wali.")
            current_loc_obj.describe()
        else:
            print(f"Nie ma tu wroga o nazwie '{argument}' lub jest już pokonany.")
        return current_location_name, True

    elif command in ["porozmawiaj", "talk", "gadaj"]:
        if not argument:
            print("Z kim chcesz porozmawiać? (np. 'porozmawiaj stary pustelnik')")
            return current_location_name, True

        target_npc = None
        for npc_obj in current_loc_obj.npcs:
            if npc_obj.name.lower() == argument.lower():
                target_npc = npc_obj
                break
        
        if target_npc:
            target_npc.talk()
        else:
            print(f"Nie ma tu postaci o nazwie '{argument}'.")
        return current_location_name, True
        
    elif command in ["pomoc", "help", "h", "?"]:
        display_welcome_message() 
        return current_location_name, True

    elif command in ["wyjdz", "quit", "q", "exit"]:
        print("Dziękujemy za grę! Do zobaczenia.")
        return current_location_name, False 
    
    else:
        print("Nieznana komenda. Wpisz 'pomoc' aby zobaczyć listę dostępnych komend.")
        return current_location_name, True

def game_loop():
    """Główna pętla gry."""
    player, game_map, current_location_name = initialize_game()
    display_welcome_message()
    
    if current_location_name in game_map:
        game_map[current_location_name].describe()
    else:
        print(f"Błąd krytyczny: Startowa lokalizacja '{current_location_name}' nie istnieje!")
        return 
    running = True
    while running:
        if not player.is_alive(): 
            print("Zginąłeś... Koniec gry.")
            running = False
            break

        new_location_name, continue_playing = handle_player_input(player, game_map, current_location_name)
        running = continue_playing
        
        if new_location_name != current_location_name:
            current_location_name = new_location_name
            if current_location_name in game_map:
                game_map[current_location_name].describe()
                if game_map[current_location_name].enemies and random.random() < 0.1:
                    random_enemy = random.choice(game_map[current_location_name].enemies)
                    print(f"Zaskakuje cię {random_enemy.name}!")
                    combat_result = combat.start_combat(player, random_enemy)
                    if combat_result == "victory":
                        game_map[current_location_name].remove_enemy(random_enemy)
                    elif combat_result == "defeat":
                        running = False
            else:
                print(f"Błąd krytyczny: Próba przejścia do nieistniejącej lokalizacji '{current_location_name}'!")
                running = False 

if __name__ == "__main__":

    try:
        game_loop()
    except KeyboardInterrupt:
        print("Gra przerwana przez użytkownika (Ctrl+C). Do widzenia!")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd krytyczny: {e}")
        print("Przepraszamy, gra musi zostać zakończona.")
    finally:
        print("Program zakończył działanie.")