# 2.2.2
## Hablar de por que son sumas cuadradas
## Especificar que sólo se normaliza para el conjunto de 5 atributos (Lo hiciste en 2.3.2 capaz es al pedo)

# Script 1
## Si intentas hacer un movimiento con el jugador 2 donde no tiene ficha te dice que ahi no hay una ficha del jugador 1 (cambiar string de error)

## Reemplazar:
### Cambiar: "Después de múltiples pruebas (se expanden las mismas en la sección 3.2)"
### Por: "Después de múltiples pruebas (las cuales se profundizan en la sección 3.2)"

# 2.3.2
## Quedó raro el i_-ésima o _i-ésima
## BASTA DE DECIR SE EXPANDE ESTO JAJAJA (Yo sacaría el último o lo reescribiria como al resto)

## Reemplazar:
### Cambiar: "diversas técnicas de normalización (se expande esto en las secciones...)"
### Por: "diversas técnicas de normalización (las cuales se detallan las secciones...)"

# 2.4.1
## Reemplazar:
### Cambiar: "consideraciones al entrenar"
### Por: "conclusiones al entrenar" (Capaz no???????)

# 2.4.2
## Y dale con se expande este punto en la sección 3.2
## Agregar a consideraciones a entrenar que el jugador escencialmente es entrenado a luchar contra su yo del pasado y que esto puede por consiguiente dar overfitting.

# 3.1
## Reemplazar:

### Cambiar: "relativa eficiencia"
### Por: "relativa eficacia"
### Y recursar IIS (?

### Cambiar: "se encaró la experimentación"
### Por: "la experimentación se encaró"

### Cambiar: "(al menos de errores identificados)"
### Por: "(al menos identificados)"
### Borraria capaz el relativamente que va antes

### Cambiar: "A falta de suficientes corridas para generar agrupamientos de configuraciones (como las obtenidas en el Test de Friedman), se compararon manualmente..."
### Por: "Debido al largo tiempo de ejecución no se pudieron generar múltiples instancias para cada configuración paramétrica, (lo cual hubiera sido útil para realizar un test de Friedman), en su lugar se compararon manualmente..."

### Cambiar: ""
### Por: ""

# 3
## (3.x 0 solo 3.1) Aclarar que siempre salvo en 3.5 se jugó contra el player anterior (si mismo)

# 3.2.1
## Pruebas y resultados: 
### Se hicieron algunas pruebas, alternando el learning ratio entre 0.5 y 0.9 y los pesos iniciales entre [0.9,0.9,0.9,0.9], [0.5,0.5,0.5,0.5] y [0.1,0.9,0.1,0.1]
## Problemas detectados:
### Tras algunas ejecuciones, B estaba teniendo demasiada prioridad en el tablero, esto causaba un loop en las decisiones de ambos jugadores, resultando en simulaciones que nunca terminaban hasta que se declaraba un empate. Tras una determinada cantidad de empates el resultado de toda iteración siempre terminaba en empate. A causa de esto se decidió implementar la métrica D.
### A su vez determinamos que una causa de las cadenas indefinidas de empate era que del conjunto de mejores tableros encontrados siempre se elegia el primero, toda simulación para determinados pesos daba siempre el mismo resultado.

# 3.2.2
## Introducción
### Se agregó la metrica D y se decidió que en caso de múltiples movimientos con igual v, elegir uno aleatoriamente de los mismos.
## Pruebas y resultados
### Se probaron con las mismas configuraciones que 3.2.1
### La nueva métrica D ayudó a disminuir la producción de empates, sin embargo estos eventualmente ocurrian, causando la misma cadena
## Problemas detectados:
### Detectamos que los primeros empates estaban causando ruido para el algoritmo de aprendizaje, penalizando un tablero en donde el jugador hizo bien sus jugadas. Esto causaba que los pesos se ajusten a valores negativos, y el jugador buscara maximizar su distancia a la meta en lugar de minimizar la misma, generando loops.

# 3.2.3
## Introducción
### Se decidó aplicarle un valor absoluto a los pesos luego de su reajuste.
## Pruebas y resultados:
### Se hicieron pruebas alternando el learning ratio entre 0.1, 0.5, 0.9 y con enfriamiento, así como con los mismos pesos iniciales de 3.2.1
### La cantidad de empates se minimizó enormement y el algoritmo lograba romper cadenas de empates consecutivos
## Problemas detectados:
### Nos dimos cuenta que aplicar un valor absoluto a los pesos rompia con los fundamentos de LMS, dado que al ajustar con un peso como -0.9, este estaba siendo transformado a 0.9 (en lugar de un valor positivo cercano a 0), por lo tanto el peso -0.9 valia más que el peso positivo 0.5.
### También nos dimos cuenta que esto sólo era un parche para el ruido que los empates introducian en los ajustes del algoritmo y no una solución al problema del ruido.

# 3.2.4
## Introducción
### Se decidó que en caso de empate no se ajusten los pesos del algoritmo, con el fin de eliminar el ruido que causaban los mismos.
## Pruebas y resultados:
### Se probaron con las mismas configuraciones que 3.2.3
### Los resultados mejoraron pero el algoritmo volvia e entrar en cadenas infinitas de empates a causa de otro ruido.
## Problemas detectados:
### Al perder los pesos pasaban a ser negativos, causando el mismo loop que en 3.2.2

# 3.2.5
## Introducción
### Se probaron dos algoritmos distintos:
#### El primero normalizaba los pesos con la norma min-max entre 0 y 1. De esta forma el ajuste era coherente con su previo valor.
#### El segundo separaba los parametros obtenidos, en lugar de recibir restas del estado del campo se recibian todos los parametros. Esto daba lugar a un ajuste válido en donde hayan pesos negativos.
## Pruebas y resultados
### Se probaron con las mismas configuraciones que 3.2.3
### Se obtuvieron mejores resultados del segundo algoritmo. Estos mismos se estudarán en detalle en la siguiente sección.
## Problemas detectados:
### Para algunas configuraciones paramétricas especificas los algoritmos seguian quedando atascados en empates. Sin embargo estos casos fueron dentro de todos raros y se encontraron configuraciones paramétricas donde lo mismo no ocurría.

# 3.4
## Borrar: "como se menciona en la sección anterior", está implicito y no aporta a esta sección


# 3.5
## La idea de entrenar contra un jugador que no estuviera intentando ganar fue descartada rapidamente. Debido a que por las reglas de las Damas Chinas, si el oponente deja una pieza en su triangulo (un evento altamente probable considerando un jugador aleatorio) y el jugador comienza a llenar el triangulo opuesto (atascando la pieza del oponente), el juego no finalizará. El jugador deberá retirar piezas del triangulo del oponente para habilitar movimientos que incentiven al oponente a retirar sus piezas del triangulo con el fin de que el jugador coloque las suyas. Esto no sólo es contraintuitivo para el ajusto de los pesos contra jugador de Damas Chinas que esté intentando ganar, sino que puede demorar una cantidad descomunal de turnos.
## A continuación se proporcionan una grafica sobre las Victorias/Derrotas/Empates vs un jugador aleatorio y una grafica del error cuadratico de V. Como se puede apreciar, al contar los empates el error cuadratico medio oscila y no logra converger a un valor.