from operator import itemgetter

class TablaHash:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]

    def _hash(self, clave):
        return clave % self.tamaño
    
    def numero_pedidos(self):
        total_pedidos = 0
        for indice in self.tabla:
            total_pedidos = total_pedidos + len(indice)
        return total_pedidos
    
    def insertar(self, clave, valor):
        indice = self._hash(clave)
        self.tabla[indice].append((clave, valor))

    def obtener(self, clave):
        indice = self._hash(clave)
        for k, v in self.tabla[indice]:
            if k == clave:
                return v
        return False 
    
    def eliminar(self, clave):
        indice = self._hash(clave)
        bucket = self.tabla[indice]
        for i, (key, valor) in enumerate(bucket):
            if key == clave:
                del bucket[i]
                return True
        return False
   
    def actualizar(self, clave, valor):
        indice = self._hash(clave)
        for k in self.tabla[indice]:
            if k == clave:
                self.tabla.remove(indice - 1)
                self.tabla.append((clave, valor))

    def dict(self):
        resultado = []
        for indice in self.tabla:
            for clave, valor in indice:
                resultado.append({
                    "id": clave,
                    "productos": valor
                })
        resultado.sort(key=itemgetter("id"))
        return resultado


pedidos = TablaHash(3)



pedidos.insertar(1, ['harina', 'galletas', 'cereales'])
pedidos.insertar(2, ['agua', 'yogures', 'miel'])
pedidos.insertar(3, ['manzanas', 'harina', 'yogures'])
