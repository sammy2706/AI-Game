import random
import time
from typing import List, Dict, Optional

class Character:
    """Represents the player character."""
    def __init__(self, name: str, char_class: str):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.exp = 0
        self.inventory = []
        self.stats = self.init_stats(char_class)
        self.abilities = self.init_abilities(char_class)
    
    def init_stats(self, char_class: str) -> Dict[str, int]:
        """Initialize stats based on character class."""
        if char_class == "Warrior":
            return {
                "health": 100,
                "max_health": 100,
                "strength": 15,
                "agility": 10,
                "magic": 5
            }
        elif char_class == "Mage":
            return {
                "health": 70,
                "max_health": 70,
                "strength": 5,
                "agility": 8,
                "magic": 20
            }
        else:  # Rogue
            return {
                "health": 80,
                "max_health": 80,
                "strength": 10,
                "agility": 20,
                "magic": 8
            }

    def init_abilities(self, char_class: str) -> List[str]:
        """Initialize abilities based on character class."""
        if char_class == "Warrior":
            return ["Heavy Strike", "Defend", "Rally"]
        elif char_class == "Mage":
            return ["Fireball", "Ice Shield", "Heal"]
        else:  # Rogue
            return ["Backstab", "Dodge", "Poison"]

    def use_ability(self, ability: str, target) -> tuple[str, int]:
        """Use an ability and return the result."""
        damage = 0
        message = ""
        
        if ability == "Heavy Strike":
            damage = self.stats["strength"] * 1.5
            message = f"{self.name} performs a powerful strike!"
        elif ability == "Fireball":
            damage = self.stats["magic"] * 2
            message = f"{self.name} launches a blazing fireball!"
        elif ability == "Backstab":
            damage = self.stats["agility"] * 1.8
            message = f"{self.name} strikes from the shadows!"
        elif ability in ["Defend", "Ice Shield", "Dodge"]:
            self.stats["health"] += 10
            message = f"{self.name} takes a defensive stance!"
        elif ability == "Heal":
            heal_amount = self.stats["magic"]
            self.stats["health"] = min(self.stats["max_health"], self.stats["health"] + heal_amount)
            message = f"{self.name} heals for {heal_amount} health!"
        
        # Returning a message and the amount of damage dealt or healing done
        return message, int(damage)


class Enemy:
    """Represents an enemy in combat."""
    def __init__(self, name: str, difficulty: str):
        self.name = name
        self.difficulty = difficulty
        self.stats = self.init_stats(difficulty)
        self.abilities = ["Attack", "Special"]

    def init_stats(self, difficulty: str) -> Dict[str, int]:
        """Initialize stats based on enemy difficulty."""
        if difficulty == "Easy":
            return {"health": 50, "strength": 8, "agility": 5}
        elif difficulty == "Medium":
            return {"health": 80, "strength": 12, "agility": 8}
        else:  # Hard
            return {"health": 120, "strength": 15, "agility": 12}

    def use_ability(self) -> tuple[str, int]:
        """Enemy uses an ability to attack the player."""
        ability = random.choice(self.abilities)
        damage = 0
        message = ""
        
        if ability == "Attack":
            damage = self.stats["strength"]
            message = f"{self.name} attacks!"
        else:  # Special
            damage = self.stats["strength"] * 1.5
            message = f"{self.name} uses a special attack!"
        
        # Returning a message and the amount of damage dealt
        return message, int(damage)


class Game:
    """Manages the game flow, locations, and player interaction."""
    def __init__(self):
        self.player = None
        self.current_location = "start"
        self.game_over = False
        self.dragon_befriended = False  # New flag for befriending the dragon
        self.locations = self.init_locations()

    def init_locations(self):
        """Initialize locations with their associated descriptions and options."""
        return {
            "start": {
                "name": "Village of Beginning",
                "description": "A peaceful village where your journey begins.",
                "options": ["haunted_forest", "enchanted_castle"]
            },
            "haunted_forest": {
                "name": "The Haunted Forest",
                "description": "A dark and misty forest filled with mysterious creatures.",
                "options": ["bandits_lair", "dragon_cave"]
            },
            "enchanted_castle": {
                "name": "The Enchanted Castle",
                "description": "A magnificent castle shrouded in magical energy.",
                "options": ["dragon_cave", "final_tower"]
            },
            "bandits_lair": {
                "name": "The Bandit's Lair",
                "description": "A hidden stronghold of dangerous outlaws.",
                "options": ["final_tower"]
            },
            "dragon_cave": {
                "name": "The Dragon's Cave",
                "description": "Home to an ancient dragon. A strange energy surrounds the place.",
                "options": ["final_tower", "befriend_dragon"]  # Added the option here
            },
            "befriend_dragon": {
                "name": "Dragon's Lair (Befriend)",
                "description": "You decided to befriend the dragon. The dragon offers you a powerful gift and guides you towards victory.",
                "options": []
            },
            "final_tower": {
                "name": "The Tower of Destiny",
                "description": "The final challenge awaits.",
                "options": []
            }
        }

    def start_game(self):
        """Start the game, allow character creation, and begin the adventure."""
        print("Welcome to the Epic Quest!")
        print("\nChoose your character class:")
        print("1. Warrior - Strong and tough")
        print("2. Mage - Magical and wise")
        print("3. Rogue - Quick and cunning")
        
        while True:
            choice = input("\nEnter your choice (1-3): ")
            if choice in ["1", "2", "3"]:
                break
            print("Invalid choice. Please try again.")
        
        name = input("\nEnter your character's name: ")
        char_class = {
            "1": "Warrior",
            "2": "Mage",
            "3": "Rogue"
        }[choice]
        
        self.player = Character(name, char_class)
        print(f"\nWelcome, {name} the {char_class}!")
        self.play_game()

    def play_game(self):
        """Main game loop."""
        while not self.game_over:
            if self.dragon_befriended:  # Skip the loop if the dragon is befriended
                break
            self.show_location()
            self.handle_location()
            
            # After each action, check if the player has been defeated
            if self.player.stats["health"] <= 0:
                self.end_game("defeat")
                break


    def show_location(self):
        """Show the player's current location and available paths."""
        location = self.locations[self.current_location]
        print(f"\n=== {location['name']} ===")
        print(location["description"])
        
        if location["options"]:
            print("\nPossible paths:")
            for i, option in enumerate(location["options"], 1):
                print(f"{i}. {self.locations[option]['name']}")

    def handle_location(self):
        """Handle actions available at the current location."""
        location = self.locations[self.current_location]
        
        if not location["options"]:
            self.final_challenge()
            return
        
        # Random encounter chance
        if random.random() < 0.7:  # 70% chance of encounter
            self.handle_encounter()
        
        print("\nWhat would you like to do?")
        print("1. Move to next location")
        print("2. Check inventory")
        print("3. View character stats")
        
        while True:
            choice = input("Enter your choice (1-3): ")
            if choice == "1":
                self.choose_next_location()
                break
            elif choice == "2":
                self.show_inventory()
            elif choice == "3":
                self.show_stats()
            else:
                print("Invalid choice. Please try again.")

    def handle_encounter(self):
        """Random encounter with an enemy."""
        difficulties = ["Easy", "Medium", "Hard"]
        enemy_types = ["Goblin", "Troll", "Dark Knight", "Evil Mage", "Shadow Beast"]
        
        enemy = Enemy(random.choice(enemy_types), random.choice(difficulties))
        print(f"\nA {enemy.name} appears!")
        
        while enemy.stats["health"] > 0 and self.player.stats["health"] > 0:
            print(f"\n{self.player.name} HP: {self.player.stats['health']}")
            print(f"{enemy.name} HP: {enemy.stats['health']}")

            print("\nYour abilities:")
            for i, ability in enumerate(self.player.abilities, 1):
                print(f"{i}. {ability}")

            while True:
                try:
                    choice = int(input("Choose your ability (number): "))
                    if 1 <= choice <= len(self.player.abilities):
                        break
                    print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a number.")

            # Player turn
            message, damage = self.player.use_ability(self.player.abilities[choice-1], enemy)
            print(message)
            enemy.stats["health"] -= damage
            print(f"Dealt {damage} damage!")
            
            if enemy.stats["health"] <= 0:
                print(f"\nYou defeated the {enemy.name}!")
                self.handle_loot()
                self.after_battle()  # Call self.after_battle() to give player a chance to rest after battle
                break
            
            # Enemy turn
            message, damage = enemy.use_ability()
            print(message)
            self.player.stats["health"] -= damage
            print(f"Took {damage} damage!")

            # Check if player is defeated
            if self.player.stats["health"] <= 0:
                print("\nYou have been defeated!")
                self.end_game("defeat")
                break

    def after_battle(self):
        """Allow the player to rest and recover health after battle."""
        if self.player.stats["health"] < self.player.stats["max_health"]:
            print(f"\nYour current health is {self.player.stats['health']}/{self.player.stats['max_health']}.")
            print("Would you like to rest and recover some health?")
            print("1. Yes")
            print("2. No")

            while True:
                choice = input("Enter your choice (1-2): ")
                if choice == "1":
                    self.rest()
                    break
                elif choice == "2":
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("You are at full health and ready to continue.")

    def rest(self):
        """Restore some health to the player."""
        heal_amount = 20  # Amount of health to restore
        self.player.stats["health"] = min(self.player.stats["max_health"], self.player.stats["health"] + heal_amount)
        print(f"You rest and recover {heal_amount} health. Your current health is {self.player.stats['health']}/{self.player.stats['max_health']}.")

    def handle_loot(self):
        """Handle loot after defeating an enemy."""
        items = ["Health Potion", "Strength Elixir", "Magic Scroll", "Ancient Artifact"]
        item = random.choice(items)
        self.player.inventory.append(item)
        print(f"You found a {item}!")

    def show_inventory(self):
        """Show the player's inventory."""
        if not self.player.inventory:
            print("\nYour inventory is empty.")
            return
        
        print("\nInventory:")
        for i, item in enumerate(self.player.inventory, 1):
            print(f"{i}. {item}")

        print("\nWould you like to use an item? (y/n)")
        if input().lower() == 'y':
            try:
                choice = int(input("Enter item number: "))
                if 1 <= choice <= len(self.player.inventory):
                    item = self.player.inventory.pop(choice-1)
                    self.use_item(item)
                else:
                    print("Invalid item number.")
            except ValueError:
                print("Please enter a valid number.")

    def use_item(self, item: str):
        """Use an item from the inventory."""
        if item == "Health Potion":
            heal = 30
            self.player.stats["health"] = min(self.player.stats["max_health"], 
                                            self.player.stats["health"] + heal)
            print(f"Healed for {heal} health!")
        elif item == "Strength Elixir":
            self.player.stats["strength"] += 5
            print("Strength increased!")
        elif item == "Magic Scroll":
            self.player.stats["magic"] += 5
            print("Magic increased!")
        elif item == "Ancient Artifact":
            self.player.stats["strength"] += 3
            self.player.stats["agility"] += 3
            self.player.stats["magic"] += 3
            print("All stats increased!")

    def show_stats(self):
        """Display the player's current stats."""
        print(f"\n=== {self.player.name}'s Stats ===")
        for stat, value in self.player.stats.items():
            print(f"{stat.capitalize()}: {value}")

    def choose_next_location(self):
        """Choose the next location to explore."""
        current = self.locations[self.current_location]
        options = current["options"]
        
        if not options:
            return

        print("\nChoose your next destination:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {self.locations[option]['name']}")

        while True:
            try:
                choice = int(input("Enter your choice: "))
                if 1 <= choice <= len(options):
                    next_location = options[choice-1]
                    if next_location == "befriend_dragon":
                        self.befriend_dragon()  # Trigger the befriend action
                        return  # Exit method after befriending to avoid loops
                    self.current_location = next_location
                    break
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def befriend_dragon(self):
        """Handle the interaction with the dragon."""
        print("\nYou have chosen to befriend the dragon. The dragon offers you a powerful gift and guides you toward victory.")
        self.player.stats["strength"] += 10
        self.player.stats["magic"] += 10
        self.dragon_befriended = True  # Set the flag to True
        self.end_game("victory_befriend")  # End the game immediately after befriending




    def end_game(self, reason: str):
        """End the game and provide appropriate feedback."""
        self.game_over = True
        if reason == "victory":
            print("\nCongratulations! You have completed your epic quest.")
        elif reason == "victory_befriend":
            print("\nYou befriended the dragon and were guided toward a peaceful victory!")  # New message for befriending the dragon
        else:  # Reason is "defeat"
            print("\nGame Over! Your journey has come to an end.")
        
        # Ask player if they want to play again
        print("\nWould you like to play again? (y/n)")
        if input().lower() == 'y':
            self.__init__()  # Reset the game state
            self.start_game()  # Start a new game
        else:
            print("Thanks for playing!")
            exit()


    def final_challenge(self):
        """This should not be called if the player befriended the dragon."""
        if self.current_location == "befriend_dragon":
            return  # Skip final challenge if the player befriended the dragon
            
        print("\nFinal Challenge: The Dark Overlord approaches!")
        boss = Enemy("Dark Overlord", "Hard")
        
        # Boss battle loop
        while boss.stats["health"] > 0 and self.player.stats["health"] > 0:
            print(f"\n{self.player.name} HP: {self.player.stats['health']}")
            print(f"{boss.name} HP: {boss.stats['health']}")
            
            # Show player abilities
            print("\nYour abilities:")
            for i, ability in enumerate(self.player.abilities, 1):
                print(f"{i}. {ability}")
            
            while True:
                try:
                    choice = int(input("Choose your ability (number): "))
                    if 1 <= choice <= len(self.player.abilities):
                        break
                    print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a number.")
            
            # Player turn
            message, damage = self.player.use_ability(self.player.abilities[choice-1], boss)
            print(message)
            boss.stats["health"] -= damage
            print(f"Dealt {damage} damage!")
            
            if boss.stats["health"] <= 0:
                print(f"\nYou defeated {boss.name}! The realm is saved!")
                self.end_game("victory")
                break
            
            # Enemy turn
            message, damage = boss.use_ability()
            print(message)
            self.player.stats["health"] -= damage
            print(f"Took {damage} damage!")



if __name__ == "__main__":
    game = Game()
    game.start_game()
