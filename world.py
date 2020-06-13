#!/usr/bin/env python
# license removed for brevity
import rospy
import gym
import cv2
import numpy as np
import imutils
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
#check world debug
env = gym.make('SpaceInvaders-v0')
image_pub = rospy.Publisher('space_invader/image_raw', CompressedImage, queue_size=10)
count=0
itera=0

def pub_image(env):
    #GYM RENDER AS IMAGE
    img = env.render(mode='rgb_array')
    #print(img)
    # ROTATE THE IMAGE THE MATRIX IS 90 grates and mirror
    img = np.flipud(np.rot90(img))
    image_np = imutils.resize(img, width=500)
    # Publish new image
    msg = CompressedImage()
    msg.header.stamp = rospy.Time.now()
    msg.format = "jpeg"
    compressed_images = cv2.imencode('.jpg', image_np)
    msg.data = np.array(compressed_images[1]).tostring()
    image_pub.publish(msg)

def open_world(vel_msg):
    global count 
    global itera
    action = int(vel_msg.data)
    obs, rew, done, info = env.step(action)
    pub_image(env)
    count = count + rew # Almacena la recompensa acumulada de la partida
    print(rew, info, done) # Imprime los datos del juego
    itera = itera + 1 # Acumula la cantidad de iteraciones hasta que la partida termine.
    if done == True:
      if int(count) >= 200: # Es la recompensa minima de una partida para poder escojer esos movimientos
      
       #Si la recompensa de la partida es suficiente entonces guardamos el numero de iteraciones en catidad_de_movimientos
        corte3=open("/home/allan/catkin_ws/src/space_invader/Cantidad_de_movimientos.txt", "a")
        corte3.write(str(itera))
        corte3.close()
        print(count,itera)
        count=0 #Reiniciamos la recompensa acumulada para empesar la proxima partida
        itera=0 #Reiniciamos el contador de iteraciones para la proxima partida
        
      #si la recompensa no es suficiente guardamos en el archivo Fin de partida el valor true que indica que esta partida termino  
      corte2=open("/home/allan/catkin_ws/src/space_invader/Fin_de_partida.txt", "a")
      corte2.write("True")
      corte2.close()
      count=0 #Reiniciamos la recompensa acumulada para empesar la proxima partida
      itera=0 #Reiniciamos el contador de iteraciones para la proxima partida
      env.reset()

# En esta metodo agrega la catidad de movimientos a una lista y la retorna a viewer 
def val():
  corte = open("/home/allan/catkin_ws/src/space_invader/Cantidad_de_movimientos.txt", "r")
  lista=corte.readline()
  corte.close()
  return (lista)
  
# En esta metodo agrega el contenido de Fin de partida (TRUE o " ") a una lista y la retorna a viewer  
def val1():
  corte1 = open("/home/allan/catkin_ws/src/space_invader/Fin_de_partida.txt", "r")
  lista=corte1.readline()
  corte1.close()
  return (lista)


if __name__ == '__main__':
    rospy.init_node('space_invader_world', anonymous=True)
    try:
        rospy.Subscriber("space_invader/move", String, open_world)
        env.reset()
        pub_image(env)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
