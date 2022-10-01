import unittest

from services.assign_random_service import AssignRandom
from src.domain.entities import Rental
from src.domain.validators import ClientValidator, MovieValidator, RentalValidator
from src.repository.client_repository import ClientRepository, ClientRepositoryException
from src.repository.movie_repository import MovieRepository, MovieRepositoryException
from src.repository.rental_repository import RentalRepository, RentalRepositoryException
from src.repository.undo_redo_repository import UndoRedoRepository
from src.services.client_service import ClientService
from src.services.movie_service import MovieService
from src.services.rental_service import RentalService
from src.services.undo_redo_service import UndoRedoService, UndoRedoServiceException


class TestClientService(unittest.TestCase):
    def setUp(self) -> None:
        self.client_validator = ClientValidator
        self.movie_validator = MovieValidator
        self.rental_validator = RentalValidator

        self.client_repository = ClientRepository(self.client_validator)
        self.movie_repository = MovieRepository(self.movie_validator)
        self.rental_repository = RentalRepository(self.rental_validator)
        self.undo_redo_repository = UndoRedoRepository

        self.client_service = ClientService(self.client_repository, self.rental_repository)
        self.movie_service = MovieService(self.movie_repository, self.rental_repository)
        self.rental_service = RentalService(self.client_repository, self.movie_repository, self.rental_repository)
        self.undo_redo_service = UndoRedoService(self.undo_redo_repository, self.client_service, self.movie_service,
                                                 self.rental_service)

    def tearDown(self) -> None:
        pass

    def test_add_client(self):
        with self.assertRaises(ClientRepositoryException):
            self.client_service.add_client("-3", "mary")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.add_client("13", "")
        self.client_service.add_client("13", "bob")

    def test_remove_client(self):
        with self.assertRaises(ClientRepositoryException):
            self.client_service.remove_client("14")
        self.client_service.add_client("13", "bob")
        self.client_service.remove_client("13")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.remove_client("-5")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.remove_client("abc")

    def test_update_client(self):
        with self.assertRaises(ClientRepositoryException):
            self.client_service.update_client("12", "13", "john")
        self.client_service.add_client("13", "bob")
        self.client_service.update_client("13", "13", "new")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.update_client("-5", "13", "new")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.update_client("13", "-13", "new")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.update_client("13", "13", "")

    def test_list_clients(self):
        with self.assertRaises(ClientRepositoryException):
            self.client_service.list_clients()
        self.client_service.add_client("13", "bob")
        all = self.client_service.list_clients
        self.assertEqual(len(all), 1)

    def test_search_by_attribute(self):
        with self.assertRaises(ClientRepositoryException):
            self.client_service.search_by_attribute("client_id", "15")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.search_by_attribute("", "15")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.search_by_attribute("client_id", "-15")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.search_by_attribute("", "15")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.search_by_attribute("client_id", "")

        self.client_service.assign_random()
        all = self.client_service.list_clients
        client_id = all[0].client_id
        self.client_service.search_by_attribute("client_id", client_id)
        with self.assertRaises(ClientRepositoryException):
            self.client_service.search_by_attribute("client_id", "")
        with self.assertRaises(ClientRepositoryException):
            self.client_service.search_by_attribute("", "")

    def test_assign_random(self):
        self.client_service.assign_random()
        all = self.client_service.list_clients
        self.assertEqual(len(all), 20)


class TestMovieService(unittest.TestCase):
    def setUp(self) -> None:
        self.client_validator = ClientValidator
        self.movie_validator = MovieValidator
        self.rental_validator = RentalValidator

        self.client_repository = ClientRepository(self.client_validator)
        self.movie_repository = MovieRepository(self.movie_validator)
        self.rental_repository = RentalRepository(self.rental_validator)

        self.client_service = ClientService(self.client_repository, self.rental_repository)
        self.movie_service = MovieService(self.movie_repository, self.rental_repository)
        self.rental_service = RentalService(self.client_repository, self.movie_repository, self.rental_repository)

    def tearDown(self) -> None:
        pass

    def test_add_movie(self):
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.add_movie("-3", "mary", "ab", "cd")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.add_movie("13", "", "ab", "cd")
        self.movie_service.add_movie("13", "bob", "ab", "cd")

    def test_remove_client(self):
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.remove_movie("14")
        self.movie_service.add_movie("13", "bob", "ab", "cd")
        self.movie_service.remove_movie("13")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.remove_movie("-5")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.remove_movie("abc")

    def test_update_client(self):
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.update_movie("12", "13", "john", "ab", "cd")
        self.movie_service.add_movie("13", "bob", "ab", "cd")
        self.movie_service.update_movie("13", "13", "new", "ab", "cd")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.update_movie("-5", "13", "new", "ab", "cd")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.update_movie("13", "-13", "new", "ab", "cd")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.update_movie("13", "13", "", "ab", "cd")

    def test_list_clients(self):
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.list_movies()
        self.movie_service.add_movie("13", "bob", "ab", "cd")
        all = self.movie_service.list_movies
        self.assertEqual(len(all), 1)

    def test_search_by_attribute(self):
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.search_by_attribute("client_id", "15")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.search_by_attribute("", "15")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.search_by_attribute("client_id", "-15")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.search_by_attribute("", "15")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.search_by_attribute("client_id", "")

        self.movie_service.assign_random()
        all = self.movie_service.list_movies
        movie_id = all[0].movie_id
        self.movie_service.search_by_attribute("movie_id", movie_id)
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.search_by_attribute("movie_id", "")
        with self.assertRaises(MovieRepositoryException):
            self.movie_service.search_by_attribute("", "")

    def test_assign_random(self):
        self.movie_service.assign_random()
        all = self.movie_service.list_movies
        self.assertEqual(len(all), 20)


class TestRentalService(unittest.TestCase):
    def setUp(self) -> None:
        self.client_validator = ClientValidator
        self.movie_validator = MovieValidator
        self.rental_validator = RentalValidator

        self.client_repository = ClientRepository(self.client_validator)
        self.movie_repository = MovieRepository(self.movie_validator)
        self.rental_repository = RentalRepository(self.rental_validator)

        self.client_service = ClientService(self.client_repository, self.rental_repository)
        self.movie_service = MovieService(self.movie_repository, self.rental_repository)
        self.rental_service = RentalService(self.client_repository, self.movie_repository, self.rental_repository)

    def tearDown(self) -> None:
        pass

    def test_make_date_object(self):
        self.rental_service.make_date_object("11.12.2012")
        with self.assertRaises(ValueError):
            self.rental_service.make_date_object("abc")

    def test_is_valid_rental(self):
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.is_valid_rental(Rental("-1", "2", "3", "11.12.2012", "12.12.2012", "N.A."))
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.is_valid_rental(Rental("1", "9999999999999", "3", "11.12.2012", "12.12.2012", "N.A."))
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.is_valid_rental(Rental("", "2", "3", "11.12.2012", "12.12.2012", "N.A."))
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.is_valid_rental(Rental("1", "2", "3", "32.12.2012", "12.12.2012", "N.A."))
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.is_valid_rental(Rental("1", "2", "3", "", "12.12.2012", "N.A."))
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.is_valid_rental(Rental("1", "2", "3", "11.12.2012", "10.12.2012", "N.A."))
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.is_valid_rental(Rental("123123", ' ', "123", "10.10.2010", "11.10.2010", "N.A."))

        self.movie_service.assign_random()
        self.client_service.assign_random()
        self.rental_service.assign_random()
        movie_id = self.rental_service.list_rentals[0].movie_id
        client_id = self.rental_service.list_rentals[0].client_id
        self.rental_service.is_valid_rental(Rental("12312", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A."))
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.is_valid_rental(Rental("12312", movie_id, '-5', "10.10.2010", "11.10.2010", "N.A."))
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.is_valid_rental(Rental("12312", '-5', client_id, "10.10.2010", "11.10.2010", "N.A."))

    def test_add_rental(self):
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.add_rental("1", "2", "3", "11.12.2012", "12.12.2012", "N.A.")

        self.movie_service.assign_random()
        self.client_service.assign_random()
        self.rental_service.assign_random()

        movie_id = self.rental_service.list_rentals[0].movie_id
        client_id = self.rental_service.list_rentals[0].client_id
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")

    def test_return_movie(self):
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.return_movie('123')

        self.movie_service.assign_random()
        self.client_service.assign_random()
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.return_movie(self.movie_service.list_movies[0].movie_id)

        self.rental_service.assign_random()
        movie_id = self.rental_service.list_rentals[0].movie_id
        client_id = self.rental_service.list_rentals[0].client_id
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")
        self.rental_service.return_movie("123123")
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.return_movie("123123")

    def test_list_rentals(self):
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.list_rentals()

        self.movie_service.assign_random()
        self.client_service.assign_random()
        self.rental_service.assign_random()
        self.assertEqual(len(self.rental_service.list_rentals), 20)

    def test_assign_random(self):
        self.movie_service.assign_random()
        self.client_service.assign_random()
        self.rental_service.assign_random()
        self.assertEqual(len(self.rental_service.list_rentals), 20)

    def test_get_movie_statistics(self):
        with self.assertRaises(MovieRepositoryException):
            self.rental_service.get_movie_statistics()

        self.movie_service.assign_random()
        self.client_service.assign_random()
        self.rental_service.assign_random()

        self.assertEqual(len(self.rental_service.list_rentals), 20)
        self.rental_service.list_rentals[0].returned_date = "10.10.2100"
        rental_id = self.rental_service.list_rentals[0].rental_id
        movie_id = self.rental_service.list_rentals[0].movie_id
        client_id = self.rental_service.list_rentals[0].client_id
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")

        stats2 = self.rental_service.get_movie_statistics
        self.assertNotEqual(len(stats2), 0)

    def test_get_client_statistics(self):
        with self.assertRaises(ClientRepositoryException):
            self.rental_service.get_client_statistics()

        self.movie_service.assign_random()
        self.client_service.assign_random()
        self.rental_service.assign_random()

        self.assertEqual(len(self.rental_service.list_rentals), 20)
        self.rental_service.list_rentals[0].returned_date = "10.10.2100"
        rental_id = self.rental_service.list_rentals[0].rental_id
        movie_id = self.rental_service.list_rentals[0].movie_id
        client_id = self.rental_service.list_rentals[0].client_id
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")

        stats1 = self.rental_service.get_client_statistics
        self.assertNotEqual(len(stats1), 0)

    def test_get_rental_statistics(self):
        with self.assertRaises(RentalRepositoryException):
            self.rental_service.get_rental_statistics()

        self.movie_service.assign_random()
        self.client_service.assign_random()
        self.rental_service.assign_random()

        self.assertEqual(len(self.rental_service.list_rentals), 20)
        self.rental_service.list_rentals[0].returned_date = "10.10.2100"
        rental_id = self.rental_service.list_rentals[0].rental_id
        movie_id = self.rental_service.list_rentals[0].movie_id
        client_id = self.rental_service.list_rentals[0].client_id
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")

        stats3 = self.rental_service.get_rental_statistics
        self.assertNotEqual(len(stats3), 0)

    def test_remove_rental(self):
        self.movie_service.assign_random()
        self.client_service.assign_random()
        self.rental_service.assign_random()
        movie_id = self.rental_service.list_rentals[0].movie_id
        client_id = self.rental_service.list_rentals[0].client_id
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")
        self.rental_service.remove_rental("123123")
        self.assertEqual(self.rental_repository.find_by_id("123123"), None)

    def test_un_return_movie(self):
        self.movie_service.assign_random()
        self.client_service.assign_random()
        self.rental_service.assign_random()
        movie_id = self.rental_service.list_rentals[0].movie_id
        client_id = self.rental_service.list_rentals[0].client_id
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")
        self.rental_service.return_movie("123123")
        self.rental_service.un_return_movie("123123")
        rental = self.rental_repository.find_by_id("123123")
        self.assertEqual(rental.returned_date, "N.A.")


class TestUndoRedoService(unittest.TestCase):
    def setUp(self) -> None:
        self.client_validator = ClientValidator
        self.movie_validator = MovieValidator
        self.rental_validator = RentalValidator

        self.client_repository = ClientRepository(self.client_validator)
        self.movie_repository = MovieRepository(self.movie_validator)
        self.rental_repository = RentalRepository(self.rental_validator)
        self.undo_redo_repository = UndoRedoRepository()

        self.client_service = ClientService(self.client_repository, self.rental_repository)
        self.movie_service = MovieService(self.movie_repository, self.rental_repository)
        self.rental_service = RentalService(self.client_repository, self.movie_repository, self.rental_repository)
        self.undo_redo_service = UndoRedoService(self.undo_redo_repository, self.client_service, self.movie_service,
                                                 self.rental_service)

    def tearDown(self) -> None:
        pass

    def test_add_client_handler(self):
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.undo)
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.redo)
        client_id = "13"
        name = "bob"
        self.client_service.add_client(client_id, name)
        self.undo_redo_service.add_client_handler(client_id, name)
        self.undo_redo_service.undo()
        self.undo_redo_service.redo()

    def test_remove_client_handler(self):
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.undo)
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.redo)
        client_id = "1"
        name = "bob"
        movie_id = "2"
        self.client_service.add_client(client_id, name)
        self.movie_service.add_movie("2", "ggg", "fff", "yyy")
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")
        removed_client, removed_rentals = self.client_service.remove_client(client_id)
        self.undo_redo_service.remove_client_handler(removed_client, removed_rentals)
        self.undo_redo_service.undo()
        self.undo_redo_service.redo()

    def test_update_client_handler(self):
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.undo)
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.redo)
        client_id = "1"
        new_name = "new"
        old_client_id = "1"
        old_name = "old"
        self.client_service.add_client(old_client_id, old_name)
        self.undo_redo_service.update_client_handler(client_id, new_name, old_client_id, old_name)
        self.undo_redo_service.undo()
        self.undo_redo_service.redo()

    def test_add_movie_handler(self):
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.undo)
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.redo)
        movie_id = "1"
        title = "ttt"
        description = "zzz"
        genre = "ggg"
        self.movie_service.add_movie(movie_id, title, description, genre)
        self.undo_redo_service.add_movie_handler(movie_id, title, description, genre)
        self.undo_redo_service.undo()
        self.undo_redo_service.redo()

    def test_remove_movie_handler(self):
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.undo)
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.redo)
        client_id = "1"
        name = "bob"
        movie_id = "2"
        self.client_service.add_client(client_id, name)
        self.movie_service.add_movie("2", "ggg", "fff", "yyy")
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")
        removed_movie, removed_rentals = self.movie_service.remove_movie(movie_id)
        self.undo_redo_service.remove_movie_handler(removed_movie, removed_rentals)
        self.undo_redo_service.undo()
        self.undo_redo_service.redo()

    def test_update_movie_handler(self):
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.undo)
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.redo)
        old_movie_id = "1"
        old_title = "old"
        old_description = "olddesc"
        old_genre = "oldgen"
        movie_id = "1"
        new_title = "new"
        new_description = "newdesc"
        new_genre = "newgen"
        self.movie_service.add_movie(old_movie_id, old_title, old_description, old_genre)
        self.undo_redo_service.update_movie_handler(old_movie_id, old_title, old_description, old_genre, movie_id,
                                                    new_title,
                                                    new_description, new_genre)
        self.undo_redo_service.undo()
        self.undo_redo_service.redo()

    def test_add_rental_handler(self):
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.undo)
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.redo)
        client_id = "1"
        name = "bob"
        movie_id = "2"
        self.client_service.add_client(client_id, name)
        self.movie_service.add_movie("2", "ggg", "fff", "yyy")
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")
        self.undo_redo_service.add_rental_handler("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")
        self.undo_redo_service.undo()
        self.undo_redo_service.redo()

    def test_return_movie_handler(self):
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.undo)
        self.assertRaises(UndoRedoServiceException, self.undo_redo_service.redo)
        client_id = "1"
        name = "bob"
        movie_id = "2"
        self.client_service.add_client(client_id, name)
        self.movie_service.add_movie(movie_id, "ggg", "fff", "yyy")
        self.rental_service.add_rental("123123", movie_id, client_id, "10.10.2010", "11.10.2010", "N.A.")
        self.undo_redo_service.return_movie_handler("123123")
        self.undo_redo_service.undo()
        self.undo_redo_service.redo()


class TestAssignRandom(unittest.TestCase):
    def setUp(self) -> None:
        self.client_validator = ClientValidator
        self.movie_validator = MovieValidator
        self.rental_validator = RentalValidator

        self.client_repository = ClientRepository(self.client_validator)
        self.movie_repository = MovieRepository(self.movie_validator)
        self.rental_repository = RentalRepository(self.rental_validator)
        self.undo_redo_repository = UndoRedoRepository()

        self.client_service = ClientService(self.client_repository, self.rental_repository)
        self.movie_service = MovieService(self.movie_repository, self.rental_repository)
        self.rental_service = RentalService(self.client_repository, self.movie_repository, self.rental_repository)
        self.undo_redo_service = UndoRedoService(self.undo_redo_repository, self.client_service, self.movie_service,
                                                 self.rental_service)
        self.assign_random = AssignRandom(self.client_service, self.movie_service, self.rental_service,
                                          self.undo_redo_service)

    def tearDown(self) -> None:
        pass

    # TODO: list was copied because MyIterator doesn't support nested for loops
    def test_assign_random_clients(self):
        self.assign_random.assign_random_clients()
        clients = self.client_service.list_clients[:]  # copy of the MyIterator object
        self.assertEqual(len(clients), 20)
        for client1 in clients:
            for client2 in clients:
                if client1 != client2:
                    self.assertNotEqual(client1.client_id, client2.client_id)

    # TODO: list was copied because MyIterator doesn't support nested for loops
    def test_assign_random_movies(self):
        self.assign_random.assign_random_movies()
        movies = self.movie_service.list_movies[:]  # copy of the MyIterator object
        self.assertEqual(len(movies), 20)
        for movie1 in movies:
            for movie2 in movies:
                if movie1 != movie2:
                    self.assertNotEqual(movie1.movie_id, movie2.movie_id)

    # TODO: list was copied because MyIterator doesn't support nested for loops
    def test_assign_random_rentals(self):
        self.assign_random.assign_random_clients()
        self.assign_random.assign_random_movies()
        self.assign_random.assign_random_rentals()
        rentals = self.rental_service.list_rentals[:]  # copy of the MyIterator object
        self.assertEqual(len(rentals), 20)
        for rental1 in rentals:
            for rental2 in rentals:
                if rental1 != rental2:
                    self.assertNotEqual(rental1.rental_id, rental2.rental_id)
