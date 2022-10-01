import unittest

from src.domain.entities import Movie, Client, Rental, UndoRedoEntity
from src.domain.validators import MiscellaneousValidator, ClientValidator, MovieValidator, RentalValidator, \
    MovieValidatorException, ClientValidatorException, RentalValidatorException, MiscellaneousValidatorException
from src.repository.client_repository import ClientRepository
from src.repository.rental_repository import RentalRepository
from src.services.client_service import ClientService


class TestMovie(unittest.TestCase):
    def test_movie(self):
        movie = Movie(15, "abc", "def", "xyz")
        self.assertEqual(movie.movie_id, 15)
        self.assertEqual(movie.title, "abc")
        self.assertEqual(movie.description, "def")
        self.assertEqual(movie.genre, "xyz")
        movie.movie_id = 1
        movie.title = "ab"
        movie.description = "de"
        movie.genre = "xy"
        self.assertEqual(movie.movie_id, 1)
        self.assertEqual(movie.title, "ab")
        self.assertEqual(movie.description, "de")
        self.assertEqual(movie.genre, "xy")
        self.assertIsInstance(str(movie), str)


class TestClient(unittest.TestCase):
    def test_client(self):
        client = Client(15, "abc")
        self.assertEqual(client.client_id, 15)
        self.assertEqual(client.name, "abc")
        client.client_id = 1
        client.name = "ab"
        self.assertEqual(client.client_id, 1)
        self.assertEqual(client.name, "ab")
        self.assertIsInstance(str(client), str)


class TestRental(unittest.TestCase):
    def test_rental(self):
        rental = Rental(11, 22, 33, "10.10.2010", "11.11.2011", "12.12.2012")
        self.assertEqual(rental.rental_id, 11)
        self.assertEqual(rental.movie_id, 22)
        self.assertEqual(rental.client_id, 33)
        self.assertEqual(rental.rented_date, "10.10.2010")
        self.assertEqual(rental.due_date, "11.11.2011")
        self.assertEqual(rental.returned_date, "12.12.2012")
        rental.rental_id = 1
        rental.movie_id = 2
        rental.client_id = 3
        rental.rented_date = "10.10.2000"
        rental.due_date = "11.11.2001"
        rental.returned_date = "12.12.2002"
        self.assertEqual(rental.rental_id, 1)
        self.assertEqual(rental.movie_id, 2)
        self.assertEqual(rental.client_id, 3)
        self.assertEqual(rental.rented_date, "10.10.2000")
        self.assertEqual(rental.due_date, "11.11.2001")
        self.assertEqual(rental.returned_date, "12.12.2002")
        self.assertIsInstance(str(rental), str)


class TestValidators(unittest.TestCase):
    def test_miscellaneous_validator(self):
        self.assertRaises(MiscellaneousValidatorException, MiscellaneousValidator.is_positive_integer, 'x')
        self.assertRaises(MiscellaneousValidatorException, MiscellaneousValidator.is_positive_integer, "-15")
        self.assertRaises(MiscellaneousValidatorException, MiscellaneousValidator.is_positive_integer, "01")
        MiscellaneousValidator.is_positive_integer('15')

        self.assertRaises(MiscellaneousValidatorException, MiscellaneousValidator.is_valid_date, '32.10.2010')
        self.assertRaises(MiscellaneousValidatorException, MiscellaneousValidator.is_valid_date, 'abc')
        MiscellaneousValidator.is_valid_date("03.12.2021")

        self.assertRaises(MiscellaneousValidatorException, MiscellaneousValidator.is_nonempty_string, "")
        MiscellaneousValidator.is_nonempty_string("text")

    def test_client_validator(self):
        client = Client('-15', "abc")
        self.assertRaises(ClientValidatorException, ClientValidator.validate, client)
        client = Client('8', "")
        self.assertRaises(ClientValidatorException, ClientValidator.validate, client)
        client = Client('12', "name")
        ClientValidator.validate(client)

    def test_movie_validator(self):
        movie = Movie("a7", "k", "def", "xyz")
        self.assertRaises(MovieValidatorException, MovieValidator.validate, movie)
        movie = Movie("-7", "k", "def", "xyz")
        self.assertRaises(MovieValidatorException, MovieValidator.validate, movie)
        movie = Movie("6", "", "", "")
        self.assertRaises(MovieValidatorException, MovieValidator.validate, movie)
        movie = Movie("6", "a", "", "")
        self.assertRaises(MovieValidatorException, MovieValidator.validate, movie)
        movie = Movie("6", "a", "b", "")
        self.assertRaises(MovieValidatorException, MovieValidator.validate, movie)
        movie = Movie("6", "a", "b", 'd')
        MovieValidator.validate(movie)

    def test_rental_validator(self):
        rental = Rental(str(-12), '13', '14', "10.11.2020", "11.11.2011", "15.10.1999")
        self.assertRaises(RentalValidatorException, RentalValidator.validate, rental)
        rental = Rental('12', '-13', '14', "10.11.2020", "11.11.2011", "15.10.1999")
        self.assertRaises(RentalValidatorException, RentalValidator.validate, rental)
        rental = Rental('12', '13', 'abc', "10.11.2020", "11.11.2011", "15.10.1999")
        self.assertRaises(RentalValidatorException, RentalValidator.validate, rental)
        rental = Rental('12', '13', '14', "", "11.11.2011", "15.10.1999")
        self.assertRaises(RentalValidatorException, RentalValidator.validate, rental)
        rental = Rental('12', '13', '14', "11.11.2011", "32.11.2011", "15.10.1999")
        self.assertRaises(RentalValidatorException, RentalValidator.validate, rental)
        rental = Rental('12', '13', '14', "11.11.2011", "02.11.2011", "15.10.99")
        self.assertRaises(RentalValidatorException, RentalValidator.validate, rental)
        rental = Rental('12', '13', '14', "10.11.2020", "11.11.2021", "N.A.")
        RentalValidator.validate(rental)
        rental = Rental('12', '13', '14', "10.11.2020", "11.11.2021", "11.11.2020")
        RentalValidator.validate(rental)

    def test_undo_redo_entity(self):
        test = UndoRedoEntity(ClientService(ClientRepository, RentalRepository).add_client, '12', 'new name')
        method = test.method
        args = test.args
        self.assertEqual(args, ('12', 'new name'))
