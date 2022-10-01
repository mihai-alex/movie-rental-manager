import random
import datetime
from operator import itemgetter

from src.iterable_data_structure import my_filter, my_sort
from src.domain.entities import Rental
from src.domain.validators import RentalValidator, RentalValidatorException
from src.repository.client_repository import ClientRepositoryException
from src.repository.movie_repository import MovieRepositoryException
from src.repository.rental_repository import RentalRepositoryException


class RentalService:
    def __init__(self, client_repository, movie_repository, rental_repository):
        self.__client_repository = client_repository
        self.__movie_repository = movie_repository
        self.__rental_repository = rental_repository

    def make_date_object(self, string):
        return datetime.datetime.strptime(string, "%d.%m.%Y")

    def is_valid_rental(self, rental):
        try:
            RentalValidator.validate(rental)
        except RentalValidatorException as rve:
            raise RentalRepositoryException(rve)

        if self.__movie_repository.find_by_id(rental.movie_id) is None:
            raise RentalRepositoryException("The given movie id does not exist.")

        if self.__client_repository.find_by_id(rental.client_id) is None:
            raise RentalRepositoryException("The given client id does not exist.")

        if (self.make_date_object(rental.rented_date) > self.make_date_object(rental.due_date)) or \
                (rental.returned_date != "N.A." and self.make_date_object(rental.returned_date) <
                 self.make_date_object(rental.rented_date)):
            raise RentalRepositoryException("The dates are not in logical order.")

        return True

    def add_rental(self, rental_id, movie_id, client_id, rented_date, due_date, returned_date):
        try:
            self.__movie_repository.get_all_entities
        except MovieRepositoryException:
            raise RentalRepositoryException("Can not rent a movie because the list of movies is empty.")

        try:
            self.__client_repository.get_all_entities
        except ClientRepositoryException:
            raise RentalRepositoryException("No clients can rent a movie. The list of clients is empty.")

        if self.__movie_repository.find_by_id(movie_id) is None:
            raise RentalRepositoryException("The movie can not be rented because it does not exist.")

        if self.__client_repository.find_by_id(client_id) is None:
            raise RentalRepositoryException("The client can not rent a movie because the client does not exist.")

        rental = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
        self.is_valid_rental(rental)

        if self.__rental_repository.find_by_id(rental_id) is not None:
            raise RentalRepositoryException("Can not add rental because the rental id already exists!")

        try:
            entities = self.__rental_repository.get_all_entities
            now = datetime.datetime.now()
            for entity in entities:
                if entity.client_id == client_id:
                    if entity.returned_date == "N.A." and self.make_date_object(entity.due_date) < now:
                        raise RentalRepositoryException(
                            "Can not rent a movie. The client has an unreturned movie that passed "
                            "it's due date for return.")
        except RentalRepositoryException:
            pass  # pass in case the list of rentals is empty

        self.__rental_repository.add_entity(rental)

    def remove_rental(self, rental_id):
        """
        Converse of the add_rental functionality, used in undo/redo
        :return: the removed rental
        """
        removed_rental = self.__rental_repository.remove_by_id(rental_id)
        return removed_rental

    def return_movie(self, rental_id):
        if len(self.__rental_repository.get_all_entities) == 0:
            raise ClientRepositoryException("Can not return movie - the list of rentals is empty.")

        current = self.__rental_repository.find_by_id(rental_id)
        if current is None:
            raise RentalRepositoryException("The rental id does not exist.")

        if current.returned_date != "N.A.":
            raise RentalRepositoryException("The movie was already returned!")

        now = datetime.datetime.now()
        rental = self.__rental_repository.find_by_id(rental_id)
        rental.returned_date = str(str(now.day) + '.' + str(now.month) + '.' + str(now.year))
        self.__rental_repository.update_entity_by_id(rental_id, rental)

    def un_return_movie(self, rental_id):
        rental = self.__rental_repository.find_by_id(rental_id)
        rental.returned_date = "N.A."
        self.__rental_repository.update_entity_by_id(rental_id, rental)

    @property
    def list_rentals(self):
        rentals = self.__rental_repository.get_all_entities
        if len(rentals) == 0:
            raise RentalRepositoryException("The list of rentals is empty.")

        return self.__rental_repository.get_all_entities

    def assign_random(self):
        counter = 1
        while counter <= 20:
            try:
                self.add_rental(str(random.randint(0, 100)), str(random.randint(0, 100)), str(random.randint(0, 100)),
                                str(random.randint(1, 31)) + '.' + str(random.randint(1, 12)) + '.' + str(
                                    random.randint(1950, 2050)),
                                str(random.randint(1, 31)) + '.' + str(random.randint(1, 12)) + '.' + str(
                                    random.randint(1950, 2050)),
                                random.choice(
                                    ["N.A.", (str(random.randint(1, 31)) + '.' + str(random.randint(1, 12)) + '.' + str(
                                        random.randint(1950, 2050)))]))
                counter = counter + 1
            except RentalRepositoryException:
                pass

    @property
    def get_movie_statistics(self):
        movies = self.__movie_repository.get_all_entities
        rentals = self.__rental_repository.get_all_entities
        statistics = []

        for movie in movies:
            days_rented = int(0)
            for rental in rentals:
                if movie.movie_id == rental.movie_id:
                    rented_date = self.make_date_object(rental.rented_date)
                    today = datetime.datetime.now()
                    returned_date = self.make_date_object(
                        str(today.day) + '.' + str(today.month) + '.' + str(today.year))
                    if rental.returned_date != "N.A.":
                        returned_date = self.make_date_object(rental.returned_date)

                    days_rented += (returned_date - rented_date).days

            statistics.append([days_rented, movie])

        # TODO: uncomment if working without custom sorting function
        # statistics.sort(key=itemgetter(0), reverse=True)

        # TODO: uncomment if working with custom sorting function
        my_sort(statistics, lambda x, y: x[0] >= y[0])

        return statistics

    @property
    def get_client_statistics(self):
        clients = self.__client_repository.get_all_entities
        rentals = self.__rental_repository.get_all_entities
        statistics = []

        for client in clients:
            days_rented = int(0)
            for rental in rentals:
                if client.client_id == rental.client_id:
                    rented_date = self.make_date_object(rental.rented_date)
                    today = datetime.datetime.now()
                    returned_date = self.make_date_object(
                        str(today.day) + '.' + str(today.month) + '.' + str(today.year))
                    if rental.returned_date != "N.A.":
                        returned_date = self.make_date_object(rental.returned_date)

                    days_rented += (returned_date - rented_date).days

            statistics.append([days_rented, client])

        # TODO: uncomment if working without custom sorting function
        # statistics.sort(key=itemgetter(0), reverse=True)

        # TODO: uncomment if working with custom sorting function
        my_sort(statistics, lambda x, y: x[0] >= y[0])

        return statistics

    @property
    def get_rental_statistics(self):
        rentals = self.__rental_repository.get_all_entities
        statistics = []

        # TODO: uncomment if working without custom filter function
        # for rental in rentals:
        #     if rental.returned_date == "N.A.":
        #         due_date = self.make_date_object(rental.due_date)
        #         today = datetime.datetime.now()
        #         returned_date = self.make_date_object(str(today.day) + '.' + str(today.month) + '.' + str(today.year))
        #
        #         if returned_date > due_date:
        #             days_delayed = (returned_date - due_date).days
        #             statistics.append([days_delayed, self.__movie_repository.find_by_id(rental.movie_id)])

        # TODO: uncomment if working without custom filter function
        filtered_rentals = my_filter(rentals, lambda x: x.returned_date == "N.A.")
        for rental in filtered_rentals:
            due_date = self.make_date_object(rental.due_date)
            today = datetime.datetime.now()
            returned_date = self.make_date_object(str(today.day) + '.' + str(today.month) + '.' + str(today.year))

            if returned_date > due_date:
                days_delayed = (returned_date - due_date).days
                statistics.append([days_delayed, self.__movie_repository.find_by_id(rental.movie_id)])

        # TODO: uncomment if working without custom sorting function
        # statistics.sort(key=itemgetter(0), reverse=True)

        # TODO: uncomment if working with custom sorting function
        my_sort(statistics, lambda x, y: x[0] >= y[0])

        return statistics
