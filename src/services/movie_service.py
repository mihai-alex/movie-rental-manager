import random

from src.domain.entities import Movie
from src.domain.validators import MiscellaneousValidator, MiscellaneousValidatorException
from src.repository.movie_repository import MovieRepositoryException


class MovieService:
    def __init__(self, movie_repository, rental_repository):
        self.__movie_repository = movie_repository
        self.__rental_repository = rental_repository

    def add_movie(self, movie_id, title, description, genre):
        if self.__movie_repository.find_by_id(movie_id) is not None:
            raise MovieRepositoryException("The movie already exists.")

        movie = Movie(movie_id, title, description, genre)
        self.__movie_repository.add_entity(movie)

    def remove_movie(self, movie_id):
        removed_movie = self.__movie_repository.remove_by_id(movie_id)
        removed_rentals = self.__rental_repository.remove_by_movie_id(movie_id)
        return removed_movie, removed_rentals

    def update_movie(self, movie_id, new_movie_id, new_title, new_description, new_genre):
        """
        :return: The movie's attributes before the update.
        """
        new_movie = Movie(new_movie_id, new_title, new_description, new_genre)
        if self.__movie_repository.find_by_id(movie_id) is None:
            raise MovieRepositoryException("The movie does not exist.")

        old_movie = self.__movie_repository.find_by_id(movie_id)
        old_movie_id = old_movie.movie_id
        old_title = old_movie.title
        old_description = old_movie.description
        old_genre = old_movie.genre

        self.__movie_repository.update_entity_by_id(movie_id, new_movie)
        return old_movie_id, old_title, old_description, old_genre

    @property
    def list_movies(self):
        return self.__movie_repository.get_all_entities

    def search_by_attribute(self, attribute, search):
        if attribute == "movie_id":
            try:
                MiscellaneousValidator.is_positive_integer(search)
            except MiscellaneousValidatorException as mve:
                raise MovieRepositoryException(mve)

        try:
            MiscellaneousValidator.is_nonempty_string(search)
        except MiscellaneousValidatorException as mve:
            raise MovieRepositoryException(mve)

        search_results = []
        entities = self.list_movies
        for entity in entities:
            if search.lower() in getattr(entity, attribute).lower():
                search_results.append(entity)

        return search_results

    def assign_random(self):
        counter = 1
        title = ["Creative", "No regrets", "Alone", "Alone 2", "For kids 1", "For kids 2", "For kids 3", "Sailor"]
        description = ["great movie", "a movie you won't forget", "such a masterpiece", "just a generic film"]
        genre = ["action", "horror", "comedy", "indie", "drama", "romantic", "thriller"]
        while counter <= 20:
            try:
                self.add_movie(str(random.randint(0, 100)), random.choice(title), random.choice(description),
                               random.choice(genre))
                counter = counter + 1
            except MovieRepositoryException:
                pass
