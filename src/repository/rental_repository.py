import os
import pickle

from domain.entities import Rental
from src.iterable_data_structure import MyIterator
from src.domain.validators import MiscellaneousValidator, MiscellaneousValidatorException, RentalValidatorException


class RentalRepositoryException(Exception):
    pass


class RentalRepository(object):
    def __init__(self, validator_class):
        self.__validator_class = validator_class
        # self.__entities = []
        self.__entities = MyIterator()

    def find_by_id(self, rental_id):
        try:
            MiscellaneousValidator.is_positive_integer(rental_id)
        except MiscellaneousValidatorException as mve:
            raise RentalRepositoryException("The rental id is not valid:" + " - " + str(mve))

        for rental in self.__entities:
            if rental.rental_id == rental_id:
                return rental

        return None

    def add_entity(self, rental):
        try:
            self.__validator_class.validate(rental)
            self.__entities.append(rental)
        except RentalValidatorException as rve:
            raise RentalRepositoryException("The rental's attributes are not valid.:" + " - " + str(rve))

    def remove_by_id(self, rental_id):
        """
        :return: the removed rental
        """
        try:
            MiscellaneousValidator.is_positive_integer(rental_id)
        except MiscellaneousValidatorException as mve:
            raise RentalRepositoryException("The rental id is not valid:" + " - " + str(mve))

        rental = self.find_by_id(rental_id)
        if rental is None:
            raise RentalRepositoryException("The id of the rental does not exist.")

        self.__entities.remove(rental)
        return rental

    def remove_by_client_id(self, client_id):
        """
        :return: the removed rentals
        """
        removed_rentals = []
        for rental in self.__entities:
            if rental.client_id == client_id:
                removed_rentals.append(self.remove_by_id(rental.rental_id))

        return removed_rentals

    def remove_by_movie_id(self, movie_id):
        """
        :return: the removed rentals
        """
        removed_rentals = []
        for rental in self.__entities:
            if rental.movie_id == movie_id:
                removed_rentals.append(self.remove_by_id(rental.rental_id))

        return removed_rentals

    def update_entity_by_id(self, rental_id, updated_rental):
        try:
            self.__validator_class.validate(updated_rental)
        except RentalValidatorException:
            raise RentalRepositoryException("The rental's attributes are not valid.")

        self.find_by_id(rental_id)  # throws a custom exception in case the rental id is not found

        for rental in self.__entities:
            if rental.rental_id == rental_id:
                rental.rental_id = updated_rental.rental_id
                rental.movie_id = updated_rental.movie_id
                rental.client_id = updated_rental.client_id
                rental.rented_date = updated_rental.rented_date
                rental.due_date = updated_rental.due_date
                rental.returned_date = updated_rental.returned_date
                return

    @property
    def get_all_entities(self):
        if len(self.__entities) == 0:
            raise RentalRepositoryException("The list of rentals is empty.")

        return self.__entities


class RentalTextFileRepository(RentalRepository):
    def __init__(self, validator_class, file_name):
        super().__init__(validator_class)
        self._file_name = file_name
        self._load_data()

    def _load_data(self):
        with open(self._file_name) as file_pointer:
            for line in file_pointer:
                attributes = line.strip().split(",")
                entity = Rental(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4],
                                attributes[5])
                super().add_entity(entity)

    def _save_to_file(self, entity):
        with open(self._file_name, 'a') as file_pointer:
            entity_to_write = entity.rental_id + "," + entity.movie_id + "," + entity.client_id + "," + \
                              entity.rented_date + "," + entity.due_date + "," + entity.returned_date + '\n'
            file_pointer.write(entity_to_write)

    def _rewrite_file(self):
        try:
            entities = super().get_all_entities
            with open(self._file_name, "wt") as file_pointer:
                for entity in entities:
                    entity_to_write = entity.rental_id + "," + entity.movie_id + "," + entity.client_id + "," + \
                                      entity.rented_date + "," + entity.due_date + "," + entity.returned_date + '\n'
                    file_pointer.write(entity_to_write)
        except RentalRepositoryException:
            open(self._file_name, 'wt').close()  # empty out the file

    def add_entity(self, entity):
        super().add_entity(entity)
        self._save_to_file(entity)

    def remove_by_id(self, entity_id):
        entity_removed = super().remove_by_id(entity_id)
        self._rewrite_file()
        return entity_removed

    def remove_by_client_id(self, client_id):
        entities_removed = super().remove_by_client_id(client_id)
        self._rewrite_file()
        return entities_removed

    def remove_by_movie_id(self, movie_id):
        entities_removed = super().remove_by_movie_id(movie_id)
        self._rewrite_file()
        return entities_removed

    def update_entity_by_id(self, entity_id, updated_entity):
        super().update_entity_by_id(entity_id, updated_entity)
        self._rewrite_file()


class RentalBinaryFileRepository(RentalRepository):
    def __init__(self, validator_class, file_name):
        super().__init__(validator_class)
        self._file_name = file_name
        self._load_data()

    def _load_data(self):
        if os.path.getsize(self._file_name) > 0:
            with open(self._file_name, "rb") as file_pointer:
                while True:
                    try:
                        entity = pickle.load(file_pointer)
                        super().add_entity(entity)
                    except EOFError:
                        break

    def _save_to_file(self, entity_to_write):
        with open(self._file_name, 'ab') as file_pointer:
            pickle.dump(entity_to_write, file_pointer)

    def _rewrite_file(self):
        try:
            entities = super().get_all_entities
            with open(self._file_name, "wb") as file_pointer:
                for entity in entities:
                    pickle.dump(entity, file_pointer)
        except RentalRepositoryException:
            open(self._file_name, 'wb').close()  # empty out the file

    def add_entity(self, entity):
        super().add_entity(entity)
        self._save_to_file(entity)

    def remove_by_id(self, entity_id):
        entity_removed = super().remove_by_id(entity_id)
        self._rewrite_file()
        return entity_removed

    def remove_by_client_id(self, client_id):
        entities_removed = super().remove_by_client_id(client_id)
        self._rewrite_file()
        return entities_removed

    def remove_by_movie_id(self, movie_id):
        entities_removed = super().remove_by_movie_id(movie_id)
        self._rewrite_file()
        return entities_removed

    def update_entity_by_id(self, entity_id, updated_entity):
        super().update_entity_by_id(entity_id, updated_entity)
        self._rewrite_file()
