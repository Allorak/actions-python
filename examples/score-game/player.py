from actions_python import Action

class Player:
    def __init__(self, name: str):
        self.name = name
        self.score: int = 0
        self.score_updated = Action(Player, int)

    def add_points(self, points: int):
        self.score += points
        self.score_updated.invoke(self, self.score)
