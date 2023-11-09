from dataclasses import dataclass


@dataclass
class PokemonStatsDTO:
    def __init__(self, id, name, type1, type2, moves, weight, height, hp, attack, defense, sp_atk, sp_def, speed):
        self.id = id
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.moves = moves
        self.weight = weight
        self.height = height
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed
