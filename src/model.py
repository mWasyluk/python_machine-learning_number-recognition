from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from paths import train_dir, validation_dir
from tensorflow.keras.layers import Dropout

batch_size = 20
epochs = 50

# init model
model = Sequential()

# CNN layers
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))

model.add(Flatten())

# dense layers
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.add(Dropout(0.5))

model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=['accuracy'])


# init data generators for both data types
train_data_generator = ImageDataGenerator(rescale=1./255, validation_split=0.2)
validation_data_generator = ImageDataGenerator(rescale=1./255, validation_split=0.2)

# load training data
train_generator = train_data_generator.flow_from_directory(
    train_dir,
    target_size=(64, 64),
    batch_size=batch_size,
    class_mode='binary',
)

# load validation data
validation_generator = validation_data_generator.flow_from_directory(
    validation_dir,
    target_size=(64, 64),
    batch_size=batch_size,
    class_mode='binary',
)

# model learning
model.fit(
   train_generator,
   steps_per_epoch=train_generator.samples // batch_size,
   epochs=epochs,
   validation_data=validation_generator,
   validation_steps=validation_generator.samples // batch_size,
)

# save the model
model.save('number-recognition')