class Item:
    """
    Klasa bazowa dla wszystkich przedmiotów w grze.
    """
    def __init__(self, name, description, value=0):
        """
        Inicjalizuje przedmiot.
        :param name: Nazwa przedmiotu.
        :param description: Opis przedmiotu.
        :param value: Wartość przedmiotu w złocie (dla potencjalnego sklepu).
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nazwa przedmiotu musi być niepustym ciągiem znaków.")
        if not isinstance(description, str):
            raise ValueError("Opis przedmiotu musi być ciągiem znaków.")
        if not isinstance(value, int) or value < 0:
            raise ValueError("Wartość przedmiotu musi być nieujemną liczbą całkowitą.")

        self.name = name
        self.description = description
        self.value = value
        self.is_magical = False
        self.rarity = "common" 

    def __str__(self):
        """
        Zwraca reprezentację stringową przedmiotu.
        """
        return f"{self.name}: {self.description} (Wartość: {self.value} Złota, Rzadkość: {self.rarity})"

    def examine(self):
        """
        Wyświetla szczegółowy opis przedmiotu.
        """
        print(f"--- {self.name} ---")
        print(f"Opis: {self.description}")
        print(f"Wartość: {self.value} Złota")
        print(f"Rzadkość: {self.rarity}")
        if self.is_magical:
            print("Przedmiot jest magiczny!")
       
        print("Możesz go użyć, sprzedać lub wyrzucić.")
        print("Zastanów się dobrze, co z nim zrobisz.")

class Weapon(Item):
    """
    Klasa reprezentująca broń. Dziedziczy po Item.
    """
    def __init__(self, name, description, damage, weapon_type="melee", value=10):
        """
        Inicjalizuje broń.
        :param name: Nazwa broni.
        :param description: Opis broni.
        :param damage: Obrażenia zadawane przez broń.
        :param weapon_type: Typ broni (np. 'melee', 'ranged').
        :param value: Wartość broni.
        """
        super().__init__(name, description, value)
        if not isinstance(damage, int) or damage <= 0:
            raise ValueError("Obrażenia broni muszą być dodatnią liczbą całkowitą.")
        if weapon_type not in ["melee", "ranged", "magic"]:
            raise ValueError("Nieznany typ broni.")

        self.damage = damage
        self.weapon_type = weapon_type
        self.durability = 100 

    def __str__(self):
        """
        Zwraca reprezentację stringową broni.
        """
        return (f"{self.name} (Broń): {self.description}, Obrażenia: {self.damage}, "
                f"Typ: {self.weapon_type}, Wartość: {self.value}, Rzadkość: {self.rarity}, "
                f"Trwałość: {self.durability}%")

    def sharpen(self):
        """
        Prosta metoda symulująca ostrzenie broni.
        """
        if self.weapon_type == "melee":
            print(f"Ostrzysz {self.name}. Wydaje się być nieco groźniejsza.")
        else:
            print(f"{self.name} nie jest bronią białą, nie możesz jej naostrzyć w ten sposób.")

class Armor(Item):
    """
    Klasa reprezentująca pancerz. Dziedziczy po Item.
    """
    def __init__(self, name, description, defense, armor_type="torso", value=15):
        """
        Inicjalizuje pancerz.
        :param name: Nazwa pancerza.
        :param description: Opis pancerza.
        :param defense: Wartość obrony pancerza.
        :param armor_type: Typ pancerza (np. 'head', 'torso', 'legs').
        :param value: Wartość pancerza.
        """
        super().__init__(name, description, value)
        if not isinstance(defense, int) or defense <= 0:
            raise ValueError("Obrona pancerza musi być dodatnią liczbą całkowitą.")
        if armor_type not in ["head", "torso", "legs", "shield", "full"]:
            raise ValueError("Nieznany typ pancerza.")

        self.defense = defense
        self.armor_type = armor_type
        self.condition = "new" 

    def __str__(self):
        """
        Zwraca reprezentację stringową pancerza.
        """
        return (f"{self.name} (Pancerz): {self.description}, Obrona: {self.defense}, "
                f"Typ: {self.armor_type}, Wartość: {self.value}, Rzadkość: {self.rarity}, "
                f"Stan: {self.condition}")

    def polish(self):
        """
        Prosta metoda symulująca polerowanie pancerza.
        """
        print(f"Polerujesz {self.name}. Lśni jak nowy!")
        if self.condition == "damaged":
            self.condition = "used"
        elif self.condition == "used":
            self.condition = "new" 


class Potion(Item):
    """
    Klasa reprezentująca miksturę. Dziedziczy po Item.
    """
    def __init__(self, name, description, effect_type, effect_value, value=5):
        """
        Inicjalizuje miksturę.
        :param name: Nazwa mikstury.
        :param description: Opis mikstury.
        :param effect_type: Rodzaj efektu (np. 'heal', 'strength_boost').
        :param effect_value: Wartość efektu.
        :param value: Wartość mikstury.
        """
        super().__init__(name, description, value)
        if effect_type not in ["heal", "mana_restore", "strength_boost", "defense_boost"]:
            raise ValueError("Nieznany typ efektu mikstury.")
        if not isinstance(effect_value, int) or effect_value <= 0:
            raise ValueError("Wartość efektu mikstury musi być dodatnią liczbą całkowitą.")

        self.effect_type = effect_type
        self.effect_value = effect_value
        self.sips_left = 1 

    def __str__(self):
        """
        Zwraca reprezentację stringową mikstury.
        """
        return (f"{self.name} (Mikstura): {self.description}, Efekt: {self.effect_type} o {self.effect_value}, "
                f"Wartość: {self.value}, Rzadkość: {self.rarity}, Pozostało łyków: {self.sips_left}")

    def use(self, target):
        """
        Aplikuje efekt mikstury na cel (np. gracza).
        :param target: Obiekt postaci, na którym mikstura ma zadziałać.
        """
        if self.sips_left <= 0:
            print(f"{self.name} jest już pusta.")
            return False

        print(f"Używasz {self.name} na {target.name}.")
        self.sips_left -= 1

        if self.effect_type == "heal":
            target.heal(self.effect_value)
        elif self.effect_type == "mana_restore" and hasattr(target, 'mana'):
            target.restore_mana(self.effect_value)
        elif self.effect_type == "strength_boost":
            if hasattr(target, 'base_attack_power'): 
                target.attack_power += self.effect_value
                print(f"{target.name} czuje przypływ siły! (+{self.effect_value} do ataku na jakiś czas)")
            else:
                print(f"{self.name} nie może zwiększyć siły {target.name} - brak odpowiedniego atrybutu.")
        elif self.effect_type == "defense_boost":
            if hasattr(target, 'base_defense_power'): 
                target.defense_power += self.effect_value
                print(f"{target.name} czuje się bardziej odporny! (+{self.effect_value} do obrony na jakiś czas)")
            else:
                print(f"{self.name} nie może zwiększyć obrony {target.name} - brak odpowiedniego atrybutu.")
        else:
            print(f"Nieznany efekt mikstury: {self.effect_type}")
            return False 

        if self.sips_left == 0:
            print(f"Butelka po {self.name} jest teraz pusta.")
        return True 






