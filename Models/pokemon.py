from attack import Attack
import random
import requests

class Pokemon:
    def __init__(self, name, p_type, health, attacks, attack, defense, speed):
        """
        Initialise un Pokémon avec ses attributs de base.
        :param name: Nom du Pokémon.
        :param p_type: Type du Pokémon.
        :param health: Points de vie du Pokémon.
        :param attacks: Liste d'objets Attack.
        :param defense: Valeur de défense du Pokémon.
        :param speed: Vitesse du Pokémon, déterminant l'ordre d'attaque dans les combats.
        """
        self.name = name
        self.type = p_type
        self.max_health = health
        self.current_health = health
        self.attacks = attacks  # Liste des objets Attack
        self.attack = attack  # Valeur de base de l'attaque
        self.defense = defense  # Valeur de base de la défense
        self.speed = speed
        self.is_knocked_out = False
        self.sleep_turns = 0
        self.status_conditions = {
            "poisoned": False, 
            "asleep": False, 
            "paralyzed": False,
            "frozen": False,
            "burned": False
        }
        self.attack_modifier = 0
        self.defense_modifier = 0
        self.speed_modifier = 0

    def take_damage(self, damage):
        """
        Reduce the Pokemon's health by the given damage amount.
        """
        self.current_health -= damage
        if self.current_health <= 0:
            self.current_health = 0
            self.is_knocked_out = True

    def heal(self, amount):
        """
        Heal the Pokemon by a given amount.
        """
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    
    def choose_attack(self, opponent_type):
        """
        Choisi une attaque aléatoirement parmi celles qui sont efficaces contre le type de l'adversaire.
        :param opponent_type: string, le type du Pokémon adverse
        """
        # Filtrer les attaques pour sélectionner celles qui sont les plus efficaces
        effective_attacks = [attack for attack in self.attacks if self.is_effective(attack, opponent_type)]

        if effective_attacks:
            # Choisir une attaque aléatoirement parmi les attaques efficaces
            return random.choice(effective_attacks)
        else:
            # Si aucune attaque n'est particulièrement efficace, choisir une attaque au hasard
            return random.choice(self.attacks)

    def is_effective(self, attack, opponent_type):
        """
        Détermine si une attaque est efficace contre un type de Pokémon donné.
        :param attack: objet Attack, l'attaque à évaluer
        :param opponent_type: string, le type du Pokémon adverse
        """
        # Utiliser un tableau d'efficacité pour déterminer si l'attaque est efficace
        effectiveness_chart = {
            "Normal": {"Combat": 0.5},
            "Feu": {"Eau": 0.5, "Sol": 0.5, "Roche": 0.5, "Plante": 2, "Glace": 2, "Insecte": 2, "Acier": 2},
            "Eau": {"Électrik": 0.5, "Plante": 0.5, "Feu": 2, "Sol": 2, "Roche": 2},
            "Électrik": {"Sol": 0.5, "Eau": 2, "Vol": 2},
            "Plante": {"Feu": 0.5, "Glace": 0.5, "Poison": 0.5, "Vol": 0.5, "Insecte": 0.5, "Eau": 2, "Sol": 2, "Roche": 2},
            "Glace": {"Feu": 0.5, "Combat": 0.5, "Roche": 0.5, "Acier": 0.5, "Plante": 2, "Sol": 2, "Vol": 2, "Dragon": 2},
            "Combat": {"Vol": 0.5, "Psy": 0.5, "Fée": 0.5, "Normal": 2, "Glace": 2, "Roche": 2, "Ténèbres": 2, "Acier": 2},
            "Poison": {"Sol": 0.5, "Psy": 0.5, "Plante": 2, "Fée": 2},
            "Sol": {"Eau": 0.5, "Plante": 0.5, "Glace": 0.5, "Feu": 2, "Électrik": 2, "Poison": 2, "Roche": 2, "Acier": 2},
            "Vol": {"Électrik": 0.5, "Glace": 0.5, "Roche": 0.5, "Combat": 2, "Insecte": 2, "Plante": 2},
            "Psy": {"Insecte": 0.5, "Spectre": 0.5, "Ténèbres": 0.5, "Combat": 2, "Poison": 2},
            "Insecte": {"Feu": 0.5, "Vol": 0.5, "Roche": 0.5, "Plante": 2, "Psy": 2, "Ténèbres": 2},
            "Roche": {"Eau": 0.5, "Plante": 0.5, "Combat": 0.5, "Sol": 0.5, "Acier": 0.5, "Feu": 2, "Glace": 2, "Vol": 2, "Insecte": 2},
            "Spectre": {"Spectre": 2, "Psy": 2, "Ténèbres": 0.5},
            "Dragon": {"Glace": 0.5, "Dragon": 2, "Fée": 0.5},
            "Ténèbres": {"Combat": 0.5, "Insecte": 0.5, "Fée": 0.5, "Psy": 2, "Spectre": 2},
            "Acier": {"Feu": 0.5, "Combat": 0.5, "Sol": 0.5, "Glace": 2, "Roche": 2, "Fée": 2},
            "Fée": {"Poison": 0.5, "Acier": 0.5, "Combat": 2, "Dragon": 2, "Ténèbres": 2}
        }
        effectiveness = effectiveness_chart.get(attack.type, {}).get(opponent_type, 1)
        return effectiveness > 1


    # Recuperer 10 pokemon
def get_pokemons(page=1, limit=10):
    offset = (page - 1) * limit
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}')
    return response.json()

# Afficher les informations d'un pokémon
def get_pokemon_details(pokedex_number):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokedex_number}/"
    response = requests.get(url)
    pokemon_details = response.json()

    attacks = pokemon_details['moves']
    attack_names = [attack['move']['name'] for attack in attacks]

    return {
        'name': pokemon_details['name'],
        'image': pokemon_details['sprites']['other']['official-artwork']['front_default'],
        'types': [type['type']['name'] for type in pokemon_details['types']],
        'height': pokemon_details['height'],
        'weight': pokemon_details['weight'],
        'stats': [base_stat['stat']['name'] for base_stat in pokemon_details['stats']],
        'stats_of': [{'name': stat['stat']['name'], 'value': stat['base_stat']} for stat in pokemon_details['stats']],
        'attacks': attack_names,
    }

    def search_pokemon(name):
        name = name.lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = request.get(url)
        return response

    def __str__(self):
        return f"{self.name} ({self.type}): {self.current_health}/{self.max_health} HP"
