class Character:
    """
    Klasa bazowa dla wszystkich postaci w grze.
    """
    def __init__(self, name, health, attack_power, defense_power):
        """
        Inicjalizuje postać.
        :param name: Imię/Nazwa postaci.
        :param health: Punkty zdrowia.
        :param attack_power: Siła ataku.
        :param defense_power: Siła obrony.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nazwa postaci musi być niepustym ciągiem znaków.")
        if not isinstance(health, int) or health <= 0:
            raise ValueError("Zdrowie musi być dodatnią liczbą całkowitą.")
        if not isinstance(attack_power, int) or attack_power < 0:
            raise ValueError("Siła ataku musi być nieujemną liczbą całkowitą.")
        if not isinstance(defense_power, int) or defense_power < 0:
            raise ValueError("Siła obrony musi być nieujemną liczbą całkowitą.")

        self.name = name
        self.max_health = health
        self.current_health = health
        self.base_attack_power = attack_power 
        self.base_defense_power = defense_power 
        self.attack_power = attack_power 
        self.defense_power = defense_power 
        self.is_blocking = False 
        self.status_effects = {} 

    def __str__(self):
        """
        Zwraca reprezentację stringową postaci.
        """
        return (f"{self.name} (HP: {self.current_health}/{self.max_health}, "
                f"ATK: {self.attack_power}, DEF: {self.defense_power})")

    def is_alive(self):
        """
        Sprawdza, czy postać wciąż żyje.
        :return: True, jeśli postać ma więcej niż 0 HP, w przeciwnym razie False.
        """
        return self.current_health > 0

    def take_damage(self, damage):
        """
        Redukuje punkty zdrowia postaci o zadaną wartość obrażeń, uwzględniając obronę.
        :param damage: Ilość obrażeń przed redukcją.
        """
        if not isinstance(damage, int) or damage < 0:
            print("Otrzymane obrażenia muszą być nieujemną liczbą całkowitą.")
            return

        actual_defense = self.defense_power
        if self.is_blocking:
            actual_defense *= 2 
            print(f"{self.name} blokuje, zwiększając swoją obronę!")

        reduced_damage = max(0, damage - actual_defense)
        self.current_health -= reduced_damage
        print(f"{self.name} otrzymuje {reduced_damage} obrażeń.")
        if self.current_health <= 0:
            self.current_health = 0
            print(f"{self.name} został pokonany!")
        self.is_blocking = False

    def heal(self, amount):
        """
        Przywraca postaci punkty zdrowia.
        :param amount: Ilość przywracanego zdrowia.
        """
        if not isinstance(amount, int) or amount <= 0:
            print("Ilość leczenia musi być dodatnią liczbą całkowitą.")
            return

        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        print(f"{self.name} odzyskuje {amount} HP. Aktualne zdrowie: {self.current_health}/{self.max_health}.")

    def attack(self, target):
        """
        Postać atakuje cel.
        :param target: Obiekt postaci (inny Character), który jest atakowany.
        """
        if not self.is_alive():
            print(f"{self.name} nie może atakować, jest pokonany/a.")
            return
        if not target.is_alive():
            print(f"{target.name} jest już pokonany/a.")
            return

        print(f"{self.name} atakuje {target.name}!")

        target.take_damage(self.attack_power)

    def defend_action(self):
        """
        Postać przygotowuje się do obrony.
        """
        if not self.is_alive():
            print(f"{self.name} nie może się bronić, jest pokonany/a.")
            return
        self.is_blocking = True
        print(f"{self.name} przygotowuje się do obrony, wzmacniając swoją gardę!")

    def apply_status_effect(self, effect_name, duration, potency=0):
        """
        Nakłada efekt statusu na postać.
        :param effect_name: Nazwa efektu (np. "poison", "stun").
        :param duration: Czas trwania efektu w turach.
        :param potency: Siła efektu (np. obrażenia od trucizny na turę).
        """
        self.status_effects[effect_name] = {'duration': duration, 'potency': potency}
        print(f"{self.name} zostaje objęty efektem: {effect_name} na {duration} tur.")

    def tick_status_effects(self):
        """
        Przetwarza efekty statusu na koniec tury.
        """
        effects_to_remove = []
        for effect, data in self.status_effects.items():
            print(f"Efekt '{effect}' działa na {self.name}.")
            if effect == "poison":
                damage = data.get('potency', 1) 
                self.take_damage(damage)
                print(f"{self.name} traci {damage} HP od trucizny.")
         
            data['duration'] -= 1
            if data['duration'] <= 0:
                effects_to_remove.append(effect)
        
        for effect in effects_to_remove:
            del self.status_effects[effect]
            print(f"Efekt '{effect}' na {self.name} skończył się.")


class Player(Character):
    """
    Klasa reprezentująca gracza. Dziedziczy po Character.
    """
    def __init__(self, name, health=100, attack_power=10, defense_power=5):
        super().__init__(name, health, attack_power, defense_power)
        self.inventory = [] 
        self.equipped_weapon = None 
        self.equipped_armor = None  
        self.gold = 50
        self.experience = 0
        self.level = 1
        self.xp_to_next_level = 100
        self.mana = 50
        self.max_mana = 50

    def add_item_to_inventory(self, item):
        """
        Dodaje przedmiot do ekwipunku gracza.
        :param item: Obiekt klasy Item lub jej pochodnych.
        """
        self.inventory.append(item)
        print(f"Zdobywasz: {item.name}.")

    def remove_item_from_inventory(self, item_name):
        """
        Usuwa przedmiot z ekwipunku gracza po nazwie.
        :param item_name: Nazwa przedmiotu do usunięcia.
        :return: Usunięty przedmiot lub None, jeśli nie znaleziono.
        """
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                self.inventory.remove(item)
                print(f"Tracisz: {item.name}.")
                return item
        print(f"Nie masz przedmiotu o nazwie '{item_name}'.")
        return None

    def show_inventory(self):
        """
        Wyświetla zawartość ekwipunku gracza.
        """
        print("\n--- Twój Ekwipunek ---")
        if not self.inventory:
            print("Ekwipunek jest pusty.")
        else:
            for i, item in enumerate(self.inventory):
                print(f"{i + 1}. {str(item)}") 
        print(f"Złoto: {self.gold}")
        print("----------------------")

    def equip_item(self, item_name):
        """
        Ekwipuje przedmiot z ekwipunku.
        :param item_name: Nazwa przedmiotu do założenia.
        """
        item_to_equip = None
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                item_to_equip = item
                break
        
        if not item_to_equip:
            print(f"Nie masz '{item_name}' w ekwipunku.")
            return

        if hasattr(item_to_equip, 'damage'): 
            if self.equipped_weapon:
                self.unequip_item_slot('weapon') 
            self.equipped_weapon = item_to_equip
            self.attack_power = self.base_attack_power + self.equipped_weapon.damage
            print(f"Zakładasz {self.equipped_weapon.name} (+{self.equipped_weapon.damage} ATK).")
            self.inventory.remove(item_to_equip) 

        elif hasattr(item_to_equip, 'defense'):
            if self.equipped_armor:
                self.unequip_item_slot('armor')
            self.equipped_armor = item_to_equip
            self.defense_power = self.base_defense_power + self.equipped_armor.defense
            print(f"Zakładasz {self.equipped_armor.name} (+{self.equipped_armor.defense} DEF).")
            self.inventory.remove(item_to_equip)
        else:
            print(f"{item_to_equip.name} nie jest bronią ani pancerzem.")


    def unequip_item_slot(self, slot_type):
        """
        Zdejmuje przedmiot z danego slotu (broń lub pancerz) i przywraca bazowe statystyki.
        :param slot_type: 'weapon' lub 'armor'.
        """
        if slot_type == 'weapon' and self.equipped_weapon:
            print(f"Zdejmujesz {self.equipped_weapon.name}.")
            self.add_item_to_inventory(self.equipped_weapon) 
            self.attack_power = self.base_attack_power
            self.equipped_weapon = None
        elif slot_type == 'armor' and self.equipped_armor:
            print(f"Zdejmujesz {self.equipped_armor.name}.")
            self.add_item_to_inventory(self.equipped_armor)
            self.defense_power = self.base_defense_power
            self.equipped_armor = None
        else:
            print(f"Nie masz niczego założonego w slocie '{slot_type}'.")

    def use_potion_from_inventory(self, potion_name):
        """
        Używa mikstury z ekwipunku.
        :param potion_name: Nazwa mikstury do użycia.
        """
        potion_to_use = None
        for item in self.inventory:
            if item.name.lower() == potion_name.lower() and hasattr(item, 'effect_type'): 
                potion_to_use = item
                break
        
        if potion_to_use:
            if potion_to_use.use(self): 
                if potion_to_use.sips_left <= 0:
                    self.inventory.remove(potion_to_use) 
            else:
                print(f"Nie udało się użyć {potion_name}.")
        else:
            print(f"Nie masz mikstury '{potion_name}' lub to nie jest mikstura.")

    def gain_experience(self, amount):
        """
        Gracz zdobywa punkty doświadczenia.
        :param amount: Ilość zdobytego XP.
        """
        if not isinstance(amount, int) or amount < 0:
            print("Ilość doświadczenia musi być nieujemną liczbą całkowitą.")
            return

        self.experience += amount
        print(f"{self.name} zdobywa {amount} punktów doświadczenia.")
        while self.experience >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        """
        Gracz awansuje na kolejny poziom.
        """
        self.level += 1
        self.experience -= self.xp_to_next_level 
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5) 

       
        health_gain = 10 + self.level * 2
        attack_gain = 2 + self.level // 2
        defense_gain = 1 + self.level // 3
        mana_gain = 5 + self.level

        self.max_health += health_gain
        self.current_health = self.max_health 
        self.base_attack_power += attack_gain
        self.attack_power += attack_gain 
        self.base_defense_power += defense_gain
        self.defense_power += defense_gain 
        self.max_mana += mana_gain
        self.mana = self.max_mana

        print(f"*** {self.name} awansuje na POZIOM {self.level}! ***")
        print(f"Zdrowie: +{health_gain} (teraz {self.max_health})")
        print(f"Atak: +{attack_gain} (bazowy teraz {self.base_attack_power})")
        print(f"Obrona: +{defense_gain} (bazowa teraz {self.base_defense_power})")
        print(f"Mana: +{mana_gain} (teraz {self.max_mana})")
        print(f"Do następnego poziomu: {self.xp_to_next_level - self.experience} XP.")
        print("Gratulacje! Jesteś silniejszy/a!")

    def restore_mana(self, amount):
        """
        Przywraca punkty many.
        :param amount: Ilość przywracanej many.
        """
        if not isinstance(amount, int) or amount <= 0:
            print("Ilość many musi być dodatnią liczbą całkowitą.")
            return

        self.mana += amount
        if self.mana > self.max_mana:
            self.mana = self.max_mana
        print(f"{self.name} odzyskuje {amount} MP. Aktualna mana: {self.mana}/{self.max_mana}.")

    def display_status(self):
        """
        Wyświetla aktualny status gracza.
        """
        print("\n--- Status Gracza ---")
        print(f"Imię: {self.name}")
        print(f"Poziom: {self.level} (XP: {self.experience}/{self.xp_to_next_level})")
        print(f"Zdrowie: {self.current_health}/{self.max_health}")
        print(f"Mana: {self.mana}/{self.max_mana}")
        print(f"Atak: {self.attack_power} (Bazowy: {self.base_attack_power})")
        print(f"Obrona: {self.defense_power} (Bazowy: {self.base_defense_power})")
        print(f"Złoto: {self.gold}")
        if self.equipped_weapon:
            print(f"Broń: {self.equipped_weapon.name} (+{self.equipped_weapon.damage} ATK)")
        else:
            print("Broń: Brak")
        if self.equipped_armor:
            print(f"Pancerz: {self.equipped_armor.name} (+{self.equipped_armor.defense} DEF)")
        else:
            print("Pancerz: Brak")
        if self.status_effects:
            print("Aktywne efekty:")
            for effect, data in self.status_effects.items():
                print(f"  - {effect.capitalize()}: {data['duration']} tur (Siła: {data.get('potency', 'N/A')})")
        print("--------------------")


class Enemy(Character):
    """
    Klasa reprezentująca przeciwnika. Dziedziczy po Character.
    """
    def __init__(self, name, health, attack_power, defense_power, experience_reward, gold_reward, loot_table=None):
        """
        Inicjalizuje przeciwnika.
        :param name: Nazwa przeciwnika.
        :param health: Punkty zdrowia.
        :param attack_power: Siła ataku.
        :param defense_power: Siła obrony.
        :param experience_reward: Doświadczenie za pokonanie.
        :param gold_reward: Złoto za pokonanie.
        :param loot_table: Lista przedmiotów, które może upuścić przeciwnik (lub funkcja generująca loot).
        """
        super().__init__(name, health, attack_power, defense_power)
        if not isinstance(experience_reward, int) or experience_reward < 0:
            raise ValueError("Nagroda XP musi być nieujemną liczbą całkowitą.")
        if not isinstance(gold_reward, int) or gold_reward < 0:
            raise ValueError("Nagroda w złocie musi być nieujemną liczbą całkowitą.")
        
        self.experience_reward = experience_reward
        self.gold_reward = gold_reward
        self.loot_table = loot_table if loot_table else [] 
       
        self.special_ability_cooldown = 0
        self.max_cooldown = 3 

    def drop_loot(self):
        """
        Zwraca listę przedmiotów upuszczonych przez przeciwnika.
        Na razie proste - zwraca całą tabelę. Można dodać losowość.
        """
        if self.loot_table:
            print(f"{self.name} upuszcza:")
            for item in self.loot_table:
                print(f"- {item.name}")
            return self.loot_table 
        return []

    def use_special_ability(self, target):
        """
        Przykładowa specjalna umiejętność. Każdy wróg może mieć inną.
        Ta jest ogólna - silniejszy atak.
        """
        if self.special_ability_cooldown == 0:
            print(f"{self.name} używa specjalnej umiejętności!")
          
            special_damage = int(self.attack_power * 1.5)
            print(f"{self.name} wykonuje POTĘŻNY CIOS zadając {special_damage} obrażeń!")
            target.take_damage(special_damage)
            self.special_ability_cooldown = self.max_cooldown 
            return True
        return False 

    def tick_cooldowns(self):
        """
        Redukuje czas odnowienia umiejętności na koniec tury.
        """
        if self.special_ability_cooldown > 0:
            self.special_ability_cooldown -= 1
            
