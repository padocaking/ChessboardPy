# pip install stockfish
from stockfish import Stockfish
import time


### STOCKFISH SETUP ###

stockfish = Stockfish("stockfish-windows-x86-64-avx2.exe")
stockfish.set_depth(15)
stockfish.set_skill_level(5)
stockfish.get_parameters()


### GLOBAL VARIABLES ###

chessboard = [
    ["R", "P", " ", " ", " ", " ", "p", "r"],
    ["N", "P", " ", " ", " ", " ", "p", "n"],
    ["B", "P", " ", " ", " ", " ", "p", "b"],
    ["Q", "P", " ", " ", " ", " ", "p", "q"],
    ["K", "P", " ", " ", " ", " ", "p", "k"],
    ["B", "P", " ", " ", " ", " ", "p", "b"],
    ["N", "P", " ", " ", " ", " ", "p", "n"],
    ["R", "P", " ", " ", " ", " ", "p", "r"],
]

moves_history = []

white_king_moved = False
black_king_moved = False

def disable_castle(piece):
    global white_king_moved
    global black_king_moved

    if piece.isupper():
        white_king_moved = True
    else:
        black_king_moved = True


def print_board():
    print("+---+---+---+---+---+---+---+---+")
    i = 7
    while i >= 0:   
        printRow = "|"
        for column in chessboard:
            printRow += f" {column[i]} |"
        printRow += f" {i}"
        print(printRow)
        print("+---+---+---+---+---+---+---+---+")
        i -= 1
    print("  0   1   2   3   4   5   6   7  ")


### CONVERSÃO COORDENADA -> NOTAÇÃO XADREZ ###

def coord_to_notation(x, y):
    notation = ""

    match x:
        case 0:
            notation += "a"
        case 1:
            notation += "b"
        case 2:
            notation += "c"
        case 3:
            notation += "d"
        case 4:
            notation += "e"
        case 5:
            notation += "f"
        case 6:
            notation += "g"
        case 7:
            notation += "h"

    notation += str(y + 1)

    return notation


def notation_to_x(letter):
    match letter:
        case "a":
            return 0
        case "b":
            return 1
        case "c":
            return 2
        case "d":
            return 3
        case "e":
            return 4
        case "f":
            return 5
        case "g":
            return 6
        case "h":
            return 7


def notation_to_y(number):
    return int(number) - 1


### FUNCIONALIDADES DE MOSTRAR LANCES POSSÍVEIS ###

def valid_position(x, y):
    if (x >= 0 and x <= 7 and y >= 0 and y <= 7):
        return True
    else:
        return False


def pawn_moves(x, y):
    piece_color = chessboard[x][y].isupper()
    direction = 1 if piece_color else -1

    def add_pawn_moves(newY, movesArr):
        if valid_position(x, newY):
            if chessboard[x][newY] == " ":
                movesArr.append([x, newY])

    moves = []

    # Andar uma casa
    oneSqrY = y + direction
    add_pawn_moves(oneSqrY, moves)

    # Andar duas casas
    twoSqrY = y + 2 * direction
    if (y == 1 and direction == 1) or (y == 6 and direction == -1):
        add_pawn_moves(twoSqrY, moves)

    # Capturas
    captures = [x + 1, x - 1]

    for captureX in captures:
        if valid_position(captureX, oneSqrY):
            if chessboard[captureX][oneSqrY].isupper() != piece_color and chessboard[captureX][oneSqrY] != " ":
                moves.append([captureX, oneSqrY])

    return moves


def piece_moves(x, y):
    def add_moves(initialX, initialY, deltaX, deltaY, movesArr):
        """
        Adiciona lances para peças de movimentos verticais e horizontais completos,
        baseando-se pelo deltaX e daltaY, que variarão entre -1, 0 e +1,
        DeltaX controla o movimento horizontal, DeltaY controla o movimento vertical.

        Parâmetros:
        - initialX: Coordenada X da peça
        - initialY: Coordenada Y da peça
        - deltaX: Direção horizontal da verificação
        - deltaY: Direção vertical da verificação
        - movesArr: array dos lances possíveis

        Função:
        - Adiciona coordenadas de lances possíveis ao array
        """

        piece_color = chessboard[initialX][initialY].isupper()
        currX = initialX
        currY = initialY

        while True:
            currX += deltaX
            currY += deltaY

            if not valid_position(currX, currY):
                break

            position = chessboard[currX][currY]

            # Caso: casa vazia, adicionar nos movimentos e continuar a checagem
            if position == " ":
                movesArr.append([currX, currY])
            # Caso: casa possua peça inimiga, adicionar nos movimentos e parar a checagem 
            elif position.isupper() != piece_color:
                movesArr.append([currX, currY])
                break
            else:
                break

    piece = chessboard[x][y].lower()

    # Os deltas definirão as direções em que serão feito as verificações dos lances
    bishop_deltas = [
        [-1,  1],   # Checa diagonal superior esquerda
        [1,  -1],   # Checa diagonal infeior direita
        [1,   1],   # Checa diagonal superior direita
        [-1, -1],   # Checa diagonal infeior esquerda
    ]
    rook_deltas = [
        [0,  1],    # Checa para cima
        [0, -1],    # Checa para baixo
        [-1, 0],    # Checa para esquerda
        [1,  0],    # Checa para direita
    ]
    queen_deltas = rook_deltas + bishop_deltas  # Checa a porra toda (pls nerf rainha)

    deltas = []
    moves = []

    if piece == "b":
        deltas = bishop_deltas
    if piece == "r":
        deltas = rook_deltas
    if piece == "q":
        deltas = queen_deltas

    for delta in deltas:
        add_moves(x, y, delta[0], delta[1], moves) 

    return moves


def single_sqr_piece_moves(x, y, pattern):
    piece_color = chessboard[x][y].isupper()

    def add_moves(newX, newY, movesArr):
        if valid_position(newX, newY):
            if chessboard[newX][newY] == " " or chessboard[newX][newY].isupper() != piece_color:
                movesArr.append([newX, newY])

    moves = []

    for movement in pattern:
        newX = x + movement[0]
        newY = y + movement[1]
        add_moves(newX, newY, moves)

    return moves


def king_moves(x, y):
    piece_color = chessboard[x][y].isupper()

    king_movement = [
        [-1, 1], [0, 1], [1, 1],
        [-1, 0], [1, 0],
        [-1, -1], [0, -1], [1, -1]
    ]

    if (piece_color and not white_king_moved) or (not piece_color and not black_king_moved):
        if chessboard[x + 1][0] == " ":
            king_movement = king_movement + [[2, 0]]

        if chessboard[x - 1][0] == " " and chessboard[x - 2][0] == " ":
            king_movement = king_movement + [[-3, 0]]

    return single_sqr_piece_moves(x, y, king_movement)


def knight_moves(x, y):
    knight_movement = [
        [ -2, 1 ], [ -1, 2 ],
        [ 1, 2 ], [ 2, 1 ],
        [ -2, -1 ], [ -1, -2 ],
        [ 1, -2 ], [ 2, -1 ],
    ]

    return single_sqr_piece_moves(x, y, knight_movement)


def show_piece_moves(x, y):
    piece = chessboard[x][y].lower()
    
    if piece == " ":
        print("No piece")
        return []
    elif piece == "p":
        return pawn_moves(x, y)
    elif piece == "n":
        return knight_moves(x, y)
    elif piece == "k":
        return king_moves(x, y)
    else:
        return piece_moves(x, y)


def show_stockfish_move():
    stockfish.set_position(moves_history)
    best_move = stockfish.get_best_move()

    x, y = notation_to_x(best_move[0]), notation_to_y(best_move[1])
    newX, newY = notation_to_x(best_move[2]), notation_to_y(best_move[3])

    return [[x, y], [newX, newY]]


### FUNCIONALIDADES DE FAZER LANCES ###

def make_piece_move(initialX, initialY, newX, newY):
    if valid_position(initialX, initialY) and valid_position(newX, newY):

        piece = chessboard[initialX][initialY]
        legalMoves = show_piece_moves(initialX, initialY)
        isPossible = False

        # Checa se lance é possível
        for moves in legalMoves:
            if moves == [newX, newY]:
                isPossible = True

        # Caso seja Roque
        if initialX == 4 and (initialY == 0 or initialY == 7) and (newX == 6 or newX == 1) and (newY == 0 or newY == 7):
            castle_move(initialX, initialY, newX, newY)
        elif isPossible:
            # Faz o lance
            chessboard[initialX][initialY] = " "
            chessboard[newX][newY] = piece

            # Adiciona no histórico de lance
            move_notation = coord_to_notation(initialX, initialY) + coord_to_notation(newX, newY)
            moves_history.append(move_notation)

            # Checa se é rei
            if piece.lower() == "k":
                disable_castle(piece)
        else:
            print("Lance invalido")
            return False


def castle_move(initialX, initialY, newX, newY):
    king = chessboard[initialX][initialY]
    rook = "R" if king.isupper() else "r"

    chessboard[initialX][initialY] = " "
    if newX == 6:
        chessboard[7][initialY] = " "
        chessboard[5][newY] = rook
    elif newX == 1:
        chessboard[0][initialY] = " "
        chessboard[2][newY] = rook

    chessboard[newX][newY] = king

    move_notation = coord_to_notation(initialX, initialY) + coord_to_notation(newX, newY)
    moves_history.append(move_notation)

    disable_castle(king)


def stockfish_piece_move():
    stockfish.set_position(moves_history)
    best_move = str(stockfish.get_best_move())

    x, y = notation_to_x(best_move[0]), notation_to_y(best_move[1])
    newX, newY = notation_to_x(best_move[2]), notation_to_y(best_move[3])

    make_piece_move(x, y, newX, newY)

    return str(x) + str(y) + str(newX) + str(newY)


#while True:
#    validMove = False
#    while not validMove:
#        print_board()
#        move = input("Faça o lance: ")
#        
#        try:
#            if make_piece_move(int(move[0]), int(move[1]), int(move[2]), int(move[3])) != False:
#                print_board()
#                validMove = True
#        except:
#            print("Formato inválido, use coordenada inicial e coordenada final. EX: 4143 (e2 => e4)")
#
#    time.sleep(1)
#    stockfish_move()
#
#    if move == "quit":
#        quit()