# Books_Lib
Books_Lib es una biblioteca de Python que te permite trabajar con datos de los libros.
## Instalación
Puedes instalar la biblioteca usando `pip install Books_Lib`
## Uso
Aquí hay un ejemplo de cómo puedes usar la biblioteca para obtener información sobre Pokémon aleatorios:
```python
from Books_Lib import SelectBooks
# Crear una instancia de SelectBooks
_author = input("ingresa el nombre a buscar ")
resultado = getAuthor(_author)
print(resultado)

```
## Archivo CSV de Pokémon
La biblioteca utiliza un archivo CSV llamado books.csv que contiene datos de Pokémon. Este archivo se incluye 
en el paquete y se utiliza para generar los datos de los libros. Si
necesitas acceder al archivo books.csv directamente, puedes encontrarlo en el directorio SelectBooks.
## Autor
Milton Alejandro Angel Cardenas 