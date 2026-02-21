
from Status import *

class Weapon:
    def __init__(self):
        self.name = None

        self.status_1 = None
        self.status_2 = None
        self.status_3 = None

        self.is_owned = True

    def getStatus(self, Number):
        if Number==1:
            return self.status_1
        elif Number==2:
            return self.status_2
        else:
            return self.status_3


# 武器

class Hototogisu(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "不知帰"
        self.status_1 = MEANING
        self.status_2 = ATTACK
        self.status_3 = REFLOW

class Kagami(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "鑑"
        self.status_1 = MAINABILITY
        self.status_2 = ATTACK
        self.status_3 = SUPPRESSION

class SimeiHittatu(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "使命必達"
        self.status_1 = MEANING
        self.status_2 = ULTIMATEEFFICIENCY
        self.status_3 = PURSUIT

class KishiSeishin(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "騎士精神"
        self.status_1 = MEANING
        self.status_2 = HP
        self.status_3 = HEALING

class Ibou(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "遺忘"
        self.status_1 = INTELLIGENCE
        self.status_2 = ARTSDAMAGE
        self.status_3 = NIGHTFALL

class Kusabi(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "楔"
        self.status_1 = MAINABILITY
        self.status_2 = CRITICAL
        self.status_3 = TECHNICALSKILL

class TelmitCutter(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "テルミット・カッター"
        self.status_1 = MEANING
        self.status_2 = ATTACK
        self.status_3 = REFLOW

class ByakuyShinsei(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "白夜新星"
        self.status_1 = MAINABILITY
        self.status_2 = ARTSSTRENGTH
        self.status_3 = TECHNICALSKILL

class FlameForge(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "フレイムフォージ"
        self.status_1 = INTELLIGENCE
        self.status_2 = ATTACK
        self.status_3 = NIGHTFALL

class DouruiKyoushoku(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "同類共食"
        self.status_1 = MAINABILITY
        self.status_2 = ARTSDAMAGE
        self.status_3 = TECHNICALSKILL

class Yumou(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "勇猛"
        self.status_1 = SPEED
        self.status_2 = PHYSICAL
        self.status_3 = SKILL

class MukasibinoIppin(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "昔日の逸品"
        self.status_1 = MEANING
        self.status_2 = HP
        self.status_3 = EFFICIENCY

class HakaiUnit(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "破壊ユニット"
        self.status_1 = MAINABILITY
        self.status_2 = ARTSSTRENGTH
        self.status_3 = ERUPTION

class HasaiKunshu(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "破砕君主"
        self.status_1 = STRENGTH
        self.status_2 = CRITICAL
        self.status_3 = CRUSHING

class JET(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "J.E.T"
        self.status_1 = MAINABILITY
        self.status_2 = ATTACK
        self.status_3 = SUPPRESSION

class SouseinoSasayaki(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "蒼星の囁き"
        self.status_1 = INTELLIGENCE
        self.status_2 = HEALINGEFFICIENCY
        self.status_3 = TECHNICALSKILL

class Taigan(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "大願"
        self.status_1 = SPEED
        self.status_2 = ATTACK
        self.status_3 = TECHNICALSKILL

class Huyao(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "フーヤオ"
        self.status_1 = MAINABILITY
        self.status_2 = CRITICAL
        self.status_3 = NIGHTFALL

class Huzan(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "負山"
        self.status_1 = SPEED
        self.status_2 = PHYSICAL
        self.status_3 = EFFICIENCY

class KagayakasikiMeisei(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "輝かしき名声"
        self.status_1 = MAINABILITY
        self.status_2 = PHYSICAL
        self.status_3 = BRUTAL

class Dairaihan(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "大雷斑"
        self.status_1 = STRENGTH
        self.status_2 = HP
        self.status_3 = HEALING