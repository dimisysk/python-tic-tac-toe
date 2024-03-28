import PySimpleGUI as sg
import my_vars as mv


def show_about_text() -> None:
    """
        Εμφανίζει πληροφορίες για την εφαρμογή
    """
    about_text = " - ΜΑΥΡΕΛΟΥ ΕΥΓΕΝΙΑ\n"
    about_text += " - ΣΥΣΚΑΚΗΣ ΔΗΜΗΤΡΙΟΣ\n"
    about_text += " - ΚΑΡΑΤΖΑΣ ΔΗΜΗΤΡΙΟΣ\n"
    about_text += " - ΜΑΡΟΥΣΟΣ ΔΗΜΟΣΘΕΝΗΣ\n"
    about_text += " - ΤΑΧΛΙΑΜΠΟΥΡΗΣ ΣΤΑΜΑΤΙΟΣ\n"

    splash_window = sg.Window('Σχετικά',
                       [[sg.Text('ΘΕ: ΠΛΗΠΡΟ - ΤΜΗΜΑ: ΗΛΕ-54', font=('ANY', 12, 'bold'), text_color='Black',
                                 background_color='White', pad=((0, 0), (10, 10)))],
                        [sg.Text('Ομαδικό Προγραμματιστικό Project (Project ID: 04)', font=('ANY', 10, 'bold'), text_color='Black',
                         background_color='White', pad=((0, 0), (0, 10)))],
                        [sg.Text('Τίτλος Project: Ανάπτυξη παιχνιδιού Τρίλιζα', background_color='White', text_color='Black')],
                        [sg.Text('Ομάδα Εργασίας 2',background_color='White', text_color='Black')],
                        [sg.Text(about_text, pad=((20, 0), (0, 0)), background_color='White', text_color='Black')],
                        [sg.Image(filename=mv.LOGO, pad=((0, 0), (20, 20)))],
                        [sg.OK('  OK  ', key='-OK-', pad=((0, 5), (10, 10)), button_color=('black', 'white'))]
                        ], icon=mv.GAME_ICON, modal=True, background_color='White', element_justification='c')
    event, values = splash_window.read()
    splash_window.close()
    return
