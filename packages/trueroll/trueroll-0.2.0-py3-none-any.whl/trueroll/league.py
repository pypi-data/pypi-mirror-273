from typing import List
from trueroll import Bowler, Alley, Tournament


class League:
    def __init__(self, name: str, alley: Alley, oil_pattern: str, team_size: int, num_games_per_night: int, season_length: int):
        """
        Initialises a league with specified parameters, setting up the environment where the league games are played,
        the type of oil pattern used, the team size, the number of games per league night, and the duration of the season.

        Args:
            name (str): The name of the league.
            alley (Alley): An Alley object where the league games are held.
            oil_pattern (str): The oil pattern used on the lanes throughout the season.
            team_size (int): The number of bowlers in each team.
            num_games_per_night (int): The number of games played each league night.
            season_length (int): The number of weeks the league runs.

        Attributes:
            teams (List[List[Bowler]]): Stores the teams participating in the league.
        """
        self.name = name
        self.alley = alley
        self.oil_pattern = oil_pattern
        self.team_size = team_size
        self.num_games_per_night = num_games_per_night
        self.season_length = season_length
        self.teams: List[List[Bowler]] = []
        # self.teams = []  # List of teams, each team is a list of Bowler objects

    def add_team(self, team: List[Bowler]):
        """
        Adds a team to the league. Ensures the team size matches the league's required team size.

        Args:
            team (List[Bowler]): A list of Bowler objects making up the team.

        Raises:
            ValueError: If the number of bowlers in the team does not match the league's specified team size.
        """
        if len(team) != self.team_size:
            raise ValueError("Team size must match the league's specified team size")
        self.teams.append(team)

    def run_season(self):
        """
        Simulates the entire season of the league, organising games per night for each team over the specified season length.

        Returns:
            Dict[str, List[Dict[str, float]]]: A dictionary with team names as keys and a list of their average scores per night as values.
        """
        results = {f"Team {i+1}": [] for i in range(len(self.teams))}
        for week in range(self.season_length):
            for i, team in enumerate(self.teams):
                tournament = Tournament(team, self.alley, self.num_games_per_night)
                tournament.run_tournament()
                results[f"Team {i+1}"].append(tournament.get_average_scores())
        return results


if __name__ == "__main__":
    # Example usage of the League class for demonstration purposes.
    alley = Alley("High Strike Lanes", "Downtown", "Synthetic")
    bowlers = [Bowler("John Doe", 0.3, 0.5), Bowler("Jane Doe", 0.25, 0.6)]
    league = League("Thursday Night Classic", alley, "Standard Oil", 2, 3, 15)
    league.add_team(bowlers)

    season_results = league.run_season()
    print(season_results)
