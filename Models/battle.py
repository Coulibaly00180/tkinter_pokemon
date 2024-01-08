from pokemon import Pokemon
from attack import Attack
import random
class Battle:
    def __init__(self, team1, team2):
        """
        Initialise une bataille entre deux équipes de Pokémon.
        :param equipe1: liste d'objets Pokemon
        :param equipe2: liste d'objets Pokemon
        """
        self.team1 = team1
        self.team2 = team2
        self.current_pokemon1 = team1[0]  # Start with the first Pokemon
        self.current_pokemon2 = team2[0]

    def combat_menu(self, current_pokemon, opponent_pokemon, team):
        """
        Affiche le menu de combat et gère le choix du joueur.
        :param current_pokemon: Pokémon actuellement en combat du joueur
        :param opponent_pokemon: Pokémon adverse
        :param team: Équipe du joueur
        """
        while True:
            print(f"\nAu tour de {current_pokemon.name} !")
            print("1. Attaque")
            print("2. Changer de Pokémon")
            print("3. Abandonner le combat")
            choice = input("Que voulez-vous faire ? ")

            if choice == "1":
                # Gérer l'attaque
                self.perform_attack(current_pokemon, opponent_pokemon)
                break  # Fin du tour après l'attaque
            elif choice == "2":
                # Afficher les Pokémon et choisir un remplaçant
                self.show_pokemon_status(team)
                new_pokemon_index = int(input("Choisissez un Pokémon (entrez le numéro) : ")) - 1
                new_pokemon = self.change_pokemon(team, current_pokemon, new_pokemon_index)
                if new_pokemon:
                    return new_pokemon  # Retourner le nouveau Pokémon pour le combat
            elif choice == "3":
                print("Vous avez abandonné le combat.")
                return None  # Retourner None pour signaler l'abandon
            else:
                print("Choix invalide, veuillez réessayer.")

    def type_effectiveness(self, attack_type, defender_type):
        """
        Calcule l'efficacité d'une attaque en fonction du type.
        """
        # Simplified effectiveness chart
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

        return effectiveness_chart.get(attack_type, {}).get(defender_type, 1)
        
    def apply_status_effect(self, attacker, defender, attack):
        """
        Applique un effet de statut ou un changement de statut à un Pokémon.
        """
        # Appliquer l'effet de statut avec la probabilité spécifiée
        if attack.status_effect and random.random() < attack.status_effect_chance:
            # Vérifier le type d'effet de statut et l'appliquer
            if attack.status_effect == "poison":
                defender.status_conditions["poisoned"] = True
                print(f"{defender.name} is poisoned!")
            elif attack.status_effect == "sleep":
                defender.status_conditions["asleep"] = True
                defender.sleep_turns = 2  # Exemple : le Pokémon dort pendant 2 tours
                print(f"{defender.name} s'endort pour 2 tours!")
            elif attack.status_effect == "paralysis":
                defender.status_conditions["paralyzed"] = True
                print(f"{defender.name} is paralyzed!")
            elif attack.status_effect == "freeze":
                defender.status_conditions["frozen"] = True
                print(f"{defender.name} is frozen solid!")
            elif attack.status_effect == "burn":
                defender.status_conditions["burned"] = True
                print(f"{defender.name} is burned!")

        # Appliquer les changements de statistiques si l'attaque en a
        if attack.stat_change:
            target = attacker if attack.stat_change_target == "self" else defender
            for stat, change in attack.stat_change.items():
                setattr(target, stat + "_modifier", getattr(target, stat + "_modifier") + change)
                print(f"La {stat} de {target.name} est modifiée de {change}.")   

    def handle_status_effects(self, pokemon):
        """
        Gère les effets de statut à long terme sur un Pokémon.
        """
        if pokemon.status_conditions["poisoned"]:
            poison_damage = 10  # Valeur exemple
            pokemon.current_health -= poison_damage
            print(f"{pokemon.name} est empoisonné et perd {poison_damage} HP!")

        if pokemon.status_conditions["burned"]:
            burn_damage = 10  # Valeur exemple
            pokemon.current_health -= burn_damage
            print(f"{pokemon.name} est brûlé et perd {burn_damage} HP!")

        if pokemon.status_conditions["asleep"]:
            # Gestion de l'effet de sommeil
            # Par exemple, un Pokémon pourrait rester endormi pendant un certain nombre de tours
            if pokemon.sleep_turns > 0:
                print(f"{pokemon.name} est endormi et ne peut pas attaquer!")
                pokemon.sleep_turns -= 1  # Décompter un tour de sommeil
            else:
                pokemon.status_conditions["asleep"] = False

        if pokemon.status_conditions["paralyzed"]:
            # Gestion de la paralysie
            # Par exemple, un Pokémon paralysé pourrait avoir une chance de ne pas pouvoir attaquer
            if random.randint(0, 1) == 0:  # 50% de chance de ne pas pouvoir attaquer
                print(f"{pokemon.name} est paralysé et ne peut pas bouger!")
            else:
                print(f"{pokemon.name} est paralysé mais peut encore attaquer!")

        if pokemon.status_conditions["frozen"]:
            # Gestion du gel
            # Un Pokémon gelé pourrait rester dans cet état jusqu'à ce qu'il soit dégelé (aléatoirement ou par une attaque spécifique)
            if random.randint(0, 1) == 0:  # Chance de rester gelé
                print(f"{pokemon.name} est toujours gelé solidement!")
            else:
                pokemon.status_conditions["frozen"] = False
                print(f"{pokemon.name} se dégèle!")

        # Vérifiez si le Pokémon est mis K.O. à cause des effets de statut
        if pokemon.current_health <= 0:
            pokemon.is_knocked_out = True
            print(f"{pokemon.name} est mis K.O. par les effets de statut!")



    def perform_round(self):
            """
            Effectue un tour de combat entre les deux Pokémon actuels.
            """
            # Gérer les effets de statut pour chaque Pokémon
            self.handle_status_effects(self.current_pokemon1)
            self.handle_status_effects(self.current_pokemon2)

            # Vérifier les conditions de statut avant l'attaque de l'Équipe 1
            if not self.check_status_before_attack(self.current_pokemon1):
                # Afficher quel Pokémon attaque
                print(f"Équipe 1: {self.current_pokemon1.name} attaque.")
                self.perform_attack(self.current_pokemon1, self.current_pokemon2)

            # Gérer le Pokémon K.O. de l'Équipe 2
            self.handle_knocked_out_pokemon(self.current_pokemon2, self.team2, "Équipe 2")

            # Vérifier les conditions de statut avant l'attaque de l'Équipe 2
            if not self.check_status_before_attack(self.current_pokemon2):
                # Afficher quel Pokémon attaque
                print(f"Équipe 2: {self.current_pokemon2.name} attaque.")
                self.perform_attack(self.current_pokemon2, self.current_pokemon1)

            # Gérer le Pokémon K.O. de l'Équipe 1
            self.handle_knocked_out_pokemon(self.current_pokemon1, self.team1, "Équipe 1")

    def check_status_before_attack(self, pokemon):
        """
        Vérifie les conditions de statut d'un Pokémon avant son attaque.
        Retourne True si le Pokémon ne peut pas attaquer.
        """
        if pokemon.status_conditions["asleep"]:
            print(f"{pokemon.name} est endormi et ne peut pas attaquer!")
            return True
        elif pokemon.status_conditions["paralyzed"]:
            print(f"{pokemon.name} est paralysé et ne peut pas bouger!")
            return True
        # Ajouter d'autres conditions de statut ici
        return False

    def handle_knocked_out_pokemon(self, pokemon, team, team_name):
        """
        Gère un Pokémon K.O. et remplace par le prochain Pokémon disponible.
        """
        if pokemon.is_knocked_out:
            print(f"{team_name}: {pokemon.name} est mis K.O. !")
            next_pokemon = self.next_pokemon(team)
            if next_pokemon:
                print(f"{team_name}: {next_pokemon.name} entre en jeu.")
            else:
                print(f"Tous les Pokémon de {team_name} sont K.O. !")


    def calculate_damage(self, attaquant, attaque, defenseur):
        """
        Calcule les dégâts d'une attaque contre un défenseur.
        """
        efficacite = self.type_effectiveness(attaque.type, defenseur.type)

        # Appliquer le modificateur d'attaque
        attack_stat = max(0, attaquant.attack + attaquant.attack_modifier)
        base_damage = attaque.power * (attack_stat / 30)  # Exemple de formule

        # Appliquer la défense du défenseur
        defense_stat = max(0, defenseur.defense + defenseur.defense_modifier)
        final_damage = max(0, base_damage - defense_stat)

        return final_damage



    def apply_stat_change(self, attaquant, defenseur, attaque):
        """
        Applique les changements de statistiques d'une attaque.
        """
        target = attaquant if attaque.stat_change_target == "self" else defenseur
        for stat, change in attaque.stat_change.items():
            # Mettre à jour le modificateur de la statistique cible
            if stat == "attack":
                target.attack_modifier += change
            elif stat == "defense":
                target.defense_modifier += change
            # et ainsi de suite pour les autres statistiques
            print(f"{target.name}'s {stat} changed by {change}.")



    def perform_attack(self, attaquant, defenseur):
        """
        Effectue une attaque d'un Pokémon sur un autre.
        """
        attaque = attaquant.choose_attack(defenseur.type)
        degats = self.calculate_damage(attaquant, attaque, defenseur)

        # Appliquer les dégâts si l'attaque en a
        if degats > 0:
            defenseur.take_damage(degats)
            print(f"{attaquant.name} utilise {attaque.name} sur {defenseur.name}, causant {degats} de dégâts !")
            print(f"HP restants de {defenseur.name}: {defenseur.current_health}/{defenseur.max_health}")
        else:
            print(f"{attaquant.name} utilise {attaque.name} mais cela n'inflige pas de dégâts.")

        # Appliquer les effets de statut de l'attaque, si existants
        self.apply_status_effect(attaquant, defenseur, attaque)

        # Appliquer les changements de statistiques si l'attaque en a
        if attaque.stat_change:
            self.apply_stat_change(attaquant, defenseur, attaque)

        # Vérifier si le défenseur est mis K.O.
        if defenseur.is_knocked_out:
            print(f"{defenseur.name} est mis K.O. !")


    def next_pokemon(self, equipe):
        """
        Sélectionne automatiquement le prochain Pokémon dans l'équipe.
        """
        for pokemon in equipe:
            if not pokemon.is_knocked_out:
                return pokemon
        return None  # Tous les Pokémon de l'équipe sont mis K.O.


    def is_team_defeated(self, team):
        """
        Vérifie si tous les Pokémon d'une équipe sont mis K.O.
        """
        return all(pokemon.is_knocked_out for pokemon in team)


    def start_battle(self):
        """
        Démarre le combat entre les deux équipes.
        """
        while not self.is_team_defeated(self.team1) and not self.is_team_defeated(self.team2):
            self.perform_round()

            # Vérifier et gérer si un Pokémon est mis K.O.
            if self.current_pokemon2 and self.current_pokemon2.is_knocked_out:
                self.current_pokemon2 = self.next_pokemon(self.team2)
                if self.current_pokemon2:
                    print(f"Équipe 2: {self.current_pokemon2.name} entre en jeu.")
                else:
                    print("Tous les Pokémon de l'Équipe 2 sont K.O. !")
                    break  # Sortir de la boucle si tous les Pokémon d'une équipe sont K.O.

            if self.current_pokemon1 and self.current_pokemon1.is_knocked_out:
                self.current_pokemon1 = self.next_pokemon(self.team1)
                if self.current_pokemon1:
                    print(f"Équipe 1: {self.current_pokemon1.name} entre en jeu.")
                else:
                    print("Tous les Pokémon de l'Équipe 1 sont K.O. !")
                    break  # Sortir de la boucle si tous les Pokémon d'une équipe sont K.O.

        # Déclarer le vainqueur
        if self.is_team_defeated(self.team1):
            print("Équipe 2 Victoire!")
        else:
            print("Équipe 1 Victoire!")



    #"""
    #def start_battle(self):
    #    """
    #    Démarre le combat entre les deux équipes.
    #    """
    #    while not self.is_team_defeated(self.team1) and not self.is_team_defeated(self.team2):
     #       # Tour de l'équipe 1
      #      new_pokemon1 = self.combat_menu(self.current_pokemon1, self.current_pokemon2, self.team1)
       #     if new_pokemon1 is None:  # Le joueur a abandonné
        #        print("Équipe 1 a abandonné le combat !")
         #       break
          #  elif new_pokemon1:
           #     self.current_pokemon1 = new_pokemon1  # Changement de Pokémon
            #else:
             #   # Vérifier si le Pokémon de l'équipe 2 est K.O.
              #  if self.current_pokemon2.is_knocked_out:
               #     self.current_pokemon2 = self.next_pokemon(self.team2)
                #    if self.current_pokemon2:
                 #       print(f"Équipe 2: {self.current_pokemon2.name} entre en jeu.")
                  #  else:
                   #     print("Tous les Pokémon de l'Équipe 2 sont K.O. !")
                    #    break

            # Tour de l'équipe 2 (similaire à celui de l'équipe 1)
            # Assurez-vous de gérer le tour de l'équipe 2 ici

            # Vérifier si le Pokémon de l'équipe 1 est K.O.
           # if self.current_pokemon1 and self.current_pokemon1.is_knocked_out:
            #    self.current_pokemon1 = self.next_pokemon(self.team1)
             #   if self.current_pokemon1:
              #      print(f"Équipe 1: {self.current_pokemon1.name} entre en jeu.")
               # else:
                #    print("Tous les Pokémon de l'Équipe 1 sont K.O. !")
                 #   break

            # Vous pouvez ajouter ici la logique pour le tour de l'équipe 2
    #"""



    def change_pokemon(self, team, current_pokemon, new_pokemon_index):
        """
        Change le Pokémon actuellement en combat.
        :param team: liste de Pokémon de l'équipe
        :param current_pokemon: Pokémon actuellement en combat
        :param new_pokemon_index: index du nouveau Pokémon dans l'équipe
        """
        
        if new_pokemon_index < 0 or new_pokemon_index >= len(team):
            print("Choix de Pokémon invalide.")
            return

        if team[new_pokemon_index].is_knocked_out:
            print(f"{team[new_pokemon_index].name} est K.O. et ne peut pas combattre.")
            return

        if team[new_pokemon_index] == current_pokemon:
            print(f"{current_pokemon.name} est déjà en combat.")
            return

        # Remplacer le Pokémon actuel par le nouveau
        print(f"{current_pokemon.name} revient. {team[new_pokemon_index].name} entre en combat.")
        return team[new_pokemon_index]

    def show_pokemon_status(self, team):
        """
        Affiche le statut de chaque Pokémon de l'équipe.
        :param team: liste des Pokémon de l'équipe
        """
        for index, pokemon in enumerate(team):
            status_info = "K.O." if pokemon.is_knocked_out else f"HP: {pokemon.current_health}/{pokemon.max_health}"
            status_effects = ", ".join([condition for condition, active in pokemon.status_conditions.items() if active])
            status_effects_info = f" - Statut: {status_effects}" if status_effects else ""
            print(f"{index + 1}. {pokemon.name} - {status_info}{status_effects_info}")
   
# Création des Pokémon avec quatre attaques chacun

# Création d'attaques de base
flame_thrower = Attack("Flame Thrower", "Fire", 90)
aqua_tail = Attack("Aqua Tail", "Water", 85)
thunder_shock = Attack("Thunder Shock", "Electric", 40)
vine_whip = Attack("Vine Whip", "Grass", 45)

# Attaques avec effets de statut
sleep_powder = Attack("Sleep Powder", "Grass", 0, status_effect="sleep")
thunder_wave = Attack("Thunder Wave", "Electric", 0, status_effect="paralysis")

# Attaque infligeant des dégâts et ayant une chance de brûler
flame_thrower = Attack("Flame Thrower", "Fire", 90, status_effect="burn", status_effect_chance=0.1)

# Attaque infligeant des dégâts et ayant une chance de paralyser
thunder_shock = Attack("Thunder Shock", "Electric", 40, status_effect="paralysis", status_effect_chance=0.1)


# Attaques modifiant les statistiques
defense_curl = Attack("Defense Curl", "Normal", 0, stat_change={"defense": 1}, stat_change_target="self")
growl = Attack("Growl", "Normal", 0, stat_change={"attack": -1}, stat_change_target="opponent")
agility = Attack("Agility", "Psychic", 0, stat_change={"speed": 2}, stat_change_target="self")


# Pokémon pour l'équipe 1
charizard = Pokemon("Charizard", "Fire", 100, [flame_thrower, sleep_powder, defense_curl, agility], 50, 45, 80)  # Exemple de stats
venusaur = Pokemon("Venusaur", "Grass", 120, [vine_whip, thunder_wave, growl, agility], 40, 50, 60)
blastoise = Pokemon("Blastoise", "Water", 110, [aqua_tail, thunder_shock, defense_curl, sleep_powder], 45, 55, 70)

# Pokémon pour l'équipe 2
pikachu = Pokemon("Pikachu", "Electric", 80, [thunder_shock, sleep_powder, defense_curl, agility], 35, 30, 120)
eevee = Pokemon("Eevee", "Normal", 95, [growl, thunder_wave, vine_whip, flame_thrower], 45, 40, 55)
jigglypuff = Pokemon("Jigglypuff", "Normal", 100, [sleep_powder, aqua_tail, thunder_wave, vine_whip], 30, 45, 60)

# Création des équipes
team1 = [charizard, venusaur, blastoise]
team2 = [pikachu, eevee, jigglypuff]

# Démarrage de la bataille
battle = Battle(team1, team2)
battle.start_battle()
