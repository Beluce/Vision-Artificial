from os import system
import mediapipe as mp
import cv2
import serial
import numpy as np
import math

# Sirve para dibujar con las utilidades de mediapipe
mp_dibujo = mp.solutions.drawing_utils

#Inicializa la solucion de deteccion de manos
mp_manos = mp.solutions.hands

objeto_hands = mp_manos.Hands(static_image_mode = False,
                              max_num_hands = 1,
                              min_detection_confidence = 0.5)

cap = cv2.VideoCapture(2)

ventana1 = "Lenguaje de senias"
cv2.namedWindow(ventana1, cv2.WINDOW_NORMAL)
cv2.resizeWindow(ventana1, 640, 480)

try:
    puerto = serial.Serial("COM5", 9600, timeout=1)
except:
    system("cls")
    print("No se ha podido establecer conexion") 

while True:
    ret, frame = cap.read()
    
    RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    resultados = objeto_hands.process(RGBframe)
    
    if resultados.multi_hand_landmarks:
        for puntos in resultados.multi_hand_landmarks:
            
            #mp_dibujo.draw_landmarks(frame, puntos, mp_manos.HAND_CONNECTIONS) #Esta linea dibuja todas las lineas y conexiones por defecto
            
            #Dedo punto abajo
            
            punto_abajo = puntos.landmark[0]
            
            #Dedos de uso general
            
            dedo_pulgar_up = puntos.landmark[4]
            dedo_indice_up = puntos.landmark[8]
            dedo_mid_up = puntos.landmark[12]
            dedo_anular_up = puntos.landmark[16]
            dedo_menique_up = puntos.landmark[20]
            
            dedo_indice_d = puntos.landmark[5]
            dedo_mid_d = puntos.landmark[9]
            dedo_anular_d = puntos.landmark[13]
            dedo_menique_d = puntos.landmark[17]
            
            dedo_pulgar_ref = puntos.landmark[2]
            
            #Dedos necesarios para la vocal E
            
            dedo_indice_E = puntos.landmark[6]
            dedo_mid_E = puntos.landmark[10]
            dedo_anular_E = puntos.landmark[14]
            dedo_menique_E = puntos.landmark[18]
            
            alto, ancho, canales = frame.shape

# COORDENADAS:

            #Punto Abajo
            
            coordPuntoAbajoX, coordPuntoAbajoY = int(punto_abajo.x * ancho), int(punto_abajo.y * alto)

            #Puntas Dedos
            
            coordPulgarX_UP, coordPulgarY_UP = int(dedo_pulgar_up.x * ancho), int(dedo_pulgar_up.y * alto)
            coordIndiceX_UP, coordIndiceY_UP = int(dedo_indice_up.x * ancho), int(dedo_indice_up.y * alto)
            coordMidX_UP, coordMidY_UP = int(dedo_mid_up.x * ancho), int(dedo_mid_up.y * alto)
            coordAnularX_UP, coordAnularY_UP = int(dedo_anular_up.x * ancho), int(dedo_anular_up.y * alto)
            coordMeniqueX_UP, coordMeniqueY_UP = int(dedo_menique_up.x * ancho), int(dedo_menique_up.y * alto)
            
            #Parte de abajo de cada dedo
            coordIndiceX_D, coordIndiceY_D = int(dedo_indice_d.x * ancho), int(dedo_indice_d.y * alto)
            coordMidX_D, coordMidY_D = int(dedo_mid_d.x * ancho), int(dedo_mid_d.y * alto)
            coordAnularX_D, coordAnularY_D = int(dedo_anular_d.x * ancho), int(dedo_anular_d.y * alto)
            coordMeniqueX_D, coordMeniqueY_D = int(dedo_menique_d.x * ancho), int(dedo_menique_d.y * alto)
            coordPulgarX_D, coordPulgarY_D = int(dedo_pulgar_ref.x * ancho), int(dedo_pulgar_ref.y * alto)
            
            #Necesarios para letra E:
            
            coordIndiceX_E, coordIndiceY_E = int(dedo_indice_E.x * ancho), int(dedo_indice_E.y * alto)
            coordMidX_E, coordMidY_E = int(dedo_mid_E.x * ancho), int(dedo_mid_E.y * alto)
            coordAnularX_E, coordAnular_E = int(dedo_anular_E.x * ancho), int(dedo_anular_E.y * alto)
            coordMeniqueX_E, coordMeniqueY_E = int(dedo_menique_E.x * ancho), int(dedo_menique_E.y * alto)
               
# Detectamos cada posicion de los dedos:

            dedoPulgar_extendido = True if coordPulgarX_UP < coordPulgarX_D else False   

            dedoIndice_levantado = True if coordIndiceY_UP < coordIndiceY_D else False     
            dedoMid_levantado = True if coordMidY_UP < coordMidY_D else False               
            dedoAnular_levantado = True if coordAnularY_UP < coordAnularY_D else False      
            dedoMenique_levantado = True if coordMeniqueY_UP < coordMeniqueY_D else False   
            
# Posiciones necesarias para cada vocal

    #Letra A
            
            #si la coordenada del pulgar de abajo + 10 es mayor que la coordenada de arriba y la misma coordenada de abajo del pulgar - 10 es menor que la coordenada de arriba entonces el dedo esta en medio

            comprobacionPulgarA = abs(coordPulgarX_D - coordPulgarX_UP) < 20
            
            dedoPulgar_straight = (coordIndiceX_UP - 10) > coordPulgarX_UP and comprobacionPulgarA
            
            #system('cls')
            #print("abs(coordPulgarX_D - coordPulgarX_UP)", abs(coordPulgarX_D - coordPulgarX_UP))
            #print("coordIndiceX_UP - 10", coordIndiceX_UP - 10)
            #print("coordPulgarX_UP", coordPulgarX_UP)
            #print("comprobacionPulgarA", comprobacionPulgarA)
            
    #Letra E
            
            dedoPulgar_E = (coordMidX_D+20) > (coordPulgarX_UP) > (coordPulgarX_D-20)
            
            dedoIndice_E = 0 < (coordIndiceY_D - coordIndiceY_UP) < 20
            dedoMid_E = 0 < (coordMidY_D - coordMidY_UP) < 20
            dedoAnular_E = -10 < (coordAnularX_D - coordAnularX_UP) < 7
            dedoMenique_E = 0 < (coordMeniqueY_D - coordMeniqueY_UP) < 20
            
            '''
            system('cls')
            print("coordIndiceY_D - coordIndiceY_UP", coordIndiceY_D - coordIndiceY_UP)
            print("coordMidY_D - coordMidY_UP", coordMidY_D - coordMidY_UP)
            print("coordAnularX_D - coordAnularX_UP", coordAnularX_D - coordAnularX_UP)
            print("coordMeniqueY_D - coordMeniqueY_UP",coordMeniqueY_D - coordMeniqueY_UP)
            print()
            print("coordMidX_D",coordMidX_D)
            print("coordPulgarX_UP",coordPulgarX_UP)
            print("coordPulgarX_D",coordPulgarX_D)
            '''
            
    #Letra O
            
            if -5 <= (coordPulgarX_UP - coordIndiceX_UP) <= 10 and -5 <= (coordPulgarX_UP - coordMidX_UP) <= 10 and -10 <= (coordPulgarX_UP - coordAnularX_UP) <= 20 and -15 <= (coordPulgarX_UP - coordMeniqueX_UP) <= 15:
                #cv2.putText(frame, "APROXIMA X", (100, 200), cv2.FONT_ITALIC, 1, (0, 255, 0), thickness=3)
                proximidadX = True
            else:
                proximidadX = False
            
            if -3 <= (coordPulgarY_UP - coordIndiceY_UP) <= 25 and -3 <= (coordPulgarY_UP - coordMidY_UP) <= 20 and  0 <= (coordPulgarY_UP - coordAnularY_UP) <= 25 and -10 <= (coordPulgarY_UP - coordMeniqueY_UP) <= 15:
                #cv2.putText(frame, "APROXIMA Y", (100, 300), cv2.FONT_ITALIC, 1, (0, 255, 0), thickness=3)
                proximidadY = True
            else:
                proximidadX = False
                
            '''
            
            system('cls')
            print("coordPulgarX_UP - coordIndiceX_UP",coordPulgarX_UP - coordIndiceX_UP)
            print("coordPulgarX_UP - coordMidX_UP",coordPulgarX_UP - coordMidX_UP)
            print("coordPulgarX_UP - coordAnularX_UP", coordPulgarX_UP - coordAnularX_UP)
            print("coordPulgarX_UP - coordMeniqueX_UP", coordPulgarX_UP - coordMeniqueX_UP)
            print()
            print(coordPulgarX_UP)
            print(coordIndiceX_UP)
            print(coordMidX_UP)
            print(coordAnularX_UP)
            print(coordMeniqueX_UP)
            print()
            print(coordPulgarY_UP)
            print(coordIndiceY_UP)
            print(coordMidY_UP)
            print(coordAnularY_UP)
            print(coordMeniqueY_UP)
            print()
            print("coordPulgarY_UP - coordIndiceY_UP", coordPulgarY_UP - coordIndiceY_UP)
            print("coordPulgarY_UP - coordMidY_UP", coordPulgarY_UP - coordMidY_UP)
            print("coordPulgarY_UP - coordAnularY_UP", coordPulgarY_UP - coordAnularY_UP)
            print("coordPulgarY_UP - coordMeniqueY_UP", coordPulgarY_UP - coordMeniqueY_UP)
            
            '''
        
            letra = "F"
            
            if(dedoPulgar_straight == True
               and dedoIndice_levantado == False 
               and dedoMid_levantado == False        
               and dedoAnular_levantado == False 
               and dedoMenique_levantado == False):   
                    
                cv2.putText(frame, "Letra A", (ancho - 120, 40), cv2.FONT_ITALIC, 1, (255, 0, 0), thickness=3) #Azul
                
                letra = "A"
            
            elif(dedoPulgar_E == True
               and dedoIndice_E == True
               and dedoMid_E == True
               and dedoAnular_E == True
               and dedoMenique_E == True):
            
                cv2.putText(frame, "Letra E", (ancho - 120, 40), cv2.FONT_ITALIC, 1, (0, 255, 0), thickness=3) #Verde
                
                letra = "E"
                
            elif(dedoPulgar_extendido == False
               and dedoIndice_levantado == False 
               and dedoMid_levantado == False        
               and dedoAnular_levantado == False 
               and dedoMenique_levantado == True):
                
                cv2.putText(frame, "Letra I", (ancho - 120, 40), cv2.FONT_ITALIC, 1, (0, 0, 255), thickness=3) #Rojo
                
                letra = "I"
                
            elif(proximidadX == True and proximidadY == True):     #Letra O
                
                cv2.putText(frame, "Letra O", (ancho - 120, 40), cv2.FONT_ITALIC, 1, (0, 255, 255), thickness=3) #Amarillo
                
                letra = "O"
                
            elif(dedoIndice_levantado == True
                 and dedoMid_levantado == True
                 and dedoPulgar_extendido == False
                 and dedoAnular_levantado == False
                 and dedoMenique_levantado == False):     #Letra U
                
                cv2.putText(frame, "Letra U", (ancho - 120, 40), cv2.FONT_ITALIC, 1, (255, 255, 0), thickness=3) #Cyan
                
                letra = "U"
            
            else:
                cv2.putText(frame, "Esperando Comando", (100, 100), cv2.FONT_ITALIC, 1, (255, 0, 170), thickness=3)
                
                letra = "F"
            
            try:
                puerto.write(f"{letra}\n".encode())
            except:
                system("cls")
                print("No se pueden mandar datos")   
            
    else:
        cv2.putText(frame, f"No se encuentran manos", (100, 100), cv2.FONT_ITALIC, 1, (0, 0, 255), thickness=3)
        
        try:
            puerto.write("F\n".encode())
        except:
            system("cls")
            print("No se pueden mandar datos")
            
    cv2.imshow(ventana1, frame)
    
    salir = cv2.waitKey(1)
    
    if salir == 27:
        break
    
cap.release()
cv2.destroyAllWindows