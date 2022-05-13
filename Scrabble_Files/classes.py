import random
import json
import os
import itertools


# This file contains all the functions, classes and their methods that are used for the project: Scrabble


def halt_and_separate():
    """This global function's purpose is to halt the program, until the user presses 'ENTER' (it allows input during
    this period, however, it does nothing). Afterwards, it gives an output as a separation indicator from what
    the user read before pressing enter and the output the user is getting. The main reason that this function is
    global, is because it can be generalized for more than 1 functions. For this instance of the project, it is
    only used in the class: Game. It is used everytime a user input is inserted to the system or there is important
    information the user needs to attend (without being requested to give input) before they proceed"""

    input("\nΠΑΤΗΣΤΕ 'ENTER' ΓΙΑ ΝΑ ΣΥΝΕΧΙΣΕΤΕ")
    print("-----------------------------------------------------------------------------------------------------------")


class Game:
    """This class represents the manager of the classes that are used, the ".txt" files that it handles, all
    rules that are required to be followed to be able to play Scrabble and UI of the game through terminal"""

    def __init__(self):
        """The initialization of the game. It initializes all its attributes. It initializes the information of the
        letters, the game's state, the CPU's gameplay, the available commands, and the data of each word"""
        # Information about the greek capital letters quantity and value in a dictionary, whose each key is the letter
        # and as value it has a list in the form of [quantity, value]
        self.letter_info = {"Α": [12, 1], "Β": [1, 8], "Γ": [2, 4], "Δ": [2, 4], "Ε": [8, 1], "Ζ": [1, 10], "Η": [7, 1],
                            "Θ": [1, 10], "Ι": [8, 1], "Κ": [4, 2], "Λ": [3, 3], "Μ": [3, 3], "Ν": [6, 1], "Ξ": [1, 10],
                            "Ο": [9, 1], "Π": [4, 2], "Ρ": [5, 2], "Σ": [7, 1], "Τ": [8, 1], "Υ": [4, 2], "Φ": [1, 8],
                            "Χ": [1, 8], "Ψ": [1, 10], "Ω": [3, 3]}

        self.state = None  # the state of the game to handle the game's actions. It does not have a default value.
        self.CPU_gameplay = "Min_Letters"  # setting of CPU. It has default value of a gameplay in the form of a string

        # dictionary which is managed the action taken, based on the state and user input. Each key is the state
        # with value a second dictionary whose key is the user input and value the action taken.
        # IMPORTANT: "Game" state does not have an action, but contains the special user inputs to handle the special
        # commands the user can do.
        self.commands = {
            "Menu": {"1": self.start_game, "2": self.show_scores, "3": self.show_settings, "q": self.quit_scrabble},
            "Scores": {"b": self.show_menu},
            "Settings": {"1": self.show_CPU_gameplay, "2": self.reset_dictionary_data, "3": self.reset_scores,
                         "b": self.show_menu},
            "Settings_CPU_Gameplay": {"1": self.set_CPU_gameplay_Min_Letters,
                                      "2": self.set_CPU_gameplay_Max_Letters,
                                      "3": self.set_CPU_gameplay_Smart,
                                      "b": self.show_settings},
            "Game": {"p": "swap_letters", "q": "self.quit_game"}
        }

        self.check_scores_file()  # creating file: 'scores.json' if it doesn't exist. Check the appropriate method

        # creating the dictionary whose each key is the length of the words it contains (in string), with
        # value a second dictionary, whose each key is a word and value the points the word provides.
        self.dictionary_data = self.generate_word_data(self.letter_info)

    def __repr__(self):
        """It represents the item based of its state, CPU gameplay (which is a settings information), and the
        information of the letters that are used to generate the words alongside their values"""
        return 'State: ' + str(self.state) + \
               '\nCPU Gameplay: ' + str(self.CPU_gameplay) + \
               '\nLetter Info: ' + str(self.letter_info)

    def get_letter_info(self):
        """getter for the letter info. Used for testing purposes"""
        return self.letter_info

    def show_dictionary_data(self):
        """getter for the dictionary, since it is not suited to be included in the the repr(). Also used for
        testing purposes."""
        print(self.dictionary_data)

    def generate_word_data(self, letter_info):
        """It checks if the 'words_dict.json' exists. If it does, it loads the data it has. Otherwise,
        it generates the file, which takes seconds to create and informs the user about the progress of the action.
        :param letter_info: The information of the letters (the quantity and value of each greek letter)
        :return the dictionary_data that can access its word and its total value fast (words with 7 letters have
        additional 50 score)"""
        if os.path.exists('words_dict.json'):  # checks if the file exists
            # loads the data, considering the file exists
            with open('words_dict.json', 'r', encoding="utf8") as f:
                return json.load(f)
        else:
            # creates the 'words_dict.json', considering it doesn't exist, and informs the user
            print("ΔΗΜΙΟΥΡΓΙΑ ΛΕΞΙΚΟΥ, ΜΗΝ ΤΕΡΜΑΤΙΣΕΤΕ ΠΡΟΩΡΑ ΤΟ ΠΡΟΓΡΑΜΜΑ...")
            word_data = {"1": {}, "2": {}, "3": {}, "4": {}, "5": {}, "6": {}, "7": {}, }
            with open('greek7.txt', 'r', encoding="utf8") as f:
                words = f.readlines()
                for index, i in enumerate(words):
                    word = i.strip('\n')
                    word_data.get(str(len(word)))[word] = self.give_value(word, letter_info)
            with open('words_dict.json', 'w') as f:
                json.dump(word_data, f)
            print("ΕΠΙΤΥΧΗΣ ΔΗΜΙΟΥΡΓΙΑ ΕΝΣΩΜΑΤΩΜΕΝΟΥ ΛΕΞΙΚΟΥ!")
            return word_data

    @staticmethod
    def check_scores_file():
        """It checks if scores file exists. If it doesn't, it just the file. Used at the beginning of the program
        and before each time the file needs to be inspected, as a defensive programming measure"""

        if not os.path.exists('scores.json'):
            print("ΔΗΜΗΟΥΡΓΙΑ ΑΡΧΕΙΟΥ ΜΕ ΣΚΟΡ")
            with open('scores.json', 'w', encoding="utf8") as f:
                scores = {}
                json.dump(scores, f)
            print("ΕΠΙΤΥΧΗΣ ΔΗΜΗΟΥΡΓΙΑ ΑΡΧΕΙΟΥ ΜΕ ΤΑ ΣΚΟΡ")

        # checks if data have been removed by the user that would result in json file corruption
        if os.path.getsize('scores.json') == 0:
            with open('scores.json', 'w', encoding="utf8") as f:
                scores = {}
                json.dump(scores, f)

    def print_scores(self):
        """method which prints the scores from the file: 'scores.json' in a user friendly way. It first makes sure that
        the file exists and not corrupted (it generates or fixes it otherwise). It also informs the user if that file is
        empty. """
        self.check_scores_file()
        with open('scores.json', 'r', encoding="utf8") as f:
            scores = json.load(f)
            if scores == {}:
                print("ΔΕΝ ΥΠΑΡΧΟΥΝ ΑΠΟΘΗΚΕΥΜΕΝΑ ΣΚΟΡ.\n")
            else:
                for a_score in scores:
                    score_data = scores.get(a_score)
                    print(str(a_score) + ". " + "ΤΡΟΠΟΣ ΠΑΙΧΝΙΔΙΟΥ ΥΠΟΛΟΓΙΣΤΗ: " + score_data[0] + ", ΣΚΟΡ ΧΡΗΣΤΗ: " +
                          str(score_data[1]) + ", ΣΚΟΡ ΥΠΟΛΟΓΙΣΤΗ: " + str(score_data[2]) +
                          ", ΥΠΟΛΟΙΠΑ ΓΡΑΜΜΑΤΑ ΣΤΟ ΣΑΚΟΥΛΑΚΙ: " + str(score_data[3]) +
                          ", ΠΡΟΩΡΟΣ ΤΕΡΜΑΤΙΣΜΟΣ ΠΑΙΧΝΙΔΙΟΥ ΑΠΟ ΠΑΙΚΤΗ: " + score_data[4] +
                          ", ΣΥΝΟΛΙΚΟΙ ΓΥΡΟΙ: " + str(score_data[5]))

    def write_scores(self, score1, score2, bag_left, player_has_quited, turns):
        """method which writes the scores in a specific way on the dictionary of 'scores.json' in the form of a
        dictionary whose key is the element index (string) with value a list in the form of
        [CPU gameplay, Player 1 score, Player 2 score, remaining letters in the bag, message if player quited the game
        before it ended, total turns].
        :param score1: The score of player 1
        :param score2: The score of player 2
        :param bag_left: The remaining letters left in the bag
        :param player_has_quited: A string which indicates if the user force ended the game
        :param turns: the turns of the game"""

        self.check_scores_file()
        with open('scores.json', 'r', encoding="utf8") as f:
            scores = json.load(f)
        with open('scores.json', 'w', encoding="utf8") as f:
            new_score = {str(len(scores)+1): [self.CPU_gameplay, score1, score2, bag_left, player_has_quited, turns]}
            scores.update(new_score)
            json.dump(scores, f)

    def menu_command_manager(self):
        """method which requests the user to give input and execute it. It validates the command based on the game's
        state and the input the user gives. It informs the user if the input they gave is valid or not. It is
        used for all states outside the state in which the game has initiated.
        :return the validation of the command given (true/false)"""

        command = input("ΕΝΤΟΛΗ: ")  # request command
        if command in self.commands.get(self.state):  # checking if command is correct
            # do specific action if the input is a valid one
            print("ΕΚΤΕΛΕΣΗ ΕΝΤΟΛΗΣ.")
            halt_and_separate()
            self.commands.get(self.state).get(command)()
        else:
            # inform user that the action is invalid
            print("ΔΕΝ ΥΠΑΡΧΕΙ Η ΕΝΤΟΛΗ ΠΟΥ ΕΙΣΗΓΑΤΕ. ΠΡΟΣΠΑΘΗΣΤΕ ΞΑΝΑ")
            halt_and_separate()
            return False
        return True

    @staticmethod
    def give_value(word, letter_info):
        """static method which calculates the value of a word, based on the word's letters and the value of each
        letter
        :param word: The word that requests value
        :param letter_info: the information of each letter (quantity and value)
        :return sum: The total value of the word"""

        sum = 0
        if len(word) == 7:
            sum = sum + 50
        for letter in word:
            sum = sum + letter_info.get(letter)[1]
        return sum

    def begin(self):
        """it initializes the game, by showing you the main menu
        IMPORTANT: this command should be exclusively used at the beginning of the game to initialize it"""
        self.show_menu()

    def show_menu(self):
        """The User Interface regarding the state of the Scrabble as 'Main Menu'. The player can navigate
        through different game features/states through this state"""
        self.state = "Menu"
        message = "ΚΥΡΙΟ ΜΕΝΟΥ ΤΟΥ SCRABBLE" \
                  "\n1: ΠΑΙΞΤΕ" \
                  "\n2: ΣΚΟΡΣ" \
                  "\n3: ΡΥΘΜΙΣΕΙΣ" \
                  "\nq: ΕΞΟΔΟΣ"
        flag = False
        while not flag:
            print(message)
            flag = self.menu_command_manager()

    def start_game(self):
        """The User Interface regarding the state of Scrabble as 'Game'. It initializes the game between the human
        player as player 1 against the computer as player 2 (the player 1 starts first)"""

        # initializing required and some new default game data for the game
        self.state = "Game"
        player = [Human(), Computer(self.CPU_gameplay, self.dictionary_data)]  # list of the 2 players
        print("ΕΝΑΡΞΗ ΠΑΙΧΝΙΔΙΟΥ!")
        print("ΠΑΙΚΤΗΣ 1:", player[0].get_characteristics(), " ΠΑΙΚΤΗΣ 2:", player[1].get_characteristics())
        bag = SakClass(self.letter_info)
        # each player gets 7 letters
        player[0].acquire_letters(bag.give_letters(7))
        player[1].acquire_letters(bag.give_letters(7))
        turn_player = 0  # default starting player
        game_end = False  # default game-ending condition
        player_has_quited = "ΟΧΙ"  # default message about forced ending of a game
        turns = 0  # the turns played in the game
        halt_and_separate()
        # loop for each player's turn, (it loops every time they perform non game-ending valid actions after the
        # appropriate game's rulings are applied after the action
        while not game_end:
            turns = turns + 1
            valid_action = False
            # loop that finishes when an action taken is valid. It is mostly defensive programming for a human player's
            # action, considering they might make a move that is against the rulings or his capabilities
            while not valid_action:
                # shows the UI of the player's letters
                self.show_game_UI(player[turn_player], turn_player, turns, bag)
                # checks if the turn player can form a word with their letters while the bag is empty
                if bag.get_amount_of_remaining_letters() == 0 and not self.word_can_be_formed(player[turn_player]):
                    print("ΔΕΝ ΜΠΟΡΕΙ ΝΑ ΦΤΙΑΧΤΕΙ ΛΕΞΗ ΜΕ ΤΑ ΔΙΑΘΕΣΗΜΑ ΓΡΑΜΑΤΑ, ΕΝΩ Ο ΣΑΚΟΣ ΕΙΝΑΙ ΑΔΕΙΟΣ")
                    valid_word_or_command = False
                    game_end = True
                else:
                    valid_word_or_command = player[turn_player].play()  # the player plays.
                if valid_word_or_command:  # checking if the player can perform that move in his power
                    if valid_word_or_command == "p":  # checking if the player gave "pass" command
                        # swaps all the 7 the letters of the player and ends turn and gives the appropriate UI messages.
                        # Also, the next player is assigned to play.
                        valid_action = True  # validates the action
                        # bag gets back the letters the player returned to the bag
                        bag.fill_letters(player[turn_player].return_letters())
                        # player gets back 7 letters
                        player[turn_player].acquire_letters(bag.give_letters(player[turn_player].require_letters()))
                        # prints the outcome of the valid action
                        print("ΑΛΛΑΓΗ ΓΡΑΜΜΑΤΩΝ ΤΟΥ ΠΑΙΚΤΗ ", (turn_player + 1))
                        print("ΝΕΑ", end=" ")
                        player[turn_player].print_letters()
                        print("ΤΕΡΜΑΤΙΣΜΟΣ ΤΟΥ ΓΥΡΟΥ ΤΟΥ ΠΑΙΚΤΗ " + str(turn_player + 1) + ".")
                        turn_player = (turn_player + 1) % 2  # assign the new player
                    elif valid_word_or_command == "q":  # checking if the player gave "quit" command
                        # ends all loops, informs the appropriate variables and gives the appropriate UI message
                        game_end = True
                        valid_action = True
                        player_has_quited = "ΝΑΙ"
                        print("ΠΡΟΟΡΟΣ ΤΕΡΜΑΤΙΣΜΟΣ ΠΑΙΧΝΙΔΙΟΥ!")
                    else:
                        # forms the word and evaluates if the word exists. If it does, it will return the appropriate
                        # points to give to the player. Returns false if the word is illegal
                        # (not in the dictionary data)
                        evaluation = self.evaluate_word_and_score(valid_word_or_command)
                        if evaluation:
                            # player removes the used letters he used, gets the appropriate points, gets new letters
                            # and UI shows the appropriate messages. Also, the next player is assigned to play.
                            player[turn_player].use_letters(valid_word_or_command)  # removes letters
                            player[turn_player].increase_score(evaluation)  # increases player's score based on the word
                            # player gets new letters from the bag
                            player[turn_player].acquire_letters(bag.give_letters(len(valid_word_or_command)))
                            # prints the outcome of the valid action
                            print("ΝΕΟ ΣΚΟΡ:", player[turn_player].get_score())
                            print("ΝΕΑ", end=" ")
                            player[turn_player].print_letters()
                            valid_action = True  # validates the action
                            turn_player = (turn_player + 1) % 2  # next player is assigned
                            # checks if the bag should have given more letters to the player
                            if bag.is_emptied_out():
                                print("Ο ΣΑΚΟΣ ΕΞΑΝΤΛΗΘΗΚΕ!")
                                game_end = True
                halt_and_separate()
        # at this point of the code, game
        self.game_results(player[0].get_score(), player[1].get_score(), bag, player_has_quited, turns)
        halt_and_separate()
        self.show_menu()  # returns to the main menu

    def show_scores(self):
        """The User Interface regarding the state of Scrabble as 'Scores'. The player can view his scores in
        this state"""

        self.state = "Scores"
        message = "\nb: ΕΠΙΣΤΡΟΦΗ"
        flag = False
        while not flag:
            self.print_scores()
            print(message)
            flag = self.menu_command_manager()

    def show_settings(self):
        """The User Interface regarding the state of Scrabble as 'Settings'. The player navigate to the CPU
        gameplay settings, reset the 'scores.json' file, or the 'words_dict.json' file (considering a potential
        corrupt or update of the latter)"""

        self.state = "Settings"
        message = "ΡΥΘΜΙΣΕΙΣ:" \
                  "\n1: ΤΡΟΠΟΣ ΠΑΙΧΝΙΔΙΟΥ ΥΠΟΛΟΓΙΣΤΗ" \
                  "\n2: ΕΠΑΝΑΡΧΙΚΟΠΟΙΗΣΗ ΕΝΣΩΜΑΤΟΜΕΝΟΥ ΛΕΞΙΚΟΥ" \
                  "\n3: ΕΠΑΝΑΡΧΙΚΟΠΟΙΗΣΗ ΤΩΝ ΣΚΟΡ" \
                  "\nb: ΕΠΙΣΤΡΟΦΗ"
        flag = False
        while not flag:
            print(message)
            flag = self.menu_command_manager()

    def show_CPU_gameplay(self):
        """The User Interface regarding the state of Scrabble as 'Settings_CPU_Gameplay'. The player can change
        the way the CPU can play during the game in this state. The can also view the current CPU gameplay"""

        self.state = "Settings_CPU_Gameplay"
        message = "ΕΠΙΛΕΞΤΕ ΤΡΟΠΟ ΠΑΙΧΝΙΔΙΟΥ ΥΠΟΛΟΓΙΣΤΗ (ΕΠΙΛΕΓΜΕΝΟΣ ΤΡΟΠΟΣ ΠΑΙΧΝΙΔΙΟΥ: " + self.CPU_gameplay + ")" + \
                  "\n1: Min_Letters (ΚΑΤΑΣΚΕΥΗ ΛΕΞΕΩΝ ΜΕ ΟΣΟΝ ΔΥΝΑΤΟΝ ΛΙΓΟΤΕΡΑ ΓΡΑΜΜΑΤΑ)" \
                  "\n2: Max_Letters (ΚΑΤΑΣΚΕΥΗ ΛΕΞΕΩΝ ΜΕ ΟΣΟΝ ΔΥΝΑΤΟΝ ΠΕΡΙΣΣΟΤΕΡΑ ΓΡΑΜΜΑΤΑ)" \
                  "\n3: Smart (ΚΑΤΑΣΚΕΥΗ ΛΕΞΕΩΝ ΠΟΥ ΠΑΡΑΓΟΥΝ ΤΟΥΣ ΠΕΡΙΣΣΟΤΕΡΟΥΣ ΠΟΝΤΟΥΣ)" \
                  "\nb: ΕΠΙΣΤΡΟΦΗ"
        flag = False
        while not flag:
            print(message)
            flag = self.menu_command_manager()

    def set_CPU_gameplay_Min_Letters(self):
        """setter of the CPU gameplay attribute into 'Min_Letters', followed by appropriate message"""

        self.CPU_gameplay = "Min_Letters"
        print("ΑΛΛΑΓΗ ΤΡΟΠΟΥ ΠΑΙΧΝΙΔΙΟΥ ΣΕ Min_Letters!\n")
        halt_and_separate()
        self.show_CPU_gameplay()

    def set_CPU_gameplay_Max_Letters(self):
        """setter of the CPU gameplay attribute into 'Max_Letters', followed by appropriate message"""

        self.CPU_gameplay = "Max_Letters"
        print("ΑΛΛΑΓΗ ΤΡΟΠΟΥ ΠΑΙΧΝΙΔΙΟΥ ΣΕ Max_Letters!\n")
        halt_and_separate()
        self.show_CPU_gameplay()

    def set_CPU_gameplay_Smart(self):
        """setter of the CPU gameplay attribute into 'Smart', followed by appropriate message"""

        self.CPU_gameplay = "Smart"
        print("ΑΛΛΑΓΗ ΤΡΟΠΟΥ ΠΑΙΧΝΙΔΙΟΥ ΣΕ Smart!\n")
        halt_and_separate()
        self.show_CPU_gameplay()

    def reset_dictionary_data(self):
        """method that resets the data of the dictionary in 'words_dict.json'. Can be used to reset the file if it's
        corrupted, or for testing purposes."""

        if os.path.exists("words_dict.json"):
            os.remove("words_dict.json")
        self.generate_word_data(self.letter_info)
        halt_and_separate()
        self.show_settings()

    def reset_scores(self):
        """method that resets the data of the scores in 'scores.json'. Can be used to reset the file if it's
        corrupted, or for testing purposes."""

        if os.path.exists("scores.json"):
            os.remove("scores.json")
        self.check_scores_file()
        print("ΕΠΙΤΥΧΗΣ ΕΠΑΝΑΡΧΙΠΟΠΟΙΗΣΗΣ ΤΩΝ ΣΚΟΡ!")
        halt_and_separate()
        self.show_settings()

    @staticmethod
    def quit_scrabble():
        """static method that prints a method which is the last message, before the game exits."""
        print("ΤΕΡΜΑΤΙΣΜΟΣ ΕΦΑΡΜΟΓΗΣ...")

    @staticmethod
    def show_game_UI(player, turn_player, turn, sakclass):
        """static method which prints the game state (player letters with its values, the player's score,
        the remaining letters in the bag, etc), in a user friendly way
        :param player instance of the class Player
        :param turn_player: Turn player, based on the index (starting from 0) of the list that has all the players
        :param sakclass: instance of the class SakClass
        :param turn: the turn the game is currently on"""

        print("ΓΥΡΟΣ " + str(turn) + " - ΣΕΙΡΑ ΤΟΥ ΠΑΙΚΤΗ " + str(turn_player + 1) + " (" + player.get_characteristics()
              + ")" + " - ΠΟΝΤΟΙ: " + str(player.get_score()) + " - ΓΡΑΜΜΑΤΑ ΣΤΟ " "ΣΑΚΟΥΛΑΚΙ: " +
              str(sakclass.get_amount_of_remaining_letters()))

        player.print_letters()
        if isinstance(player, Human):
            print("ΠΑΡΑΚΑΛΩ, ΕΙΣΑΓΕΤΕ ΛΕΞΗ Η ΕΝΤΟΛΗ (p: ΑΛΛΑΓΗ ΓΡΑΜΜΑΤΩΝ, q: ΤΕΡΜΑΤΙΣΜΟΣ ΠΑΙΧΝΙΔΙΟΥ)!")

    def evaluate_word_and_score(self, word):
        """method which checks if the word given exists
        :param word: The word given
        :return either the points the word if it exists on the dictionary which was loaded from 'words_dict.json'.
        Otherwise, it returns false"""

        if word in self.dictionary_data.get(str(len(word))):
            points = self.dictionary_data.get(str(len(word))).get(word)
            print("ΕΓΚΥΡΗ ΛΕΞΗ: " + word + ", ΠΟΝΤΟΙ: " + str(points))
            return points
        else:
            print("Η ΛΕΞΗ ΠΟΥ ΕΙΣΗΓΑΤΕ ΔΕΝ ΥΠΑΡΧΕΙ. ΠΑΡΑΚΑΛΩ, ΟΡΙΣΤΕ ΝΕΑ ΛΕΞΗ Η ΕΝΤΟΛΗ")
            return False

    def game_results(self, score1, score2, sakclass, player_has_quited, turns):
        """It prints the results of the game and updates the file, based on the info of the game
        :param score1: the score of the player 1
        :param score2: the score of the player 2
        :param sakclass instance of the class SakClass
        :param player_has_quited: message that defines if the player terminated the game early\
        :param turns: the turns of the game"""

        print("ΤΕΛΙΚΟ ΣΚΟΡ ΠΑΙΚΤΗ 1:", score1)
        print("ΤΕΛΙΚΟ ΣΚΟΡ ΠΑΙΚΤΗ 2:", score2)
        print("ΥΠΟΛΟΙΠΑ ΓΡΑΜΜΑΤΑ ΣΕ ΣΑΚΟΥΛΑΚΙ:", sakclass.get_amount_of_remaining_letters())
        self.check_scores_file()
        if score1 > score2:
            print("Ο ΠΑΙΚΤΗΣ 1 ΕΙΝΑΙ ΝΙΚΗΤΗΣ!")
        elif score1 < score2:
            print("Ο ΠΑΙΚΤΗΣ 2 ΕΙΝΑΙ ΝΙΚΗΤΗΣ!")
        else:
            print("ΙΣΟΠΑΛΙΑ!")
        self.write_scores(score1, score2, sakclass.get_amount_of_remaining_letters(), player_has_quited, turns)

    def word_can_be_formed(self, player):
        """method that checks if the player can form a word with their available letters
        :param player: an instance of a player
        :return true if the player can form a word with their given letters, otherwise, returns false"""

        list_of_letters_without_values = player.get_letters_without_values()
        # the double loop of the word's length to be checked and the permutations it can provide
        for word_length in range(1, 8):
            for permutation in itertools.permutations(list_of_letters_without_values, word_length):
                word = ''.join(permutation)  # makes a list that is a product set of permutation into a string
                # checks if the formed word exists in the dictionary
                if word in self.dictionary_data.get(str(word_length)):
                    return True
        return False


class SakClass:
    """This class represents the bag that contains all the letters of the game and manages them"""

    def __init__(self, letter_info):
        """constructor of the the bag, which filling it with the appropriate letters. It also has a boolean attribute
        whose purpose is to notify if the bag should have given more letters than it gave
        :param letter_info: the information of each letter (including its total quantity and its value)"""
        self.bag = []  # list of the bag. Each element is a list in the form of [letter, letter_value]
        self.letter_info = letter_info  # the information of each letter to fill out the bag
        self.refill_bag()  # filling out the bag
        # the state which notifies if the bag gave less letters than it should have (because it was emptied out)
        self.emptied_out = False

    def __repr__(self):
        """representation of the instance, through the letters currently on its bag, alongside of whether it should
        give more letters than it gave to the player that they requested (emptied out)"""
        return 'Bag: ' + str(self.bag) + \
               '\nEmptied out: ' + str(self.emptied_out)

    def refill_bag(self):
        """method that fills the attribute that is a list with letters in the form of [letter, letter_value],
        based on the quantity of each letter which is specified in the attribute of letter info"""

        self.bag = []
        for letter in self.letter_info:
            for amount_of_letters in range(self.letter_info.get(letter)[0]):
                self.bag.append([letter, self.letter_info.get(letter)[1]])
        random.shuffle(self.bag)

    def give_letters(self, quantity):
        """method which removes random letters of the bag, based on the quantity. It also checks if the required
        letters are more than the letters than the letters the bag actually has
        :param quantity: the quantity of the letters required
        :return an random array with elements from the bag, in the form of [letter, letter_value] """
        if len(self.bag) < quantity:
            # bag's action if there aren't enough letters than the ones required
            remaining_letters = len(self.bag)
            self.emptied_out = True
            return [self.bag.pop(random.randrange(len(self.bag))) for _ in range(remaining_letters)]
        # bag's action if there are enough letters to give
        return [self.bag.pop(random.randrange(len(self.bag))) for _ in range(quantity)]

    def fill_letters(self, array_of_letters):
        """method that puts inside the bag a list of letters whose element is in the form of [letter, letter_value]
        :param array_of_letters: the array of letters given back to the bag"""
        for letter in array_of_letters:
            self.bag.append(letter)

    def is_emptied_out(self):
        """getter of whether the bag is emptied out or not:
        :return if the bag is emptied out or not (boolean)"""

        return self.emptied_out

    def get_amount_of_remaining_letters(self):
        """getter of the length of the bag
        :return the length of the bag"""
        return len(self.bag)


class Player:
    """This class represents the player. Its main purpose is to give specific attributes and methods to specific
    category of players, which both categories of players share"""

    def __init__(self):
        """constructor of the class of player which initializes the score to 0 and gives him an array that will
        include the letters he has"""
        self.score = 0  # a player's initial score should be 0
        self.letters_array = []  # a player starts out without letters.

    def __repr__(self):
        """representation of the player, based on all his attributes"""
        return 'Score: ' + str(self.score) + \
               '\nBag: ' + str(self.letters_array)

    @staticmethod
    def get_characteristics():
        """method that gives a string which specifies the category of the player. It is mostly used for the children
        classes of the current class.
        :return a string that specifies the category of the player"""
        return "ΑΓΝΩΣΤΗ ΚΑΤΗΓΟΡΙΑ ΠΑΙΚΤΗ"

    def acquire_letters(self, array_of_letters):
        """method which gives an array of letters on the player's available letters
        :param array_of_letters: the array of letters each player gets """
        for letter in array_of_letters:
            self.letters_array.append(letter)

    def require_letters(self):
        """method that gives amount of letters the player needs to have a total of 7 letters
        :return the amount of letters the players needs to have a total of 7 letters"""
        return 7 - len(self.letters_array)

    def increase_score(self, score_up):
        """increment of the player's score
        :param score_up: the value that increments into the score"""
        self.score = self.score + score_up

    def get_letters_array(self):
        """getter of the letters of the player
        :return the array of letters of the player"""
        return self.letters_array

    def get_score(self):
        """getter of the player's score
        :return the score of the player"""
        return self.score

    def return_letters(self):
        """the player removes the letters from his possession into the bag. Therefore, this method has to give away the
        letters the player had
        :return the letters the player had"""
        return_letters = list(self.letters_array)
        self.letters_array = []
        return return_letters

    @staticmethod
    def is_command(command):
        """"method that checks if the input is a command of the game
        :param: command: the word that is determined whether is a command or not
        :return true if the the input is command (q or p). Otherwise, return false."""
        if command == 'q' or command == "p":
            return True
        return False

    def play(self):
        """method that performs the player's playing action. It is used exclusively for the children classes
        of the class player. If it is used on this class instead, it prints a message that the player was not defined
        correctly"""
        print("ΔΕΝ ΟΡΙΣΤΙΚΕ ΤΟ ΕΙΔΟΣ ΤΟΥ ΠΑΙΚΤΗ. ΔΕΝ ΛΑΜΒΑΝΕΤΑΙ ΠΡΑΞΗ!")

    def use_letters(self, word):
        """method that removes the letters from the array of the player based on the word they used. This methods
        should only be used when the player has the letters required to form the specific word
        :param word: The word the player formed and therefore the letters required to form the word and remove them
        from the player's array"""

        for letter in word:
            for letter_with_value in self.letters_array:
                if letter == letter_with_value[0]:
                    self.letters_array.remove(letter_with_value)
                    break

    def print_letters(self):
        """method that prints out the letters with their values in a user friendly way"""

        print("ΓΡΑΜΜΑΤΑ: ", end="")
        for letters in range(len(self.letters_array)):
            print("'" + self.letters_array[letters][0] + "'" + ":", self.letters_array[letters][1], end="  ")
        print()

    def get_letters_without_values(self):
        """method that returns the letters without their values
        :return a list of each of the user's letters (without the values)"""

        return [letter[0] for letter in self.letters_array]


class Human(Player):
    """This class represents the human player. It inherits attributes and methods from its father class, Player.
    It contains all the required methods of the human that are required for them to interact with the game of
    Scrabble"""

    def __init__(self):
        """Constructor of the class of Human. It fully inherits it from the Player class."""
        super().__init__()

    def get_characteristics(self):
        """method that overrides the original method, which gives a specific string that determines the player's
        category
        :return a string that determines the human player's category"""
        return "ΧΡΗΣΤΗΣ"

    @staticmethod
    def has_capital_greek_letters(word):
        """static method with defensive programming purposes, which checks whether the word given does not have
        any greek capital letters. It also checks if the word given is an empty string, it prints the appropriate
        message in here, considering its a message that refers to the human player being able to form that word,
        rather than the word being valid in the dictionary.
        IMPORTANT: this method should be used after it was determined that special commands have been checked
        :param word: the word that needs said validation
        :return true, if the word if valid based on said criteria, otherwise, it returns false."""

        if len(word) == 0:  # checks if the word is empty string
            print("ΒΑΛΑΤΕ ΜΗ ΕΠΙΤΡΕΠΤΗ ΚΕΝΗ ΕΙΣΟΔΟ. ΠΑΡΑΚΑΛΩ, ΕΙΣΑΓΕΤΕ ΝΕΑ ΛΕΞΗ Η ΕΝΤΟΛΗ")
            return False
        # the valid characters
        viable_letters = ["Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η", "Θ", "Ι", "Κ", "Λ", "Μ", "Ν", "Ξ", "Ο", "Π", "Ρ",
                          "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω"]
        for letter in word:  # checking if each character of the word is valid
            if letter not in viable_letters:
                print("H ΛΕΞΗ ΠΟΥ ΣΧΗΜΑΤΗΣΑΤΕ ΕΧΕΙ ΧΑΡΑΚΤΗΡΕΣ ΠΟΥ ΔΕΝ ΕΙΝΑΙ ΚΑΦΑΛΑΙΟΙ ΚΑΙ ΕΛΛΗΝΙΚΟΙ "
                      "(ΟΥΤΕ ΑΠΟΤΕΛΟΥΝ ΕΝΤΟΛΗ). ΠΑΡΑΚΑΛΩ, ΕΙΣΑΓΕΤΕ ΝΕΑ ΛΕΞΗ Η ΕΝΤΟΛΗ")
                return False
            return True

    def can_form_word(self, word):
        """method which determines whether the word given can be created with a permutation of the user's array of
        letters (however, permutation isn't used as a way to determine that)
        :param word: the word that requires said validation
        :return true if the word is valid by said criteria, otherwise, return false"""

        no_num_letter_array = [letter[0] for letter in self.letters_array]  # creating an array with just the letters
        # checking if the word has more letters than the user's available letters (7)
        if len(word) > len(no_num_letter_array):
            print("Η ΛΕΞΗ ΠΟΥ ΣΧΗΜΑΤΗΣΑΤΕ ΔΕΝ ΜΠΟΡΕΙ ΝΑ ΣΧΗΜΑΤΙΣΤΕΙ ΑΠΟ ΤΑ ΓΡΑΜΜΑΤΑ ΠΟΥ ΚΑΤΕΧΕΤΕ (ΧΡΗΣΗ ΠΕΡΙΣΣΟΤΕΡΩΝ "
                  "ΓΡΑΜΜΑΤΩΝ ΑΠΟ ΑΥΤΩΝ ΠΟΥ ΚΑΤΕΧΕΤΕ). ΠΑΡΑΚΑΛΩ ΕΙΣΑΓΕΤΕ ΝΕΑ ΛΕΞΗ Η ΕΝΤΟΛΗ")
            return False
        clone_letters_array = list(no_num_letter_array)
        # checking if you can remove a letter from the array for each letter the word has (to determine if you can
        # form the word based on your letters)
        for letter in word:
            if letter in clone_letters_array:
                clone_letters_array.remove(letter)
            else:
                print("Η ΛΕΞΗ ΠΟΥ ΣΧΗΜΑΤΗΣΑΤΕ ΔΕΝ ΜΠΟΡΕΙ ΝΑ ΣΧΗΜΑΤΙΣΤΕΙ ΑΠΟ ΤΑ ΓΡΑΜΜΑΤΑ ΠΟΥ ΚΑΤΕΧΕΤΕ. ΠΑΡΑΚΑΛΩ, "
                      "ΕΙΣΑΓΕΤΕ ΝΕΑ ΛΕΞΗ Η ΕΝΤΟΛΗ")
                return False
        return True

    def play(self):
        """method that performs the human player's turn, by allowing them to give an input of a word or command
        and gives the validation of the human player's input
        :return the validation of user's input"""

        command_or_word = input("ΕΝΤΟΛΗ/ΛΕΞΗ: ")
        if self.is_command(command_or_word):
            return command_or_word
        elif self.has_capital_greek_letters(command_or_word) and self.can_form_word(command_or_word):
            return command_or_word
        return False


class Computer(Player):
    """This class represents the computer player. It inherits attributes and methods from its father class, Player.
    It contains all the required methods of the computer that are required for them to interact with the game of
    Scrabble"""

    def __init__(self, gameplay, dictionary_data):
        """Constructor of the class of Human. It inherits it from the Player class. It also has a few
        attributes regarding the gameplay of the CPU (how it should play), the dictionary of the words, that is
        basically the learning part of the computer, which helps it determine which words to form and a dictionary
        that is used to determine its actions, based on the gameplay attribute of the computer
        :param gameplay: the gameplay the computer is going to use (a string value from game's settings)
        :param dictionary_data: the data of the dictionary (each words with the value/score the word provides"""

        super().__init__()
        self.gameplay = gameplay
        self.dictionary_data = dictionary_data
        self.actions = {"Min_Letters": self.play_min_letters,
                        "Max_Letters": self.play_max_letters,
                        "Smart": self.play_smart}

    def get_characteristics(self):
        """method that overrides the original method, which gives a specific string that determines the computer's
        category
        :return a string that determines the computer player's category"""
        return "ΥΠΟΛΟΓΙΣΤΗΣ - " + str(self.gameplay)

    def play(self):
        """the methods that is used for the computer to play. The algorithm/gameplay it will perform is determined
        by the gameplay that the computer is being assigned to (the gameplay attribute). It has some defensive
        programing based on whether the computer's gameplay is valid (because the computer gameplay can be
        assigned wrongly), and it gives the word the computer picked, based on the algorithm it used
        :return the word the computer will use"""

        if self.gameplay not in self.actions:
            print("ΣΦΑΛΜΑ ΣΤΟΝ ΟΡΙΣΜΟ ΤΟΥ ΤΡΟΠΟΥ ΠΑΙΧΝΙΔΙΟΥ ΤΟΥ ΥΠΟΛΟΓΙΣΤΗ!")
        else:
            return self.actions.get(self.gameplay)()

    def play_smart(self):
        """this method is the smart algorithm the computer will use to select a word and picks randomly a word
        among the words that provide the highest amount of points.
        :return a random word or action that is considered the most optimal"""
        # this is the least optional action, which will be picked if the computer cannot form any word
        # it has the form of, [[list of words], total value]
        command_or_words = [["p"], -1]
        # creates the list of the letters without their values
        no_num_letter_array = self.get_letters_without_values()
        # loop based on each word's length
        for word_length in range(1, 8):
            # loop based on every permutation of the list of letters in sets whose length is equal to the word's length
            for permutation in itertools.permutations(no_num_letter_array, word_length):
                word = ''.join(permutation)  # makes a list that is a product set of permutation into a string
                # checks if the formed word exists in the dictionary
                if word in self.dictionary_data.get(str(word_length)):
                    word_value = self.dictionary_data.get(str(word_length)).get(word)  # gets the word's value
                    # compares the word's value with the current most optional action:
                    # updates the value and adds the word as the currently only element of the potential optimal actions
                    if word_value > command_or_words[1]:
                        command_or_words = [[word], word_value]
                    # appends word in the most optional words if it's equally valuable and does not already exist
                    # in the potential actions
                    elif word_value == command_or_words[1]:
                        if word not in command_or_words[0]:
                            command_or_words[0].append(word)
        # takes a random word ("p" if no word could be formed), based on the possible optimal actions
        action = random.choice(command_or_words[0])
        return action

    def play_min_letters(self):
        """this method is the smart algorithm the computer will use to select a word and picks randomly a word
        among the words that require the minimum amount of letters.
        :return a random word or action with the minimum possible amount of letters"""
        # this is the least optional action, which will be picked if the computer cannot form any word
        # it has the form of, [list of words]
        command_or_words = ["p"]
        # creates the list of the letters without their values
        no_num_letter_array = self.get_letters_without_values()
        # loop based on every permutation of the list of letters in sets whose length is equal to the word's length
        # starting from the lowest amount of possible letters that they can be formed to the highest. It breaks
        # the loop once the computer finds all the words with length equals to any length of letters it first
        # detects
        for word_length in range(1, 8):
            # loop based on every permutation of the list of letters in sets whose length is equal to the word's length
            for permutation in itertools.permutations(no_num_letter_array, word_length):
                word = ''.join(permutation)  # makes a list that is a product set of permutation into a string
                # checks if the formed word exists in the dictionary
                if word in self.dictionary_data.get(str(word_length)):
                    # check if the only stored action of the computer is to pass. If yes, it replaces that
                    # action with with the valid word
                    if command_or_words == ["p"]:
                        command_or_words = [word]
                    # checks if the word already exists in the potential actions through an another permutation
                    # (considering there is no "pass" action in potential actions). If it doesn't, it adds the word
                    # in the potential words that the computer can use
                    elif word not in command_or_words:
                        command_or_words.append(word)
            # once all the permutations of a specific amount of letters is performed, if there are words in the list
            # of computer's potential actions, the loop stops here
            if "p" not in command_or_words:
                break
        # choosing a random word/action through the list of words
        action = random.choice(command_or_words)
        return action

    def play_max_letters(self):
        """this method is the smart algorithm the computer will use to select a word and picks randomly a word
        among the words that require the maximum amount of letters.
        :return a random word or action with the maximum possible amount of letters"""
        # this is the least optional action, which will be picked if the computer cannot form any word
        # it has the form of, [list of words]
        command_or_words = ["p"]
        # creates the list of the letters without their values
        no_num_letter_array = self.get_letters_without_values()
        # loop based on every permutation of the list of letters in sets whose length is equal to the word's length
        # starting from the highest amount of possible letters that they can be formed to the lowest. It breaks
        # the loop once the computer finds all the words with length equals to any length of letters it first
        # detects
        for word_length in range(7, 0, -1):
            # loop based on every permutation of the list of letters in sets whose length is equal to the word's length
            for permutation in itertools.permutations(no_num_letter_array, word_length):
                word = ''.join(permutation)  # makes a list that is a product set of permutation into a string
                # checks if the formed word exists in the dictionary
                if word in self.dictionary_data.get(str(word_length)):
                    # check if the only stored action of the computer is to pass. If yes, it replaces that
                    # action with with the valid word
                    if command_or_words == ["p"]:
                        command_or_words = [word]
                    # checks if the word already exists in the potential actions through an another permutation
                    # (considering there is no "pass" action in potential actions). If it doesn't, it adds the word
                    # in the potential words that the computer can use
                    elif word not in command_or_words:
                        command_or_words.append(word)
            # once all the permutations of a specific amount of letters is performed, if there are words in the list
            # of computer's potential actions, the loop stops here
            if "p" not in command_or_words:
                break
        # choosing a random word/action through the list of words
        action = random.choice(command_or_words)
        return action
