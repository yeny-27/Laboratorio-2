#!/usr/bin/env python
# license removed for brevity
import rospy
import numpy as np
import gym
#check world debug
import sys
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
import pygame
from pygame.locals import *
import cv2
from time import sleep
from random import randint, uniform,random
from world import val,val1
import Recupera as cr #Importamos a la clase recupera
count = -1
lista=[]
video_size = 700, 500
velocity_publisher = rospy.Publisher('space_invader/move', String, queue_size=10)

recuperar=cr.recupera() 
#agregamos el resultado de el metodo lee que esta dentro de la clase recupera a data_file
data_file=recuperar.lee()

def key_action():
  try:
      if data_file != []: # Si data_file no esta vacio entonces entra
        mov=int(data_file.pop(0)) # Quita la pocision 0 de data file
        
        print("Movimientos del archivo restantes: ", len(data_file))
        
        #Si data_file tiene llega a 0 datos entonces limpiamos todos los archivos
        if len(data_file) == 0:
          readFile = open("/home/allan/catkin_ws/src/space_invader/Cantidad_de_movimientos.txt",'r')
          lines = readFile.readlines()
          readFile.close()
      
          w = open("/home/allan/catkin_ws/src/space_invader/Cantidad_de_movimientos.txt",'w')
          w.writelines([item for item in lines[:-1]])
          w.write("0")
          w.close()
          
          readFile = open("/home/allan/catkin_ws/src/space_invader/Fin_de_partida.txt",'r')
          lines = readFile.readlines()
          readFile.close()
      
          w = open("/home/allan/catkin_ws/src/space_invader/Fin_de_partida.txt",'w')
          w.writelines([item for item in lines[:-1]])
          w.close()
        
        # Movemos la nave con los mivimientos de que extrajimos del archivo Mejores_Movimientos
        print("Movimiento",mov)
        if mov == 1:
          return "1"
        if mov == 2:
          return "2"
        if mov == 5:
          return "5"
        if mov == 0:
          return "0"
    
      else: #Si el archivo de Mejores_Movimientos esta vacio o ya jugamos con esos movimientos pasamos a jugar de forma manual Para obtener nuevos movimientos
        global count
        global lista
        mov=0 # Establecemos que vale 0 por si no presionamos ninguna tecla osea la nave no hace nada
        
        # Controlamos la nave con las teclas de forma manual
        keys=pygame.key.get_pressed()
        if keys[K_LEFT]:
          mov= 5
        if keys[K_UP]:
          mov= 1
        if keys[K_RIGHT]:
          mov= 2
        count = count + 1 # esta variable acumula la catidad de iteraciones del metodo key_action()
        lista.append(mov) # Añadimos los movimientos a una lista
    
        print(count,val())
        
        #Si count(Cantidad de iteraciones del metodo key_action()) es igual a el valor del metodo val(Que contiene la cantidad de movimientos que se realizaron en world.py)
        # Y val es mayor a 0 lo que significa que en world.py una partida termino y complio con la recompensa minima que le configuramos
        if count == int(val()) and int(val()) > 0:
          print("Iteracion",count)
          
          #Entonces guardamos los movimientos realizados en el archivo Mejores_Movimientos
          with open("/home/allan/catkin_ws/src/space_invader/Mejores_Movimientos.txt", "a") as datos2:
            datos2.writelines("\n".join(map(str,lista)))
          
          # En la proximas lineas de la 92 a la 99 limpiamos la cantidad de movimientos para recibir la proxima partida que cumpla con la recompensa necesaria.
          readFile = open("/home/allan/catkin_ws/src/space_invader/Cantidad_de_movimientos.txt",'r')
          lines = readFile.readlines()
          readFile.close()
      
          w = open("/home/allan/catkin_ws/src/space_invader/Cantidad_de_movimientos.txt",'w')
          w.writelines([item for item in lines[:-1]])
          w.write("0")
          w.close()
          count=0 # devolvemos a 0 la catidad de iteraciones del metodo key_action()
  
        #Si el metodo val1 que viene de world.py es True significa que termino una partida 
        if val1() == "True":
          lista=[] #Limpiamos la lista que guarda los movimientos para que empiece a guarda los nuevos movimintos de la proxima partida
          
          #Tambien limpiamos este archivo para saber cuando termina la proxima partida 
          readFile = open("/home/allan/catkin_ws/src/space_invader/Fin_de_partida.txt",'r')
          lines = readFile.readlines()
          readFile.close()
      
          print("True",lista)
      
          w = open("/home/allan/catkin_ws/src/space_invader/Fin_de_partida.txt",'w')
          w.writelines([item for item in lines[:-1]])
          w.close()
          count=0 #devolvemos a 0 la catidad de iteraciones del metodo key_action()
  
        print(" Movimiento manual:{}".format(mov))
  
        if mov == 5:
          return "5"
        if mov == 1:
          return "1"
        if mov == 2:
          return "2"
        if mov == 0:
          return "0"
  
  except Exception:
    print("No funciona :=(")
  

def callback(ros_data):
    np_arr = np.fromstring(ros_data.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    screen = pygame.display.set_mode(video_size)
    surf = pygame.surfarray.make_surface(image_np)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    vel_msg = key_action()
    velocity_publisher.publish(vel_msg)

def main(args):
    '''Initializes and cleanup ros node'''
    rospy.init_node('agent', anonymous=True)
    subscriber = rospy.Subscriber('space_invader/image_raw', CompressedImage, callback)
    try:
        screen = pygame.display.set_mode(video_size)
        vel_msg = key_action()
        velocity_publisher.publish(vel_msg)
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down ROS Gym Image Viewer module")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
