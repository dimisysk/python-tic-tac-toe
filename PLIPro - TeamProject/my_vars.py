import os

# "ΣΤΑΘΕΡΕΣ"

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

# Εικόνες με σύμβολα τρίλιζας (Χ και Ο). Με πράσινο φόντο όταν συμπληρώνεται τρίλιζα
GAME_HISTORY_FILE_NAME = CURRENT_DIR + '\\game_history.csv'  # Αρχείο ιστορικότητας παιχνιδιών (.CSV format / UTF- Encoding)
GAME_ICON = CURRENT_DIR + '\\images\\tic-tac-toe.ico'
X_SYMBOL = CURRENT_DIR + '\\images\\X1.png'
X_SYMBOL_GREEN = CURRENT_DIR + '\\images\\X1_Green.png'
O_SYMBOL = CURRENT_DIR + '\\images\\O1.png'
O_SYMBOL_GREEN = CURRENT_DIR + '\\images\\O1_Green.png'
LOGO = CURRENT_DIR + '\\images\\Logo.png'

AI_PLAYER_SIMPLE = 'Simple Player'
AI_PLAYER_AVG = 'Average Player'
AI_PLAYER_EXPERT = 'Expert Player'

PLAY_FIRST = 1              # Αρχή παιχνιδιού - Πρώτος παίζει ο παίκτης 1
PLAYER_TYPE = 'H'           # Αρχή παιχνιδιού - Πρώτος παίκτης είναι άνθρωπος
COMPUTER_PLAYS_FIRST = 0     # Αν πρέπει να ξεκινήσει πρώτος ο υπολογιστής = 1

# Shared μεταβλητές
PLAYER_1_NAME = ''      # Όνομα παίκτη 1 ή default τιμή
PLAYER_2_NAME = ''      # Όνομα παίκτη 2 ή default τιμή
GAME_MODE = ''          # Τύπος παιχνιδιού (κωδικοποιημένο HH, HC, CC)
COMPUTER_LEVEL = ''     # Επίπεδο ικανότητας υπολογιστή
PLAYERS = []            # Λίστα με τα ονόματα των παικτών που δόθηκαν ή default τιμές
CURRENT_PLAYER = ''     # Κρατάμε τον τρέχοντα παίκτη (όνομα)
GAME_MODE_TEXT = ''     # Λεκτικό για τον τύπο παιχνιδιού

# Σκορ για κάθε κύκλο παιχνιδιών
WINNER_PLAYER = ''
SCORE_P1 = 0  # Σκορ παίκτη 1
SCORE_P2 = 0  # Σκορ παίκτη 2
SCORE_DRAWS = 0  # Ισοπαλίες


def set_vars(my_vars: dict):
    """
        Συνάρτηση που αποθηκεύει τις παραμέτρους του παιχνιδιού που ορίσαμε στην αρχική οθόνη.
    Args:
        my_vars (dict): Λεξικό με values που επιστρέφει η μέθοδος window.read()
    """
    global PLAYER_1_NAME, PLAYER_2_NAME, GAME_MODE, COMPUTER_LEVEL
    global PLAYER_TYPE, GAME_MODE_TEXT, COMPUTER_PLAYS_FIRST, PLAYERS

    PLAYER_1_NAME = 'Παίκτης 1 (X)'  # Όνομα 1ου παίκτη. Default τιμή αν δεν καταχωρηθεί όνομα
    PLAYER_2_NAME = 'Παίκτης 2 (O)'  # Όνομα 2ου παίκτη. Default τιμή αν δεν καταχωρηθεί όνομα
    GAME_MODE = 'HH'  # Τύπος παιχνιδιού : ΗΗ=Άνθρωπος-Άνθρωπος, HC=Άνθρωπος-Υπολογιστής, CC=Υπολογιστής-Υπολογιστής
    COMPUTER_LEVEL = ''  # Επίπεδο ικανότητας Υπολογιστή (Αυτοματοποιημένος παίκτης)

    if my_vars['-HUMAN_HUMAN-']:
        GAME_MODE_TEXT = 'Άνθρωπος vs Άνθρωπος'
        if my_vars['-PLAYER1_NAME-'] != '':
            PLAYER_1_NAME = my_vars['-PLAYER1_NAME-'] + ' (X)'
        if my_vars['-PLAYER2_NAME-'] != '':
            PLAYER_2_NAME = my_vars['-PLAYER2_NAME-'] + ' (O)'
    elif my_vars['-HUMAN_COMPUTER-']:
        GAME_MODE_TEXT = 'Άνθρωπος vs Υπολογιστή'
        GAME_MODE = 'HC'
        PLAYER_2_NAME = 'Υπολογιστής (O)'
        if my_vars['-PLAYER1_NAME-'] != '':
            PLAYER_1_NAME = my_vars['-PLAYER1_NAME-'] + ' (X)'
    elif my_vars['-COMPUTER_COMPUTER-']:
        GAME_MODE_TEXT = 'Υπολογιστής vs Υπολογιστή'
        GAME_MODE = 'CC'
        PLAYER_1_NAME = 'Υπολογιστής 1 (X)'
        PLAYER_2_NAME = 'Υπολογιστής 2 (O)'
        PLAYER_TYPE = 'C'
        COMPUTER_PLAYS_FIRST = 1

    if my_vars['-HUMAN_COMPUTER-'] or my_vars['-COMPUTER_COMPUTER-']:
        if my_vars['-COMPUTER_LEVEL_SIMPLE-']:
            COMPUTER_LEVEL = AI_PLAYER_SIMPLE
        elif my_vars['-COMPUTER_LEVEL_AVERAGE-']:
            COMPUTER_LEVEL = AI_PLAYER_AVG
        else:
            COMPUTER_LEVEL = AI_PLAYER_EXPERT

    PLAYERS = ['', PLAYER_1_NAME, PLAYER_2_NAME]
    return
