# BiblioDig
 Es una biblioteca de Python que nos permite trabajar con libros de distintos autores
 ## Instalación
 Puedes instalar la biblioteca usando pip install BiblioDig_Py
 ## Uso
 Aquí hay un ejemplo de cómo puedes usar la biblioteca para obtener información sobre Pokémon aleatorios:
 python
 from Pokemon_Library import RandomPokemon
 # Crear una instancia de RandomPokemon
 pokemon = RandomPokemon()
 # Generar un Pokemón aleatorio
 pokemon.generate_random()
 # Obtener el nombre del Pokemón generado
 pokemon_name = pokemon.getName()
 # Imprimir el nombre del Pokemón
 print("Nombre del Pokemón:", pokemon_name)
 
 ## Archivo CSV de Books
 La biblioteca utiliza un archivo CSV llamado books.csv que contiene datos de Auotores y Libros. Este archivo se incluye en el paquete y se utiliza para encontrar libros y autores. Si 
necesitas acceder al archivo books.csv directamente, puedes encontrarlo en el directorio buscador_libros.
 ## Autor
 Luz Lizeth Vazquez 