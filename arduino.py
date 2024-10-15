# pip intall pyserial
import serial.tools.list_ports

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

while True:
    if serialInst.in_waiting > 0:
        read = serialInst.read_all()
        newRead = read.decode('utf-8')
        print(newRead)
        serialInst.write(newRead.encode('utf-8'))

    #command = input("Coordenada: ")
    #serialInst.write(command.encode('utf-8'))

    #if command == "exit":
    #    serialInst.close()
    #    quit()