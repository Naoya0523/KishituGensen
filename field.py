
from Status import *

class Field:
    def __init__(self):
        self.field_name = None
        self.status_1s = set()
        self.status_2s = set()
        self.status_3s = set()

class CentralArea(Field):
    def __init__(self):
        super().__init__()

        self.field_name = '中枢エリア'

        self.status_1s = {SPEED, STRENGTH, MEANING, INTELLIGENCE, MAINABILITY}
        self.status_2s = {ATTACK, SCORCHING, ELECTROMAGNETIC, COLD, NATURE, ARTSSTRENGTH, ULTIMATEEFFICIENCY, ARTSDAMAGE}
        self.status_3s = {ALLOUT, PURSUIT, CRUSHING, SKILL, ERUPTION, SUPPRESSION, REFLOW, EFFICIENCY}


class OriginiumPark(Field):
    def __init__(self):
        super().__init__()

        self.field_name = '源石研究パーク'
        self.status_1s = {SPEED, STRENGTH, MEANING, INTELLIGENCE, MAINABILITY}
        self.status_2s = {ATTACK, PHYSICAL, ELECTROMAGNETIC, COLD, NATURE, CRITICAL, ULTIMATEEFFICIENCY, ARTSDAMAGE}
        self.status_3s = {SUPPRESSION, PURSUIT, SOARING, SKILL, TECHNICALSKILL, HEALING, BONECUTTING, EFFICIENCY}

class MiningArea(Field):
    def __init__(self):
        super().__init__()

        self.field_name = '鉱山エリア'
        self.status_1s = {SPEED, STRENGTH, MEANING, INTELLIGENCE, MAINABILITY}
        self.status_2s = {HP, PHYSICAL, SCORCHING, COLD, NATURE, CRITICAL, ARTSSTRENGTH, HEALINGEFFICIENCY}
        self.status_3s = {ALLOUT, SUPPRESSION, SKILL, BRUTAL, TECHNICALSKILL, ERUPTION, NIGHTFALL, EFFICIENCY}

class EnergyHighlands(Field):
    def __init__(self):
        super().__init__()

        self.field_name = 'エネルギー高地'
        self.status_1s = {SPEED, STRENGTH, MEANING, INTELLIGENCE, MAINABILITY}
        self.status_2s = {ATTACK, HP, PHYSICAL, SCORCHING, NATURE, CRITICAL, ARTSSTRENGTH, HEALINGEFFICIENCY}
        self.status_3s = {PURSUIT, CRUSHING, SOARING, BRUTAL, TECHNICALSKILL, HEALING, BONECUTTING, REFLOW}

class WulingCastle(Field):
    def __init__(self):
        super().__init__()

        self.field_name = '武陵城'
        self.status_1s = {SPEED, STRENGTH, MEANING, INTELLIGENCE, MAINABILITY}
        self.status_2s = {ATTACK, HP, ELECTROMAGNETIC, COLD, CRITICAL, ULTIMATEEFFICIENCY, ARTSDAMAGE, HEALINGEFFICIENCY}
        self.status_3s = {ALLOUT, CRUSHING, BRUTAL, HEALING, BONECUTTING, ERUPTION, NIGHTFALL, REFLOW}
