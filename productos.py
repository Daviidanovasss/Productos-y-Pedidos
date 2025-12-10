from bintrees import AVLTree

productos = AVLTree()

productos.insert(1, 'harina')
productos.insert(2, 'agua')
productos.insert(3, 'manzanas')
productos.insert(4, 'galletas')
productos.insert(5, 'yogures')
productos.insert(6, 'cereales')
productos.insert(7, 'miel')

def productos_dict():
    return {clave: valor for clave, valor in productos.items()}