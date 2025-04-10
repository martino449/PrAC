import pickle
from uuid import uuid4
from datetime import datetime
from tkinter import simpledialog
import tkinter as tk
from tkinter import ttk
from sys import exit
from typing import NoReturn
import csv
RUNNING_MODE = "debug"
root = tk.Tk()
class Document:
    def __init__(self, title, posizione, keywords=None, id=None) -> NoReturn:
        self.id = generate_id()
        self.title = title
        self.posizione = posizione
        self.created_at = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        self.keywords = keywords or [title]  # Aggiunge il titolo tra le parole chiave se non specificato
        documents[self.id] = self  # Usa l'ID come chiave nel dizionario

    def __repr__(self) -> str:
        return f"""Documento:
            Titolo:    \t{self.title},
            Posizione: \t{self.posizione},
            ID:        \t{self.id},
            Aggiunto al sistema il:  \t{self.created_at}
            Ultima modifica il:      \t{self.updated_at}  \n"""
    
    def update(self, title, posizione, keywords):
        self.title = title
        self.posizione = posizione
        self.updated_at = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        self.keywords = keywords
# Dizionario che conterrà i documenti
documents = {str:Document} #Formato ID:Document
def debug_crash_decorator(func) -> any:
    """
    Decorator that wraps a function to handle exceptions.

    If an exception occurs during the execution of the wrapped function,
    it handles the error based on the current mode. In debug mode, the 
    application will exit with an error message. In other modes, it will 
    display the error in a message box.

    Parameters
    ----------
    func : function
        The function to be wrapped by the decorator.

    Returns
    -------
    function
        The wrapped function.
    """

    def wrapper(*args, **kwargs):
        try:
            print(f"Funzione eseguita: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            if RUNNING_MODE == "debug":  # Se siamo in modalità debug
                exit(f"Errore in modalità debug: {str(e)}")  # Manda il programma in crash
            else:
                BOX(f"Errore: {str(e)}")  # Altrimenti stampa l'errore
    return wrapper

def BOX(text) -> NoReturn:
    """
    Shows a message box with the given text.

    Parameters
    ----------
    text : str
        The text to be shown in the message box.

    Returns
    -------
    NoReturn
    """
    
    tk.messagebox.showinfo("PrAC info", text)

@debug_crash_decorator
def OUT(text) -> NoReturn:
    """
    Shows a message box with the given text.
    The text can be selected and copied.

    Parameters
    ----------
    text : str
        The text to be shown in the message box.

    Returns
    -------
    NoReturn
    """
    global root
    # Crea una finestra secondaria (Toplevel) sopra la root esistente
    top_window = tk.Toplevel(root)
    top_window.title("PrAC info")
    
    # Imposta la finestra secondaria come "always on top"
    top_window.attributes("-topmost", True)
    
    # Crea un widget Text (non modificabile)
    text_widget = tk.Text(top_window, height=35, width=50, wrap=tk.WORD)
    text_widget.insert(tk.END, text)
    
    # Rendi il widget Text non modificabile
    text_widget.config(state=tk.DISABLED)
    
    # Posiziona il widget nella finestra
    text_widget.pack(padx=10, pady=10)
    
    # Aggiungi un pulsante per chiudere la finestra
    close_button = tk.Button(top_window, text="Chiudi", command=top_window.destroy)
    close_button.pack(pady=10)

@debug_crash_decorator
def gui_entry(prompt="Inserisci un valore:") -> None | str:    
    """
    Richiede all'utente di inserire un valore tramite finestra di dialogo.
    
    Parameters
    ----------
    prompt : str, optional
        Il testo che verrà mostrato all'utente all'interno della finestra di dialogo.
        Se non specificato, viene usato il valore di default "Inserisci un valore:".
    
    Returns
    -------
    None | str
        Il valore inserito dall'utente. Se l'utente annulla la richiesta, viene restituito None.
    """

    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale
    risposta = simpledialog.askstring("gui_entry", prompt)
    return risposta




# Funzione per generare un ID unico
def generate_id() -> str:
    return str(uuid4())



# Funzione per trovare un documento tramite ID
@debug_crash_decorator
def find_by_id(document_id):
    assert document_id is not None, "ID non valido"
    assert document_id in documents, "Documento non trovato"
    return documents.get(document_id)

# Funzione per trovare documenti tramite parola chiave
@debug_crash_decorator
def find_by_key(keyword) -> list:
    assert keyword is not None, "parola chiave non valida"
    if keyword == "":
        return [document 
                for document in documents.values()]
    found_docs = []
    for document in documents.values():
        if keyword in document.keywords:
            found_docs.append(document)
    return found_docs


@debug_crash_decorator
def find_by_position(position) -> list:
    assert position is not None, "posizione non valida"
    found_docs = []
    for document in documents.values():
        if document.posizione == position:
            found_docs.append(document)
    return found_docs




# Funzione per salvare i documenti su file
@debug_crash_decorator
def save_documents(filename='documents.pkl') -> NoReturn:
    with open(filename, 'wb') as f:
        pickle.dump(documents, f)
    print(f"Documenti salvati nel file {filename}")

# Funzione per caricare i documenti da file
@debug_crash_decorator
def load_documents(filename='documents.pkl') -> NoReturn:
    global documents
    try:
        with open(filename, 'rb') as f:
            documents = pickle.load(f)
        print(f"Documenti caricati da {filename}")
    except FileNotFoundError:
        print("Nessun file trovato, inizializzando nuovi documenti.")
        documents = {}


@debug_crash_decorator
def add_document() -> Document:
    title = gui_entry("Inserisci il titolo del documento: ")
    posizione = gui_entry("Inserisci la posizione del documento: ")
    keywords = gui_entry("Inserisci le parole chiave del documento (separa con virgole): ").split(",")
    assert title is not None or title != "", "Titolo non valido"
    assert posizione is not None or posizione != "", "Posizione non valida"
    assert keywords is not None or keywords != "", "Parole chiave non valide"
    new_document = Document(title, posizione, keywords)
    OUT(f"Documento aggiunto: {new_document}")
    return new_document

@debug_crash_decorator
def update_document() -> Document:
    document_id = gui_entry("Inserisci l'ID del documento da aggiornare: ")
    document = find_by_id(document_id)
    assert document is not None, "Documento non trovato"
    title = gui_entry("Inserisci il nuovo titolo del documento: ")
    posizione = gui_entry("Inserisci la nuova posizione del documento: ")
    keywords = gui_entry("Inserisci le nuove parole chiave del documento (separa con virgole): ").split(",")
    assert title is not None or title != "", "Titolo non valido"
    assert posizione is not None or posizione != "", "Posizione non valida"
    document.update(title, posizione, keywords)
    OUT(f"Documento aggiornato: {document}")
    return document

def gui_find_by_position() -> NoReturn:
    position = gui_entry("Inserisci la posizione del documento da cercare: ")
    found_docs = find_by_position(position)
    OUT(f"Documenti trovati: {found_docs}")

@debug_crash_decorator
def delete_document() -> NoReturn:
    document_id = gui_entry("Inserisci l'ID del documento da eliminare: ")
    document = find_by_id(document_id)
    assert document is not None, "Documento non trovato"
    del documents[document_id]
    save_documents()
    OUT(f"Documento eliminato: {document}")

@debug_crash_decorator
def find_key_gui() -> NoReturn:
    keyword = gui_entry("Inserisci la parola chiave da cercare: ")
    OUT(f"Documenti trovati: {find_by_key(keyword)}") if keyword else OUT("alcun documento trovato")

@debug_crash_decorator
def find_id_gui() -> NoReturn:
    document_id = gui_entry("Inserisci l'ID del documento da cercare: ")
    OUT(f"Documento trovato: {find_by_id(document_id)}") if document_id else OUT("Documento non trovato")


@debug_crash_decorator
def export_documents_to_csv(filename='documents.csv') -> NoReturn:
    assert filename is not None or filename != "", "Nome del file non valido"
    assert filename.endswith('.csv'), "Il file deve essere un CSV"
    assert documents is not None or documents != {}, "Nessun documento presente nel catalogo"
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Intestazioni CSV
        writer.writerow(['ID', 'Titolo', 'Posizione', 'Creato il', 'Ultima modifica', 'Parole chiave'])
        for doc in documents.values():
            writer.writerow([
                doc.id,
                doc.title,
                doc.posizione,
                doc.created_at,
                doc.updated_at,
                ";".join(doc.keywords)  # parole chiave separate da ;
            ])
    
    BOX(f"Documenti esportati con successo in '{filename}'.")

def main() -> NoReturn:

    global root
    global RUNNING_MODE

    print("Benvenuto in PrAC!")

    def on_closing() -> NoReturn:
        save_documents()  # Salva i documenti prima di chiudere
        if RUNNING_MODE == "debug":
            BOX("Chiusura dell'applicazione")
        root.quit()  # Chiude l'applicazione

    commands = {
            "Crea nuovo documento": add_document,
            "Modifica documento": update_document,
            "Cancella documento": delete_document,
            "Trova documento per ID": lambda: OUT(f"Documento trovato: {find_by_id(gui_entry('Inserisci l\'ID del documento: '))}"),
            "Trova documenti per parola chiave": lambda: OUT(f"Documenti trovati: {find_by_key(gui_entry('Inserisci la parola chiave: '))}"),
            "Salva catalogo": lambda: save_documents(),
            "Carica catalogo": lambda: load_documents(),
            "trova con id": find_id_gui,
            "ricerca con parola chiave": find_key_gui,
            "Esporta documenti in csv": lambda: export_documents_to_csv(gui_entry("Inserisci il nome del file CSV: ")),
            "trova con posizione": gui_find_by_position,
        }



    # Funzione generica per l'esecuzione di comandi
    @debug_crash_decorator
    def execute_command(cmd) -> NoReturn:
        assert cmd in commands, f"Comando '{cmd}' non riconosciuto"
        commands[cmd]()



    # Creazione della finestra principale

    root.title("PrAC")
    root.geometry("800x600")
    root.configure(bg="#592b3d")

    # Collega l'evento di chiusura con la funzione on_closing
    root.protocol("WM_DELETE_WINDOW", on_closing)


    # Dati delle sezioni e comandi (può essere facilmente esteso)
    sections = {
        "Gestione documenti": ["Crea nuovo documento", "Modifica documento", "Cancella documento"],
        "Ricerca documenti": ["ricerca con parola chiave", "trova con id", "trova con posizione"],
        "Gestione sistema": ["Salva catalogo", "Carica catalogo", "Esporta documenti in csv"],
    }

    # Frame principale
    main_frame = tk.Frame(root, bg="#2c3e50")
    main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    style = ttk.Style()
    style.configure("TButton", 
                    font=("Courier", 11, "bold"),  # Aumenta la dimensione del font
                    padding=6,                   # Aggiunge più spazio attorno al testo
                    foreground="black",           # Colore del testo
                    background="#2c3e50",         # Colore di sfondo
                    relief="flat")                # Elimina il bordo per un aspetto più pulito

    for section, cmds in sections.items():
        section_frame = tk.LabelFrame(main_frame, text=section, bg="#2c3e50", fg="white", font=("Ariel", 12, "bold"), padx=20, pady=20)
        section_frame.pack(fill=tk.X, pady=15)

        # Crea i pulsanti per ogni comando nella sezione
        for i, cmd in enumerate(cmds):
            button = ttk.Button(section_frame, text=cmd, command=lambda cmd=cmd: execute_command(cmd), style="TButton")
            
            # Impostazione per una griglia che permetta ai bottoni di adattarsi
            button.grid(row=i // 4, column=i % 4, padx=15, pady=15, sticky="nsew")

            # Rendi le righe e le colonne della griglia espandibili
            section_frame.grid_columnconfigure(i % 4, weight=1)
            section_frame.grid_rowconfigure(i // 4, weight=1)

    # Avvio dell'interfaccia grafica
    root.mainloop()


if __name__ == "__main__":
    load_documents()
    main()

