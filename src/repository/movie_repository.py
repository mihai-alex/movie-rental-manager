import os
import pickle

from domain.entities import Movie
from src.iterable_data_structure import MyIterator
from src.domain.validators import MiscellaneousValidator, MiscellaneousValidatorException, MovieValidatorException


class MovieRepositoryException(Exception):
    pass


class MovieRepository(object):
    def __init__(self, validator_class):
        self.__validator_class = validator_class
        # self.__entities = []
        self.__entities = MyIterator()

    def find_by_id(self, movie_id):
        try:
            MiscellaneousValidator.is_positive_integer(movie_id)
        except MiscellaneousValidatorException as mve:
            raise MovieRepositoryException("The movie id is not valid:" + " - " + str(mve))

        for movie in self.__entities:
            if movie.movie_id == movie_id:
                return movie

        return None

    def add_entity(self, movie):
        try:
            self.__validator_class.validate(movie)
            self.__entities.append(movie)
        except MovieValidatorException as mve:
            raise MovieRepositoryException("The movie's attributes are not valid.:" + " - " + str(mve))

    def remove_by_id(self, movie_id):
        """
        :return: The removed movie
        """
        try:
            MiscellaneousValidator.is_positive_integer(movie_id)
        except MiscellaneousValidatorException as mve:
            raise MovieRepositoryException("The movie id is not valid:" + " - " + str(mve))

        if self.find_by_id(movie_id) is None:
            raise MovieRepositoryException("The movie does not exist.")

        movie = self.find_by_id(movie_id)
        self.__entities.remove(movie)
        return movie

    def update_entity_by_id(self, movie_id, updated_movie):
        try:
            self.__validator_class.validate(updated_movie)
        except MovieValidatorException:
            raise MovieRepositoryException("The movie's attributes are not valid.")

        self.find_by_id(movie_id)

        for movie in self.__entities:
            if movie.movie_id == movie_id:
                movie.movie_id = updated_movie.movie_id
                movie.title = updated_movie.title
                movie.description = updated_movie.description
                movie.genre = updated_movie.genre
                return

    @property
    def get_all_entities(self):
        if len(self.__entities) == 0:
            raise MovieRepositoryException("The list of movies is empty.")

        return self.__entities


class MovieTextFileRepository(MovieRepository):
    def __init__(self, validator_class, file_name):
        super().__init__(validator_class)
        self._file_name = file_name
        self._load_data()

    def _load_data(self):
        with open(self._file_name) as file_pointer:
            for line in file_pointer:
                attributes = line.strip().split(",")
                entity = Movie(attributes[0], attributes[1], attributes[2], attributes[3])
                super().add_entity(entity)

    def _save_to_file(self, entity):
        with open(self._file_name, 'a') as file_pointer:
            entity_to_write = entity.movie_id + "," + entity.title + "," + entity.description + "," + \
                              entity.genre + '\n'
            file_pointer.write(entity_to_write)

    def _rewrite_file(self):
        try:
            entities = super().get_all_entities
            with open(self._file_name, "wt") as file_pointer:
                for entity in entities:
                    entity_to_write = entity.movie_id + "," + entity.title + "," + entity.description + "," + \
                                      entity.genre + '\n'
                    file_pointer.write(entity_to_write)
        except MovieRepositoryException:
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


class MovieBinaryFileRepository(MovieRepository):
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
        except MovieRepositoryException:
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
