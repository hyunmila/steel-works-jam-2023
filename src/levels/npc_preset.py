import pygame
from core.animation import Animation
from components.dialog_box import DialogBox
from components.npc import NPC
from core.color import Color
from components.map import Tile

NPC_JOLA = Animation(sheet=pygame.image.load("res/jola.png").convert_alpha(), cols=4, frame_rate=5)
NPC_BOSS = Animation(sheet=pygame.image.load("res/holo.png").convert_alpha(), cols=6, frame_rate=5)
NPC_NOTE = Animation(sheet=pygame.image.load("res/holonotatka.png").convert_alpha(), cols=6, frame_rate=5)

# 36 znakow na linie
# lvl 1
BOSS_TEXT = [
    [
    "'You! Get me 2 ultracans of some\njuice! Quickly!' - Boss",
    "He didn't even know your name...\nAnd why exactly does he need this\nstuff...?"
    ], #3
    [
    "Quickly! How long am I supposed to\nwait?' - Boss",
    "Is the job as future manager really\nworth it...?",
    "I mean, one advantage is that I\nwon't have any competition because,\n well, nobody wants a job as\n stressful as this one..."
    "I'd better go..."
    ] #4
]
NOTE_TEXT = [
    [
    "It's the year 2051. Right after\ngraduating, you got an internship\noffer in a market leading company.",
    "Soon after joining, you realized\nthat your boss is quite eccentric\nwealthy man..."
    ], #1
    [
    "Company is associated with\nbioengineering, so you kinda\nexpected this boring job in some\nkind of old laboratory.",
    "However, instead of that, you got\nthe office job with sweet Mrs Jola\nand lots of stressing tasks from\nyour boss..."
    ], #2
    [
    "You can collect items by walking\ninto them. Your equipment is under\nthe 'Q' button. ",
    "Interactions start under the 'E'\nbutton. Finish your level after\nachieving the main goal by climbing\nthe job ladder."
    ] #5
]
JOLA_TEXT = []
# lvl 2
NOTE_TEXT += [
    [
    "By clicking the left mouse button\nyou can shoot the enemy.",
    "Try upgrading your weapon by\ncollecting the found items and\n putting them together in a workshop\nplaced in your equipment.",
    "Take an item from the workshop and\n hide it back to the equipment by\nclicking the right mouse button.",
    "Be careful! If the elements are put\ntogether with some gaps, something\nmay explode!"
    ] #2
]
BOSS_TEXT += [
    [
    "Monsters! Monsters everywhere!",
    "There was an unexpected leakage from\n the laboratory resulting in the\nmutation of all the workers into\n monsters!",
    "I'm at the highest floor, in my\noffice. Quick, help me!' - Boss"
    ] #1
]
# lvl 3
BOSS_TEXT += [
    [
    "I need an extraphotocopier, coffee\n supermachine and 5 ultracans.",
    "It's an important business. Also\nclear the place from monsters, so we\n are able to run away! - Boss"
    ]
]
# lvl 4
# BOSS_TEXT += [
#     [
#     "As a manager, you should have your\nown hiperlaptop and office\n supersupplies.",
#     "Collect all you can find. - Boss"
#     ]
# ]
# lvl 4
BOSS_TEXT += [
    [
    "Turns out, the leakage in laboratory\nwas caused by fastplants research.",
    "Collect all of them so we can test\nthem and try to find out what\nhappened.",
    "Don't forget the monsters! - Boss"
    ]
]
# # lvl 6
# BOSS_TEXT += [
#     [
#     "The monsters destroyed the whole\nreception and now it needs a full\nrestoration",
#     "Collect 2 copies of every item.\nRemember to kill as many monsters\nas possible! - Boss"
#     ]
# ]
# lvl 7
BOSS_TEXT += [
    [
    "I've been waiting for so long for\n you, I got really hungry.",
    "Bring me an app-le. - Boss"
    ]
]
# lvl boss
JOLA_TEXT += [
    [
    "'Hello dear, I was waiting for you.'",
    "Where is the boss??",
    "'He is not here and he will not be.\nIt was me giving you orders all\nthis time.'",
    "What is this all stuff for?\nWhat is going on?",
    "'This stuff will lead to great\nthings... my creation!'",
    "'The boss was just a coverup, and\nthe experiment on employees\nsucceeded!'",
    "'Thanks to that and all of your hard\nwork I will soon destroy the world\nby making all humans the brainless\nmonsters, killing each other!'",
    "'But excuse me for now, because I\nhave to put one last element to my\nmachine. Give me the app-le, it will\ngive it the power supply!'",
    "Oh no! I can't give her the app-le.\nI have to defeat her to save the\nworld!"
    ]
]
def get_npc(dialogbox : DialogBox):
    jola = {}
    boss = {}
    note = {}
    for i, text in enumerate(JOLA_TEXT, start = 1):
        jola[(i, 0, 0)] = Tile("", collision = False, interactible=NPC(dialog_box=dialogbox, animation=NPC_JOLA, text=text))
        

    for i, text in enumerate(BOSS_TEXT, start = 1):
        boss[(0, i, 0)] = Tile("", collision = False, interactible=NPC(dialog_box=dialogbox, animation=NPC_BOSS, text=text))
        print(text)
    
    for i, text in enumerate(NOTE_TEXT, start = 1):
        note[(0, 0, i)] = Tile("", collision = False, interactible=NPC(dialog_box=dialogbox, animation=NPC_NOTE, text=text))

    return {**jola, **boss, **note}