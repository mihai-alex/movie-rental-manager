import unittest

from src.domain.entities import Client, Movie, Rental
from src.domain.validators import ClientValidator, MovieValidator, RentalValidator
from src.repository.client_repository import ClientRepository, ClientRepositoryException, ClientTextFileRepository, \
    ClientBinaryFileRepository
from src.repository.movie_repository import MovieRepository, MovieRepositoryException, MovieTextFileRepository, \
    MovieBinaryFileRepository
from src.repository.rental_repository import RentalRepository, RentalRepositoryException, RentalTextFileRepository, \
    RentalBinaryFileRepository
from src.repository.undo_redo_repository import UndoRedoRepository


class TestClientRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = ClientRepository(ClientValidator)

    def tearDown(self) -> None:
        pass

    def test_find_by_id(self):
        self.assertEqual(self.repo.find_by_id('123'), None)
        client = Client('15', "abc")
        self.repo.add_entity(client)
        self.repo.find_by_id('15')
        self.assertEqual(self.repo.find_by_id('20'), None)

    def test_add_entity(self):
        client = Client('-15', "abc")
        self.assertRaises(ClientRepositoryException, self.repo.add_entity, client)
        client = Client('15', "abc")
        self.repo.add_entity(client)

    def test_remove_by_id(self):
        with self.assertRaises(ClientRepositoryException):
            self.repo.remove_by_id('12222')
        client = Client('15', "abc")
        self.repo.add_entity(client)
        self.assertRaises(ClientRepositoryException, self.repo.remove_by_id, '20')
        self.assertRaises(ClientRepositoryException, self.repo.remove_by_id, 'abc')
        self.assertRaises(ClientRepositoryException, self.repo.remove_by_id, '-5')
        self.assertRaises(ClientRepositoryException, self.repo.find_by_id, 'abc')
        self.assertRaises(ClientRepositoryException, self.repo.find_by_id, '-5')
        self.repo.remove_by_id('15')

    def test_update_entity_by_id(self):
        with self.assertRaises(ClientRepositoryException):
            self.repo.update_entity_by_id('12', Client('-15', "abc"))
        client = Client('15', "abc")
        self.repo.add_entity(client)
        self.assertRaises(ClientRepositoryException, self.repo.update_entity_by_id, '-5', client)
        self.repo.update_entity_by_id('15', Client('15', "new"))

    def test_get_all_entities(self):
        with self.assertRaises(ClientRepositoryException):
            self.repo.get_all_entities()
        client = Client('15', "abc")
        self.repo.add_entity(client)
        all = self.repo.get_all_entities


# TODO: add tests to this class (file repo)
class TestClientTextFileRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.file_repo = ClientTextFileRepository(ClientValidator, "../data/clients.txt")

    def tearDown(self) -> None:
        pass

    def test_load_data(self):
        pass

    def test_save_to_file(self):
        pass

    def test_rewrite_file(self):
        pass

    def test_add_entity(self):
        pass

    def test_remove_by_id(self):
        pass

    def test_update_entity_by_id(self):
        pass


# TODO: add tests to this class (file repo)
class TestClientBinaryFileRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.file_repo = ClientBinaryFileRepository(ClientValidator, "../data/clients.bin")

    def tearDown(self) -> None:
        pass

    def test_load_data(self):
        pass

    def test_save_to_file(self):
        pass

    def test_rewrite_file(self):
        pass

    def test_add_entity(self):
        pass

    def test_remove_by_id(self):
        pass

    def test_update_entity_by_id(self):
        pass


class TestMovieRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = MovieRepository(MovieValidator)

    def tearDown(self) -> None:
        pass

    def test_find_by_id(self):
        self.assertEqual(self.repo.find_by_id('123'), None)
        movie = Movie('15', "abc", "a", "b")
        self.repo.add_entity(movie)
        self.repo.find_by_id('15')
        self.assertEqual(self.repo.find_by_id('20'), None)

    def test_add_entity(self):
        movie = Movie('-15', "abc", "a", "b")
        self.assertRaises(MovieRepositoryException, self.repo.add_entity, movie)
        movie = Movie('15', "abc", "a", "b")
        self.repo.add_entity(movie)

    def test_remove_by_id(self):
        with self.assertRaises(MovieRepositoryException):
            self.repo.remove_by_id('12')
        movie = Movie('15', "abc", "a", "b")
        self.repo.add_entity(movie)
        self.assertRaises(MovieRepositoryException, self.repo.remove_by_id, '20')
        self.assertRaises(MovieRepositoryException, self.repo.remove_by_id, 'abc')
        self.assertRaises(MovieRepositoryException, self.repo.remove_by_id, '-5')
        self.assertRaises(MovieRepositoryException, self.repo.find_by_id, 'abc')
        self.assertRaises(MovieRepositoryException, self.repo.find_by_id, '-5')
        self.repo.remove_by_id('15')

    def test_update_entity_by_id(self):
        with self.assertRaises(MovieRepositoryException):
            self.repo.update_entity_by_id('12', Movie('-15', "abc", 'z', 't'))
        movie = Movie('15', "abc", 'z', 't')
        self.repo.add_entity(movie)
        self.assertRaises(MovieRepositoryException, self.repo.update_entity_by_id, '-5', movie)
        self.repo.update_entity_by_id('15', Movie('15', "new", "a", "b"))

    def test_get_all_entities(self):
        with self.assertRaises(MovieRepositoryException):
            self.repo.get_all_entities()
        movie = Movie('15', "abc", "a", "b")
        self.repo.add_entity(movie)
        all = self.repo.get_all_entities


# TODO: add tests to this class (file repo)
class TestMovieTextFileRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.file_repo = MovieTextFileRepository(MovieValidator, "../data/movies.txt")

    def tearDown(self) -> None:
        pass

    def test_load_data(self):
        pass

    def test_save_to_file(self):
        pass

    def test_rewrite_file(self):
        pass

    def test_add_entity(self):
        pass

    def test_remove_by_id(self):
        pass

    def test_update_entity_by_id(self):
        pass


# TODO: add tests to this class (file repo)
class TestMovieBinaryFileRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.file_repo = MovieBinaryFileRepository(MovieValidator, "../data/movies.bin")

    def tearDown(self) -> None:
        pass

    def test_load_data(self):
        pass

    def test_save_to_file(self):
        pass

    def test_rewrite_file(self):
        pass

    def test_add_entity(self):
        pass

    def test_remove_by_id(self):
        pass

    def test_update_entity_by_id(self):
        pass


class TestRentalRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = RentalRepository(RentalValidator)

    def tearDown(self) -> None:
        pass

    def test_find_by_id(self):
        self.assertEqual(self.repo.find_by_id('123'), None)
        rental = Rental('14', '100', '17', "12.12.2012", "10.10.2020", "09.10.2020")
        self.repo.add_entity(rental)
        self.repo.find_by_id('14')
        self.assertEqual(self.repo.find_by_id('20'), None)

    def test_add_entity(self):
        rental = Rental('-14', '100', '17', "12.12.2012", "10.10.2020", "09.10.2020")
        self.assertRaises(RentalRepositoryException, self.repo.add_entity, rental)
        rental = Rental('14', '100', '17', "12.12.2012", "10.10.2020", "09.10.2020")
        self.repo.add_entity(rental)
        rental = Rental('-15', "abc", ' ', 'j', "", '"12.12.2012"')
        self.assertRaises(RentalRepositoryException, self.repo.add_entity, rental)
        rental = Rental('15', '13', '12', "12.12.2012", "10.10.2020", "N.A.")
        self.repo.add_entity(rental)

    def test_remove_by_id(self):
        with self.assertRaises(RentalRepositoryException):
            self.repo.remove_by_id('12')
        rental = Rental('14', '100', '17', "12.12.2012", "10.10.2020", "09.10.2020")
        self.repo.add_entity(rental)
        self.assertRaises(RentalRepositoryException, self.repo.remove_by_id, '20')
        self.assertRaises(RentalRepositoryException, self.repo.remove_by_id, 'abc')
        self.assertRaises(RentalRepositoryException, self.repo.remove_by_id, '-5')
        self.assertRaises(RentalRepositoryException, self.repo.find_by_id, 'abc')
        self.assertRaises(RentalRepositoryException, self.repo.find_by_id, '-5')
        self.repo.remove_by_id('14')

    def test_remove_by_client_id(self):
        rental = Rental('14', '100', '17', "12.12.2012", "10.10.2020", "09.10.2020")
        self.repo.add_entity(rental)
        self.repo.remove_by_client_id("17")

    def test_remove_by_movie_id(self):
        rental = Rental('14', '100', '17', "12.12.2012", "10.10.2020", "09.10.2020")
        self.repo.add_entity(rental)
        self.repo.remove_by_movie_id("14")
        self.repo.remove_by_client_id("100")

    def test_update_entity_by_id(self):
        with self.assertRaises(RentalRepositoryException):
            self.repo.update_entity_by_id('1000', Rental('14', '100', '17', "", "10.10.2020", "09.10.2020"))
        rental = Rental('14', '100', '17', "12.12.2012", "10.10.2020", "09.10.2020")
        self.repo.add_entity(rental)
        self.assertRaises(RentalRepositoryException, self.repo.update_entity_by_id, '-5', rental)
        self.repo.update_entity_by_id('14', Rental('14', '1', '7', "17.12.2012", "10.10.2020", "09.10.2020"))

    def test_get_all_entities(self):
        with self.assertRaises(RentalRepositoryException):
            self.repo.get_all_entities()
        rental = Rental('14', '100', '17', "12.12.2012", "10.10.2020", "09.10.2020")
        self.repo.add_entity(rental)
        all = self.repo.get_all_entities


# TODO: add tests to this class (file repo)
class TestRentalTextFileRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.file_repo = RentalTextFileRepository(RentalValidator, "../data/rentals.txt")

    def tearDown(self) -> None:
        pass

    def test_load_data(self):
        pass

    def test_save_to_file(self):
        pass

    def test_rewrite_file(self):
        pass

    def test_add_entity(self):
        pass

    def test_remove_by_id(self):
        pass

    def test_remove_by_client_id(self):
        pass

    def test_remove_by_movie_id(self):
        pass

    def test_update_entity_by_id(self):
        pass


# TODO: add tests to this class (file repo)
class TestRentalBinaryFileRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.file_repo = RentalBinaryFileRepository(RentalValidator, "../data/rentals.bin")

    def tearDown(self) -> None:
        pass

    def test_load_data(self):
        pass

    def test_save_to_file(self):
        pass

    def test_rewrite_file(self):
        pass

    def test_add_entity(self):
        pass

    def test_remove_by_id(self):
        pass

    def test_remove_by_client_id(self):
        pass

    def test_remove_by_movie_id(self):
        pass

    def test_update_entity_by_id(self):
        pass


class TestUndoRedoRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = UndoRedoRepository()

    def tearDown(self) -> None:
        pass

    def test_properties(self):
        self.repo._undo_operations.append(1)
        self.repo._undo_converses.append(1)
        self.repo._redo_operations.append(1)
        self.repo._redo_converses.append(1)
        self.assertEqual(1, self.repo.undo_operations)
        self.assertEqual(1, self.repo.undo_converses)
        self.assertEqual(1, self.repo.redo_operations)
        self.assertEqual(1, self.repo.redo_converses)

    def test_add_remove_clear(self):
        self.assertEqual(self.repo.is_undo_empty(), True)
        self.assertEqual(self.repo.is_redo_empty(), True)
        self.repo.add_undo_operation(1)
        self.repo.add_undo_converse(1)
        self.repo.add_redo_operation(1)
        self.repo.add_redo_converse(1)
        self.assertEqual(self.repo.is_undo_empty(), False)
        self.assertEqual(self.repo.is_redo_empty(), False)
        self.assertEqual(1, self.repo.undo_operations)
        self.assertEqual(1, self.repo.undo_converses)
        self.assertEqual(1, self.repo.redo_operations)
        self.assertEqual(1, self.repo.redo_converses)
        self.repo.remove_undo()
        self.repo.remove_redo()
        self.assertEqual(self.repo.is_undo_empty(), True)
        self.assertEqual(self.repo.is_redo_empty(), True)
        self.repo.add_redo_operation(1)
        self.repo.add_redo_converse(1)
        self.repo.clear_redo()
        self.assertEqual(self.repo.is_redo_empty(), True)
