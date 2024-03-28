import time

import PySimpleGUI as sg
import numpy as np
import random
import copy
import sys
from datetime import datetime

from my_vars import *
import my_vars as mv
import historical_data
import show_about


def game_board() -> sg.Window:
    layout = [[sg.Text(f'Τύπος παιχνιδιού: {mv.GAME_MODE_TEXT}')],
              [sg.Text(f'Επίπεδο Υπολογιστή: {mv.COMPUTER_LEVEL}')],
              [sg.Text(f'Παίζει ο: {mv.PLAYERS[PLAY_FIRST]}', key='-CURRENT_PLAYER-')]]
    for row in range(3):
        new_row = []
        for column in range(3):
            new_row.append(sg.Button(size=(18, 9), key=(row, column), image_filename=''))
        layout.append(new_row)
    layout.append([sg.Button('Αρχικοποίηση', key='-RESET-'), sg.Button('Έξοδος', key='-EXIT-')])
    return sg.Window('Τρίλιζα', layout, use_default_focus=False, icon=GAME_ICON, finalize=True)


class Board:
    """
        Κλάση που δημιουργεί το αντικείμενο Board.
        Είναι το "λογικό" κομμάτι του ταμπλό σε nd.array(3,3) όπου καταγράφουμε την εξέλιξη του παιχνιδιού:
            Διαθέσιμες θέσεις, ποια θέση χρησιμοποιήθηκε, έλεγχο αν η κίνηση που έγινε δίνει νικητή κ.α.
    """
    def __init__(self):
        self.squares = np.zeros((3, 3))
        self.empty_sq = self.squares
        self.used_squares = 0
        self.winner = []
        self.corner = [(0, 0), (0, 2), (2, 0), (2, 2)]
        self.sides = [(0, 1), (1, 0), (1, 2), (2, 1)]

    def check_for_winner(self) -> int:
        """
            Επιστρέφει 0: Το παιχνίδι δεν έχει τελειώσει ή είναι ισοπαλία
            Επιστρέφει 1: Ο Παίκτης 1 κερδίζει
            Επιστρέφει 2: Ο Παίκτης 2 κερδίζει
        """

        # Ελέγχουμε για τρίλιζα σε όλες τις στήλες
        for col in range(3):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if self.squares[0][col] == 1:
                    # λίστα με τον παίκτη που κερδίζει και tuples με τα τετράγωνα που κάνουν τρίλιζα
                    self.winner = [1, (0, col), (1, col), (2, col)]
                else:
                    self.winner = [2, (0, col), (1, col), (2, col)]
                return self.squares[0][col]  # Επιστρέφει το αποτέλεσμα

        # Ελέγχουμε για τρίλιζα σε όλες τις γραμμές
        for row in range(3):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if self.squares[row][0] == 1:
                    self.winner = [1, (row, 0), (row, 1), (row, 2)]
                else:
                    self.winner = [2, (row, 0), (row, 1), (row, 2)]
                return self.squares[row][0]

        # Ελέγχουμε για τρίλιζα στη διαγώνιο (0,0) (1,1) (2,2)
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if self.squares[1][1] == 1:
                self.winner = [1, (0, 0), (1, 1), (2, 2)]
            else:
                self.winner = [2, (0, 0), (1, 1), (2, 2)]
            return self.squares[1][1]

        # Ελέγχουμε για τρίλιζα στην διαγώνιο (2,0) (1,1) (0,2)
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if self.squares[1][1] == 1:
                self.winner = [1, (0, 2), (1, 1), (2, 0)]
            else:
                self.winner = [2, (0, 2), (1, 1), (2, 0)]
            return self.squares[1][1]

        # Ισοπαλία ή παιχνίδι σε εξέλιξη
        self.winner = [0, ]
        return 0

    def mark_square(self, row, col, player) -> None:
        """
            Μέθοδος που μαρκάρει μία θέση ότι έχει χρησιμοποιηθεί.
            Ενημερώνει την ιδιότητα used_squares με το πόσα τετράγωνα έχουν παίξει.
            Συντεταγμένες (row, col) θέσης που επιλέχθηκε

            @param row: Γραμμή
            @param col: Στήλη
            @param player: Παίχτης που έπαιξε στη θέση row, col
        """
        self.squares[row][col] = player
        self.used_squares += 1

        for i in range(len(self.corner)):   # Αφαιρούμε από τις διαθέσιμες γωνίες αυτή που έπαιξε
            if (row, col) == self.corner[i]:
                self.corner.pop(i)
                return
        for i in range(len(self.sides)):   # Αφαιρούμε από τις διαθέσιμες μεσαίες θέσεις αυτή που έπαιξε
            if (row, col) == self.sides[i]:
                self.sides.pop(i)
                return

    def empty_squares(self, row, col) -> bool:
        """
            Συνάρτηση για τον έλεγχο μίας θέσης αν είναι κενή

            Συντεταγμένες (row, col) θέσης που επιλέχθηκε
            @param row
            @param col
            @return: True αν η θέση row,col είναι κενή
        """
        return self.squares[row][col] == 0

    def get_empty_squares(self) -> list:
        """
            @return: Λίστα με τις κενές θέσεις
        """
        empty_sqrs = []
        for row in range(3):
            for col in range(3):
                if self.empty_squares(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self) -> bool:
        """
            @return: True αν το ταμπλό είναι γεμάτο
        """
        return self.used_squares == 9

    def isempty(self) -> bool:
        """
            @return: True αν το ταμπλό είναι κενό
        """
        return self.used_squares == 0


class AI:
    """
        Κλάση που υλοποιεί τον αυτοματοποιημένο παίκτη.

        Μέθοδοι:
        rnd(): Τυχαίο παίξιμο - Απλός παίκτης
        medium_player(): Απλή στρατηγική - Μέτριος παίκτης
        minimax(): Αξιολόγηση όλων των κινήσεων μπροστά - Expert παίκτης
    """

    def __init__(self, player=2):
        self.level = mv.COMPUTER_LEVEL
        self.player = player

    @staticmethod
    def rnd(board) -> tuple:  # --- Τυχαία επιλογή θέσης ---
        """
            Μέθοδος που υλοποιεί το τυχαίο παίξιμο επιλέγοντας μία από τις διαθέσιμες κενές θέσεις.

            @param board: Αντικείμενο Board()
            @return: Tuple (row,col) με την τυχαία θέση που επιλέχθηκε
        """
        empty_sqrs = board.get_empty_squares()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx]  # (row, col)

    # ******************************************************************************************************************
    # TODO: Medium level player
    # ******************************************************************************************************************

    def medium_player(self, board) -> tuple:  # --- CPU is Medium Player ---
        empty_sqrs = board.get_empty_squares()

        # Αν ξεκινάει ο υπολογιστής και είναι η πρώτη κίνηση (άδειο ταμπλό),
        # η προτεινόμενη στρατηγική είναι να παίξει σε κάποια γωνία
        # https://www.wikihow.com/Win-at-Tic-Tac-Toe

        # Παίζει κάποια από τις τέσσερεις γωνίες αν είναι ελεύθερη
        if board.squares[0][0] == 0 or board.squares[0][2] == 0 or board.squares[2][0] == 0 or board.squares[2][2] == 0:
            if len(board.corner) > 0:
                i = random.randrange(0, len(board.corner))
                idx = board.corner[i]
                while idx not in empty_sqrs:
                    i = random.randrange(0, len(board.corner))
                    idx = board.corner[i]
                return idx

        # Παίζει το κεντρικό τετράγωνο αν είναι ελεύθερο
        if board.squares[1][1] == 0:
            return 1, 1

        # Παίζει σε κάποιο μέσο πλευράς αν είναι ελεύθερο
        elif board.squares[0][1] == 0 or board.squares[1][0] == 0 or board.squares[1][2] == 0 or board.squares[2][1] == 0:
            i = random.randrange(0, len(board.sides))
            idx = board.sides[i]
            while idx not in empty_sqrs:
                i = random.randrange(0, len(board.sides))
                idx = board.sides[i]
            board.sides.pop(i)
            return idx

    # --- CPU is EXPERT (MINIMAX) ---
    def minimax(self, board, maximizing: bool) -> tuple:
        """
            Μέθοδος που υλοποιεί τον Expert παίκτη.
            Δημιουργεί ένα πλήρες αντίγραφο του Board() και αξιολογεί αναδρομικά όλες τις κινήσεις πριν επιλεγεί μία θέση.

            @param board: Αντικείμενο Board()
            @param maximizing: Boolean. True/False ανάλογα την κίνηση που υπολογίζει (κίνηση που θα κάνει ή επόμενη κίνηση αντιπάλου)
            @return: Tuple(min/max_eval, best_move) -> Αποτέλεσμα αξιολόγησης, καλύτερη κίνηση
        """
        case = board.check_for_winner()

        if case == 1:
            return 1, None  # eval, move

        if case == 2:
            return -1, None

        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # --- MAIN EVAL ---

    def eval(self, board) -> tuple:
        """
            Μέθοδος που επιστρέφει τη θέση που θα παίξει ο αυτοματοποιημένος παίκτης, ανάλογα με το επίπεδό του.
            @param board:
            @return: Tuple(row,col) η θέση που θα παίξει.
        """
        # Αν ξεκινάει ο υπολογιστής και είναι η πρώτη κίνηση (άδειο ταμπλό),
        # η πρώτη θέση επιλέγεται τυχαία για τον απλό και τον expert παίκτη, διαφορετικά ο αλγόριθμος minimax
        # θα έχει πάντα το ίδιο αποτέλεσμα.
        # Ο πρώτος παίκτης που παίζει τυχαία την πρώτη κίνηση έχει μειονέκτημα γιατί δεν υπάρχει πρόβλεψη.
        if self.level == mv.AI_PLAYER_SIMPLE or self.level == mv.AI_PLAYER_EXPERT:
            move = ()
            if board.isempty():
                move = self.rnd(board)
                return move

        if self.level == mv.AI_PLAYER_SIMPLE:
            # random choice
            move = self.rnd(board)
        elif self.level == mv.AI_PLAYER_AVG:
            move = self.medium_player(board)
        elif self.level == mv.AI_PLAYER_EXPERT:
            eval, move = self.minimax(board, False)

        return move


class Game:
    """
        Κλάση που υλοποιεί τις μεθόδους για τον έλεγχο της ροής του παιχνιδιού και την αποτύπωση των κινήσεων στο GUI
    """
    def __init__(self, window):
        self.board = Board()
        self.ai = AI()
        self.running = True
        self.first_player = mv.PLAY_FIRST
        self.player = self.first_player  # 1-παίζει Χ #2-παίζει Ο
        self.window = window
        mv.CURRENT_PLAYER = mv.PLAYERS[self.player]

    def draw_symbol(self, row, col) -> None:
        """
            Εμφανίζει στο ταμπλό το σύμβολο κάθε παίκτη
            Συντεταγμένες (row, col) θέσης που επιλέχθηκε
            @param row
            @param col
        """
        if self.player == 1:
            self.window.Element((row, col)).update(image_filename=X_SYMBOL)
        elif self.player == 2:
            self.window.Element((row, col)).update(image_filename=O_SYMBOL)
        self.window.Element((row, col)).update(disabled=True)  # Απενεργοποιούμε το κουμπί-θέση που επιλέχθηκε

    def make_move(self, row, col):
        """
        Μέθοδος που εκτελείτε σε κάθε κίνηση. Ενημερώνει το Board(), εμφανίζει το κατάλληλο σύμβολο για τον παίκτη,
        αλλάζει τη σειρά (επόμενη κίνηση = επόμενος παίκτης)
        Συντεταγμένες (row, col) θέσης που επιλέχθηκε
        @param row: Γραμμή
        @param col: Στήλη
        """
        self.board.mark_square(row, col, self.player)
        self.draw_symbol(row, col)
        self.next_turn()

    def next_turn(self):
        """
            Εναλλαγή παικτών
        """
        self.player = self.player % 2 + 1

    def isover(self) -> bool:
        """
            @return: True / False αν έχουμε νικητή ή ισοπαλία (γεμάτο ταμπλό)
        """
        return self.board.check_for_winner() != 0 or self.board.isfull()

    # def reset(self):
    #     """
    #         "Μηδενίζει" το παιχνίδι
    #     """
    #     self.__init__(self)


def set_game_params() -> None:
    """
        Εμφανίζει την αρχική οθόνη όπου ορίζονται οι επιλογές του παιχνιδιού.
        Υπάρχει drop-down menu από όπου μπορούμε να διαβάσουμε τα αποτελέσματα των παιχνιδιών (ιστορικό)
        και να δούμε πληροφορίες για την εφαρμογή (ΘΕ, Τμήμα, Ομάδα Ανάπτυξης)
    """
    menu_def = [['&Επιλογές', ['Ιστορικό παιχνιδιών', 'Σχετικά', '---', 'Έξοδος']]]

    col1 = [[sg.Frame(
        layout=[[sg.Radio('Άνθρωπος-Άνθρωπος', "GAME_MODE", default=True, key='-HUMAN_HUMAN-', enable_events=True)],
                [sg.Radio('Άνθρωπος-Υπολογιστής', "GAME_MODE", key='-HUMAN_COMPUTER-', enable_events=True)],
                [sg.Radio('Υπολογιστής-Υπολογιστής', "GAME_MODE", key='-COMPUTER_COMPUTER-', enable_events=True)]],
        title='Τύπος Παιχνιδιού', size=(250, 120), vertical_alignment='c', key='-GAME_MODE_CHOICE-')]]
    col2 = [[sg.Text('Παίκτης 1 (Χ): ', pad=((5, 0), (10, 10)), key='-P1-'),
             sg.Input(size=(20, 1), pad=((0, 5), (10, 10)), key='-PLAYER1_NAME-')],
            [sg.Text('Παίκτης 2 (O): ', pad=((5, 0), (10, 10)), key='-P2-'),
             sg.Input(size=(20, 1), pad=((0, 5), (10, 10)), key='-PLAYER2_NAME-')]]
    col3 = [
        [sg.Frame(layout=[[sg.Radio('Αρχάριος', "COMPUTER_AI_LEVEL", default=True, key='-COMPUTER_LEVEL_SIMPLE-')],
                          [sg.Radio('Μέτριος', "COMPUTER_AI_LEVEL", key='-COMPUTER_LEVEL_AVERAGE-')],
                          [sg.Radio('Expert', "COMPUTER_AI_LEVEL", key='-COMPUTER_LEVEL_EXPERT-')]],
                  title='Ικανότητα Υπολογιστή', size=(250, 120), vertical_alignment='c',
                  key='-COMPUTER_AI_CHOICES-')]]
    layout = [[sg.Menu(menu_def, tearoff=False)],
              [sg.Text('Τρίλιζα - Επιλογές παιχνιδιού', font=('ANY', 14, 'bold'), pad=(5, 5))],
              [sg.Col(col1, pad=(5, 3), element_justification='c'),
               sg.Col(col2, pad=(5, 3), element_justification='c'),
               sg.Col(col3, pad=(5, 3), element_justification='c')],
              [sg.Button('ΕΝΑΡΞΗ', key="-STARTGAME-", pad=((1, 10), (10, 10))),
               sg.Button('ΕΞΟΔΟΣ', key='-EXITBUTTON-', pad=((1, 1), (10, 10)))]]

    init_window = sg.Window('.: Τρίλιζα :.', layout, finalize=True, element_justification='c', icon=GAME_ICON)

    # Διάβασμα επιλογών
    while True:
        event, values = init_window.read()
        # print(event, values)  # TOREMOVE: for debugging only
        if event in (sg.WIN_CLOSED, 'Έξοδος', '-EXITBUTTON-'):  # Επέλεξε τερματισμό παιχνιδιού
            sys.exit()
        if event == '-HUMAN_COMPUTER-':  # Ελέγχουμε τύπο παιχνιδιού
            init_window['-P1-'].update(visible=True)
            init_window['-PLAYER1_NAME-'].update(visible=True)
            init_window['-P2-'].update(visible=False)
            init_window['-PLAYER2_NAME-'].update(visible=False)
        elif event == '-COMPUTER_COMPUTER-':
            init_window['-P1-'].update(visible=False)
            init_window['-PLAYER1_NAME-'].update(visible=False)
            init_window['-P2-'].update(visible=False)
            init_window['-PLAYER2_NAME-'].update(visible=False)
        elif event == '-HUMAN_HUMAN-':
            init_window['-P1-'].update(visible=True)
            init_window['-PLAYER1_NAME-'].update(visible=True)
            init_window['-P2-'].update(visible=True)
            init_window['-PLAYER2_NAME-'].update(visible=True)
        elif event == 'Ιστορικό παιχνιδιών':  # Επέλεξε εμφάνιση Ιστορικού
            historical_data.show_historical_data()
        elif event == 'Σχετικά':  # Επέλεξε εμφάνιση πληροφοριών εφαρμογής
            init_window.disappear()
            show_about.show_about_text()
            init_window.reappear()
        elif event == '-STARTGAME-':  # Επέλεξε έναρξη παιχνιδιού
            set_vars(values)
            init_window.disappear()
            return


def mark_winner(window, board):
    if board.winner[0]:
        if board.winner[0] == 1:
            window.Element(board.winner[1]).update(image_filename=X_SYMBOL_GREEN)
            window.Element(board.winner[2]).update(image_filename=X_SYMBOL_GREEN)
            window.Element(board.winner[3]).update(image_filename=X_SYMBOL_GREEN)
        else:
            window.Element(board.winner[1]).update(image_filename=O_SYMBOL_GREEN)
            window.Element(board.winner[2]).update(image_filename=O_SYMBOL_GREEN)
            window.Element(board.winner[3]).update(image_filename=O_SYMBOL_GREEN)

    for row in range(3):
        for col in range(3):
            window.Element((row, col)).update(disabled=True)
    return


def update_stat(board: Board) -> None:
    """
    Ενημερώνει τις μεταβλητές στις οποίες κρατάμε το επιμέρους σκορ (Νίκες κάθε παίκτη, Ισοπαλίες).

    Ενημερώνει το ιστορικό αρχείο των παιχνιδιών, δημιουργώντας μία λίστα με τα στοιχεί του παιχνιδιού που τελείωσε,
    την οποία περνάει στη συνάρτηση write_game_history που καλείται από το module historical_data

    @param board: Δέχεται ως όρισμα αντικείμενο τύπου Board()
    @return: None
    """
    if board.isfull() and board.check_for_winner() == 0:  # ΙΣΟΠΑΛΙΑ
        winner = 'ΙΣΟΠΑΛΙΑ'
        mv.WINNER_PLAYER = 'Κανένας - ΙΣΟΠΑΛΙΑ !'
        mv.SCORE_DRAWS += 1
    elif board.check_for_winner() == 1:  # Νικητής ο παίκτης 1
        winner = mv.PLAYERS[1]
        mv.WINNER_PLAYER = winner
        mv.SCORE_P1 += 1
    else:
        winner = mv.PLAYERS[2]
        mv.WINNER_PLAYER = winner
        mv.SCORE_P2 += 1
    if mv.GAME_MODE == 'HH':
        game_type = 'Άνθρωπος - Άνθρωπος'
    elif mv.GAME_MODE == 'HC':
        game_type = 'Άνθρωπος - Υπολογιστής'
    else:
        game_type = 'Υπολογιστής - Υπολογιστής'
    game_data = [(datetime.now().strftime("%d/%m/%Y")), game_type, mv.COMPUTER_LEVEL, winner]
    historical_data.write_game_history(game_data)


def my_popup(title: str) -> tuple:
    """
    Συνάρτηση για τη δημιουργία ενός pop-up παραθύρου στο οποίο εμφανίζεται το αποτέλεσμα του παιχνιδιού
    και το επιμέρους σκορ.
    Δίνει τις επιλογές για Νέο Παιχνίδι ή Έξοδο.

    @param title: Ο τίτλος του παραθύρου
    @return: Tuple με το event του window, το window
    """
    popup_window = sg.Window(title,
                       [[sg.Text(f'Νικητής είναι: {mv.WINNER_PLAYER}', font=('ANY', 12, 'bold'), text_color='Yellow', pad=((0, 0), (10, 10)))],
                        [sg.Text('Αποτελέσματα παιχνιδιών', font=('ANY', 10, 'bold'), text_color='DarkBlue')],
                        [sg.Text(f'Νίκες {mv.PLAYERS[1]}: {mv.SCORE_P1}')],
                        [sg.Text(f'Νίκες {mv.PLAYERS[2]}: {mv.SCORE_P2}')],
                        [sg.Text(f'Ισοπαλίες: {mv.SCORE_DRAWS}')],
                        [sg.OK('Νέο παιχνίδι', key='-OK-', pad=((0, 5), (10, 10))), sg.Cancel('ΤΕΛΟΣ', key='-EXIT-', pad=((0, 5), (10, 10)))]
                        ], icon=GAME_ICON, modal=True)
    event, values = popup_window.read()
    return event, popup_window


def main():
    set_game_params()

    window = game_board()
    game = Game(window)
    board = game.board
    ai = game.ai

    while True:
        window.reappear()
        window.refresh()
        window['-CURRENT_PLAYER-'].update('Παίζει ο: ' + mv.PLAYERS[game.player])
        if mv.GAME_MODE == 'HH' or mv.GAME_MODE == 'HC' and game.player == 1: # and not mv.COMPUTER_PLAYS_FIRST:
            if mv.PLAYER_TYPE == 'H':   # Παίζει ο άνθρωπος
                event, values = window.read()
                # print(event, values)  # TOREMOVE: for debugging only
                if event == sg.WIN_CLOSED or event == '-EXIT-':
                    break
                if event == '-RESET-':  # Αρχικοποίηση παιχνιδιού
                    del game
                    del board
                    del ai
                    window.close()
                    window = game_board()
                    game = Game(window)
                    board = game.board
                    ai = game.ai
                    continue
                pos = event
                row = pos[0]
                col = pos[1]
                if board.empty_squares(row, col) and game.running:
                    game.make_move(row, col)
                    if game.isover():
                        game.running = False
                        mark_winner(window, board)
                        update_stat(board)  # Γράφουμε στο αρχείο τα στοιχεία του παιχνιδιού που τελείωσε
                        play_again = my_popup('Αποτελέσματα')
                        if play_again[0] == '-OK-':
                            play_again[1].close()
                            # Νέο παιχνίδι στη σειρά -> Εναλλαγή πρώτου παίκτη
                            mv.PLAY_FIRST = mv.PLAY_FIRST % 2 + 1
                            if mv.PLAY_FIRST == 2:  # Άλλαξε ο παίκτης που ξεκινάει σε υπολογιστής
                                mv.COMPUTER_PLAYS_FIRST = 1
                            del game
                            del board
                            del ai
                            window.close()
                            window = game_board()
                            game = Game(window)
                            board = game.board
                            ai = game.ai
                            continue
                        elif play_again[0] == '-EXIT-':
                            sys.exit()
        if (mv.GAME_MODE == 'HC' or mv.GAME_MODE == 'CC') and game.running:
            time.sleep(.5)   # Ένα μικρό delay 0.5 δευτερόλεπτα για να βλέπουμε τις κινήσεις του υπολογιστή.
            row, col = ai.eval(board)
            game.make_move(row, col)
            if mv.GAME_MODE == 'HH' or mv.GAME_MODE == 'HC':
                mv.PLAYER_TYPE = 'H'    # Έχει κάνει κίνηση ο υπολογιστής, αλλάζει η σειρά στον άνθρωπο
            if game.isover():
                game.running = False
                mark_winner(window, board)
                update_stat(board)
                play_again = my_popup('Αποτελέσματα')
                if play_again[0] == '-OK-':
                    play_again[1].close()
                    mv.PLAY_FIRST = mv.PLAY_FIRST % 2 + 1
                    if mv.PLAY_FIRST == 2:  # Άλλαξε ο παίκτης που ξεκινάει σε υπολογιστής
                        mv.COMPUTER_PLAYS_FIRST = 1
                    del game
                    del board
                    del ai
                    window.close()
                    window = game_board()
                    game = Game(window)
                    board = game.board
                    ai = game.ai
                    event, values = window.read()

                    if event == '-RESET-':
                        del game
                        del board
                        del ai
                        window.close()
                        window = game_board()
                        game = Game(window)
                        board = game.board
                        ai = game.ai
                        continue
                    elif event == '-EXIT-':
                        break
                elif play_again[0] == '-EXIT-':
                    sys.exit()
    window.close()
    sys.exit()


if __name__ == '__main__':
    main()
