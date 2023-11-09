from dataclasses import dataclass


@dataclass
class PokemonSpeciesDTO:
    def __init__(self, id, name, gender_rate, base_happiness, is_baby, is_legendary, is_mythical, hatch_counter, has_gender_differences, forms_switchable):
        self.id = id
        self.name = name
        self.gender_rate = gender_rate
        self.base_happiness = base_happiness
        self.is_baby = is_baby
        self.is_legendary = is_legendary
        self.is_mythical = is_mythical
        self.hatch_counter = hatch_counter
        self.has_gender_differences = has_gender_differences
        self.forms_switchable = forms_switchable
