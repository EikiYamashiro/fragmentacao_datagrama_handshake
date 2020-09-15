#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação Client
####################################################

from enlace import *
import time
import datagrama
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import math

z = 0
#Quando o msgType for 10, é um handshake
h = 10
#Quando o msgType for 20, é uma mensagem
m = 20
#EOP definido como 2304
e = 2304

zero_b = z.to_bytes(3, 'big')
mt_handshake = h.to_bytes(4, 'big')
mt_message = m.to_bytes(4, 'big')
eop = e.to_bytes(4, 'big')

def create_handshake():
    head = create_head((0).to_bytes(2, 'big'), (0).to_bytes(2, 'big'), (0).to_bytes(2, byteorder='big'), mt_handshake)
    datagrama = head + eop
    return datagrama

def create_head(contador, sizeMensagem, sizePayload, msgType):
    #Numero do pacote
    #Numero total de pacotes
    #Tamanho do payload 
    #Tipo de mensagem 
    head = contador + sizeMensagem + sizePayload + msgType
    return head
    

def create_datagram_list(mensagem):
    datagrama = []
    c_total = 0
    contador = 0
    ID = 1
    sizeMensagem_int = math.ceil(len(mensagem)/114)
    sizeMensagem = sizeMensagem_int.to_bytes(2, byteorder='big')
    dg_list = []
    #Cada rodada cria um novo payload
    while c_total < len(mensagem)-1:
        
        if len(mensagem)-contador < 114:
            payload = mensagem[contador:]
            head = create_head(ID.to_bytes(2, 'big'), sizeMensagem, len(payload).to_bytes(2, byteorder='big'), mt_message)
            datagrama = head + payload + eop
            dg_list.append(datagrama)
            ID += 1
            break
        else:
            payload = mensagem[0+contador:114+contador]
            head = create_head(ID.to_bytes(2, 'big'), sizeMensagem, len(payload).to_bytes(2, byteorder='big'), mt_message)
            datagrama = head + payload + eop
            contador += 114
            ID += 1
            
        #Adiciona o datagrama na lista de datagramas
        dg_list.append(datagrama)
        
        #Zera os valores das variaveis
        playload = []
        head = []
        datagrama = []
        
        
    return dg_list
        
        
        

def main():
    try:
        #Enlace com COM1
        com1 = enlace('COM1') 
        com1.enable()
        
        #Abre a interface para o usuário selecionar a imagem
        #print('Escolha uma imagem:')
        #Tk().withdraw()
        #image_selected = askopenfilename(filetypes=[("Image files", ".png .jpg .jpeg")])
        #print("Imagem selecionada: {}".format(image_selected))
        imageR = "C:/Users/eikis/OneDrive/Área de Trabalho/Insper/ClientServer/Client/sophia.png"
        handshake = create_handshake()
        
        print("ENVIANDO HANDSHAKE")
        com1.sendData(handshake)
        t = True
        while t==True:
            
            time.sleep(5)
            if com1.rx.getIsEmpty():
                resp = input("Servidor inativo. Tentar novamente? S/N")
                if resp == "N":
                    s
            else:
                t = False
                print("HANDSHAKE RECEBIDO")
                
             
        #Carrega imagem para transmissão
        print("Carregando imagem para transmissao...")
        print("-----------------------------------")
        txBufferClient = open(imageR, 'rb').read()
        size_real = len(txBufferClient)
        txSizeClient = len(txBufferClient).to_bytes(4, byteorder='big')
        print("Criando datagramas...")
            
        datagrama_list = create_datagram_list(txBufferClient)
        
        print("Lista de datagramas criada com sucesso!")
        for datagrama in datagrama_list:
            head = datagrama[:10]
            payload = datagrama[10:-4]
            eop = datagrama[-4:]
            #---------------------SEND--HEAD-------------------------
            com1.sendData(head)
            time.sleep(0.5)
            #-------------------SEND--PLAYLOAD-----------------------
            com1.sendData(payload)
            time.sleep(0.5)
            #---------------------SEND--EOP--------------------------
            com1.sendData(eop)
            time.sleep(0.5)
        
        print("Saiu do for!")
        
        # Encerra comunicação
        com1.disable()
        print("-----------------------------------")
        print("Comunicação encerrada!")
        print("-----------------------------------")
    except:
        print("ops! :-\\")
        com1.disable()

if __name__ == "__main__":
    main()
