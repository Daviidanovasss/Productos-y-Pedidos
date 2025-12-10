# Importamos de los módulos necesarios para construir la API
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json

# Importamos la estructura de la tabla hash con los pedidos
# y el árbol AVL que almacena los productos
from pedidos import pedidos
from productos import productos_dict, productos

# Creamos la aplicación FastAPI.
app = FastAPI()

# Creamos el endpoint raíz '/' donde se generan las estructuras JSON de productos y pedidos,
# se serializan temporalmente y se devuelven json completas de ambos elementos en la respuesta.
@app.get("/")
def root():
    productos_json = productos_dict()
    productos_string = json.dumps(productos_json)
    productos_serializados = json.loads(productos_string)
    pedidos_string = json.dumps(pedidos.dict())
    pedidos_serializados = json.loads(pedidos_string)
    return JSONResponse(content={
        "Lista de pedidos": pedidos_serializados,
        "Lista de productos": productos_serializados
    },
    status_code=201
)

# Definimos el endpoint GET '/productos' que recibe un ID y devuelve el producto asociado.
# Este proceso incluye serializar el árbol AVL, recorrer sus claves y comprobar si existe el ID solicitado.
@app.get("/productos")
async def get_productos(product_id: str):
    productos_json = productos_dict()
    productos_string = json.dumps(productos_json)
    productos_serializados = json.loads(productos_string)
    print(productos_serializados)
    for id_producto in productos.keys():
        if id_producto == product_id:
            return JSONResponse(content={"message": f"El producto es: {productos_serializados[product_id]}"}, status_code=201)
    raise HTTPException(status_code=404, detail="Producto no existente")


# Creamos el endpoint GET '/pedidos' que puede devolver todos los pedidos o uno específico.
# Primero serializamos la tabla hash y después validamos si el pedido existe antes de devolverlo.
@app.get("/pedidos")
async def get_pedidos(pedido_id : int = None):
   pedidos_string = json.dumps(pedidos.dict())
   pedidos_serializados = json.loads(pedidos_string)
   if pedido_id == None:
        return JSONResponse(content=(f'Los pedidos son:{pedidos_serializados}'))
   if pedidos.obtener(pedido_id) == False:
        raise HTTPException(status_code=404, detail="Pedido no existente")
   else:
        return JSONResponse(content={"message": f"El pedido es: {pedidos_serializados[pedido_id]}"}, status_code=201)
       
# Creamos el endpoint POST '/productos' que permite añadir un producto nuevo.
# Iniciamos leyendo el JSON recibido, generamos un nuevo ID y verificamos que el producto no exista previamente.
@app.post("/productos")
async def agregar_producto(request: Request):
    data = await request.json()
    producto = data.get("nombre")
    nuevo_id = len(productos) + 1
    if producto in productos:
            return JSONResponse(content={"message": "Producto ya exixtente"}, status_code=201)
    productos.insert(nuevo_id, producto)
    return JSONResponse(content={"message": "Producto añadido correctamente"}, status_code=201)

# Definimos el endpoint POST '/pedidos' para crear un pedido nuevo.
# Se validan que los productos estén dentro del árbol binario, se genera un nuevo ID 
# y se inserta toda la información en la tabla hash.
@app.post("/pedidos")
async def agregar_producto(request: Request):
    data = await request.json()
    productos_nuevos = data.get("productos")
    for producto_nuevo in productos_nuevos:
        if producto_nuevo not in productos.values():
                raise HTTPException(status_code=404, detail="1 o varios pedidos no disponibles")
    nuevo_id = int(pedidos.numero_pedidos() + 1)
    print(productos)
    pedidos.insertar(nuevo_id, productos_nuevos)
    return JSONResponse(content={"message": "Pedido añadido correctamente"}, status_code=201)

   
# Creamos el endpoint DELETE '/pedidos' para eliminar un pedido según su ID.
# Verificamos si existe y si es así, lo eliminamos de la tabla hash.
@app.delete("/pedidos")
async def delete_pedido(pedido_id: int):
    if pedidos.eliminar(pedido_id) == False:
        raise HTTPException(status_code=404, detail="Pedido no existente")
    else:
        pedidos.eliminar(pedido_id)
        return JSONResponse(content={"message": "Pedido eliminado correctamente"}, status_code=201)
    
    
# Definimos el endpoint PUT '/pedidos/{pedido_id}' para modificar un pedido existente.
# Procesamos el JSON recibido, validamos los nuevos productos, eliminamos el pedido previo
# y lo recreamos con la información actualizada.
@app.put("/pedidos/{pedido_id}")
async def put_product(pedido_id: int, request: Request):
    data = await request.json()
    nuevos_productos = data.get("productos")
    if pedidos.eliminar(pedido_id) == False:
        raise HTTPException(status_code=404, detail="Pedido no existente")
    else:
        pedidos.eliminar(pedido_id)
        for nuevo_produto in nuevos_productos:
            if nuevo_produto not in productos:
                raise HTTPException(status_code=404, detail="1 o varios pedidos no disponibles")
        pedidos.insertar(pedido_id, nuevos_productos)
        return JSONResponse(content={"message": f'Pedido modificado correctamente'}, status_code=201)