import datetime


class MiscellaneousValidatorException(Exception):
    pass


class ClientValidatorException(Exception):
    pass


class MovieValidatorException(Exception):
    pass


class RentalValidatorException(Exception):
    pass


class MiscellaneousValidator:
    """
    Miscellaneous validator class for validating various properties.
    """

    @staticmethod
    def is_positive_integer(number):
        """
        Check if a string can be represented as a positive integer,
        :param number: string
        """
        if str.isnumeric(number) is False:
            raise MiscellaneousValidatorException("The value is not a positive integer.")

        if number[0] == '0' and len(number) > 1:
            raise MiscellaneousValidatorException("The integer can not start with 0!")

        number = int(number)
        if number < 0:
            raise MiscellaneousValidatorException("The value is not a positive integer.")

    @staticmethod
    def is_valid_date(date):
        """
        Checks if a string can represent a valid date
        :param date: string
        """
        try:
            datetime.datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            raise MiscellaneousValidatorException("The date is not valid.")

    @staticmethod
    def is_nonempty_string(string):
        """
        Checks if a string is nonempty.
        :param string: string
        """
        if len(string) == 0:
            raise MiscellaneousValidatorException("The string must be nonempty.")


class ClientValidator:
    """
    Validator class for the client entity.
    """

    @staticmethod
    def validate(client):
        """
        Validates a client's attributes
        :param client: client entity
        """
        try:
            MiscellaneousValidator.is_positive_integer(client.client_id)
        except MiscellaneousValidatorException:
            raise ClientValidatorException("The client id has to be a positive integer.")

        try:
            MiscellaneousValidator.is_nonempty_string(client.name)
        except MiscellaneousValidatorException:
            raise ClientValidatorException("The client name must be a nonempty string.")


class MovieValidator:
    """
    Validator class for the movie entity.
    """

    @staticmethod
    def validate(movie):
        """
        Validates a movie's attributes
        :param movie: movie entity
        """
        try:
            MiscellaneousValidator.is_positive_integer(movie.movie_id)
        except MiscellaneousValidatorException:
            raise MovieValidatorException("The movie id has to be a positive integer.")

        try:
            MiscellaneousValidator.is_nonempty_string(movie.title)
            MiscellaneousValidator.is_nonempty_string(movie.description)
            MiscellaneousValidator.is_nonempty_string(movie.genre)
        except MiscellaneousValidatorException:
            raise MovieValidatorException("The movie title, description and genre must be nonempty strings.")


class RentalValidator:
    """
    Validator class for the rental entity.
    """

    @staticmethod
    def validate(rental):
        """
        Validates a rental's attributes
        :param rental: rental entity
        """
        try:
            MiscellaneousValidator.is_positive_integer(rental.rental_id)
            MiscellaneousValidator.is_positive_integer(rental.movie_id)
            MiscellaneousValidator.is_positive_integer(rental.client_id)
        except MiscellaneousValidatorException:
            raise RentalValidatorException("The rental, movie and client ids have to be positive integers.")

        try:
            MiscellaneousValidator.is_valid_date(rental.rented_date)
            MiscellaneousValidator.is_valid_date(rental.due_date)
            if rental.returned_date == "N.A.":
                pass
            else:
                MiscellaneousValidator.is_valid_date(rental.returned_date)
        except MiscellaneousValidatorException:
            raise RentalValidatorException("The rented, due and returned dates must be valid "
                                           "and of the form: dd.mm.yyyy")

        if datetime.datetime.strptime(rental.rented_date, "%d.%m.%Y") > datetime.datetime.now():
            raise RentalValidatorException("The rented date must be before the current date.")

        if datetime.datetime.strptime(rental.rented_date, "%d.%m.%Y") > datetime.datetime.strptime(rental.due_date,
                                                                                                   "%d.%m.%Y"):
            raise RentalValidatorException("The rented date must be before the due date.")

        if rental.returned_date != "N.A.":
            if datetime.datetime.strptime(rental.rented_date, "%d.%m.%Y") > datetime.datetime.strptime(
                    rental.returned_date, "%d.%m.%Y"):
                raise RentalValidatorException("The returned date must be after the rented date.")
