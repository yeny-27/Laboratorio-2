class recupera:
  contador=0
  def __init__(self):
    pass
    
  def lee(self):
    archivo=open("/home/allan/catkin_ws/src/space_invader/Mejores_Movimientos.txt", "r")
    data=archivo.read()
    d=data.split("\n")
    d=d[:len(d)-1]
    pos = []
    self.contador += 1
    for i in d:
      pos.append(i.split(",")[0])
    return pos
  
