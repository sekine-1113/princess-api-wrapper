from enum import IntEnum


class IdolType(IntEnum):
    Princess = 1
    Fairy = 2
    Angel = 3
    Ex = 5


class CardRarity(IntEnum):
    N = 1
    R = 2
    SR = 3
    SSR = 4


class ExType(IntEnum):
    Null = 0
    PST = 1
    PSTR = 2
    PSTP = 3
    Fes = 4
    Anniversary_1st = 5
    Extra = 6
    Anniversary_2nd = 7
    ExtraPSTR = 8
    ExtraPSTP = 9
    Anniversary_3rd = 10
    ExtraPSTR_2 = 11
    ExtraPSTP_2 = 12
    Anniversary_4th = 13
    SHS = 14
    Special = 15
    Anniversary_5th = 16


class EventType(IntEnum):
    Showtime = 1
    Millicolle = 2
    Theater = 3
    Tour = 4
    Anniversary = 5
    Working = 6
    Aprilfool =7
    Gamecorner = 8
    Millicolle_box_gasha = 9
    Twinstage = 10
    Tune = 11
    Twinstage_total_highscore = 12
    Tale = 13
    Talkparty = 14
    Treasure = 16


class Lang:
    Japanese = "ja"
    Korean = "ko"
    Chinese = "zh"
