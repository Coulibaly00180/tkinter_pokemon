class Team:
    def __init__(self, nom_equipe):
        self.nom_equipe = nom_equipe
        self.pokemons = []

    def ajouter_pokemon(self, pokemon):
        if len(self.pokemons) < 6:
            self.pokemons.append(pokemon)
            print(f"{pokemon.nom} a été ajouté à l'équipe {self.nom_equipe}.")
        else:
            print(f"L'équipe {self.nom_equipe} est déjà complète. Vous ne pouvez pas ajouter plus de Pokémon.")

    def afficher_equipe(self):
        if not self.pokemons:
            print(f"L'équipe {self.nom_equipe} est vide.")
            return
        print(f"Équipe {self.nom_equipe} :")
        for pokemon in self.pokemons:
            pokemon.afficher()
            print()

    def est_pleine(self):
        return len(self.pokemons) == 6

    def obtenir_pokemon_actif(self):
        for pokemon in self.pokemons:
            if not pokemon.est_ko():
                return pokemon
        return None  # Tous les Pokémon sont KO
