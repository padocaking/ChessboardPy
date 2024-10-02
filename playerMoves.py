chessboard = [
    ["R", "P", " ", " ", " ", " ", "p", "r"],
    ["N", "P", " ", " ", " ", " ", "p", "n"],
    ["B", "P", " ", " ", " ", " ", "p", "b"],
    ["Q", "P", " ", "Q", " ", " ", "p", "q"],
    ["K", "P", " ", " ", " ", " ", "p", "k"],
    ["B", "P", " ", " ", " ", " ", "p", "b"],
    ["N", "P", " ", " ", " ", " ", "p", "n"],
    ["R", "P", " ", " ", " ", " ", "p", "r"],
]


def print_board():
    print("  +---+---+---+---+---+---+---+---+")
    i = 7
    while i >= 0:   
        printRow = f"{i + 1} |"
        for column in chessboard:
            printRow += f" {column[i]} |"
        print(printRow)
        print("  +---+---+---+---+---+---+---+---+")
        i -= 1
    print("    A   B   C   D   E   F   G   H  ")


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


def knight_moves(x, y):
    piece_color = chessboard[x][y].isupper()

    def add_knight_moves(newX, newY, movesArr):
        if valid_position(newX, newY):
            if chessboard[newX][newY] == " " or chessboard[newX][newY].isupper() != piece_color:
                movesArr.append([newX, newY])

    knight_movement = [
        [ -2, 1 ], [ -1, 2 ],
        [ 1, 2 ], [ 2, 1 ],
        [ -2, -1 ], [ -1, -2 ],
        [ 1, -2 ], [ 2, -1 ],
    ]

    moves = []

    for movement in knight_movement:
        newX = x + movement[0]
        newY = y + movement[1]
        add_knight_moves(newX, newY, moves)

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


def calculate_piece_moves(x, y):
    piece = chessboard[x][y].lower()
    
    if piece == " ":
        print("Nenhuma peca encontrada")
        return
    elif piece == "p":
        return pawn_moves(x, y)
    elif piece == "k":
        return knight_moves(x, y)
    else:
        return piece_moves(x, y)


### FUNCIONALIDADES DE FAZER LANCES ###

def make_move(initialX, initialY, newX, newY):
    piece = chessboard[initialX][initialY]
    legalMoves = calculate_piece_moves(initialX, initialY)
    isPossible = False

    for moves in legalMoves:
        if moves == [newX, newY]:
            isPossible = True

    if isPossible:
        chessboard[initialX][initialY] = " "
        chessboard[newX][newY] = piece
    else:
        print("Lance invalido")

    print_board()

