import pkg_resources
import pandas as pd

class BuscadorLibros:
    FILE_PATH = pkg_resources.resource_filename(__name__, 'books.csv')


    def buscar_titulo(self, titulo):
        file = self.FILE_PATH
        datos = pd.read_csv(file)
        buscar = datos[datos["Title"] == titulo]
        if buscar.empty:
            return "No se encontró el libro"
        else:
            return buscar

    def buscar_autor(self, autor):
        file = self.FILE_PATH
        datos = pd.read_csv(file)
        buscar = datos[datos["Author"] == autor]
        if buscar.empty:
            return "No se encontro el Autor"
        else:
            return buscar