import random

from src.repository.client_repository import ClientRepositoryException
from src.repository.movie_repository import MovieRepositoryException
from src.repository.rental_repository import RentalRepositoryException


class AssignRandom:
    def __init__(self, client_service, movie_service, rental_service, undo_redo_service):
        self.__client_service = client_service
        self.__movie_service = movie_service
        self.__rental_service = rental_service
        self.__undo_redo_service = undo_redo_service

    def assign_random_clients(self):
        counter = 1
        names = ["John", "Alex Mercer", "John Doe", "Ion Vasile", "George", "Marian", "Sandy", "Jane", "Mariah Jones"]
        while counter <= 20:
            try:
                client_id = str(random.randint(0, 100))
                name = random.choice(names)
                self.__client_service.add_client(client_id, name)
                self.__undo_redo_service.add_client_handler(client_id, name)
                counter = counter + 1
            except ClientRepositoryException:
                pass

    def assign_random_movies(self):
        counter = 1
        titles = ["Creative", "No regrets", "Alone", "Alone 2", "For kids 1", "For kids 2", "For kids 3", "Sailor"]
        descriptions = ["great movie", "a movie you won't forget", "such a masterpiece", "just a generic film"]
        genres = ["action", "horror", "comedy", "indie", "drama", "romantic", "thriller"]
        while counter <= 20:
            try:
                movie_id = str(random.randint(0, 100))
                title = random.choice(titles)
                description = random.choice(descriptions)
                genre = random.choice(genres)
                self.__movie_service.add_movie(movie_id, title, description, genre)
                self.__undo_redo_service.add_movie_handler(movie_id, title, description, genre)
                counter = counter + 1
            except MovieRepositoryException:
                pass

    def assign_random_rentals(self):
        counter = 1
        while counter <= 20:
            try:
                rental_id = str(random.randint(0, 100))
                movie_id = str(random.randint(0, 100))
                client_id = str(random.randint(0, 100))
                rented_date = str(random.randint(1, 31)) + '.' + str(random.randint(1, 12)) + '.' + str(
                    random.randint(1950, 2050))
                due_date = str(random.randint(1, 31)) + '.' + str(random.randint(1, 12)) + '.' + str(
                    random.randint(1950, 2050))
                returned_date = random.choice(["N.A.", (
                        str(random.randint(1, 31)) + '.' + str(random.randint(1, 12)) + '.' + str(
                    random.randint(1950, 2050)))])
                self.__rental_service.add_rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
                self.__undo_redo_service.add_rental_handler(rental_id, movie_id, client_id, rented_date, due_date,
                                                            returned_date)
                counter = counter + 1
            except RentalRepositoryException:
                pass
