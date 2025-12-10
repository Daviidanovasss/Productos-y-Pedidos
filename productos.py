from bintrees import AVLTree

# Creamos una estructura de datos tipo árbol AVL
productos = AVLTree()

# Insertamos en el árbol los productos disponibles, con su ID correcpondiente.
productos.insert(1, 'harina')
productos.insert(2, 'agua')
productos.insert(3, 'manzanas')
productos.insert(4, 'galletas')
productos.insert(5, 'yogures')
productos.insert(6, 'cereales')
productos.insert(7, 'miel')

# Definimos una función que convierte el árbol en un diccionario estándar de Python.
# Esta conversión permite serializar los datos fácilmente y utilizarlos en formato JSON.
def productos_dict():
    return {clave: valor for clave, valor in productos.items()}