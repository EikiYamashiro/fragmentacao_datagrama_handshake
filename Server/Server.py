#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação Server
####################################################

from enlace import *
import time
import datagrama
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def main():
    try:
        com2 = enlace('COM2')
        com2.enable() 
        print("Server disponível")
        com2.rx.getIsEmpty()
        while True:
            #----------------------GET--HEAD--------------------------
            head, nRx = com2.getData(10)
            print("Recebendo HEAD do Client...")
            sizePayload = head[5]
            sizeMensagem = head[3]
            numeroPacote = head[1]
            print("sizeMensagem: {}".format(sizeMensagem))
            print("numeroPacote: {}".format(numeroPacote))
            print("sizePayload: {}".format(sizePayload))
            print("---------------------------------")
            
            #---------------------GET--PAYLOAD-------------------------
            payload, nRx = com2.getData(sizePayload)
            print("payload {0} e {1}".format(nRx, sizePayload))
            print("Recebendo PAYLOAD do Client...")
            print("---------------------------------")
            
            #-----------------------GET--EOP---------------------------
            eop, nRx = com2.getData(4)
            print("Recebendo EOP do Client...")
            print("---------------------------------")
            time.sleep(0.5)
            print(" ")
            print(" ")
            
            if eop != b'\x00\x00\x00\x17':
                break
            if sizeMensagem == numeroPacote:
                break
            
        print("-------------------------------------")
        print("Comunicação encerrada")
        print("-------------------------------------")
        com2.disable()  
    except:
        print("ops! :-\\")
        com2.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
