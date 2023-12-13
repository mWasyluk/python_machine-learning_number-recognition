from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from paths import validation_dir, train_dir

batch_size = 30
model = load_model('number-recognition')

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

data_generator = ImageDataGenerator(rescale=1./255, validation_split=0.2)

test_generator = data_generator.flow_from_directory(
    validation_dir,
    target_size=(64, 64),
    batch_size=batch_size,
    class_mode='categorical',
)

test_loss, test_accuracy = model.evaluate(test_generator, steps=test_generator.samples // batch_size)

print(f'Test Loss: {test_loss}')
print(f'Test Accuracy: {test_accuracy}')