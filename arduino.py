# pip intall pyserial
import serial.tools.list_ports
import time
from chess import show_piece_moves
from chess import make_piece_move

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

waiting_for_fix = False

initialX = 8
initialY = 8

def show_move(x, y):
    moves_arr = show_piece_moves(x, y)
    moves_output = ""

    if len(moves_arr) > 0:
        for move in moves_arr:
            moves_output += str(move[0]) + str(move[1])

    if moves_output == "":
        serialInst.write("88".encode('utf-8'))
    else:
        serialInst.write(moves_output.encode('utf-8'))


def make_move(iniX, iniY, x, y):
    x = int(command[1])
    y = int(command[2])

    print("m" + str(x) + str(y))

    if make_piece_move(iniX, iniY, x, y) == False:
        serialInst.write((str(x) + str(y) + str(iniX) + str(iniY)).encode('utf-8'))
    else:
        xy = str(x) + str(y)
        serialInst.write(xy.encode('utf-8'))


while True:
    if serialInst.in_waiting > 0:
        read = serialInst.read_all()
        command = read.decode('utf-8')

        typ = command[0]
        x = int(command[1])
        y = int(command[2])

        match typ:
            case "s":
                show_move(x, y)
                initialX = x
                initialY = y

            case "m":
                make_move(initialX, initialY, x, y)


    #command = input("Coordenada: ")
    #serialInst.write(command.encode('utf-8'))

    #if command == "exit":
    #    serialInst.close()
    #    quit()