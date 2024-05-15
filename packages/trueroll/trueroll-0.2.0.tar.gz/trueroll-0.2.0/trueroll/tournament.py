from typing import List, Dict, Tuple
from trueroll import Game, Bowler, Alley


class Tournament:
    def __init__(self, bowlers: List[Bowler], alley: Alley, num_games: int = 1):
        """
        Initialize a Tournament instance with bowlers, the alley where the tournament is played, and the number of games each bowler will play.

        Parameters:
            bowlers (List[Bowler]): A list of `Bowler` objects representing the participants.
            alley (Alley): The `Alley` object representing the venue of the tournament.
            num_games (int): The number of games each bowler will play in the tournament.

        Attributes:
            results (Dict[str, List[List[int]]]): A dictionary to store results for each bowler.
        """
        self.bowlers = bowlers
        self.alley = alley
        self.num_games = num_games
        self.results: Dict[str, List[List[Tuple[int, ...]]]] = {bowler.name: [] for bowler in bowlers}
        # self.results = {bowler.name: [] for bowler in bowlers}

    def run_tournament(self):
        """
        Simulate the entire tournament, running the specified number of games for each bowler.
        """
        for _ in range(self.num_games):
            game = Game(self.bowlers, self.alley)
            game_results = game.simulate_game()
            for name, scores in game_results.items():
                self.results[name].append(scores)

    def get_results(self) -> Dict[str, List[int]]:
        """
        Calculate and return the total scores for each bowler over the course of the tournament.

        Returns:
            Dict[str, List[int]]: A dictionary with bowler names as keys and lists of their total scores for each game as values.
        """
        total_scores = {name: [sum(sum(frame) for frame in game) for game in games] for name, games in self.results.items()}
        return total_scores

    def get_average_scores(self) -> Dict[str, float]:
        """
        Calculate and return the average scores for each bowler in the tournament.

        Returns:
            Dict[str, float]: A dictionary with bowler names as keys and their average score as values.
        """
        average_scores = {name: sum(scores) / len(scores) if scores else 0 for name, scores in self.get_results().items()}
        return average_scores


if __name__ == "__main__":
    bowlers = [Bowler("John Doe", strike_prob=0.3, spare_prob=0.5), Bowler("Jane Smith", strike_prob=0.4, spare_prob=0.4)]
    alley = Alley("Strike Zone", "Synthetic", "Medium")
    tournament = Tournament(bowlers, alley, num_games=5)
    tournament.run_tournament()
    print("Results:", tournament.get_results())
    print("Average Scores:", tournament.get_average_scores())
