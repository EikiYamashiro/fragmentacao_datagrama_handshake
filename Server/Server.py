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
h = 10
e = 2304
eop = e.to_bytes(4, 'big')

confirm_msg = (29).to_bytes(1, 'big')
error_msg = (5).to_bytes(1, 'big')

def error_print():
    print("---------------------------------")
    print("---------------------------------")
    print("-------------ERROR---------------")
    print(' ')
    print("TAMANHO DO PAYLOAD DO HEAD DIFERENTE DO RECEBIDO!!!")
    print(' ')
    print("-------------ERROR---------------")
    print("---------------------------------")
    print("---------------------------------")

def main():
    try:
        msg_error = "Comunicação sem erros!"
        com2 = enlace('COM2')
        com2.enable() 
        print("Server disponível")
        com2.rx.getIsEmpty()
        #----------------------GET--HANDSAHKE-------------------------
        handshake_recebido, nRx = com2.getData(14)
        print("-------------------------------------")
        print("HANDSHAKE!!!")
        print("-------------------------------------")
        com2.sendData(handshake_recebido)
        imageW = "recebidaCopia.png"
        list_payload = []
        verifica_id = 1
        antecede_number = 0
        while True:
            
            #----------------------GET--HEAD--------------------------
            head, nRx = com2.getData(10)
            print("Recebendo HEAD do Client...")
            sizePayload = head[5]
            sizeMensagem = head[3]
            numeroPacote = head[1]
            if verifica_id != 1:
                antecede_number += 1
            
            print(numeroPacote)
            print("sizeMensagem: {}".format(sizeMensagem))
            print("numeroPacote: {}".format(numeroPacote))
            print("sizePayload: {}".format(sizePayload))
            print("---------------------------------")
            if sizePayload!=114 and sizeMensagem != verifica_id:
                sizePayload = 114
                error_print()
                msg_error = "Comunicação com erro no datagrama de ID: {}".format(verifica_id)
            if verifica_id != numeroPacote:
                msg_error = "Comunicação com erro no datagrama de ID: {}".format(verifica_id)
                
                
            #---------------------GET--PAYLOAD-------------------------
            payload, nRx = com2.getData(sizePayload)
            print("payload {0} e {1}".format(nRx, sizePayload))
            print("Recebendo PAYLOAD do Client...")
            print("---------------------------------")
            list_payload.append(payload)
            
            
            
            #-----------------------GET--EOP---------------------------
            eop, nRx = com2.getData(4)
            print("Recebendo EOP do Client...")
            print("---------------------------------")
            time.sleep(0.5)
            print(" ")
            print(" ")
            
            verifica_id += 1
            
            if eop != b'\x00\x00\t\x00':
                break
            if sizeMensagem == numeroPacote:
                break
            
        mensagem = b''.join(list_payload)  
        f = open(imageW, 'wb')
        f.write(mensagem)
        f.close()
        
        print(msg_error)
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
