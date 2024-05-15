# Biblioteca

La clase `Biblioteca` es una representación de una colección de libros en Python. Permite gestionar y consultar información sobre libros almacenados en un archivo CSV.

## Descripción

Esta biblioteca proporciona funcionalidades para buscar libros por título o por autor, así como para acceder y modificar atributos específicos de libros. Está diseñada para ser fácil de usar y extender según sea necesario.

## Instalación

1. Clona este repositorio.
2. Asegúrate de tener instalado `pandas`.
3. Coloca el archivo `books_new.csv` en el mismo directorio que el script Python.

```bash
pip install pandas

import pkg_resources
import pandas as pd

class Biblioteca:
    FILE_PATH = pkg_resources.resource_filename(__name__, 'books_new.csv')

    def __init__(self):
        self._file = pd.read_csv(Biblioteca.FILE_PATH)
        self._title = None
        self._author = None
        self._genre = None
        self._sub_genre = None
        self._height = None
        self._publisher = None

    def buscar_libro(self, titulo):
        libro = self._file[self._file['Title'] == titulo]

        if libro.empty:
            return f"El libro '{titulo}' no se encontró."
        else:
            autor = libro['Author'].values[0]
            genero = libro['Genre'].values[0]
            paginas = libro['Height'].values[0]
            editorial = libro['Publisher'].values[0]

            return {
                "Author": autor,
                "Genre": genero,
                "Height": paginas,
                "Publisher": editorial
            }

    def buscar_por_autor(self, autor):
        libros = self._file[self._file['Author'] == autor]

        if libros.empty:
            return f"El autor '{autor}' no tiene libros registrados."
        else:
            resultados = []
            for _, libro in libros.iterrows():
                resultados.append({
                    "Title": libro['Title'],
                    "Genre": libro['Genre'],
                    "Height": libro['Height'],
                    "Publisher": libro['Publisher']
                })
            return resultados

    # Getters
    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def genre(self):
        return self._genre

    @property
    def sub_genre(self):
        return self._sub_genre

    @property
    def height(self):
        return self._height

    @property
    def publisher(self):
        return self._publisher

    # Setters
    @title.setter
    def title(self, value):
        self._title = value

    @author.setter
    def author(self, value):
        self._author = value

    @genre.setter
    def genre(self, value):
        self._genre = value

    @sub_genre.setter
    def sub_genre(self, value):
        self._sub_genre = value

    @height.setter
    def height(self, value):
        self._height = value

    @publisher.setter
    def publisher(self, value):
        self._publisher = value

# Ejemplo de uso:
biblioteca = Biblioteca()
resultado_libro = biblioteca.buscar_libro('Some Book Title')
print(resultado_libro)

resultado_autor = biblioteca.buscar_por_autor('Some Author Name')
print(resultado_autor)

# Ejemplo de uso de getters y setters
biblioteca.title = "Nuevo Título"
print(biblioteca.title)


### Explicación del Archivo README.md:

- **Título y Descripción**: Proporciona una breve descripción de la biblioteca.
- **Instalación**: Instrucciones para instalar las dependencias necesarias y colocar el archivo CSV en el directorio adecuado.
- **Uso**: Ejemplo de código que muestra cómo utilizar la clase `Biblioteca`, incluyendo la creación de una instancia, la búsqueda de libros por título y autor, y el uso de getters y setters.
- **Métodos**: Descripción de los métodos `buscar_libro` y `buscar_por_autor`, incluyendo parámetros y valores de retorno.
- **Getters y Setters**: Lista de atributos para los cuales se han definido getters y setters.
