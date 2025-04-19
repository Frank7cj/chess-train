# Chess Train

Chess Train is a Python-based chess training tool that allows users to play chess against an AI engine, analyze moves, and save or resume games. It leverages the `python-chess` library and a UCI-compatible chess engine (e.g., Stockfish) to provide a rich chess-playing experience.

## Features

- **Play Chess**: Play chess against an AI engine with customizable configurations.
- **Save and Resume Games**: Save the current game state and resume it later.
- **Move Analysis**: Analyze moves using the chess engine and calculate win probabilities.
- **Customizable Settings**: Configure player side, engine limits, and other parameters via a configuration file.
- **Command Support**: Use commands like `!help`, `!bestMove`, and `!saveState` during gameplay.

## Requirements

- Python 3.7 or higher
- A UCI-compatible chess engine (e.g., Stockfish)

### Python Dependencies

The required Python libraries are listed in the `requirements.txt` file:

```txt
chess==1.10.0
python-chess==1.999
```

Install them using:

```bash
pip install -r requirements.txt
```

## Setup

1. **Install Stockfish**: Download and install Stockfish or another UCI-compatible chess engine. Update the `engine_path` in the code if necessary.
2. **Configuration**: Copy `template.config` to a new file (e.g., `config.config`) and update the settings as needed:
   - `GameConfig`: Specify the log file and engine path.
   - `PlayerConfig`: Set the player side (`WHITE` or `BLACK`) and whether to show scores.
   - `EngineConfig`: Configure engine-specific parameters.
   - `EngineLimits`: Set limits for time, depth, nodes, or mate search.

3. **Run the Program**: Start the chess training tool using:

```bash
python chess_train.py --configFile <path_to_config_file>
```

## Commands

During gameplay, you can use the following commands:

- `!help`: Display available commands.
- `!bestMove`: Let the engine play the best move.
- `!saveState [saveFilePath]`: Save the current game state to a file. If no file path is provided, a default file name is generated.

## Example Usage

1. Start a new game with a configuration file:

    ```bash
    python chess_train.py --configFile config.config
    ```

2. Resume a saved game:

    ```bash
    python chess_train.py --resumeGame <path_to_saved_game_file>
    ```

## File Structure

- `chess_train.py`: Main script for the chess training tool.
- `template.config`: Template configuration file for customizing settings.
- `requirements.txt`: Python dependencies.
- `.gitignore`: Specifies files and directories to ignore in version control.

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## Acknowledgments

- [python-chess](https://python-chess.readthedocs.io/): A Python library for chess handling.
- [Stockfish](https://stockfishchess.org/): A powerful open-source chess engine.
