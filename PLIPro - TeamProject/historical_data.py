import PySimpleGUI as sg
import csv
from my_vars import *


def show_historical_data() -> None:
    """
        Συνάρτηση που διαβάζει το αρχείο με τα ιστορικά στοιχεί των παιχνιδιών
        Εμφανίζει πίνακα τύπου grid με τα αποτελέσματα
    """
    headers = ['Ημερομηνία', 'Τύπος Παιχνιδιού', 'Επίπεδο Υπολογιστή', 'Νικητής']   # Επικεφαλίδες πίνακα
    historical_data = []

    #  Διαβάζουμε τα δεδομένα από τοα αρχείο CSV
    try:
        with open(GAME_HISTORY_FILE_NAME, 'r', encoding='UTF-8') as history_data_file:
            csv_reader = csv.reader(history_data_file)
            for row in csv_reader:
                historical_data.append(row)
    except FileNotFoundError:
        sg.popup_error('Δεν βρέθηκε αρχείο ιστορικών δεδομένων', grab_anywhere=True, modal=True, icon=GAME_ICON)
        return None

    # Δημιουργούμε το layout. Ένας πίνακας με 4 στήλες και ένα button για κλείσιμο του παραθύρου
    # Το παράθυρο με τα στοιχεία είναι modal (δεν μπορεί να "κρυφτεί").
    # Ο αριθμός γραμμών θα είναι 20 ή όσες οι γραμμές του αρχείου αν είναι λιγότερες από 20
    game_history_layout = [[sg.Table(values=historical_data, headings=headers, auto_size_columns=True,
                            num_rows=min(len(historical_data), 20), justification='left', key='-HISTORY-', tooltip='Ιστορικό παιχνιδιών')],
                            [sg.Button('Κλείσιμο', key='-CLOSE_HISTORY_DATA-')]]
    history_window = sg.Window('Ιστορικό Παιχνιδιών', game_history_layout, modal=True, icon=GAME_ICON)
    while True:
        event, values = history_window.read()
        if event in ('-CLOSE_HISTORY_DATA-', sg.WIN_CLOSED):
            history_window.close()
            break
    return None


def write_game_history(historical_data: list) -> None:
    """
        Συνάρτηση που ενημερώνει το αρχείο ιστορικών στοιχείων παιχνιδιών
        Καλείται μετά το τέλος κάθε παιχνιδιού.
        Κάθε γραμμή είναι της μορφής: "Ημερομηνία,Τύπος Παιχνιδιού,Επίπεδο Υπολογιστή (ή κενό),Νικητής"
    Args:
        historical_data (list): Λίστα με τα στοιχεία του παιχνιδιού που θα αποθηκευτούν ως μία γραμμή comma separated
    """
    try:
        with open(GAME_HISTORY_FILE_NAME, 'a', encoding='UTF8', newline="") as history_data_file:
            writer = csv.writer(history_data_file)
            writer.writerow(historical_data)
    except FileNotFoundError:
        sg.popup_error('Δεν βρέθηκε αρχείο ιστορικών δεδομένων', grab_anywhere=True, modal=True, icon=GAME_ICON)
    return None
