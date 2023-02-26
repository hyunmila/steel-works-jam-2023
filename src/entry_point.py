from game import Game
from levels.test_level import TestLevel
from levels.art_test_level import ArtTestLevel
from levels.next_test_level import NextTestLevel

game = Game(
    levels={
        "test-level": TestLevel,
        "art-test-level": ArtTestLevel,
        "next-test-level": NextTestLevel,
    },
    initial_level="art-test-level",
)
