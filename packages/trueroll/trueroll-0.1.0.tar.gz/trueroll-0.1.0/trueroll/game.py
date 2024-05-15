from typing import List, Tuple, Dict, Iterator, Optional
import numpy as np
from trueroll import Bowler, Alley


class Game:
    """
    Manages the simulation of a bowling game, providing detailed frame-by-frame results for each bowler.

    This class supports simulations on specified alleys with distinct characteristics, influencing the gameplay of the bowlers.

    Attributes:
        bowlers (List[Bowler]): A list of `Bowler` objects participating in the game.
        alley (Alley): The `Alley` object specifying the lane type and oil pattern where the game is played.
        random_seed (Optional[int]): Seed for the random number generator to ensure reproducibility, if provided.
    """
    def __init__(self, bowlers: List[Bowler], alley: Alley, random_seed: Optional[int] = None):
        """
        Initialises a game with a list of bowlers and the alley where the game is played.

        Parameters:
            bowlers (List[Bowler]): List of Bowler objects participating in the game.
            alley (Alley): The Alley object specifying the lane type and oil pattern.
            random_seed (int, optional): Random seed for reproducibility of the simulation.
        """
        self.bowlers = bowlers
        self.alley = alley
        self.random_seed = random_seed

    def simulate_frame(self, bowler: Bowler, frame_number: int) -> Tuple[int, ...]:
        """
        Simulates a single frame for a given bowler based on the frame number.

        Parameters:
            bowler (Bowler): The Bowler object for whom the frame is simulated.
            frame_number (int): The frame number (0-indexed, 0-9).

        Returns:
            Tuple[int, ...]: A tuple representing the result of the frame (pins knocked down in each roll).
        """
        if frame_number < 9:
            return self.simulate_regular_frame(bowler)
        else:
            return self.simulate_last_frame(bowler)

    def simulate_regular_frame(self, bowler: Bowler) -> Tuple[int, int]:
        """
        Simulates a regular frame (not the last one), accounting for strikes and open frames.

        Parameters:
            bowler (Bowler): The Bowler object for whom the frame is simulated.

        Returns:
            Tuple[int, int]: A tuple of two integers representing the pins knocked down in each roll.
        """
        strike = np.random.rand() < bowler.strike_prob
        if strike:
            return (10, 0)
        first_roll = np.random.randint(0, 11)
        second_roll = np.random.randint(0, 11 - first_roll)
        return (first_roll, second_roll)

    def simulate_last_frame(self, bowler: Bowler) -> Tuple[int, ...]:
        """
        Simulates the 10th frame, which may include up to three rolls depending on the bowler's performance.

        Parameters:
            bowler (Bowler): The Bowler object for whom the last frame is simulated.

        Returns:
            Tuple[int, int, int]: A tuple of up to three integers representing the pins knocked down in each roll.
        """
        rolls = []

        # Simulate the first roll
        if np.random.rand() < bowler.strike_prob:
            rolls.append(10)
        else:
            rolls.append(np.random.randint(0, 11))

        # Simulate the second roll
        if rolls[0] == 10:  # First roll was a strike
            if np.random.rand() < bowler.strike_prob:
                rolls.append(10)
            else:
                rolls.append(np.random.randint(0, 11))
        else:
            second_roll = np.random.randint(0, 11 - rolls[0])
            rolls.append(second_roll)

        # Simulate the third roll if needed
        if sum(rolls[:2]) >= 10:  # Strike or spare in first two rolls
            if np.random.rand() < bowler.strike_prob:
                rolls.append(10)
            else:
                rolls.append(np.random.randint(0, 11))

        return tuple(rolls[:3])  # Ensure only up to three rolls are returned

    def frame_by_frame_generator(self) -> Iterator[Dict[str, Tuple[int, ...]]]:
        """
        A generator to simulate the game frame-by-frame, yielding results for each frame for all bowlers.

        Yields:
            Iterator[Dict[str, Tuple[int, ...]]]: An iterator that yields a dictionary representing the frame results of each bowler.
        """
        for frame_number in range(10):
            frame_results = {}
            for bowler in self.bowlers:
                frame_results[bowler.name] = self.simulate_frame(bowler, frame_number)
            yield frame_results

    def simulate_game(self) -> Dict[str, List[Tuple[int, ...]]]:
        """
        Simulates a complete game for all bowlers, returning the frame-by-frame results.

        Returns:
            Dict[str, List[Tuple[int, ...]]]:: A dictionary where keys are bowler names and values are lists of tuples, each tuple representing a frame.
        """
        if self.random_seed is not None:
            np.random.seed(self.random_seed)
        results: Dict[str, List[Tuple[int, ...]]] = {bowler.name: [] for bowler in self.bowlers}
        for frame_results in self.frame_by_frame_generator():
            for name, frame in frame_results.items():
                results[name].append(frame)
        return results


if __name__ == "__main__":
    # Example usage:
    bowlers = [Bowler(name="John Doe", strike_prob=0.3, spare_prob=0.5),
               Bowler(name="Jane Doe", strike_prob=0.4, spare_prob=0.6)]
    alley = Alley("Strike Zone", "Synthetic", "Medium")
    game = Game(bowlers, alley)
    results = game.simulate_game()
    print("Game Results:")
    for bowler, frames in results.items():
        print(f"{bowler}: {frames}")
