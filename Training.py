import sys
import os

import keras
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras import layers
from keras import models
from keras import callbacks
from keras.applications import InceptionResNetV2
from keras import optimizers
from keras.callbacks import EarlyStopping, ReduceLROnPlateau

from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import time
import random
import gc   #Gabage collector for cleaning deleted data from memory

#Import some packages to use
import cv2
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import ticker
import seaborn as sns

from pathlib import Path
#Lets take a look at our directory
import shutil
import matplotlib.pyplot as plt

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#print(os.listdir("../input"))

start = time.time()

train_data_path = Path('./data/train')
validation_data_path = './data/test'

"""
Parameters
"""
# img_width, img_height = 300, 300
img_width, img_height = 150, 150
# img_width, img_height = 640, 960
epochs = 20
# epochs = 40
batch_size = 32
samples_per_epoch = 1000
validation_steps = 300
nb_filters1 = 32
nb_filters2 = 64
conv1_size = 3
conv2_size = 2
pool_size = 2
classes_num = 2
lr = 0.0002

# conv_base = InceptionResNetV2(weights='imagenet', include_top=False, input_shape=(150,150,3))
# conv_base.summary()
prior = keras.applications.VGG16(
    include_top=False, 
    weights='imagenet',
    input_shape=(150, 150, 3)
)
prior.summary()

model = models.Sequential()
# model.add(conv_base)
model.add(prior)
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.1, name='Dropout_Regularization'))
model.add(layers.Dense(classes_num, activation='sigmoid'))  #Sigmoid function at the end because we have just two classes


#Lets see our model
model.summary()


# Freeze the VGG16 model, e.g. do not train any of its weights.
# We will just use it as-is.
for cnn_block_layer in model.layers[0].layers:
    cnn_block_layer.trainable = False
model.layers[0].trainable = False



model.compile(loss='categorical_crossentropy', optimizer=optimizers.RMSprop(lr=2e-5), metrics=['acc'])

##model = Sequential()
##model.add(Convolution2D(nb_filters1, conv1_size, conv1_size, border_mode ="same", input_shape=(img_width, img_height, 3)))
##model.add(Activation("relu"))
##model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))
##
##model.add(Convolution2D(nb_filters2, conv2_size, conv2_size, border_mode ="same"))
##model.add(Activation("relu"))
##model.add(MaxPooling2D(pool_size=(pool_size, pool_size), dim_ordering='th'))
##
##model.add(Flatten())
##model.add(Dense(256))
##model.add(Activation("relu"))
##model.add(Dropout(0.5))
##model.add(Dense(classes_num, activation='softmax'))
##
##model.compile(loss='categorical_crossentropy',
##              optimizer=optimizers.RMSprop(lr=lr),
##              metrics=['accuracy'])

train_datagen = ImageDataGenerator(
    rescale=1. / 255, #Scale the image between 0 and 1
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

## Validation data
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

"""
Tensorboard log
"""
log_dir = Path('./tf-log/')
tb_cb = callbacks.TensorBoard(log_dir=log_dir, histogram_freq=0)
cbks = [tb_cb]

model.fit_generator(
    train_generator,
    samples_per_epoch=samples_per_epoch,
    epochs=epochs,
    validation_data=validation_generator,
    # callbacks=cbks,
    validation_steps=validation_steps,
    callbacks=[
        EarlyStopping(patience=3, restore_best_weights=True),
        ReduceLROnPlateau(patience=2)
    ])

target_dir = Path('./models/')
if not os.path.exists(target_dir):
  os.mkdir(target_dir)
model.save(Path('./models/model.h5'))
model.save_weights(Path('./models/weights.h5'))


#Confution Matrix and Classification Report
# num_of_test_samples = 48
num_of_test_samples = 112
Y_pred = model.predict_generator(validation_generator, num_of_test_samples // batch_size+1)
y_pred = np.argmax(Y_pred, axis=1)
print('Confusion Matrix')
print(confusion_matrix(validation_generator.classes, y_pred))
print('Classification Report')
print(classification_report(validation_generator.classes, y_pred))

#Calculate execution time
end = time.time()
dur = end-start

if dur<60:
    print("Execution Time:",dur,"seconds")
elif dur>60 and dur<3600:
    dur=dur/60
    print("Execution Time:",dur,"minutes")
else:
    dur=dur/(60*60)
    print("Execution Time:",dur,"hours")
