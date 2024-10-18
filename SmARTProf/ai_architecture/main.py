import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tensorflow as tf
from keras import layers, models
from keras.callbacks import Callback
from keras.callbacks import ModelCheckpoint


def pregatirea_imaginilor(image_path):
    image = Image.open(image_path).resize((50, 50)).convert("L")
    image_array = np.array(image)
    return image_array / 255.0


def incarca_imaginile(folder_path, label):
    images = []
    labels = []
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if os.path.isfile(image_path):
            images.append(pregatirea_imaginilor(image_path))
            labels.append(label)
    return images, labels


def incarca_datele():
    X = []
    y = []

    folder_paths = [f"class_{i}" for i in range(5)]

    for i, folder in enumerate(folder_paths):
        images, labels = incarca_imaginile(folder, i)
        for image_array in images:
            X.append(image_array)
            label_vector = np.zeros(5) #in functie de nr de clase
            label_vector[i] = 1
            y.append(label_vector)

    return np.array(X), np.array(y)


X, y = incarca_datele()
X_antrenare, X_test, y_antrenare, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_antrenare = X_antrenare.reshape(-1, 50, 50, 1)
X_test = X_test.reshape(-1, 50, 50, 1)

model = models.Sequential()

model = models.load_model('D:\ProiectRebelDOT\model//bestmodel.keras')

# model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(50, 50, 1)))
# model.add(layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
#
# model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
#
# model.add(layers.Conv2D(128, (3, 3), activation='relu'))
# model.add(layers.MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
#
# model.add(layers.Flatten())
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dense(5, activation='softmax')) #11 nr de clase = nr de neuroni output


learning_rate = 0.005
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

model.compile(optimizer=optimizer,
              loss='categorical_crossentropy',
              metrics=['accuracy'])


class RealTimePlot(Callback):
    def __init__(self):
        self.epoch_count = 0
        plt.ion()
        self.fig, (self.ax_loss, self.ax_acc) = plt.subplots(1, 2, figsize=(12, 5))
        self.ax_loss.set_title("Evoluția pierderii")
        self.ax_acc.set_title("Evoluția acurateții")
        self.loss_values = []
        self.val_loss_values = []
        self.acc_values = []
        self.val_acc_values = []

    def on_epoch_end(self, epoch, logs=None):
        self.epoch_count += 1
        self.loss_values.append(logs['loss'])
        self.val_loss_values.append(logs['val_loss'])
        self.acc_values.append(logs['accuracy'])
        self.val_acc_values.append(logs['val_accuracy'])

        self.ax_loss.clear()
        self.ax_acc.clear()

        self.ax_loss.plot(range(self.epoch_count), self.loss_values, label="Pierderea antrenamentului")
        self.ax_loss.plot(range(self.epoch_count), self.val_loss_values, label="Pierderea testării")
        self.ax_loss.set_title("Evoluția pierderii")
        self.ax_loss.legend()

        self.ax_acc.plot(range(self.epoch_count), self.acc_values, label="Acuratețea antrenamentului")
        self.ax_acc.plot(range(self.epoch_count), self.val_acc_values, label="Acuratețea testării")
        self.ax_acc.set_title("Evoluția acurateții")
        self.ax_acc.legend()

        plt.pause(0.1)


real_time_plot = RealTimePlot()
history = model.fit(X_antrenare, y_antrenare, epochs=50, batch_size=32, validation_data=(X_test, y_test),
                    callbacks=[real_time_plot])

test_loss, test_acc = model.evaluate(X_test, y_test)
print(f'Acuratețea pe setul de testare: {test_acc * 100:.2f}%')


def prezice_imagine(image_path):
    image_array = pregatirea_imaginilor(image_path)
    image_array = image_array.reshape(1, 50, 50, 1)
    predictie = model.predict(image_array)
    clasa_prezisa = np.argmax(predictie)
    return clasa_prezisa


image_path = "D:\ProiectRebelDOT\drawing.png"
clasa_prezisa = prezice_imagine(image_path)
print(f'Clasa prezisă pentru imaginea aleasă: {clasa_prezisa}')

image = Image.open(image_path)
plt.imshow(image, cmap='gray')
plt.title(f'Clasa prezisă: {clasa_prezisa}')
plt.show()

checkpoint = ModelCheckpoint('D:\ProiectRebelDOT\model//bestmodel.keras', save_best_only=True, monitor='val_loss', mode='min')

history = model.fit(X_antrenare, y_antrenare, epochs=50, batch_size=32, validation_data=(X_test, y_test),
                    callbacks=[real_time_plot, checkpoint])


#apple
#envelope
#eye
#parachute
#television
