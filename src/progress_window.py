from tkinter import Tk, ttk, Label

class ProgressWindow():
    def __init__(self, model_name):
        root = Tk()
        root.title(f"Model {model_name}")
        root.eval('tk::PlaceWindow . center')
        self.root = root

        progress_label = Label(root, text=f"Postęp tworzenia modelu \"{model_name}\"")
        progress_label.grid(row=0, column=0, pady=10, padx=10, sticky="s")
        
        progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", maximum=100, value=0, length=300)
        progress_bar.grid(row=1, column=0, pady=10, padx=10, sticky="we")
        self.progress_bar = progress_bar

    def update(self, new_val):
        self.progress_bar['value'] = new_val
        self.progress_bar.update()
        if self.progress_bar['value'] >= 100:
            self.root.destroy()
    