from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import numpy as np
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense

#training and test data taken from images in directory
training_dir = 'trainingFlickr/train' #1000 per label
validation_dir = 'trainingFlickr/validation'#1000 per label
test_dir = 'trainingFlickr/test'
img_width = 150
img_height = 150
batch_size = 16

def get_weights_from_vgg16():

    datagen = ImageDataGenerator(rescale=1. / 255)
    model = load_model('vgg16_conv_150pixels.h5')

    #generate
    generator = datagen.flow_from_directory(
            training_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode=None,    #this means our generator will only yield batches of data, no labels
            shuffle=False) # our data will be in order, so all first 1000 images will be 0s, then 1000 1s
    # a generator that yields batches of numpy data
    bottleneck_features_train = model.predict_generator(generator)

    np.save(open('bottleneck_features_train_birdplane.npy', 'w'), bottleneck_features_train)

    generator = datagen.flow_from_directory(
            validation_dir,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            class_mode=None,
            shuffle=False)
    bottleneck_features_validation = model.predict_generator(generator)
    np.save(open('bottleneck_features_validation_birdplane.npy', 'w'), bottleneck_features_validation)

    return

# print train_data.shape
# print train_data.ndim
# print train_data.size
# print train_data[100]

def train_connected_model():

    train_data = np.load(open('bottleneck_features_train_birdplane.npy'))

    # the features were saved in order, so recreating the labels is easy
    train_labels = np.array([0]*2000 + [1]*2000)

    validation_data = np.load(open('bottleneck_features_validation_birdplane.npy'))

    validation_labels = np.array([0]*500 + [1]*500)
#train fully connected model given train data (features from conv model)
    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=50,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels))
    model.save_weights('bottleneck_fc_model_birdplane.h5')
    model.save('bird_plane_connectedontopvgg16.h5')

    return 'trained'

train_connected_model()