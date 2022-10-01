from src.domain.entities import UndoRedoEntity
from src.repository.client_repository import ClientRepositoryException
from src.repository.movie_repository import MovieRepositoryException
from src.repository.rental_repository import RentalRepositoryException


class UndoRedoServiceException(Exception):
    pass


class UndoRedoService:
    def __init__(self, undo_redo_repository, client_service, movie_service, rental_service):
        self.__undo_redo_repository = undo_redo_repository
        self.__client_service = client_service
        self.__movie_service = movie_service
        self.__rental_service = rental_service

    def add_client_handler(self, client_id, name):
        self.clear_redo()  # redo is cleared after every operation that changes data!!!
        undo_operation_objects = [UndoRedoEntity(self.__client_service.remove_client, client_id)]
        undo_converse_objects = [UndoRedoEntity(self.__client_service.add_client, client_id, name)]
        self.add_undo_operation(undo_operation_objects)
        self.add_undo_converse(undo_converse_objects)

    def remove_client_handler(self, removed_client, removed_rentals):
        self.clear_redo()  # redo is cleared after every operation that changes data!!!
        undo_operation_objects = [
            UndoRedoEntity(self.__client_service.add_client, removed_client.client_id, removed_client.name)]

        for index in range(len(removed_rentals)):
            removed_rental = removed_rentals[index]
            rental_id = removed_rental.rental_id
            movie_id = removed_rental.movie_id
            client_id = removed_rental.client_id
            rented_date = removed_rental.rented_date
            due_date = removed_rental.due_date
            returned_date = removed_rental.returned_date
            undo_operation_objects.append(
                UndoRedoEntity(self.__rental_service.add_rental, rental_id, movie_id, client_id, rented_date,
                               due_date, returned_date))

        undo_converse_objects = [UndoRedoEntity(self.__client_service.remove_client, removed_client.client_id)]
        self.add_undo_operation(undo_operation_objects)
        self.add_undo_converse(undo_converse_objects)

    def update_client_handler(self, client_id, new_name, old_client_id, old_name):
        self.clear_redo()  # redo is cleared after every operation that changes data!!!
        undo_operation_objects = [
            UndoRedoEntity(self.__client_service.update_client, client_id, old_client_id, old_name)]
        undo_converse_objects = [
            UndoRedoEntity(self.__client_service.update_client, old_client_id, client_id, new_name)]
        self.add_undo_operation(undo_operation_objects)
        self.add_undo_converse(undo_converse_objects)

    def add_movie_handler(self, movie_id, title, description, genre):
        self.clear_redo()  # redo is cleared after every operation that changes data!!!
        undo_operation_objects = [UndoRedoEntity(self.__movie_service.remove_movie, movie_id)]
        undo_converse_objects = [
            UndoRedoEntity(self.__movie_service.add_movie, movie_id, title, description, genre)]
        self.add_undo_operation(undo_operation_objects)
        self.add_undo_converse(undo_converse_objects)

    def remove_movie_handler(self, removed_movie, removed_rentals):
        self.clear_redo()  # redo is cleared after every operation that changes data!!!
        undo_operation_objects = [
            UndoRedoEntity(self.__movie_service.add_movie, removed_movie.movie_id, removed_movie.title,
                           removed_movie.description, removed_movie.genre)]

        for index in range(len(removed_rentals)):
            removed_rental = removed_rentals[index]
            rental_id = removed_rental.rental_id
            movie_id = removed_rental.movie_id
            client_id = removed_rental.client_id
            rented_date = removed_rental.rented_date
            due_date = removed_rental.due_date
            returned_date = removed_rental.returned_date
            undo_operation_objects.append(
                UndoRedoEntity(self.__rental_service.add_rental, rental_id, movie_id, client_id, rented_date,
                               due_date, returned_date))

        undo_converse_objects = [UndoRedoEntity(self.__movie_service.remove_movie, removed_movie.movie_id)]
        self.add_undo_operation(undo_operation_objects)
        self.add_undo_converse(undo_converse_objects)

    def update_movie_handler(self, old_movie_id, old_title, old_description, old_genre, movie_id, new_title,
                             new_description, new_genre):
        self.clear_redo()  # redo is cleared after every operation that changes data!!!
        undo_operation_objects = [
            UndoRedoEntity(self.__movie_service.update_movie, movie_id, old_movie_id, old_title, old_description,
                           old_genre)]
        undo_converse_objects = [
            UndoRedoEntity(self.__movie_service.update_movie, old_movie_id, movie_id, new_title, new_description,
                           new_genre)]
        self.add_undo_operation(undo_operation_objects)
        self.add_undo_converse(undo_converse_objects)

    def add_rental_handler(self, rental_id, movie_id, client_id, rented_date, due_date, returned_date):
        self.clear_redo()  # redo is cleared after every operation that changes data!!!
        undo_operation_objects = [
            UndoRedoEntity(self.__rental_service.remove_rental, rental_id)]
        undo_converse_objects = [
            UndoRedoEntity(self.__rental_service.add_rental, rental_id, movie_id, client_id, rented_date,
                           due_date, returned_date)]
        self.add_undo_operation(undo_operation_objects)
        self.add_undo_converse(undo_converse_objects)

    def return_movie_handler(self, rental_id):
        self.clear_redo()  # redo is cleared after every operation that changes data!!!
        undo_operation_objects = [
            UndoRedoEntity(self.__rental_service.un_return_movie, rental_id)]
        undo_converse_objects = [
            UndoRedoEntity(self.__rental_service.return_movie, rental_id)]
        self.add_undo_operation(undo_operation_objects)
        self.add_undo_converse(undo_converse_objects)

    def undo(self):
        if self.__undo_redo_repository.is_undo_empty() is True:
            raise UndoRedoServiceException("There is nothing to undo!")

        operation_object_list = []
        converse_object_list = []
        for index in range(len(self.__undo_redo_repository.undo_operations)):
            operation = self.__undo_redo_repository.undo_operations[index]
            operation_object_list.append(operation)
            method = operation.method
            args = operation.args

            try:
                method(*args)
            except (RentalRepositoryException, MovieRepositoryException, ClientRepositoryException) as error:
                # raise UndoRedoServiceException(error)
                pass

        for index in range(len(self.__undo_redo_repository.undo_converses)):
            converse = self.__undo_redo_repository.undo_converses[index]
            converse_object_list.append(converse)

        self.__undo_redo_repository.remove_undo()
        self.__undo_redo_repository.add_redo_operation(converse_object_list)
        self.__undo_redo_repository.add_redo_converse(operation_object_list)

    def redo(self):
        if self.__undo_redo_repository.is_redo_empty() is True:
            raise UndoRedoServiceException("There is nothing to redo!")

        operation_object_list = []
        converse_object_list = []
        for index in range(len(self.__undo_redo_repository.redo_operations)):
            operation = self.__undo_redo_repository.redo_operations[index]
            operation_object_list.append(operation)
            method = operation.method
            args = operation.args

            try:
                method(*args)
            except (RentalRepositoryException, MovieRepositoryException, ClientRepositoryException) as error:
                # raise UndoRedoServiceException(error)
                pass

        for index in range(len(self.__undo_redo_repository.redo_converses)):
            converse = self.__undo_redo_repository.redo_converses[index]
            converse_object_list.append(converse)

        self.__undo_redo_repository.remove_redo()
        self.__undo_redo_repository.add_undo_operation(converse_object_list)
        self.__undo_redo_repository.add_undo_converse(operation_object_list)

    def add_undo_operation(self, objects):
        self.__undo_redo_repository.add_undo_operation(objects)

    def add_undo_converse(self, objects):
        self.__undo_redo_repository.add_undo_converse(objects)

    def add_redo_operation(self, objects):
        self.__undo_redo_repository.add_redo_operation(objects)

    def add_redo_converse(self, objects):
        self.__undo_redo_repository.add_redo_converse(objects)

    def clear_redo(self):
        self.__undo_redo_repository.clear_redo()
