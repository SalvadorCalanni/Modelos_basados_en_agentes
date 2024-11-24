import networkx as nx
import numpy as np



def generar_estimulo(coclea, largo):
  '''Genera un estímulo de largo 'largo' en la red coclea'''
  max = len(coclea) - largo
  inicio_estim = np.random.randint(0, max+1)
  return list(range(inicio_estim, inicio_estim + largo))

def generar_estimulos_dist_reg(coclea, largo, distancia_interestim):
  '''Genera estímulos de largo 'largo' en la red coclea con una distancia entre ellos de 'distancia_interestim'''
  max = len(coclea) - (largo * 2 + distancia_interestim)
  inicio_estim = np.random.randint(0, max+1)
  estimulos = []
  for i in range (inicio_estim, inicio_estim + largo):
    estimulos.append(i)
  for i in range (inicio_estim + largo + distancia_interestim, inicio_estim + largo*2 + distancia_interestim):
    estimulos.append(i)
  return estimulos
  
def generar_estimulos_dist_rand(coclea, largo_max):
  largo = np.random.randint(1, largo_max)
  estim1 = generar_estimulo(coclea, largo)
  largo = np.random.randint(1, largo_max)
  estim2 = generar_estimulo(coclea, largo)
  return estim1 + estim2
  
def generar_estimulos_dist_rand_largo_fijo(coclea, largo):
  estim1 = generar_estimulo(coclea, largo)
  estim2 = generar_estimulo(coclea, largo)
  return estim1 + estim2

def generar_estimulos_largo_partido(coclea, largo, cantidad):
  largo_ind = largo // cantidad
  estimulos = []
  for i in range(cantidad):
    estimulos += generar_estimulo(coclea, largo_ind)
  return estimulos

def vertices_estimulo(nucleo, estimulo):
  '''Devuelve los vértices del núcleo que están en el estímulo'''
  edges_estimulo = []
  for j in nucleo.edges():
    if j[0] in estimulo or j[1] in estimulo:
      edges_estimulo.append(j)
  return edges_estimulo

def actualizar_pesos(nucleo, edges_estimulo, estimulo):
  '''Actualiza los pesos de las aristas del núcleo que están en el estímulo'''
  for j in edges_estimulo:
    if j[0] in estimulo and j[1] in estimulo:
      nucleo[j[0]][j[1]]['weight'] = nucleo[j[0]][j[1]]['weight'] + 2
    else:
      nucleo[j[0]][j[1]]['weight'] = nucleo[j[0]][j[1]]['weight'] - 1
      
      
def eliminar_pesos_negativos(nucleo):
  '''Elimina las aristas con peso negativo'''
  for j in list(nucleo.edges()):
    if nucleo[j[0]][j[1]]['weight'] < 0:
      nucleo.remove_edge(j[0], j[1])
      
      
def iniciar_red (n_neu, peso_inicial):
    coclea = list(range(0, n_neu))

    nucleo = nx.complete_graph(n_neu)


    #Inicialización de pesos
    for u, v in nucleo.edges():
        nucleo[u][v]['weight'] = peso_inicial
    return nucleo, coclea    
 
def entrenar(nucleo, coclea, largo_estim, cantidad_estim, pasos):
    
    lista_vertices = []
    for i in range(pasos):

        estim = generar_estimulos_largo_partido(coclea, largo_estim, cantidad_estim)

        edges_estimulo = vertices_estimulo(nucleo, estim)

        actualizar_pesos(nucleo, edges_estimulo, estim)

        eliminar_pesos_negativos(nucleo)

        lista_vertices.append(len(list(nucleo.edges())))
    
    return lista_vertices
 
def x_tau_porcentaje (lista_vertices, porcentaje):
    valor = (max(lista_vertices)-min(lista_vertices))*(porcentaje/100)+min(lista_vertices)
    dif = []
    
    i = 0
    me_pase = False #hago esto porque sabemos que una vez que pase ese valor se va a alejar
    
    while i < len(lista_vertices) and not me_pase:
        if lista_vertices[i]-valor < 0:
            me_pase = True
        dif.append(abs(lista_vertices[i]-valor))
        i += 1
        
    return (dif.index(min(dif)), valor)
  
def x_tau_medio (lista_vertices):
    y = (lista_vertices[0] + lista_vertices[-1]) / 2 
    dif = []
    for i in lista_vertices:
        dif.append(abs(i-y))
    return (dif.index(min(dif)), y)