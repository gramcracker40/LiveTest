import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Example dataset dimensions
num_classes = 5  # For example purposes, adjust as per your dataset
image_width = 28  # Adjust to match the width of your preprocessed images
image_height = 28  # Adjust to match the height of your preprocessed images

# Placeholder for dataset loading and preprocessing
# Replace these with actual loading of your images and labels
images = np.random.rand(1000, image_height, image_width, 1)  # Example images, replace with actual image data
labels = np.random.randint(0, num_classes, 1000)  # Example labels, replace with actual labels

# Convert labels to one-hot encoding
labels = to_categorical(labels, num_classes)

# Split dataset into training, validation, and test sets
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.2, random_state=42)
train_images, val_images, train_labels, val_labels = train_test_split(train_images, train_labels, test_size=0.25, random_state=42)  # 0.25 x 0.8 = 0.2

# CNN model definition
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(image_height, image_width, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(num_classes, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Data augmentation configuration (optional)
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')

# Model training
# Without data augmentation
# model.fit(train_images, train_labels, epochs=10, validation_data=(val_images, val_labels))

# With data augmentation
datagen.fit(train_images)
model.fit(datagen.flow(train_images, train_labels, batch_size=32),
          steps_per_epoch=len(train_images) / 32, epochs=10,
          validation_data=(val_images, val_labels))
