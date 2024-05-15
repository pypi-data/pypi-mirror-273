# Lib_charPk
Pokemon_Library es una biblioteca de Python que te permite trabajar con datos de bibliografias de libros.
## Instalación
Puedes instalar la biblioteca usando `pip install Lib_charPk`
## Uso
Aquí hay un ejemplo de cómo puedes usar la biblioteca para obtener información sobre Bibliografias de libros:

```python
from fndy_bks import findbook

# Crear una instancia de RandomPokemon
book = findbook()
# Generar un Pokemón aleatorio
book.generate_books()
# Obtener el nombre del libro solicitado
book_title = book.getTitle()
# Imprimir el nombre del Pokemón
print("EL libro es: ", book_title)
```
## Archivo CSV de Book
La biblioteca utiliza un archivo CSV llamado books.csv que contiene datos de libros. Este archivo se incluye en el paquete y se utiliza para generar bibliografias aleatorios. Si
necesitas acceder al archivo pokemon.csv directamente, puedes encontrarlo en el directorio find_book.
## Autor
Missael Angel Cardenas 