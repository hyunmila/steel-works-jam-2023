from game import Game
from levels.test_level import TestLevel
from levels.art_test_level import ArtTestLevel
from levels.next_test_level import NextTestLevel
from levels.lvl1 import FirstLevel
from levels.lvl2 import SecondLevel
from levels.lvl3 import ThirdLevel
from levels.lvl4 import FourthLevel
from levels.lvl7 import SeventhLevel
from levels.lvlboss import BossLevel
from levels.end import EndLevel


game = Game(
    levels={
        # "test-level": TestLevel,
        # "art-test-level": ArtTestLevel,
        # "next-test-level": NextTestLevel,
        "lvl1" : FirstLevel,
        "lvl2" : SecondLevel,
        "lvl3" : ThirdLevel,
        "lvl4" : FourthLevel,
        "lvl7" : SeventhLevel,
        "lvlboss" : BossLevel,
        "end" : EndLevel

    },
    initial_level="lvl1"#"art-test-level",
)
