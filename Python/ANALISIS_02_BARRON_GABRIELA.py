"""
@author: baorz.gab

Este programa realiza los siguientes procesos:
    1. Lista top 10 rutas de origen-destino mas demandadas
    2. Lista transportes usados en exportacion e importacion (demanda)
    3. Lista valor de importaciones y exportaciones por pais
    4. Generar un resporte .txt con lo anterior
    5. Despliega un menu de opciones para visualizar lo anterior
"""

#importamos las librerias que vamos a usar
import csv #para manipular la base de datos
import os #para mas adelante hacer una funcion que borre pantalla (solo para dar una mejor UX)


"""
En esta primer parte vamos a pasar los datos que nos dieron en el archivo csv a una lista
esto para poder manipular mejor los datos mas adelante.
"""
lista_datos = []#nombramos la lista donde guardaremos los datos 
with open("synergy_logistics_database.csv", "r") as archivo: #abrimos el archivo csv
    lector = csv.DictReader(archivo) #leemos el archivo en forma de diccionario
    for registro in lector: #ciclo para recorrer el archivo
        lista_datos.append(registro) #llenamos la lista con los datos del archivo

""""
OPCION 1: TOP 10 RUTAS MAS DEMANDADAS
--------------------------------------
Para esta función nos pasaran como parametro la direccion (exportacion o importacion) que tiene el producto,
despues, en un bucle for vamos a recorrer dato por dato para ir verificando que tiene la direccion correcta, 
para ir contando cuantas veces se ha exportado o importado de ese origen al destino el producto se anido otro bucle for y asi 
tener un conteo de las rutas con mayor demanda. 
"""

def demanda_exportacion_importacion(direccion): #definimos la funcion y que parametros le vamos a pasar -> direccion = ("Imports" o "Exports")
    rutas_contadas = [] #definimos una lista para guardar todas las rutas
    rutas_conteo = [] #definimos una lista para guardar la ruta con sus datos adicionales

    for ruta in lista_datos: #vamos a recoorer la lista tomando en cada iteración el atributo direction
        if ruta["direction"] == direccion: #verificamos que el dato direction sea el mismo que el del parametro de la función
            ruta_actual = [ruta["origin"], ruta["destination"]] #definimos los paises en los que nos encontramos en esta iteración
            if ruta_actual not in rutas_contadas: #si los paises no estan en la lista de todas las rutas avanzamos, si no se cumple se pasa a la siguiente iteración
                cont_ruta = 0 #inicializamos nuestro contador de cuantas veces se repite esa ruta
                cont_venta = 0 #inicializamos el contador de valor total
                for lista_rutas in lista_datos: #recorremos de nuevo la lista de datos pero esta vez para hacer el conteo de cuantas veces se reíte la ruta actual
                    if ruta_actual == [lista_rutas["origin"], lista_rutas["destination"]]: #si la ruta de esta iteración correponde a la ruta actual avanzamos
                        cont_ruta += 1 #actualizamos el contador
                        cont_venta += int(lista_rutas["total_value"]) #actualizamos el contador de valor total

                rutas_contadas.append(ruta_actual) #agregamos valores a la lista -> rutas_contadas = [ruta actual] la de esta iteración para pasar a la siguiente ruta
                rutas_conteo.append([ruta["origin"], ruta["destination"], cont_ruta, cont_venta]) #agregamos valores a la lista -> rutas_conteo =[origen, destino, demanda, valor total]
                

    rutas_conteo.sort(reverse = True, key = lambda x:(x[2],x[3])) #ordenamos en orden descendente conforme al atributo demanda o cont_ruta y valor total o cont_venta
    return rutas_conteo #para finalziar esta funcion, regresamos la lista que obtuvimos


"""
OPCION 2: RUTAS USADAS
---------------------------
Esta función es bastante similiar a la anterior, solo que en esta ocación vamos a tener una lista con los medios de transporte que se usan, en vez de la ruta
 
"""
def transporte_exportacion_importacion(direccion): #definimos la funcion y que parametros le vamos a pasar -> direccion = ("Imports" o "Exports")
    medio_transporte = [] #lista donde se guardan los medios de trasnporte 
    transporte_conteo = [] #lista donde guardaremos los datos del medio de transporte y sus adicionales
    
    for transporte in lista_datos: #recorremos la lista de datos para buscar los medios de transporte
        if transporte["direction"] == direccion: #verificamos que la direccion de la iteración actual sea la misma que la del parametro que le pasamos a la funcion, si no pasamos a la siguiente iteración
            medio_transporte_actual = [transporte["direction"],transporte["transport_mode"]]#definimos la direccion y el transporte de la iteración actual
            if medio_transporte_actual not in medio_transporte: #condición, si el dato definido anteriormente no esta en la lista de medios de trasnporte avanzamos a hacer el conteo de demanda y valor total si no pasamos a la sig iteración
                cont_transporte = 0 #inicializamos el contador de demanda del transporte
                cont_venta = 0 #inicializamos el contador de valor total para ese transporte
                for transporte_lista in lista_datos: #vamos a recorrer la lista para hacer el conteo para ese medio de transporte
                    if medio_transporte_actual == [transporte_lista["direction"],transporte_lista["transport_mode"]]: #condición, si el transporte actual (primer bucle) corresponde al de la iteración de este bucle
                        cont_transporte += 1 #actualizamos contadores
                        cont_venta += int(transporte_lista["total_value"])
                medio_transporte.append(medio_transporte_actual) #agregamos valores -> medio_transporte = [medio de transporte] (air, sea, etc)
                transporte_conteo.append([transporte["transport_mode"], cont_transporte, cont_venta]) #agregamos valores -> transporte_conteo = [medio de transporte, demanda, valor total]
    
    transporte_conteo.sort(reverse = True, key = lambda x:(x[1],x[2])) #ordenamos la lista de forma descendente conforme a la demanda y valor total
    return transporte_conteo #regresamos la lista que obtuvimos 


"""
OPCION 3: VALOR POR PAIS DE IMPORTACIONES Y EXPORTACIONES
----------------------------------------------------------
Para encontrar la lista con los piases que conforman el 80% del valor total en exportaciones e importaciones, lo primero que debemos
calculas es el valor total de todos los datos, por lo que con un ciclo for y un contador sacaremos ese dato, ahora,
para calulcar el porcentaje por pais haremos uso de dos ciclos for, uno anidado dentro del otro, primero tomaremos un pais y con el ciclo anidado
contademos cuantas veces se repite; ya que tenemos la cuenta, sacamos el porcentaje y lo agregamos a la lista con los datos;
por ultimo haremos una lista con los porcentajes acumulados, ya que este valor nos dara pauta para saber cuales paises forman el 80% del valor
total; para esto recorreremos la lista obtenida ya ordenada anteriormente e iremos sumando los porcentajes y agregandolos a la lista final, la condicion
de paro seria que si es mayor a 0.8 salga del bucle. Ordenamos la lista para asi sabes cuales son los paises que mas aportan y asi tener correctamente el orden en el porcentaje acumulado
"""
def porcentaje_paises(direccion): #definimos la funcion y los parametros que le pasarmos -> direccion = ("Imports" o Exports")
    paises = [] #lista donde guardaremos los paises que ya hemos recorrido
    acum_paises = [] #lista para guardar los paises, valor total(por pais) y porcentaje
    valor_total = 0 #inicializamos el contador para el valor total de todos los datos
    for valor in lista_datos: #recorremos la lista de datos para sumar atributo "total_value"
        if valor["direction"] == direccion: #condicion, si corresponde el atributo "direction" a la direccion del parametro de la funcion
            valor_total += int(valor["total_value"]) #actualizamos nuestro valor total 
            
    for ruta in lista_datos: #ahora, recorremos la lista de datos para calcular el valor total por pais 
        pais_actual = [direccion, ruta["origin"]] #guardamos el pais actual y la direccion (exports o impors)
        valor_pais = 0 #inicializamos un contador para el acumulado del valor total
        contador = 0 #inicializamos un contador para saber cuantas veces se repite ese pais
        if pais_actual not in paises: #condicion, si el pais de la iteracion actual no esta en la lista de paises avanzamos, si no pasamos a la siguiente iteración
            for acumulado_pais in lista_datos: #recorremos de nuevo la lista de datos, esta vez para contabilizar el valor total 
                if pais_actual == [acumulado_pais["direction"], acumulado_pais["origin"]]: #condición, si la direccion y pais de la variable pais_actual corresponden a la de la iteración en el bucle anidado
                    valor_pais += int(acumulado_pais["total_value"]) #actualizamos el contador de valor total por pais
                    contador += 1 #acutalizamos contador
            
            porcentaje = round(valor_pais / valor_total,3) #una vez que terminamos de contar para un pais, calculamos el porcentaje
            paises.append(pais_actual) #agregamos el pais que contabilizamos a la lista de paises
            acum_paises.append([direccion, ruta["origin"], contador, valor_pais, porcentaje]) #agregamos valores a la lista -> acum_paises = [direccion(exports o imports), pais, demanda (repeticiones), valor total por pais, porcentaje]
    
    acum_paises.sort(reverse=True, key = lambda x:(x[4], x[3])) #ordenamos nuestra lista obtenida de forma descendente, conforme al porcentaje y al valor total
    
    lista_porcentaje_acum = [] #definimos una nueva lista, para guardar el porcentaje acumulado
    porcentaje_acum = 0 #inicializamos la variable para el porcentaje acumulado
    for paises in acum_paises: #recorremos la lista obtenida 
        porcentaje_acum += paises[4] #actualizamos el porcentaje acumulado
        if porcentaje_acum >= 0.8: #condicion, si el porcentaje acumulado es mayor a 0.8 salimos del buble si no seguimos avanzando
            break
        lista_porcentaje_acum.append([paises[0],paises[1], paises[2], paises[3], paises[4], round(porcentaje_acum,3)]) #agregamos valores a la lista -> lista_porcentaje_acum = [[direccion(exports o imports), pais, demanda (repeticiones), valor total por pais, porcentaje, porcentaje acumulado]
    return lista_porcentaje_acum #regresamos la ultima lista que obtuvimos 

#mandamos llamar a las funciones para asignarles una variable, y asi poder usarlas posteriormente
conteo_exportaciones = demanda_exportacion_importacion("Exports")
conteo_importanciones = demanda_exportacion_importacion("Imports")
    
transporte_exportaciones = transporte_exportacion_importacion("Exports")
transporte_importaciones = transporte_exportacion_importacion("Imports")

valores_paises_exportaciones = porcentaje_paises("Exports")
valores_paises_importaciones = porcentaje_paises("Imports")


"""
Esta función generara un archivo .txt donde escribe las listas que obtuvimos en las funciones anteriores.
"""
def reporte(): 
    
    escribir_archivo = open("reporte_synergy_logistics.txt", "w") #abrimos un archivo .txt en modo escritura donde se colocaran las listas de las funciones anteriores
    
    escribir_archivo.write("\n\t \t \tTOP 10 RUTAS DE EXPORTACIÓN MAS DEMANDADAS \n")
    escribir_archivo.write("{:<3} {:<15} {:<15} {:<8} {:<3} \n".format('','Origen','Destino', 'Demanda', 'Valor Total')) #se da forma a la tabla que se va a imprimir 
    for i in range(1,11):
        escribir_archivo.write("{:<3} {:<15} {:<15} {:<8}  ${:<3} \n".format(i, conteo_exportaciones[i-1][0],conteo_exportaciones[i-1][1],conteo_exportaciones[i-1][2], conteo_exportaciones[i-1][3]))#se da forma a la tabla que se va a imprimir 
    
    escribir_archivo.write("\n\t \t \tTOP 10 RUTAS DE IMPORTACIÓN MAS DEMANDADAS \n")
    escribir_archivo.write("{:<3} {:<15} {:<15} {:<8} {:<3} \n".format('','Origen','Destino', 'Demanda', 'Valor Total'))#se da forma a la tabla que se va a imprimir 
    for i in range(1,11):
        escribir_archivo.write("{:<3} {:<15} {:<15} {:<8}  ${:<3} \n".format(i, conteo_importanciones[i-1][0],conteo_importanciones[i-1][1],conteo_importanciones[i-1][2], conteo_importanciones[i-1][3]))
    
    escribir_archivo.write("\n\t \t \tVALOR POR MODO DE TRANSPORTE (EXPORTACIONES) \n")
    escribir_archivo.write("{:<3} {:<12} {:<15} {:<3} \n".format('','Transporte', 'Demanda','Valor Total'))#se da forma a la tabla que se va a imprimir 
    for i in range(1,5):
        escribir_archivo.write("{:<3} {:<12} {:<15}  ${:<3} \n".format(i, transporte_exportaciones[i-1][0],transporte_exportaciones[i-1][1],transporte_exportaciones[i-1][2]))#se da forma a la tabla que se va a imprimir 
    
    escribir_archivo.write("\n\t \t \tVALOR POR MODO DE TRANSPORTE (IMPORTACIONES) \n")
    escribir_archivo.write("{:<3} {:<12} {:<15} {:<3} \n".format('','Transporte', 'Demanda','Valor Total'))#se da forma a la tabla que se va a imprimir 
    for i in range(1,5):
        escribir_archivo.write("{:<3} {:<12} {:<15}  ${:<3} \n".format(i, transporte_importaciones[i-1][0],transporte_importaciones[i-1][1],transporte_importaciones[i-1][2]))#se da forma a la tabla que se va a imprimir 
        
    escribir_archivo.write("\n\t \t \tPAISES QUE GENERAN EL 80% DEL VALOR EN EXPORTACIONES \n")
    escribir_archivo.write("{:<3} {:<12} {:<15} {:<15} {:<3} \n".format('','País', 'Valor Total','Porcentaje', 'Porcentaje acum'))#se da forma a la tabla que se va a imprimir 
    for pais in range(len(valores_paises_importaciones)):
        escribir_archivo.write("{:<3} {:<12} {:<15} {:<15} {:<3} \n".format(pais+1, valores_paises_exportaciones[pais][1],valores_paises_exportaciones[pais][3],valores_paises_exportaciones[pais][4],valores_paises_exportaciones[pais][5]))#se da forma a la tabla que se va a imprimir 
        
    escribir_archivo.write("\n\t \t \tPAISES QUE GENERAN EL 80% DEL VALOR EN IMPORTACIONES \n")
    escribir_archivo.write("{:<3} {:<12} {:<15} {:<15} {:<3} \n".format('','País', 'Valor Total','Porcentaje', 'Porcentaje acum'))#se da forma a la tabla que se va a imprimir 
    for pais in range(len(valores_paises_importaciones)):
        escribir_archivo.write("{:<3} {:<12} {:<15} {:<15} {:<3} \n".format(pais+1, valores_paises_importaciones[pais][1],valores_paises_importaciones[pais][3],valores_paises_importaciones[pais][4],valores_paises_importaciones[pais][5]))#se da forma a la tabla que se va a imprimir 
    escribir_archivo.close() #cerramos el archivo
    
"""
Definimos la función para limpiar la pantalla, esta funcion identifica por si sola en que sistema estamos
"""   
def borrarPantalla(): 
    if os.name == "posix" or os.name == "mac": #Si el sistema es linux
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos": #Si el sistema es de microsoft
        os.system ("cls")

def menu():
    while True: #Bucle para opciones del menú
        borrarPantalla() #limpiamos pantalla 
        #menu de opciones
        print ("Menú de opciones")
        print ("\t1-. Listado de las 10 rutas de exportación e importacion mas demandadas")
        print ("\t2-. Valor por medio de transporte")
        print ("\t3-. Valor total de importaciones y exportaciones")
        print ("\t4-. Generar reporte en archivo .txt")
        print ("\t5-. Salir")
        opcionMenu = input("Ingresa una opción ")
        
        #si se selecciono tal opcion
        if opcionMenu == "1":
            borrarPantalla() #limpiamos pantalla 
            #imprimimos los valores correspondientes a la opción del menu
            print("\n\t \t \tTOP 10 RUTAS DE EXPORTACIÓN MAS DEMANDADAS \n")
            print("{:<3} {:<15} {:<15} {:<8} {:<3} \n".format('','Origen','Destino', 'Demanda', 'Valor Total'))
            for i in range(1,11):
                print("{:<3} {:<15} {:<15} {:<8} ${:<3}".format(i, conteo_exportaciones[i-1][0],conteo_exportaciones[i-1][1],conteo_exportaciones[i-1][2], conteo_exportaciones[i-1][3]))
            print("\n") 
            print("\n") 
            print("\n\t \t \tTOP 10 RUTAS DE IMPORTACIÓN MAS DEMANDADAS \n")
            print("{:<3} {:<15} {:<15} {:<8} {:<3} \n".format('','Origen','Destino', 'Demanda', 'Valor Total'))
            for i in range(1,11):
                print("{:<3} {:<15} {:<15} {:<8} ${:<3}".format(i, conteo_importanciones[i-1][0],conteo_importanciones[i-1][1],conteo_importanciones[i-1][2], conteo_importanciones[i-1][3]))
            print("\n") 
            input("\npulsa enter para continuar...")
            
            
        elif opcionMenu == "2":
            borrarPantalla() #limpiamos pantalla 
            #imprimimos los valores correspondientes a la opción del menu
            print("\n\t \t \tVALOR POR MODO DE TRANSPORTE (EXPORTACIONES) \n")
            print("{:<3} {:<12} {:<15} {:<3} \n".format('','Transporte', 'Demanda','Valor Total'))
            for i in range(1,5):
                print("{:<3} {:<12} {:<15} ${:<3}".format(i, transporte_exportaciones[i-1][0],transporte_exportaciones[i-1][1],transporte_exportaciones[i-1][2]))
            print("\n") 
            print("\n") 
            print("\n\t \t \tVALOR POR MODO DE TRANSPORTE (IMPORTACIONES) \n")
            print("{:<3} {:<12} {:<15} {:<3} \n".format('','Transporte', 'Demanda','Valor Total'))
            for i in range(1,5):
                print("{:<3} {:<12} {:<15} ${:<3}".format(i, transporte_importaciones[i-1][0],transporte_importaciones[i-1][1],transporte_importaciones[i-1][2]))
            print("\n") 
            input("\npulsa enter para continuar...")
            
        elif opcionMenu == "3":
            borrarPantalla() #limpiamos pantalla 
            #imprimimos los valores correspondientes a la opción del menu
            print("\n\t \t \tPAISES QUE GENERAN EL 80% DEL VALOR EN EXPORTACIONES \n")
            print("{:<3} {:<12} {:<15} {:<15} {:<3} \n".format('','País', 'Valor Total','Porcentaje', 'Porcentaje acum'))
            for pais in range(len(valores_paises_importaciones)):
                print("{:<3} {:<12} {:<15} {:<15} {:<3}".format(pais+1, valores_paises_exportaciones[pais][1],valores_paises_exportaciones[pais][3],valores_paises_exportaciones[pais][4],valores_paises_exportaciones[pais][5]))
            print("\n") 
            print("\n") 
            
            print("\n\t \t \tPAISES QUE GENERAN EL 80% DEL VALOR EN IMPORTACIONES \n")
            print("{:<3} {:<12} {:<15} {:<15} {:<3} \n".format('','País', 'Valor Total','Porcentaje', 'Porcentaje acum'))
            for pais in range(len(valores_paises_importaciones)):
                print("{:<3} {:<12} {:<15} {:<15} {:<3}".format(pais+1, valores_paises_importaciones[pais][1],valores_paises_importaciones[pais][3],valores_paises_importaciones[pais][4],valores_paises_importaciones[pais][5]))
            print("\n") 
            input("\npulsa enter para continuar...")
            
        elif opcionMenu == "4":
            borrarPantalla() #limpiamos pantalla 
            reporte() #Mandamos a llamar a la funcion reporte para que se genere el archivo .txt
            #inidicamos la ruta donde se guardo el archivo
            print("\n EL REPORTE HA SIDO GENERADO, SE GUARDO EN LA MISMA CARPETA QUE ESTE ARCHIVO \n")
            input("\npulsa enter para continuar...")
            
        elif opcionMenu == "5":
            exit() #salimos del programa 
            
        else:
            print ("")
            input("No has pulsado ninguna opción correcta...\n pulsa una tecla para continuar...")
            
menu() #mandamos llamar a la función menu que es la que mandara llamar a todas las demas funciones
        
        
            
            

    
    
    
