from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import json
from pedidos import pedidos
from productos import productos_dict, productos

app = FastAPI()

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
       

@app.post("/productos")
async def agregar_producto(request: Request):
    data = await request.json()
    producto = data.get("nombre")
    nuevo_id = len(productos) + 1
    if producto in productos:
            return JSONResponse(content={"message": "Producto ya exixtente"}, status_code=201)
    productos.insert(nuevo_id, producto)
    return JSONResponse(content={"message": "Producto añadido correctamente"}, status_code=201)


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

   

@app.delete("/pedidos")
async def delete_pedido(pedido_id: int):
    if pedidos.eliminar(pedido_id) == False:
        raise HTTPException(status_code=404, detail="Pedido no existente")
    else:
        pedidos.eliminar(pedido_id)
        return JSONResponse(content={"message": "Pedido eliminado correctamente"}, status_code=201)
    

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