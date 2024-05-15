# Books_pkg
Books_pkg es una biblioteca de Python que te permite trabajar con datos de los libros.
## Instalación
Puedes instalar la biblioteca usando `pip install Books_pkg`
## Uso
Aquí hay un ejemplo de cómo puedes usar la biblioteca para obtener información sobre los autore y los nombre de los libros:
```python
from Books_pkg import RandomBooks
# Crear una instancia de SelectBooks
_author = input("ingresa el nombre a buscar ")
resultado = getAuthor(_author)
print(resultado)

```
## Archivo CSV de Pokémon
La biblioteca utiliza un archivo CSV llamado books.csv que contiene datos de Pokémon. Este archivo se incluye 
en el paquete y se utiliza para generar los datos de los libros. Si
necesitas acceder al archivo books.csv directamente, puedes encontrarlo en el directorio RandomBooks.
## Autor
Milton Alejandro Angel Cardenas 