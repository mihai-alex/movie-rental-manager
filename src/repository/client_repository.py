import os
import pickle

from domain.entities import Client
from src.domain.validators import MiscellaneousValidator, MiscellaneousValidatorException, ClientValidatorException
from src.iterable_data_structure import MyIterator


class ClientRepositoryException(Exception):
    pass


class ClientRepository(object):
    def __init__(self, validator_class):
        self.__validator_class = validator_class
        # self.__entities = []
        self.__entities = MyIterator()

    def find_by_id(self, client_id):
        try:
            MiscellaneousValidator.is_positive_integer(client_id)
        except MiscellaneousValidatorException as mve:
            raise ClientRepositoryException("The client id is not valid:" + " - " + str(mve))

        for client in self.__entities:
            if client.client_id == client_id:
                return client

        return None

    def add_entity(self, client):
        try:
            self.__validator_class.validate(client)
            self.__entities.append(client)
        except ClientValidatorException as cve:
            raise ClientRepositoryException("The client's attributes are not valid:" + " - " + str(cve))

    def remove_by_id(self, client_id):
        """
        :return: The removed client
        """
        try:
            MiscellaneousValidator.is_positive_integer(client_id)
        except MiscellaneousValidatorException as mve:
            raise ClientRepositoryException("The client id is not valid:" + " - " + str(mve))

        if self.get_all_entities is None:
            raise ClientRepositoryException("The list of clients is empty.")

        client = self.find_by_id(client_id)
        if client is None:
            raise ClientRepositoryException("The given client is not in the list.")

        self.__entities.remove(client)
        return client

    def update_entity_by_id(self, client_id, updated_client):
        try:
            self.__validator_class.validate(updated_client)
            self.find_by_id(client_id)
        except ClientValidatorException as cve:
            raise ClientRepositoryException("The client's attributes are not valid:" + " - " + str(cve))

        for client in self.__entities:
            if client.client_id == client_id:
                client.client_id = updated_client.client_id
                client.name = updated_client.name
                return

    @property
    def get_all_entities(self):
        if len(self.__entities) == 0:
            raise ClientRepositoryException("The list of clients is empty.")

        return self.__entities


class ClientTextFileRepository(ClientRepository):
    def __init__(self, validator_class, file_name):
        super().__init__(validator_class)
        self._file_name = file_name
        self._load_data()

    def _load_data(self):
        with open(self._file_name) as file_pointer:
            for line in file_pointer:
                attributes = line.strip().split(",")
                entity = Client(attributes[0], attributes[1])
                super().add_entity(entity)

    def _save_to_file(self, entity):
        with open(self._file_name, 'a') as file_pointer:
            entity_to_write = entity.client_id + "," + entity.name + '\n'
            file_pointer.write(entity_to_write)

    def _rewrite_file(self):
        try:
            entities = super().get_all_entities
            with open(self._file_name, "wt") as file_pointer:
                for entity in entities:
                    entity_to_write = entity.client_id + "," + entity.name + '\n'
                    file_pointer.write(entity_to_write)
        except ClientRepositoryException:
            open(self._file_name, 'wt').close()  # empty out the file

    def add_entity(self, entity):
        super().add_entity(entity)
        self._save_to_file(entity)

    def remove_by_id(self, entity_id):
        entity_removed = super().remove_by_id(entity_id)
        self._rewrite_file()
        return entity_removed

    def update_entity_by_id(self, entity_id, updated_entity):
        super().update_entity_by_id(entity_id, updated_entity)
        self._rewrite_file()


class ClientBinaryFileRepository(ClientRepository):
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
        except ClientRepositoryException:
            open(self._file_name, 'wb').close()  # empty out the file

    def add_entity(self, entity):
        super().add_entity(entity)
        self._save_to_file(entity)

    def remove_by_id(self, entity_id):
        entity_removed = super().remove_by_id(entity_id)
        self._rewrite_file()
        return entity_removed

    def update_entity_by_id(self, entity_id, updated_entity):
        super().update_entity_by_id(entity_id, updated_entity)
        self._rewrite_file()
