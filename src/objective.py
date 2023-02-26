from typing import Dict

class Objective:

    def __init__(self, items: Dict[str, int] = {}, kill_all = False):
        self.items = items
        self.kill_all = kill_all

    def satisfied(self, player, enemies):
        
        player_items = player.weapon.all_items()

        for item, count in self.items:
            if item in player_items:
                if count < player_items[item]:
                    return False
            else:
                return False
        
        if self.kill_all and len(enemies) > 0:
            return False
        
        return True
