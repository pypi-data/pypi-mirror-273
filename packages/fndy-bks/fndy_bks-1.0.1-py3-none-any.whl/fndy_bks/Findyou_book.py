import pandas as pd
import pkg_resources


class findbook:
    FILE_PATH = pkg_resources.resource_filename(__name__, 'books.csv')

    def __init__(self):
        self._file = pd.read_csv(findbook.FILE_PATH)
        self._books = None
        self._title = None
        self._author = None
        self._genre = None
        self._height = None
        self._publisher = None

    def gen_book(self):
        self._books = self._file.sample()
        self._title = self._books["Title"].values[0]
        self._author = self._books["Author"].values[0]
        self._genre = self._books["Genre"].values[0]
        self._height = self._books["Height"].values[0]
        self._publisher = self._books["Publisher"].values[0]

    def find_title(self,title):
        datos = self._file
        buscar = datos[datos["Title"] == title]
        if buscar.size == 0:
            return "the book does not exist. "
        else:
            return buscar

    def find_author(self,author):
        datos = self._file
        buscar = datos[datos["Author"] == author]
        if buscar.size == 0:
            return "The author does not exist. "
        else:
            return buscar