---
title: Agenda
class:

  - Visão Geral sobre Visão Computacional
  - Python e OpenCV
  - Aquisição de imagens pela camêra
  - Detecção de Marcadores
  - Bordas e Contornos
  - Perspectiva
  - Threshold Adaptativo
  - Identificação 
  - [Bonus] Computação Gráfica

---
title: Visão Computacional	
class: segue dark nobackground

---
title: Visão Computacional 
content_class: flexbox vcenter

" Visão computacional é a ciência responsável pela visão de uma máquina, pela forma como um computador enxerga o meio à sua volta,
extraindo informações significativas a partir de imagens capturadas por câmeras de vídeo, sensores, scanners, entre outros dispositivos.
Estas informações permitem reconhecer, manipular e pensar sobre os objetos que compõem uma imagem "
Ballard, Dana Harry, Computer Vision, PrenticeHall, 1982.

---
title: Visão Computacional 

 <div id="left" style="float: left"> 
Aplicações Automobilísticas
 </div>
 
 <div id="right" style="float: right; background: #EEEEEE;">
        <img src="images/visi_car.png">
		
 </div> 
	<footer class="source white">http://visigenie.com/images/visi_hero.png</footer>
---
title: Realidade Aumentada 
content_class: flexbox vcenter

Citar um exemplo

---
title: Python & OpenCV	
class: segue dark nobackground

---
title: Python & OpenCV	
content_class: flexbox vcenter

Packages and dependencias and which version we are using in this project

---
title: Aquisição de Imagem
class: segue dark nobackground

---
title: Aquisição de Imagem pela Webcam	
content_class: flexbox vcenter

Exemplo de Código:
<pre class="prettyprint" data-lang="Python">
from cv2 import *
# initialize the camera
cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
if s:    # frame captured without any errors
    namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
    imshow("cam-test",img)
    waitKey(0)
    destroyWindow("cam-test")
    imwrite("filename.jpg",img) #save image
</pre>

---
title: Aquisição de Imagem pela Webcam
content_class: flexbox vcenter

Talvez alguma imagem segurando os marcadores??

---
title:  Tratamento da Imagem
content_class: flexbox vcenter

Colocando a imagem capturada em escalas de cinza e redimensionando
<pre class="prettyprint" data-lang="Python">
	Código de tratamento da imagem
</pre>

---
title: Detecção dos Marcadores
class: segue dark nobackground

---
title: Algoritmo de Borda (Canny)
content_class: flexbox vcenter

Explicação sobre identificação das bordas

---
title: Algoritmo de Borda (Canny)
content_class: flexbox vcenter


<pre class="prettyprint" data-lang="Python">


	Code Goes Here



</pre>

---
title: Algoritmo de Borda (Canny)
content_class: flexbox vcenter

IMAGE GOES HERE!

---
title: Algoritmo de contorno
content_class: flexbox vcenter

Explicação sobre obtenção dos contornos

---
title: Algoritmo de contorno
content_class: flexbox vcenter

<pre class="prettyprint" data-lang="Python">


	Code Goes Here


</pre>

---
title: Algoritmo de contorno
content_class: flexbox vcenter

IMAGE GOES HERE!

---
title: Algoritmo de Contorno
content_class: flexbox vcenter

Filtragem e porque filtramos

---
title: Algoritmo de Contorno
content_class: flexbox vcenter

Ordenação 
(uma imagem comparando talvez ele ordenado VS não ordenado)

---
title: Extração de Perspectiva
class: segue dark nobackground

---
title: Extração de Perspectiva
content_class: flexbox vcenter

Explicação sobre perspectiva

--- 
title: Extração de Perspectiva
content_class: flexbox vcenter

Image Goes Here

---
title: Threshold adaptativo
content_class: flexbox vcenter

Explanation

---
title: Identificação dos marcadores
class: segue dark nobackground

---
title: Marcadores
content_class: flexbox vcenter

Explicação sobre os ID's dos marcadores e pq usamos 4 diferentes

---
title: Orientação dos Marcadores

Realmente necessário??


---
title: Aplicação Gráfica 
subtitle: Fazendo uma aplicação gráfica rodando nos marcadores
content_class: flexbox vcenter



Image Goes Here

---
title: Features
content_class: flexbox vcenter

Image to use as explaination about detection with features


Explicação sobre o que é isso

