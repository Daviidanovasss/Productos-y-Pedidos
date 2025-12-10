from operator import itemgetter

class TablaHash:

    # Inicializamos la tabla hash con el tamaño indicado.
    # Para cada posición de la tabla se crea una lista vacía donde se almacenarán los elementos.
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]

    # Calculamos la posición dentro de la tabla hash a partir de la clave,
    # aplicando la operación módulo para mantener el índice dentro del rango válido.
    def _hash(self, clave):
        return clave % self.tamaño
    
    # Este método recorre todos los índices y suma la cantidad total de pedidos almacenados,
    # devolviendo el número total de elementos insertados en la tabla hash.
    # Nos servirá más adelante para calcular el índice de los nuevos pedidos automáticamente.
    def numero_pedidos(self):
        total_pedidos = 0
        for indice in self.tabla:
            total_pedidos = total_pedidos + len(indice)
        return total_pedidos
    

    # Inserta un nuevo pedido. Para ello:
    # 1) Calculamos en qué índice debe colocarse.
    # 2) Añadimos su id (clave) y productos (valor) dentro de la lista correspondiente.
    def insertar(self, clave, valor):
        indice = self._hash(clave)
        self.tabla[indice].append((clave, valor))

    # Permite obtener el valor asociado a una clave concreta.
    # Buscamos dentro del índice correspondiente y devolvemos el valor si lo existe.
    def obtener(self, clave):
        indice = self._hash(clave)
        for key, valor in self.tabla[indice]:
            if key == clave:
                return valor
        return False 
    
    # Elimina un pedido existente a partir de su clave.
    # Recorremos el índice correspondiente, y si encuentramos la clave, eliminamos el elemento.
    def eliminar(self, clave):
        indice = self._hash(clave)
        bucket = self.tabla[indice]
        for i, (key, valor) in enumerate(bucket):
            if key == clave:
                del bucket[i]
                return True
        return False
   
    # Actualiza el valor asociado a una clave concreta.
    # Si encontramo la clave en el índice calculado, eliminamos el registro antiguo
    # y añadimos uno nuevo con la información actualizada.
    def actualizar(self, clave, valor):
        indice = self._hash(clave)
        for key in self.tabla[indice]:
            if key == clave:
                self.tabla.remove(indice - 1)
                self.tabla.append((clave, valor))

    # Convierte toda la tabla hash en una lista de diccionarios,
    # que posteriormente puede ser serializada a JSON.
    # Cada elemento contiene el id y la lista de productos asociados.
    def dict(self):
        resultado = []
        for indice in self.tabla:
            for clave, valor in indice:
                resultado.append({
                    "id": clave,
                    "productos": valor
                })
        
        # Ordena la lista resultante por el id del pedido, facilitando su recuperación ID.
        resultado.sort(key=itemgetter("id"))
        return resultado

# Creamos la tabla hash con un tamaño inicial de 3 índices
pedidos = TablaHash(3)


#Insertamos 3 pedidos de ejemplo en la tabla, com su ID y sus productos.
pedidos.insertar(1, ['harina', 'galletas', 'cereales'])
pedidos.insertar(2, ['agua', 'yogures', 'miel'])
pedidos.insertar(3, ['manzanas', 'harina', 'yogures'])