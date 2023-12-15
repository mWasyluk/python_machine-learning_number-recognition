from tkinter import Tk, Button, Entry, Label, Frame, messagebox
from model_utils import ModelUtils
from globals import GREEN_COLOR, RED_COLOR

class NewModelWindow(Tk):
    global width, height
    width, height = 64, 64

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.title("Nowy Model")

        class_frame = Frame(self)
        class_frame.grid(row=0, column=0, columnspan=4, pady=10, sticky="n")

        # model name entry
        name_label = Label(class_frame, text="Nazwa modelu:")
        name_label.grid(row=0, column=0, pady=10, padx=10)

        name_entry = Entry(class_frame, width=15, validate="key", justify="center")
        name_entry.grid(row=0, column=1, pady=10, padx=10)
        self.name_entry = name_entry

        # batch size entry
        batch_label = Label(class_frame, text="Ilość próbek (batch size):")
        batch_label.grid(row=1, column=0, pady=10, padx=10)

        batch_entry = Entry(class_frame, width=4, validate="key", justify="center")
        batch_entry.grid(row=1, column=1, pady=10, padx=10)
        self.batch_entry = batch_entry

        # model name entry
        epochs_label = Label(class_frame, text="Ilość powtórzeń (epochs):")
        epochs_label.grid(row=2, column=0, pady=10, padx=10)

        epochs_entry = Entry(class_frame, width=4, validate="key", justify="center")
        epochs_entry.grid(row=2, column=1, pady=10, padx=10)
        self.epochs_entry = epochs_entry
        
        # train button
        button_frame = Frame(class_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="e")

        reset_button = Button(button_frame, text="Wytrenuj", bg=GREEN_COLOR, fg="white", command=self.train_model)
        reset_button.grid(row=0, column=0, padx=5)

        reset_button = Button(button_frame, text="Anuluj", bg=RED_COLOR, fg="white", command=self.destroy)
        reset_button.grid(row=0, column=1, padx=5)

    # train new model with provided configs
    def train_model(self):
        name = self.name_entry.get()
        batch_size = self.batch_entry.get()
        epochs = self.epochs_entry.get()

        # validate configs
        if not name:
            messagebox.showerror("Błąd", "Nazwa nie może być pusta.")
            return
        
        if not batch_size.isdigit() or int(batch_size) <= 0 :
            messagebox.showerror("Błąd", "Ilość próbek musi być liczbą całkowitą wiekszą od 0.")
            return
        
        if not epochs.isdigit() or int(epochs) <= 0 :
            messagebox.showerror("Błąd", "Ilość powtórzeń musi być liczbą całkowitą wiekszą od 0.")
            return

        # close and train
        self.destroy()
        ModelUtils.train_new_model(name, int(batch_size), int(epochs))
