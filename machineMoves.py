from stockfish import Stockfish
stockfish = Stockfish("stockfish-windows-x86-64-avx2.exe")
stockfish.set_depth(15)
stockfish.set_skill_level(15)
stockfish.get_parameters()

position = []
stockfish.set_position()

loops = 0

while loops < 20:
    best_move = stockfish.get_best_move()
    print(best_move)
    stockfish.make_moves_from_current_position([best_move])
    print(stockfish.get_board_visual())
    loops = loops + 1