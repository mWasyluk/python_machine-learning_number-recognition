from keras.preprocessing import image
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import numpy as np
from globals import TRAIN_PATH, VALIDATION_PATH, MODELS_PATH
from progress_window import ProgressWindow
from tkinter import messagebox

class ModelUtils():

    # trains a new model with the given params and display a progress bar
    @staticmethod
    def train_new_model(model_name, batch_size, epochs):
        progress_bar = ProgressWindow(model_name)
        # init model
        model = Sequential()

        # CNN layers
        model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
        model.add(MaxPooling2D((3, 3)))
        
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D((3, 3)))

        model.add(Conv2D(128, (3, 3), activation='relu'))
        model.add(MaxPooling2D((3, 3)))
        
        model.add(Flatten())

        progress_bar.update(5)

        # dense layers
        model.add(Dense(128, activation='relu'))
        model.add(Dense(10, activation='softmax'))

        # model.add(Dropout(0.5))

        optimizer = Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=['accuracy'])

        progress_bar.update(10)

        # init data generators for both data types
        train_data_generator = image.ImageDataGenerator(rescale=1./255)
        validation_data_generator = image.ImageDataGenerator(rescale=1./255)

        # load training data
        train_generator = train_data_generator.flow_from_directory(
            TRAIN_PATH,
            target_size=(64, 64),
            batch_size=batch_size,
            class_mode='binary',
        )

        progress_bar.update(20)

        # load validation data
        validation_generator = validation_data_generator.flow_from_directory(
            VALIDATION_PATH,
            target_size=(64, 64),
            batch_size=batch_size,
            class_mode='binary',
        )

        progress_bar.update(30)

        early_stopping_callback = EarlyStopping(
            monitor='val_accuracy',
            patience=epochs*0.33,  
            restore_best_weights=True
        )

        # model learning
        model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // batch_size + 1,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=validation_generator.samples // batch_size + 1,
            callbacks=[early_stopping_callback] 
        )
        
        progress_bar.update(90)

        # save the model
        path = f"{MODELS_PATH}{model_name}"
        model.save(path)

        test_loss, test_accuracy = ModelUtils.test_model_parameters(model_name, batch_size)

        progress_bar.update(99)

        # show result and ask if retrain model
        needs_retrain = messagebox.askyesno(f"Wynik modelu {model_name}", 
                                                f"Model pomyślnie ukończył trening. Wynik testu:\n"\
                                                f"  > Strata walidacyjna: {'{:.2f}'.format(test_loss)};\n"\
                                                f"  > Dokładność walidacyjna: {'{:.2f}%'.format(test_accuracy*100)}\n"\
                                                "Czy chcesz powtórzyć trening?"
        )
        
        progress_bar.update(100)
        
        if needs_retrain:
            ModelUtils.train_new_model(model_name, batch_size, epochs)
    
    # returns model by name
    @staticmethod
    def load_model(model_name):
        model = load_model(f"{MODELS_PATH}{model_name}")
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    # returns model loss and accuracy by name
    @staticmethod
    def test_model_parameters(model_name, batch_size):
        model = ModelUtils.load_model(model_name)

        data_generator = image.ImageDataGenerator(rescale=1./255)
        test_generator = data_generator.flow_from_directory(
            VALIDATION_PATH,
            target_size=(64, 64),
            batch_size=batch_size,
            class_mode='categorical',
        )

        test_loss, test_accuracy = model.evaluate(
            test_generator, 
            steps=test_generator.samples // batch_size + 1
        )
        return test_loss, test_accuracy
    
    # predict number on the given image
    @staticmethod
    def get_model_prediction(model_name, img):
        # provide the model
        try:
            model = ModelUtils.load_model(model_name)
        except OSError as e:
            messagebox.showerror("Błąd", f"Nie odnaleziono modelu {model_name}")
            return
        
        # prepare an image array
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0 

        # predict number on the image
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        
        # display result
        return predicted_class
    