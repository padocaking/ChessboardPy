# pip intall pyserial
import serial.tools.list_ports
from chess import chessboard, make_piece_move, show_piece_moves, stockfish_piece_move
import time

### ARDUINO SERIAL CONNECTION

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for one in ports:
    portsList.append(str(one))
    print(str(one))

com = input("Select Com Port for Arduino#: ")

for i in range(len(portsList)):
    if portsList[i].startswith("COM" + str(com)):
        use = "COM" + str(com)
        print(use)

serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()



### ARDUINO CHESS CODE

initialX = 8
initialY = 8

piece_up = False
white_turn = True

def show_move(x, y):
    global white_turn
    global piece_up

    if (chessboard[x][y].isupper() and white_turn) or (not chessboard[x][y].isupper() and not white_turn):
        moves_arr = show_piece_moves(x, y)
        moves_output = f"l{x}{y}"

        print("s" + str(x) + str(y))

        if len(moves_arr) > 0:
            for move in moves_arr:
                moves_output += str(move[0]) + str(move[1])

        serialInst.write(moves_output.encode('utf-8'))
        print(moves_output)
    else:
        wrong_turn = f"c{x}{y}"
        serialInst.write(wrong_turn.encode('utf-8'))
        print(wrong_turn)
        piece_up = False


def make_move(iniX, iniY, x, y):
    global white_turn

    x = int(command[1])
    y = int(command[2])

    print("m" + str(x) + str(y))

    if not(x == iniX and y == iniY):
        if make_piece_move(iniX, iniY, x, y) == False:
            invalid_move = "e" + str(x) + str(y) + str(iniX) + str(iniY)
            serialInst.write(invalid_move.encode('utf-8'))
            print(invalid_move)
        else:
            serialInst.write(f"v{x}{y}".encode('utf-8'))
            white_turn = not white_turn
    else:
        cancel_move = "r"
        serialInst.write(cancel_move.encode('utf-8'))

def make_stockfish_move(iniX, iniY, x, y):
    make_piece_move(iniX, iniY, x, y)


while True:
    if serialInst.in_waiting > 0:
        read = serialInst.read_all()
        command = read.decode('utf-8')
        print(read)

        typ = command[0]
        x = int(command[1])
        y = int(command[2])

        if len(command) > 5:
            endX = int(command[3])
            endY = int(command[4])

        match typ:
            case "s":
                if not piece_up:
                    piece_up = True
                    show_move(x, y)
                    initialX = x
                    initialY = y

            case "m":
                make_move(initialX, initialY, x, y)
                piece_up = False

            case "f":
                make_stockfish_move(x, y, endX, endY)


        print("-------------")


    #command = input("Coordenada: ")
    #serialInst.write(command.encode('utf-8'))

    #if command == "exit":
    #    serialInst.close()
    #    quit()