from actions import Action

from player import Player


class Game:
    def __init__(self, players: list[Player]):
        self.players = players

        for player in players:
            player.score_updated.connect(self.on_player_score_changed)

        self.leader: Player = self.players[0]
        self.leader_changed = Action(Player)

    def on_player_score_changed(self, player: Player, score: int):
        if player.score > self.leader.score:
            self.leader = player
            self.leader_changed.invoke(self.leader)