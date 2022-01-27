import cv2
import numpy as np
import serial

com = 'COM4'
baud = 9600
ser = serial.Serial(com, baud)
cap = cv2.VideoCapture(0)  #Creamos una variable para abrir la cámara

manzana_min = np.array([0, 112, 150],np.uint8)  ## HSV (tinte saturación y brillo) Variables con información de tonos de azul que queremos procesar
manzana_max = np.array([21, 255, 255],np.uint8)  ##Variables con información de tonos de azul que queremos procesar
#contador = 0
while True:
    ret, frame = cap.read()        #ret = la imagen se abrío correctamente, frame = La imagen que se está capturando
    frame = cv2.resize(frame,(500,500))

    if ret:                        #Si la imagen se capturó correctamente entramos a este if
        frame = cv2.flip(frame, 1) #-1 para wewbcam        #Reflejamos la imagen para tener una mejor perspetiva
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    #Convertimos el frame de RGB a HSV
        frameHSV = cv2.medianBlur(frameHSV, 51)
        mascara = cv2.inRange(frameHSV, manzana_min, manzana_max)    #Creamos una mascara con esta función sobre el frame captado
        mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel=np.ones((9,9),np.uint8))
        contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   #buscamos contornos en la mascara que aacabamos de crear en tonos de verde
        x = []
        y = []

        for c in contornos:             #Hacemos un recorrido de los contornos que se encontraron
            area = cv2.contourArea(c)    ##Calculamos el área de cada contorno que encontró
            if area > 1000:
                M = cv2.moments(c)       ##Encontramos los momentos para calcular el centroide
                if M["m00"] == 0:
                     M["m00"] = 1
                x.append(int(M["m10"] / M["m00"]) )     ##Estas son las ccordenadas x y y del centro de la figura detectada
                y.append(int(M['m01'] / M['m00']))
                font = cv2.FONT_HERSHEY_SIMPLEX     ##Declaro el tipo de fuente
                print(area)

                if len(x)==1:
                    cv2.circle(frame, (x[0], y[0]), 7, (0, 0, 255),-1)  ##dibujamos un pequeño circulo rojo -1relleno, radio 7
                    cv2.putText(frame, 'x = {}  y = {}'.format(x[0], y[0]), (20 ,400), font, 1, (0, 0, 255), 2, cv2.LINE_AA)    ##escribimos las coordenadas indicadas
                    nuevoContorno = cv2.convexHull(c)     ##Une todos los puntos que encontro en una forma cerrada
                    cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 3)  ##Dibujamos el nuevo contorno encontrado
                    #ser.write(b"x{} y{}".format(x,y))
                elif len(x)==2:
                    cv2.circle(frame, (x[0], y[0]), 7, (0, 0, 255),-1)  ##dibujamos un pequeño circulo rojo -1relleno, radio 7
                    cv2.putText(frame, 'x = {}  y = {}'.format(x[0], y[0]), (20, 400), font, 1, (0, 0, 255), 2,cv2.LINE_AA)  ##escribimos las coordenadas indicadas
                    nuevoContorno = cv2.convexHull(c)  ##Une todos los puntos que encontro en una forma cerrada
                    cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0),3)  ##Dibujamos el nuevo contorno encontrado

                    cv2.circle(frame, (x[1], y[1]), 7, (0, 0, 255),-1)  ##dibujamos un pequeño circulo rojo -1relleno, radio 7
                    cv2.putText(frame, 'x = {}  y = {}'.format(x[1], y[1]), (20, 450), font, 1, (0, 0, 255), 2,cv2.LINE_AA)  ##escribimos las coordenadas indicadas
                    nuevoContorno = cv2.convexHull(c)  ##Une todos los puntos que encontro en una forma cerrada
                    cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0),3)  ##Dibujamos el nuevo contorno encontrado

                elif len(x)==3:
                    cv2.circle(frame, (x[0], y[0]), 7, (0, 0, 255),-1)  ##dibujamos un pequeño circulo rojo -1relleno, radio 7
                    cv2.putText(frame, 'x = {}  y = {}'.format(x[0], y[0]), (20, 400), font, 1, (0, 0, 255), 2,cv2.LINE_AA)  ##escribimos las coordenadas indicadas
                    nuevoContorno = cv2.convexHull(c)  ##Une todos los puntos que encontro en una forma cerrada
                    cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0),3)  ##Dibujamos el nuevo contorno encontrado

                    cv2.circle(frame, (x[1], y[1]), 7, (0, 0, 255),-1)  ##dibujamos un pequeño circulo rojo -1relleno, radio 7
                    cv2.putText(frame, 'x = {}  y = {}'.format(x[1], y[1]), (20, 450), font, 1, (0, 0, 255), 2,cv2.LINE_AA)  ##escribimos las coordenadas indicadas
                    nuevoContorno = cv2.convexHull(c)  ##Une todos los puntos que encontro en una forma cerrada
                    cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0),3)  ##Dibujamos el nuevo contorno encontrado

                    cv2.circle(frame, (x[2], y[2]), 7, (0, 0, 255),-1)  ##dibujamos un pequeño circulo rojo -1relleno, radio 7
                    cv2.putText(frame, 'x = {}  y = {}'.format(x[2], y[2]), (20, 450), font, 1, (0, 0, 255), 2,cv2.LINE_AA)  ##escribimos las coordenadas indicadas
                    nuevoContorno = cv2.convexHull(c)  ##Une todos los puntos que encontro en una forma cerrada
                    cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0),3)  ##Dibujamos el nuevo contorno encontrado

    # contador += 1
    # if contador == 10:

        if len(x)>0:
            if x[0]<240:
                ser.write(b"derecha\n")       #D derecha
                #print('derecha')
            elif x[0]>260:
                ser.write(b"izquierda\n")       #I izquierda
            elif x[0]>240 and x[0]<260:
                ser.write(b"parox\n")         #S Stop x
            if y[0]<240:
                ser.write(b"abajo\n")       #Ab abajo
            elif y[0]>260:
                ser.write(b"arriba\n")       #Ar arriba
            elif y[0]>240 and x[0]<260:
                ser.write(b"paroy\n")         #S Stop y
            if area<25000:
                ser.write(b"acercar1\n")
            elif area>25000:
                ser.write(b"quieto1\n")
            if area<100000:
                ser.write(b"acercar2\n")
            elif area>100000:
                ser.write(b"quieto2\n")

        else:
            ser.write(b"SC\n")    #sin contornos
            #contador = 0

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

cap.release()
cv2.destroy