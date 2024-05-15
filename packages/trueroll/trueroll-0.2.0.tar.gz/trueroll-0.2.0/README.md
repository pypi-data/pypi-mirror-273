# TrueRoll: Ten-Pin Bowling Simulation

TrueRoll is an extensive simulation toolkit designed for modeling ten-pin bowling games. It offers a comprehensive suite of classes that simulate games, tournaments, leagues, and more, providing a realistic and detailed representation of bowling dynamics. The project also includes a scoring system compatible with various bowling rules, a database for persisting game results, and an environment setup using poetry for easy package management.

## Features

- **Simulation Classes**: Simulate bowling games frame by frame or as complete games using different probabilities for strikes, spares, and opens.
- **Scoring Systems**: Includes traditional, current frame, and 9-pin no-tap scoring systems.
- **Bowling Database**: A SQLite database integration for storing and managing bowling games, bowlers, alleys, and tournaments.
- **League and Tournament Support**: Organize and run bowling tournaments and leagues with multiple games and multiple bowlers, customizable for different team sizes and frequencies.
- **Documentation**: Auto-generated API documentation using MkDocs for easy reference and usage.

## Getting Started

1. **Installation**: Clone the repository and install dependencies using Poetry.
   ```bash
   git clone https://github.com/your-github/trueroll.git
   cd trueroll
   poetry install
   ```

2. **Running Simulations**: You can start simulations directly from the command line or by using the provided Python scripts.
   ```python
   python -m trueroll
   ```

3. **Documentation**: To build and view the documentation locally:
   ```bash
   poetry run mkdocs serve
   ```

4. **Testing**: Run tests using the integrated testing suite to ensure everything is working as expected.
   ```bash
   poetry run pytest
   ```

## Contribution

Contributions are welcome! Please read the contributing guide for directions on how to submit pull requests to the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.