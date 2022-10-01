"""
Assigned problem: 3. Movie Rental
"""
from src.domain.validators import ClientValidator, MovieValidator, RentalValidator
from src.repository.client_repository import ClientRepository, ClientTextFileRepository, ClientBinaryFileRepository
from src.repository.movie_repository import MovieRepository, MovieTextFileRepository, MovieBinaryFileRepository
from src.repository.rental_repository import RentalRepository, RentalTextFileRepository, RentalBinaryFileRepository
from src.repository.undo_redo_repository import UndoRedoRepository
from src.services.client_service import ClientService
from src.services.movie_service import MovieService
from src.services.rental_service import RentalService
from src.services.undo_redo_service import UndoRedoService
from src.ui.console import Console

import configparser

if __name__ == '__main__':
    client_validator = ClientValidator
    movie_validator = MovieValidator
    rental_validator = RentalValidator

    # Reading from the settings.properties file
    config = configparser.RawConfigParser()
    config.read("settings.properties")
    repository_type = config.get("SETTINGS", "repository")
    client_repository, movie_repository, rental_repository = None, None, None
    if repository_type == "inmemory":
        client_repository = ClientRepository(client_validator)
        movie_repository = MovieRepository(movie_validator)
        rental_repository = RentalRepository(rental_validator)
    elif repository_type == "textfiles":
        client_repository = ClientTextFileRepository(client_validator, config.get("SETTINGS", "clients"))
        movie_repository = MovieTextFileRepository(movie_validator, config.get("SETTINGS", "movies"))
        rental_repository = RentalTextFileRepository(rental_validator, config.get("SETTINGS", "rentals"))
    elif repository_type == "binaryfiles":
        client_repository = ClientBinaryFileRepository(client_validator, config.get("SETTINGS", "clients"))
        movie_repository = MovieBinaryFileRepository(movie_validator, config.get("SETTINGS", "movies"))
        rental_repository = RentalBinaryFileRepository(rental_validator, config.get("SETTINGS", "rentals"))

    undo_redo_repository = UndoRedoRepository()

    client_service = ClientService(client_repository, rental_repository)
    movie_service = MovieService(movie_repository, rental_repository)
    rental_service = RentalService(client_repository, movie_repository, rental_repository)
    undo_redo_service = UndoRedoService(undo_redo_repository, client_service, movie_service, rental_service)

    console = Console(client_service, movie_service, rental_service, undo_redo_service)
    console.run_console()
