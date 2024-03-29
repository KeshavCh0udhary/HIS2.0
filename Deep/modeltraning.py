import tensorflow as tf
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Concatenate, Flatten, Dense, Reshape
from keras.models import Model
from keras.applications import Xception
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
import cv2
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# Assuming image dimensions are 224x224x3
img_width, img_height, img_channels = 224, 224, 3

# Encoder
input_img = Input(shape=(img_width, img_height, img_channels))
xception_base = Xception(weights='imagenet', include_top=False)
x = xception_base(input_img)

# Additional convolutional layers for encoding
x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)

# Flatten for connecting to a dense layer
x = Flatten()(x)

# Dense layers for encoding
encoded = Dense(128, activation='relu')(x)

# Decoder
x = Dense(64 * int(img_width / 4) * int(img_height / 4), activation='relu')(encoded)
x = Reshape((int(img_width / 4), int(img_height / 4), 64))(x)
x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(img_channels, (3, 3), activation='sigmoid', padding='same')(x)

# Classifier on top
classifier = Dense(1, activation='sigmoid')(encoded)

# Combined model
model = Model(inputs=input_img, outputs=[decoded, classifier])

# Compile the model
model.compile(optimizer=Adam(lr=0.001),
              loss=['mean_squared_error', 'binary_crossentropy'],
              loss_weights=[1, 0.5],  # Adjust the weights as needed
              metrics=['accuracy'])

# Display the model architecture
model.summary()

# Set up ImageDataGenerators for training and validation
train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    './CelebAMask-HQ',
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode='binary'
)

validation_generator = test_datagen.flow_from_directory(
    './CelebAMask-HQ',
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode='binary'
)

# Train the model
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // 32,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // 32
)
