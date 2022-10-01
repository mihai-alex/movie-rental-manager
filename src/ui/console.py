from src.services.assign_random_service import AssignRandom
from src.repository.client_repository import ClientRepositoryException
from src.repository.movie_repository import MovieRepositoryException
from src.repository.rental_repository import RentalRepositoryException
from src.services.undo_redo_service import UndoRedoServiceException


class Console:
    def __init__(self, client_service, movie_service, rental_service, undo_redo_service):
        self.__client_service = client_service
        self.__movie_service = movie_service
        self.__rental_service = rental_service
        self.__undo_redo_service = undo_redo_service

    def print_menu(self):
        print("\n1. manage clients")
        print("2. manage movies")
        print("3. manage rentals")
        print("4. display statistics")
        print("5. undo")
        print("6. redo")
        print("X. exit")
        print("> ", end="")

    def print_submenu_clients(self):
        print("\t1. add a client")
        print("\t2. remove a client")
        print("\t3. update a client")
        print("\t4. list all clients")
        print("\t5. search for a client")
        print("\tB. back to main menu")
        print("\t> ", end="")

    def print_submenu_search_clients(self):
        print("\t\t1. search by client id")
        print("\t\t2. search by name")
        print("\t\tB. back to main menu")
        print("\t\t> ", end="")

    def print_submenu_movies(self):
        print("\t1. add a movie")
        print("\t2. remove a movie")
        print("\t3. update a movie")
        print("\t4. list all movies")
        print("\t5. search for a movie")
        print("\tB. back to main menu")
        print("\t> ", end="")

    def print_submenu_search_movies(self):
        print("\t\t1. search by movie id")
        print("\t\t2. search by title")
        print("\t\t3. search by description id")
        print("\t\t4. search by genre")
        print("\t\tB. back to main menu")
        print("\t\t> ", end="")

    def print_submenu_rentals(self):
        print("\t1. rent movie / add new rental")
        print("\t2. return a movie")
        print("\t3. list all rentals")
        print("\tB. back to main menu")
        print("\t> ", end="")

    def print_submenu_statistics(self):
        print("\t1. most rented movies")
        print("\t2. most active clients")
        print("\t3. late rentals of currently rented movies")
        print("\tB. back to main menu")
        print("\t> ", end="")

    def clients_command_1(self):
        client_id = input("Enter client id: ").strip()
        name = input("Enter client name: ").strip()
        try:
            self.__client_service.add_client(client_id, name)
            self.__undo_redo_service.add_client_handler(client_id, name)
        except ClientRepositoryException as error:
            print(str(error))

    def clients_command_2(self):
        client_id = input("Enter client id: ").strip()
        try:
            removed_client, removed_rentals = self.__client_service.remove_client(client_id)
            self.__undo_redo_service.remove_client_handler(removed_client, removed_rentals)
        except ClientRepositoryException as error:
            print(str(error))

    def clients_command_3(self):
        client_id = input("Enter client id: ").strip()
        new_name = input("Enter new client name: ").strip()
        try:
            old_client_id, old_name = self.__client_service.update_client(client_id, client_id, new_name)
            self.__undo_redo_service.update_client_handler(client_id, new_name, old_client_id, old_name)
        except ClientRepositoryException as error:
            print(str(error))

    def clients_command_4(self):
        try:
            clients = self.__client_service.list_clients
            for client in clients:
                print(str(client))
        except ClientRepositoryException as error:
            print(str(error))

    def clients_command_5(self):
        self.print_submenu_search_clients()
        command = input().strip().lower()
        if command == '1' or command == '2':
            search = input("\t\t\t> search for: ").strip()
            calls = {'1': "client_id", '2': "name"}
            try:
                search_results = self.__client_service.search_by_attribute(calls[command], search)
                if len(search_results) == 0:
                    print("Nothing was found.")
                else:
                    for entity in search_results:
                        print(str(entity))
            except ClientRepositoryException as error:
                print(str(error))
        elif command == 'b':
            pass
        else:
            print("The command is not valid!")

    def handle_clients(self):
        command = input().strip().lower()
        if command == '1':
            self.clients_command_1()
        elif command == '2':
            self.clients_command_2()
        elif command == '3':
            self.clients_command_3()
        elif command == '4':
            self.clients_command_4()
        elif command == '5':
            self.clients_command_5()
        elif command == 'b':
            pass
        else:
            print("The command is not valid!")

    def movies_command_1(self):
        movie_id = input("Enter movie id: ").strip()
        title = input("Enter movie title: ").strip()
        description = input("Enter movie description: ").strip()
        genre = input("Enter movie genre: ").strip()
        try:
            self.__movie_service.add_movie(movie_id, title, description, genre)
            self.__undo_redo_service.add_movie_handler(movie_id, title, description, genre)
        except MovieRepositoryException as error:
            print(str(error))

    def movies_command_2(self):
        movie_id = input("Enter movie id: ").strip()
        try:
            removed_movie, removed_rentals = self.__movie_service.remove_movie(movie_id)
            self.__undo_redo_service.remove_movie_handler(removed_movie, removed_rentals)
        except MovieRepositoryException as error:
            print(str(error))

    def movies_command_3(self):
        movie_id = input("Enter movie id: ").strip()
        new_title = input("Enter new movie title: ").strip()
        new_description = input("Enter new movie description: ").strip()
        new_genre = input("Enter new movie genre: ").strip()
        try:
            old_movie_id, old_title, old_description, old_genre = self.__movie_service.update_movie(movie_id, movie_id,
                                                                                                    new_title,
                                                                                                    new_description,
                                                                                                    new_genre)
            self.__undo_redo_service.update_movie_handler(old_movie_id, old_title, old_description, old_genre, movie_id,
                                                          new_title,
                                                          new_description,
                                                          new_genre)
        except MovieRepositoryException as error:
            print(str(error))

    def movies_command_4(self):
        try:
            movies = self.__movie_service.list_movies
            for movie in movies:
                print(str(movie))
        except MovieRepositoryException as error:
            print(str(error))

    def movies_command_5(self):
        self.print_submenu_search_movies()
        command = input().strip().lower()
        if command == '1' or command == '2' or command == '3' or command == '4':
            search = input("\t\t\t> search for: ").strip()
            calls = {'1': "movie_id", '2': "title", '3': "description", '4': "genre"}
            try:
                search_results = self.__movie_service.search_by_attribute(calls[command], search)
                if len(search_results) == 0:
                    print("Nothing was found.")
                else:
                    for entity in search_results:
                        print(str(entity))
            except MovieRepositoryException as error:
                print(str(error))
        elif command == 'b':
            pass
        else:
            print("The command is not valid!")

    def handle_movies(self):
        command = input().strip().lower()
        if command == '1':
            self.movies_command_1()
        elif command == '2':
            self.movies_command_2()
        elif command == '3':
            self.movies_command_3()
        elif command == '4':
            self.movies_command_4()
        elif command == '5':
            self.movies_command_5()
        elif command == 'b':
            pass
        else:
            print("The command is not valid!")

    def rentals_command_1(self):
        rental_id = input("Enter rental id: ").strip()
        movie_id = input("Enter movie id: ").strip()
        client_id = input("Enter client id: ").strip()
        rented_date = input("Enter rented date of the form: dd.mm.yyyy: ").strip()
        due_date = input("Enter due date of the form: dd.mm.yyyy: ").strip()
        returned_date = input("If the return date is not available, type \"N.A.\" or leave empty, else\n"
                              "Enter returned date of the form: dd.mm.yyyy: ").strip()

        if len(returned_date) == 0:
            returned_date = "N.A."

        try:
            self.__rental_service.add_rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
            self.__undo_redo_service.add_rental_handler(rental_id, movie_id, client_id, rented_date, due_date,
                                                        returned_date)
        except (RentalRepositoryException, MovieRepositoryException, ClientRepositoryException) as error:
            print(str(error))

    def rentals_command_2(self):
        rental_id = input("Enter rental id of the entry for which the return will be made: ").strip()
        try:
            self.__rental_service.return_movie(rental_id)
            self.__undo_redo_service.return_movie_handler(rental_id)
        except RentalRepositoryException as error:
            print(str(error))

    def rentals_command_3(self):
        try:
            rentals = self.__rental_service.list_rentals
            for rental in rentals:
                print(str(rental))
        except RentalRepositoryException as error:
            print(str(error))

    def handle_rentals(self):
        command = input().strip().lower()
        if command == '1':
            self.rentals_command_1()
        elif command == '2':
            self.rentals_command_2()
        elif command == '3':
            self.rentals_command_3()
        elif command == 'b':
            pass
        else:
            print("The command is not valid!")

    def print_statistics(self, statistics, criteria):
        if len(statistics) == 0:
            print("No statistics to display.")
        else:
            for statistic in statistics:
                print(criteria, end=": ")
                # for attribute in statistic:
                #     print(str(attribute))
                print(str(statistic[0]))
                print(str(statistic[1]))

    def statistics_command_1(self):
        try:
            statistics = self.__rental_service.get_movie_statistics
            self.print_statistics(statistics, "- the number of days rented")
        except (MovieRepositoryException, RentalRepositoryException) as mre:
            print(str(mre))

    def statistics_command_2(self):
        try:
            statistics = self.__rental_service.get_client_statistics
            self.print_statistics(statistics, "- the number of movie rental days of the client")
        except (ClientRepositoryException, RentalRepositoryException) as cre:
            print(str(cre))

    def statistics_command_3(self):
        try:
            statistics = self.__rental_service.get_rental_statistics
            self.print_statistics(statistics, "- the number of days of delay for the currently rented movie")
        except RentalRepositoryException as rre:
            print(str(rre))

    def handle_statistics(self):
        command = input().strip().lower()
        if command == '1':
            self.statistics_command_1()
        elif command == '2':
            self.statistics_command_2()
        elif command == '3':
            self.statistics_command_3()
        elif command == 'b':
            pass
        else:
            print("The command is not valid!")

    def run_console(self):
        # TODO: comment/uncomment for the "assign random" functionalities WITHOUT undo/redo - from the entities' service
        # self.__client_service.assign_random()
        # self.__movie_service.assign_random()
        # self.__rental_service.assign_random()

        # TODO: comment/uncomment for the "assign random" functionalities WITH undo/redo - from assign_random_service
        assign_random = AssignRandom(self.__client_service, self.__movie_service, self.__rental_service,
                                     self.__undo_redo_service)
        assign_random.assign_random_clients()
        assign_random.assign_random_movies()
        assign_random.assign_random_rentals()

        while True:
            self.print_menu()
            command = input().strip().lower()
            if command == '1':
                self.print_submenu_clients()
                self.handle_clients()
            elif command == '2':
                self.print_submenu_movies()
                self.handle_movies()
            elif command == '3':
                self.print_submenu_rentals()
                self.handle_rentals()
            elif command == '4':
                self.print_submenu_statistics()
                self.handle_statistics()
            elif command == '5':
                try:
                    self.__undo_redo_service.undo()
                except UndoRedoServiceException as error:
                    print(str(error))
            elif command == '6':
                try:
                    self.__undo_redo_service.redo()
                except UndoRedoServiceException as error:
                    print(str(error))
            elif command == 'x':
                print("You exited the program.")
                return
            else:
                print("The command is not valid!")
