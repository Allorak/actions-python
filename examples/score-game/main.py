from player import Player
from game import Game
import time
from loguru import logger


class PlayerLogger:
    def __init__(self, players: list[Player]):
        for player in players:
            player.score_updated.connect(self.on_player_score_updated)

    def on_player_score_updated(self, player: Player, score: int):
        logger.info(f"Player score updated. {player.name} has {score} points")

def print_leader(player: Player):
    logger.info(f"Leader changed. New leader is {player.name}")

def main():
    players = [Player("Player 1"), Player("Player 2"),
               Player("Player 3"), Player("Player 4")]

    player_logger = PlayerLogger(players)

    game = Game(players)
    game.leader_changed.connect(print_leader)

    time.sleep(2)
    players[1].add_points(10)
    time.sleep(2)
    players[2].add_points(11)
    time.sleep(2)
    players[1].add_points(5)
    time.sleep(2)
    players[0].add_points(1)
    time.sleep(2)
    players[0].add_points(5)
    time.sleep(2)
    players[0].add_points(20)
    time.sleep(2)
    players[3].add_points(30)
    time.sleep(2)
    players[0].add_points(100)

if __name__ == "__main__":
    main()