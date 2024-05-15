import pkg_resources
import pandas as pd
class BuscarBiblioteca:

    FILE_PATH = pkg_resources.resource_filename(__name__, 'books_new.csv')

    def __init__(self):
        self._file = pd.read_csv(BuscarBiblioteca.FILE_PATH)
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
