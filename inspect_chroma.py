import sys
import os
import chromadb
from app.core.config import settings

# Asegurar que podemos importar desde app
sys.path.append(os.getcwd())

def inspect_chroma():
    print("--- Inspeccionando ChromaDB ---")
    
    # Conectarse a la DB persistente
    client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
    
    # Listar colecciones
    collections = client.list_collections()
    print(f"\nColecciones encontradas: {[c.name for c in collections]}")
    
    if not collections:
        print("No hay colecciones. Ingiere algún documento primero.")
        return

    # Usar la primera colección (generalmente solo hay una por defecto o la que definiste)
    collection_name = collections[0].name
    collection = client.get_collection(collection_name)
    
    count = collection.count()
    print(f"\nColección: '{collection_name}'")
    print(f"Total de documentos (chunks): {count}")
    
    if count == 0:
        return

    # Obtener algunos items para visualizar (limitado a 3)
    # Chroma permite hacer 'peek' o 'get'
    data = collection.peek(limit=3)
    
    print("\n--- Muestra de datos (primeros 3 chunks) ---")
    
    ids = data['ids']
    metadatas = data['metadatas']
    documents = data['documents']
    
    for i in range(len(ids)):
        print(f"\n[Chunk {i+1}]")
        print(f"ID: {ids[i]}")
        print(f"Metadatos: {metadatas[i]}")
        print(f"Contenido (primeros 200 chars): {documents[i][:200]}...")

if __name__ == "__main__":
    try:
        inspect_chroma()
    except Exception as e:
        print(f"Error inspeccionando ChromaDB: {e}")
