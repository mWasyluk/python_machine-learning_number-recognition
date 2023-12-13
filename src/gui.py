import os
from tkinter import Tk, ttk, Button, Entry, Label, Frame, messagebox, Checkbutton, StringVar
from paths import validation_dir, train_dir
from canvas import CustomCanvas
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import load_model

# validate class name input
def validate_input(new_value):
    if new_value == '' or (new_value.isdigit() and 0 <= int(new_value) <= 9):
        return True
    else:
        return False

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
    else:
        messagebox.showerror("Błąd", "Wprowadź poprawną klasę (cyfra 0-9) przed zapisaniem pliku.")


# predict number on the given image
def predict(img):
    # provide the model
    model = load_model('number-recognition')
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # prepare an image array
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0 

    # predict number on the image
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    
    # display result
    messagebox.showinfo("Wynik", f"Obrazek przedstawia cyfrę {predicted_class}" )


# init window
root = Tk()
root.title("Rozpoznawanie cyfr")
root.eval('tk::PlaceWindow . center')

# init tabs frame
tab_frame = ttk.Notebook(root)
tab_frame.grid(row=0, column=0, columnspan=5, pady=10, padx=10, sticky="nswe")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# init tab collecting new data
def init_training_tab():
    train_tab = ttk.Frame(tab_frame)
    tab_frame.add(train_tab, text="Dodaj dane treningowe")

    # class name entry
    class_frame = Frame(train_tab)
    class_frame.grid(row=0, column=0, columnspan=4, pady=10, sticky="n")

    label = Label(class_frame, text="Cyfra (nazwa klasy):")
    label.grid(row=0, column=0, pady=10, padx=10)

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
    savePathVar = StringVar(value=train_dir)
    save_as_train = Checkbutton(train_tab, text='Zapisz w zbiorze treningowym', 
                                variable=savePathVar, onvalue=train_dir, offvalue=validation_dir)
    save_as_train.grid(row=2, column=0, pady=10, padx=10, sticky="e")

    # option buttons frame
    button_frame = Frame(train_tab)
    button_frame.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="e")

    reset_button = Button(button_frame, text="Wyczyść", command=lambda:canvas.reset_canvas(canvas))
    reset_button.grid(row=0, column=1, padx=5)

    # save image and clear canvas
    def save():
        save_image(canvas.toImage(), input_entry.get(), savePathVar.get())
        canvas.reset_canvas(None)

    save_button = Button(button_frame, text="Zapisz", command=save)
    save_button.grid(row=0, column=2, padx=5)

# init tab predicting numbers
def init_testing_tab():
    test_tab = ttk.Frame(tab_frame)
    tab_frame.add(test_tab, text="Rozpoznaj cyfrę")
    

    # canvas frame
    canvas_frame = Frame(test_tab)
    canvas_frame.config(cursor="pencil")
    canvas_frame.grid(row=0, column=0, columnspan=4, pady=10, padx=10)
    test_tab.rowconfigure(0, weight=1)
    test_tab.columnconfigure(0, weight=1)

    canvas = CustomCanvas(master=canvas_frame, width=64, height=64)
    canvas.grid(row=0, column=0)

    # option buttons frame
    button_frame = Frame(test_tab)
    button_frame.grid(row=1, column=0, columnspan=4, pady=10, padx=10, sticky="e")

    reset_button = Button(button_frame, text="Wyczyść", command=lambda:canvas.reset_canvas(canvas))
    reset_button.grid(row=0, column=1, padx=5)

    save_button = Button(button_frame, text="Sprawdź", command=lambda:predict(canvas.toImage()))
    save_button.grid(row=0, column=2, padx=5)

init_training_tab()
init_testing_tab()

root.mainloop()