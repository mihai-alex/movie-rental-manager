from src.domain.entities import Client
from src.repository.client_repository import ClientRepositoryException
from src.domain.validators import MiscellaneousValidatorException, MiscellaneousValidator

import random


class ClientService:
    def __init__(self, client_repository, rental_repository):
        self.__client_repository = client_repository
        self.__rental_repository = rental_repository

    def add_client(self, client_id, name):
        if self.__client_repository.find_by_id(client_id) is not None:
            raise ClientRepositoryException("The client already exists.")

        client = Client(client_id, name)
        self.__client_repository.add_entity(client)

    def remove_client(self, client_id):
        """
        :return: The removed client and rental.
        """
        removed_client = self.__client_repository.remove_by_id(client_id)
        removed_rentals = self.__rental_repository.remove_by_client_id(client_id)
        return removed_client, removed_rentals

    def update_client(self, client_id, new_client_id, new_name):
        """
        :return: The client's attributes before the update.
        """
        new_client = Client(new_client_id, new_name)
        if self.__client_repository.find_by_id(client_id) is None:
            raise ClientRepositoryException("The client does not exist.")

        old_client_id = client_id
        old_name = self.__client_repository.find_by_id(client_id).name

        self.__client_repository.update_entity_by_id(client_id, new_client)
        return old_client_id, old_name

    @property
    def list_clients(self):
        return self.__client_repository.get_all_entities

    def search_by_attribute(self, attribute, search):
        if attribute == "client_id":
            try:
                MiscellaneousValidator.is_positive_integer(search)
            except MiscellaneousValidatorException as mve:
                raise ClientRepositoryException(mve)

        try:
            MiscellaneousValidator.is_nonempty_string(search)
        except MiscellaneousValidatorException as mve:
            raise ClientRepositoryException(mve)

        search_results = []
        entities = self.list_clients
        for entity in entities:
            if search.lower() in getattr(entity, attribute).lower():
                search_results.append(entity)

        return search_results

    def assign_random(self):
        counter = 1
        names = ["John", "Alex Mercer", "John Doe", "Ion Vasile", "George", "Marian", "Sandy", "Jane", "Mariah Jones"]
        while counter <= 20:
            try:
                self.add_client(str(random.randint(0, 100)), random.choice(names))
                counter = counter + 1
            except ClientRepositoryException:
                pass
