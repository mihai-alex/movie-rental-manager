class Movie:
    """
    Class for the movie entities
    """

    def __init__(self, movie_id, title, description, genre):
        self.__movie_id = movie_id
        self.__title = title
        self.__description = description
        self.__genre = genre

    @property
    def movie_id(self):
        return self.__movie_id

    @movie_id.setter
    def movie_id(self, value):
        self.__movie_id = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def genre(self):
        return self.__genre

    @genre.setter
    def genre(self, value):
        self.__genre = value

    def __str__(self):
        return "movie id: " + str(self.__movie_id) + ";   title: " + str(self.__title) + ";   description: " + \
               str(self.__description) + ";   genre: " + str(self.__genre)


class Rental:
    """
    Class for the rental entities
    """

    def __init__(self, rental_id, movie_id, client_id, rented_date, due_date, returned_date):
        self.__rental_id = rental_id
        self.__movie_id = movie_id
        self.__client_id = client_id
        self.__rented_date = rented_date
        self.__due_date = due_date
        self.__returned_date = returned_date

    @property
    def rental_id(self):
        return self.__rental_id

    @rental_id.setter
    def rental_id(self, value):
        self.__rental_id = value

    @property
    def movie_id(self):
        return self.__movie_id

    @movie_id.setter
    def movie_id(self, value):
        self.__movie_id = value

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value):
        self.__client_id = value

    @property
    def rented_date(self):
        return self.__rented_date

    @rented_date.setter
    def rented_date(self, value):
        self.__rented_date = value

    @property
    def due_date(self):
        return self.__due_date

    @due_date.setter
    def due_date(self, value):
        self.__due_date = value

    @property
    def returned_date(self):
        return self.__returned_date

    @returned_date.setter
    def returned_date(self, value):
        self.__returned_date = value

    def __str__(self):
        return "rental id: " + str(self.__rental_id) + ";   movie id: " + str(self.__movie_id) + \
               ";   client id: " + str(self.__client_id) + ";   rented date: " + str(self.__rented_date) + \
               ";   due date: " + str(self.__due_date) + ";   returned date: " + str(self.__returned_date)


class Client:
    """
    Class for the client entities
    """

    def __init__(self, client_id, name):
        self.__client_id = client_id
        self.__name = name

    @property
    def client_id(self):
        return self.__client_id

    @client_id.setter
    def client_id(self, value):
        self.__client_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __str__(self):
        return "client id: " + str(self.__client_id) + ";   name: " + str(self.__name)


class UndoRedoEntity:
    def __init__(self, method, *args):
        self.__method = method
        self.__args = args

    @property
    def method(self):
        return self.__method

    @property
    def args(self):
        return self.__args
