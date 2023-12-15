import os
from tkinter import Tk, ttk, Button, Entry, Label, Frame, messagebox, Checkbutton, StringVar
from custom_canvas import CustomCanvas

from globals import VALIDATION_PATH, TRAIN_PATH, MODELS_PATH, RED_COLOR, GREEN_COLOR
from new_model_window import NewModelWindow
from model_utils import ModelUtils

# init window
root = Tk()
root.title("Rozpoznawanie cyfr")
root.eval('tk::PlaceWindow . center')

s = ttk.Style(root)
print(s.theme_use("winnative"))

# init tabs frame
tab_frame = ttk.Notebook(root)
tab_frame.grid(row=0, column=0, columnspan=5, pady=10, padx=10, sticky="nswe")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# init tab collecting new data
def init_training_tab():
    train_tab = ttk.Frame(tab_frame)
    tab_frame.add(train_tab, text="Dodaj dane")

    # class name entry
    class_frame = Frame(train_tab)
    class_frame.grid(row=0, column=0, columnspan=4, pady=10, sticky="n")

    label = Label(class_frame, text="Cyfra (nazwa klasy):")
    label.grid(row=0, column=0, pady=10, padx=10)

    # validate class name input
    def validate_input(new_value):
        if new_value == '' or (new_value.isdigit() and 0 <= int(new_value) <= 9):
            return True
        else:
            return False

    input_entry = Entry(class_frame, width=2, validate="key", validatecommand=(root.register(validate_input), '%P'), justify="center")
    input_entry.grid(row=0, column=1, pady=10, padx=10)

    # canvas frame
    canvas_frame = Frame(train_tab)
    canvas_frame.config(cursor="pencil")
    canvas_frame.grid(row=1, column=0, columnspan=4, pady=10, padx=10)
    train_tab.rowconfigure(1, weight=1)
    train_tab.columnconfigure(1, weight=1)

    canvas = CustomCanvas(master=canvas_frame, width=64, height=64)
    canvas.grid(row=0, column=0)

    # image save path selection
    savePathVar = StringVar(value=TRAIN_PATH)
    save_as_train = Checkbutton(train_tab, text='Zapisz w zbiorze treningowym', 
                                variable=savePathVar, onvalue=TRAIN_PATH, offvalue=VALIDATION_PATH)
    save_as_train.grid(row=2, column=0, pady=10, padx=10, sticky="e")

    # option buttons frame
    button_frame = Frame(train_tab)
    button_frame.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="e")

    # open training config window
    def train_model():
        window = NewModelWindow()
        window.eval('tk::PlaceWindow . center')
        window.mainloop()

    reset_button = Button(button_frame, text="Wytrenuj", foreground="white", bg=GREEN_COLOR, command=train_model)
    reset_button.grid(row=0, column=0, padx=5)

    reset_button = Button(button_frame, text="Wyczyść", command=lambda:canvas.reset_canvas(canvas), foreground="white", bg=RED_COLOR)
    reset_button.grid(row=0, column=1, padx=5)

    # save image in the given path and class
    def save_image(image, imgClass, path):
        # verify class
        if imgClass.isdigit() and 0 <= int(imgClass) <= 9:
            index = 0
            # find first unused index
            while True:        
                file_name = f"{imgClass}{index}.png"
                file_path = os.path.join(f'{path}{imgClass}/', file_name)
                if not os.path.exists(file_path):
                    image.save(file_path)
                    break
                else:
                    index += 1
            canvas.reset_canvas(None)
        else:
            messagebox.showerror("Błąd", "Wprowadź poprawną klasę (cyfra 0-9) przed zapisaniem pliku.")

    save_button = Button(button_frame, text="Zapisz", command=lambda:save_image(canvas.toImage(), input_entry.get(), savePathVar.get()))
    save_button.grid(row=0, column=2, padx=5)

# init model selection frame
def init_model_selection(root, row):
    model_frame = Frame(root)
    model_frame.grid(row=row, column=0, columnspan=4, pady=10, padx=10, sticky="e")

    label = Label(model_frame, text="Wybierz model:")
    label.grid(row=0, column=0, padx=10, pady=10)

    selected_model_var = StringVar(model_frame)

    # craete dropdown menu
    models = [""]
    option_menu = ttk.OptionMenu(model_frame, selected_model_var, models[0], *models)
    option_menu.config(width=15)
    option_menu.grid(row=0, column=1, padx=10, pady=10)
    
    # reload model options
    def reload():
        models = [folder for folder in os.listdir(MODELS_PATH) if os.path.isdir(os.path.join(MODELS_PATH, folder))]
        def get_default_model():
            for m in models:
                if "default" in m:
                    return m
            return models[0]
        option_menu.set_menu(get_default_model(), *models)
        
    reload()
    # add reload button
    reset_button = Button(model_frame, text="↻", command=reload, foreground="white", bg=RED_COLOR)
    reset_button.grid(row=0, column=2, padx=2)

    return selected_model_var

# init tab predicting numbers
def init_testing_tab():
    test_tab = ttk.Frame(tab_frame)
    tab_frame.add(test_tab, text="Rozpoznaj cyfrę")
    
    prediction_var = StringVar(master=test_tab, value="")
    selected_model_var = init_model_selection(test_tab, row=0)

    # canvas frame
    canvas_frame = Frame(test_tab)
    canvas_frame.config(cursor="pencil")
    canvas_frame.grid(row=1, column=0, columnspan=4, pady=10, padx=10)
    test_tab.rowconfigure(0, weight=1)
    test_tab.columnconfigure(0, weight=1)

    canvas = CustomCanvas(master=canvas_frame, width=64, height=64)
    canvas.grid(row=0, column=0)

    prediction_label_text = "Predykcja: "
    prediction_label = Label(test_tab, text=prediction_label_text)
    prediction_label.grid(row=2, column=0, pady=10, padx=10)

    # option buttons frame
    button_frame = Frame(test_tab)
    button_frame.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="e")

    def clear():
        canvas.reset_canvas(canvas)
        prediction_label.config(text = prediction_label_text)

    reset_button = Button(button_frame, text="Wyczyść", command=clear, foreground="white", bg=RED_COLOR)
    reset_button.grid(row=0, column=1, padx=5)

    def predict_number():
        pred = ModelUtils.get_model_prediction(selected_model_var.get(), canvas.toImage())
        prediction_var.set(pred)
        prediction_label.config(text = f"{prediction_label_text}{prediction_var.get()}")

    save_button = Button(button_frame, text="Sprawdź", command=predict_number)
    save_button.grid(row=0, column=2, padx=5)

init_training_tab()
init_testing_tab()

root.mainloop()
