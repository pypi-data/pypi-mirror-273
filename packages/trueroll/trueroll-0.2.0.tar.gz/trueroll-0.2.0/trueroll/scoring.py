class Scoring:
    @staticmethod
    def traditional(frames: list) -> int:
        """
        Calculate the traditional bowling score from a list of frames.

        Each frame should be represented by a tuple indicating the number of pins knocked down in each roll.

        Parameters:
            frames (list): A list of tuples representing the game frames.

        Returns:
            int: The total score calculated based on traditional bowling rules.
        """
        score = 0

        for i in range(10):
            frame = frames[i]

            # Strike
            if frame[0] == 10:
                score += 10
                if i < 9:
                    next_frame = frames[i + 1]
                    if next_frame[0] == 10:
                        score += 10
                        if i + 1 < 9:
                            score += frames[i + 2][0]
                        else:
                            score += next_frame[1]
                    else:
                        score += next_frame[0] + next_frame[1]
                else:
                    score += frame[1] + frame[2]

            # Spare
            elif sum(frame) == 10:
                score += 10
                if i < 9:
                    score += frames[i + 1][0]
                else:
                    score += frame[2]

            # Open frame
            else:
                score += sum(frame)

        return score

    @staticmethod
    def current_frame(frames: list) -> int:
        """
        Calculate the score using current frame scoring rules, also known as World Bowling scoring.

        Parameters:
            frames (list): A list of tuples representing the game frames.

        Returns:
            int: The total score calculated based on current frame (World Bowling) rules.
        """
        score = 0
        for frame in frames:
            if frame[0] == 10:  # Strike
                score += 30
            elif sum(frame) == 10:  # Spare
                score += 10 + frame[0]
            else:
                score += sum(frame)
        return score

    @staticmethod
    def nine_pin_no_tap(frames: list) -> int:
        """
        Calculate the score for a 9-pin no-tap game, where knocking down 9 pins counts as a strike.

        Parameters:
            frames (list): A list of tuples representing the game frames.

        Returns:
            int: The total score calculated based on 9-pin no-tap rules.
        """
        score = 0
        for i, frame in enumerate(frames):
            first_roll = frame[0]
            if first_roll == 9 or first_roll == 10:
                if i < 9:  # Not the last frame
                    next_frame = frames[i + 1]
                    score += 10 + next_frame[0] + (next_frame[1] if len(next_frame) > 1 else 0)
                else:  # Last frame
                    score += 10 + frame[1] + frame[2]
            elif sum(frame[:2]) == 10:  # Spare
                score += 10 + (frames[i + 1][0] if i < 9 else frame[2])
            else:
                score += sum(frame)
        return score


if __name__ == "__main__":
    frames = [(10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (9, 1), (10, 0), (9, 1), (10, 0), (9, 1, 8)]
    traditional_score = Scoring.traditional(frames)
    current_frame_score = Scoring.current_frame(frames)
    nine_pin_no_tap_score = Scoring.nine_pin_no_tap(frames)
    print(f"Traditional Score: {traditional_score}")
    print(f"Current Frame Score: {current_frame_score}")
    print(f"Nine Pin No Tap Score: {nine_pin_no_tap_score}")
