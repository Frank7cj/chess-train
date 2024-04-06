import argparse
import configparser
import datetime
import random
import re
from io import TextIOWrapper

import chess
import chess.engine
import chess.pgn

DEFAULT_MAX_ENGINE_LIMIT = 1


class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr


def display_board(board: chess.Board, bot_perspective: chess.Color):
    r = range(8, 0, -1) if bot_perspective == chess.WHITE else range(1, 9, 1)

    print("  a b c d e f g h")
    print(" +-----------------+")
    for rank in r:
        row = f"{rank}|"
        for file in range(8):
            square = chess.square(file, rank - 1)
            piece = board.piece_at(square)
            if piece is None:
                row += "  "
            else:
                row += piece.unicode_symbol() + " "
        row += f"|{rank}"
        print(row)
    print(" +-----------------+")
    print("  a b c d e f g h")


def calculate_win_probabilities(board: chess.Board, engine: chess.engine.SimpleEngine, engine_limit: chess.engine.Limit):

    result = engine.analyse(board, engine_limit)

    evaluation_score = result["score"].relative.score()

    if evaluation_score > 0:
        white_win_probability = 1 / (1 + 10 ** (-evaluation_score / 400))
        black_win_probability = 1 - white_win_probability
    elif evaluation_score < 0:
        black_win_probability = 1 / (1 + 10 ** (evaluation_score / 400))
        white_win_probability = 1 - black_win_probability
    else:
        white_win_probability = 0.5
        black_win_probability = 0.5

    return white_win_probability, black_win_probability


def save_move(node: chess.pgn.Game, file: TextIOWrapper):
    exporter = chess.pgn.StringExporter(
        headers=False, variations=True, comments=True)
    move_string = node.accept(exporter)
    file.write(move_string + "\n")


def is_uci_move(move_str: str):
    uci_pattern = re.compile(r'^[a-h][1-8][a-h][1-8][qrbn]?$')

    if uci_pattern.match(move_str):
        return True
    else:
        return False


def get_user_move(board: chess.Board, user_input: str):
    if not is_uci_move(user_input):
        print("Invalid input. Please enter a valid UCI move.")
        raise ValueError
    move = chess.Move.from_uci(user_input)
    if move in board.legal_moves:
        return move
    else:
        print("Invalid move. Please try again.")
        raise ValueError


def play_chess(engine_path: str = "stockfish/stockfish-ubuntu-x86-64-avx2",
               file: TextIOWrapper = None,
               player_side: chess.Color = chess.WHITE,
               engine_config: chess.engine.ConfigMapping = {},
               engine_limits: chess.engine.Limit = chess.engine.Limit()):
    if file is not None:
        file.write('='*50 + '\n')
        file.write("{datetime} | CHESS TRAIN\n".format(
            datetime=datetime.datetime.now().isoformat()))
        file.write('-'*50 + '\n')
        player_color_name = 'WHITE' if player_side == chess.WHITE else 'BLACK'
        file.write("\tPlayer side: {player_side}\n".format(
            player_side=player_color_name))
        file.write("\tEngine Limits\n")
        for key, value in engine_limits.__dict__.items():
            if value is not None:
                file.write("\t\t{key}: {value}\n".format(key=key, value=value))
        file.write('='*50 + '\n')

    board = chess.Board()
    game = chess.pgn.Game()
    game.setup(board)
    node = game
    display_board(board, player_side)

    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        while not board.is_game_over():
            if board.turn == player_side:
                user_input = input(
                    "Enter your move (in UCI format, e.g., 'e2e4') or !help for best move: ")
                if user_input == '!help':
                    move = engine.play(board, chess.engine.Limit())
                else:
                    try:
                        move = get_user_move(board, user_input)
                    except:
                        continue
            else:
                result = engine.play(board=board,
                                     limit=engine_limits,
                                     options=engine_config)
                move = result.move
                print(f"AI plays: {move.uci()}")

            board.push(move)
            display_board(board, player_side)

            node = node.add_main_variation(
                chess.Move.from_uci(str(board.peek())))
            if file is not None:
                save_move(node, file)

    print("Game Over")
    print("Result: ", board.result())

    file.write("Result: " + board.result() + "\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--configFile',
                        type=str,
                        help='Specify a config file with AnalysisLimits',
                        required=False)

    args = parser.parse_args()

    config = CaseSensitiveConfigParser()
    config.read(args.configFile)

    # Player Config
    player_side = config['PlayerConfig']['side']\
        if config.has_option('PlayerConfig', 'side')\
        else random.choice([chess.BLACK, chess.WHITE])
    player_side = chess.WHITE if player_side == 'WHITE' else chess.BLACK

    # Engine Config
    engine_config = dict(config['EngineConfig'])\
        if config.has_section('EngineConfig') else {}

    # Engine Limits
    limit_params = dict(config['EngineLimits']) \
        if config.has_section('EngineLimits') else {}
    limit_params = {key: int(value) if str(value).isdigit()
                    else value
                    for key, value in limit_params.items()}
    if limit_params.get('time') is None:
        limit_params['time'] = DEFAULT_MAX_ENGINE_LIMIT
    engine_limits = chess.engine.Limit(**limit_params)

    file = open(config['GameConfig']['export_file'], "a")\
        if config.has_option('GameConfig', 'export_file') else None

    play_chess(file=file, player_side=player_side,
               engine_limits=engine_limits, engine_config=engine_config)

    file.close()
