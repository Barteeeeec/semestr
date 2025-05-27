
import random 

def display_combat_status(player, enemy):
    """
    Wyświetla status gracza i przeciwnika podczas walki.
    :param player: Obiekt gracza.
    :param enemy: Obiekt przeciwnika.
    """
    print("--- STAN WALKI ---")
   # print(f"TY: {player.name} | HP: {player.current_health}/{player.max_health} | Mana: {player.mana}/{player.max_mana}")
    #if player.status_effects:
    #    print(f"  Twoje efekty: {', '.join([f'{k} ({v['czas trwania']} tur)' for k,v in player.status_effects.items()])}")
    #    print(f"  Twoje efekty: {', '.join([f'{k.capitalize()} ({v['duration']} tur)' for k,v in player.status_effects.items()])}")
    #print(f"WRÓG: {enemy.name} | HP: {enemy.current_health}/{enemy.max_health}")
    #if enemy.status_effects:
    #    print(f"  Efekty wroga: {', '.join([f'{k} ({v['duration']} tur)' for k,v in enemy.status_effects.items()])}")
    #    print(f"  Efekty wroga: {', '.join([f'{k.capitalize()} ({v['duration']} tur)' for k,v in enemy.status_effects.items()])}")
    #print("--------------------")
    #print()
    print(f"TY: {player.name} | HP: {player.current_health}/{player.max_health} | Mana: {player.mana}/{player.max_mana}")
    if player.status_effects:
        
        effects_str_list = []
        for k, v in player.status_effects.items():
            effects_str_list.append(f"{k.capitalize()} ({v['duration']} tur)")
        print(f"  Twoje efekty: {', '.join(effects_str_list)}")
    print(f"WRÓG: {enemy.name} | HP: {enemy.current_health}/{enemy.max_health}")
    if enemy.status_effects:
        effects_str_list_enemy = []
        for k, v in enemy.status_effects.items():
            effects_str_list_enemy.append(f"{k.capitalize()} ({v['duration']} tur)")
        print(f"  Efekty wroga: {', '.join(effects_str_list_enemy)}")
    print("--------------------")
    print()






def player_turn(player, enemy):
    """
    Obsługuje turę gracza w walce.
    :param player: Obiekt gracza.
    :param enemy: Obiekt przeciwnika.
    :return: True jeśli walka trwa, False jeśli gracz uciekł lub coś zakończyło walkę.
    """
    print("--- TWOJA TURA ---")
    while True:
        print("Wybierz akcję:")
        print("1. Atakuj")
        print("2. Broń się")
        print("3. Użyj przedmiotu (mikstury)")
        print("4. Sprawdź status")
        print("5. Uciekaj (ryzykowne!)")
        if player.mana >= 10: 
             print("6. Magiczny Pocisk (koszt: 10 Many)")

        choice = input("Twój wybór: > ")

        if choice == '1':
            player.attack(enemy)
            break
        elif choice == '2':
            player.defend_action()
            break
        elif choice == '3':
            if not player.inventory:
                print("Nie masz żadnych przedmiotów w ekwipunku.")
                continue 

            print("Której mikstury chcesz użyć? (Wpisz nazwę lub numer, lub 'anuluj')")
            potion_options = []
            for i, item_obj in enumerate(player.inventory):
                if hasattr(item_obj, 'effect_type'): 
                    print(f"{i+1}. {item_obj.name}")
                    potion_options.append(item_obj)
            
            if not potion_options:
                print("Nie masz żadnych mikstur.")
                continue

            potion_choice = input("Wybór mikstury: > ")
            if potion_choice.lower() == 'anuluj':
                continue
            
            selected_potion = None
            try:
                potion_idx = int(potion_choice) - 1
                if 0 <= potion_idx < len(potion_options):
                    selected_potion = potion_options[potion_idx]
            except ValueError: 
                for p_opt in potion_options:
                    if p_opt.name.lower() == potion_choice.lower():
                        selected_potion = p_opt
                        break
            
            if selected_potion:
                player.use_potion_from_inventory(selected_potion.name)
                break 
            else:
                print("Nieprawidłowy wybór mikstury.")
                continue 

        elif choice == '4':
            player.display_status()
            enemy_status_line = f"{enemy.name}: HP: {enemy.current_health}/{enemy.max_health}, ATK: {enemy.attack_power}, DEF: {enemy.defense_power}"
            print(f"Status przeciwnika: {enemy_status_line}")
            if enemy.status_effects:
     #            print(f"  Efekty wroga: {', '.join([f'{k} ({v['duration']} tur)' for k,v in enemy.status_effects.items()])}")
                """
            Wyświetla status gracza i przeciwnika podczas walki.
            :param player: Obiekt gracza.
            :param enemy: Obiekt przeciwnika.
            """
            # type: (characters.Player, characters.Enemy) -> None
            print("\n--- STAN WALKI ---")
            print(f"TY: {player.name} | HP: {player.current_health}/{player.max_health} | Mana: {player.mana}/{player.max_mana}")
            if player.status_effects:
                # Tworzymy listę stringów opisujących efekty
                effects_str_list = []
                for k, v in player.status_effects.items():
                    effects_str_list.append(f"{k.capitalize()} ({v['duration']} tur)")
                # Łączymy stringi i wyświetlamy
                print(f"  Twoje efekty: {', '.join(effects_str_list)}")

            print(f"WRÓG: {enemy.name} | HP: {enemy.current_health}/{enemy.max_health}")
            if enemy.status_effects:
                # To samo dla wroga
                effects_str_list_enemy = []
                for k, v in enemy.status_effects.items():
                    effects_str_list_enemy.append(f"{k.capitalize()} ({v['duration']} tur)")
                print(f"  Efekty wroga: {', '.join(effects_str_list_enemy)}")
            print("--------------------")
            print()
            continue
        elif choice == '5':
            escape_chance = 0.5 
            if player.current_health < player.max_health / 4:
                escape_chance = 0.25 
            
            print("Próbujesz uciec...")
            if random.random() < escape_chance:
                print("Udało ci się uciec!")
                return False
            else:
                print("Nie udało się uciec! Tracisz turę.")
                break 
        elif choice == '6' and player.mana >= 10:
            player.mana -= 10
            magic_damage = player.base_attack_power + player.level * 2 
            print(f"Ciskasz Magiczny Pocisk w {enemy.name}, zadając {magic_damage} obrażeń magicznych (ignoruje część obrony)!")
            
            enemy.take_damage(magic_damage) 
            break
        elif choice == '6' and player.mana < 10:
            print("Nie masz wystarczająco Many na Magiczny Pocisk!")
            continue
        else:
            print("Nieprawidłowa komenda. Spróbuj ponownie.")
    
    player.tick_status_effects() 
    return True 

def enemy_turn(enemy, player):
    print(f"--- TURA {enemy.name.upper()} ---")
    
    if hasattr(enemy, 'use_special_ability') and enemy.special_ability_cooldown == 0:
       
        if random.random() < 0.4: 
            if enemy.name == "Leśny Pająk": 
                print(f"{enemy.name} pluje jadem!")
                if random.random() < 0.6: 
                    player.apply_status_effect("poison", 3, potency=enemy.attack_power // 3) 
                else:
                    print(f"{player.name} unika jadu!")
                enemy.special_ability_cooldown = enemy.max_cooldown 
            elif enemy.use_special_ability(player): 
                pass 
            else: 
                enemy.attack(player)
        else: 
            enemy.attack(player)
    elif enemy.current_health < enemy.max_health / 3 and random.random() < 0.3: 
        enemy.defend_action()
    else: 
        enemy.attack(player)

    enemy.tick_status_effects() 
    enemy.tick_cooldowns() 


def start_combat(player, enemy_instance):
    print(f"!!! Rozpoczyna się walka: {player.name} vs {enemy_instance.name} !!!")
    
   
    player.is_blocking = False
    enemy_instance.is_blocking = False
    
    turn_order = [player, enemy_instance]
    if random.random() < 0.5:
        print(f"{enemy_instance.name} jest szybszy i atakuje pierwszy!")
        current_turn_idx = 1 
    else:
        print(f"{player.name} jest szybszy i atakuje pierwszy!")
        current_turn_idx = 0

    while player.is_alive() and enemy_instance.is_alive():
        display_combat_status(player, enemy_instance)
        
        active_character = turn_order[current_turn_idx % 2]
        passive_character = turn_order[(current_turn_idx + 1) % 2]

        if active_character == player:
            if not player_turn(player, enemy_instance): 
                return "escaped"
        else: 
            enemy_turn(enemy_instance, player)
            input("Naciśnij Enter, aby kontynuować...") 
            
        current_turn_idx += 1
    
    display_combat_status(player, enemy_instance) 
    if player.is_alive():
        print(f"*** {player.name} zwycięża walkę! ***")
        xp_reward = enemy_instance.experience_reward
        gold_reward = enemy_instance.gold_reward
        print(f"Zdobywasz {xp_reward} XP i {gold_reward} złota.")
        player.gain_experience(xp_reward)
        player.gold += gold_reward
        
        dropped_items = enemy_instance.drop_loot()
        if dropped_items:
            for item_obj in dropped_items:
                player.add_item_to_inventory(item_obj) 
        return "victory"
    else:
        print(f"--- {player.name} został pokonany... KONIEC GRY? ---")
        return "defeat"