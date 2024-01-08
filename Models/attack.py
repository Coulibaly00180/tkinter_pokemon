class Attack:
    def __init__(self, name, a_type, power, status_effect=None, status_effect_chance=0, status_change=None, stat_change=None, stat_change_target="self"):
        """
        Initialise une attaque avec ses attributs de base et des effets supplémentaires.
        :param name: Nom de l'attaque.
        :param a_type: Type de l'attaque.
        :param power: Puissance de l'attaque.
        :param status_effect: Effet de statut infligé par l'attaque (par exemple, "poison").
        :param status_change: Changement de statut provoqué par l'attaque (par exemple, diminution de la vitesse).
        :param stat_change: Changement de stat
        """
        self.name = name
        self.type = a_type
        self.power = power  # Puissance de l'attaque
        self.status_effect = status_effect  # Effet de statut potentiel
        self.status_effect_chance = status_effect_chance  # Probabilité de l'effet de statut (0 à 1)
        self.status_change = status_change
        self.stat_change = stat_change
        self.stat_change_target = stat_change_target  # "self" ou "opponent"

    def __str__(self):
        return f"{self.name} ({self.type}, Power: {self.power}, Status Effect: {self.status_effect})"
