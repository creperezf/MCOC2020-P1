# MCOC2020-P1

![image](https://user-images.githubusercontent.com/69158551/91098577-b6073b00-e62f-11ea-9630-537056b81932.png)

#  Entrega 2:
  * Gráfico de orbita del satelite:
    
    ![grafica_satelite](https://user-images.githubusercontent.com/69158551/91511160-122ac300-e8ad-11ea-8f08-ef4a877b73f2.png)

    Como se puede ver en el gráfico, para que el satelite tenga una orbita perfecta a 700 km de la tierra este tiene que ir a un velocidad v(t) igual a 7000 m/s.
    Para encontrar esta velocidad solo bastó con probar numeros y ver en que momento la orbita era de solo una linea circular.
    En caso de que el satelite fuese a una velocidad de 10000 m/s se vería así:


    ![image](https://user-images.githubusercontent.com/69158551/91511707-5a96b080-e8ae-11ea-8461-2e1e98e7912f.png)

    y para 5000 m/s:

    ![image](https://user-images.githubusercontent.com/69158551/91512047-1657e000-e8af-11ea-9c7f-fad48c49db4e.png)


  * Gráfico de historias de tiempo de x(t), y(t) y z(t), para dos órbitas completas:
  
    ![Distancia para 2 orbitas](https://user-images.githubusercontent.com/69158551/91511158-11922c80-e8ad-11ea-886f-c4d67bf220ae.png)
    
  * Gráfico de distancia al centro de la tierra del satélite vs. el tiempo:

    ![r (t) para 2 orbitas](https://user-images.githubusercontent.com/69158551/91511154-10f99600-e8ad-11ea-967f-0b7fe94c3292.png)
    
    Se puede ver que las cumbres del gráfico, al estar por sobre las lineas limites muestran que no topa con la atmosfera, como ejemplo de que pase lo contrario se puede ver lo siguiente con una velocidad de 5000 m/s, donde se puede ver claramente que choca con la atmosfera y posteriormente con la tierra.
    
    ![image](https://user-images.githubusercontent.com/69158551/91518057-4908d500-e8bd-11ea-9b37-1f37a7ad2c1f.png)
    
# Entrega 5
  * 1.- Gráfica sin Js:
  
  ![Gráfica_1_sin_perfeccionar](https://user-images.githubusercontent.com/69158551/92348322-33f42900-f0a9-11ea-9bb6-affc2bc4b6fc.png)
  
  Gráfica con Js:
  
![Gráfica_2_con_perfeccionar](https://user-images.githubusercontent.com/69158551/92348330-38b8dd00-f0a9-11ea-889f-10e23fbdf920.png)

  * 2.- 
  ![Gráfica_4_comparación](https://user-images.githubusercontent.com/69158551/92348337-3e162780-f0a9-11ea-959d-aec7387f6fd3.png)
  
  La diferencia de la deriba de odeint y eulerint es bastante grande ya que al ser tan pocas subdivisiones los resultados obtenidos son completamente diferentes. Se demora bastante poco en ambos (odeint y eulerint) correr mi programa por lo que se puede aumentar las subdivisiones.
  
  * 3.- 
  La gráfica muestra solamente hasta 300 subdivisiones ya que el programa se demora bastante en calcularlo, 
  
  * 4.- ![Gráfica_3_comparación](https://user-images.githubusercontent.com/69158551/92348339-3f475480-f0a9-11ea-812a-e4607331a697.png)
