import tensorflow as tf
from tensorflow import keras


def create_model(input_shape, unique_speakers):
    ''' Create, complie and return a model 
    '''
    dropout_rate = .25
    regularazation = 0.001
    audio_input = keras.layers.Input(shape=input_shape)
    conv1 = keras.layers.Conv2D(16, kernel_size=(3, 3), padding='same',
                               activation='relu', input_shape=input_shape)(audio_input)
    maxpool1 = keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2)(conv1)
    batch1 = keras.layers.BatchNormalization()(maxpool1)
    conv2 = keras.layers.Conv2D(32, kernel_size=(3, 3), padding='same',
                               activation='relu', input_shape=input_shape)(batch1)
    maxpool2 = keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2)(conv2)
    batch2 = keras.layers.BatchNormalization()(maxpool2)
    conv3 = keras.layers.Conv2D(64, kernel_size=(3, 3), padding='same',
                activation='relu')(batch2)
    maxpool3 = keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2)(conv3)
    batch3 = keras.layers.BatchNormalization()(maxpool3)
    flt = keras.layers.Flatten()(batch3)
    drp1 = keras.layers.Dropout(dropout_rate)(flt)
    dense1 = keras.layers.Dense(unique_speakers * 2, activation='relu',
                kernel_regularizer=keras.regularizers.l2(regularazation))(drp1)
    drp2 = keras.layers.Dropout(dropout_rate)(dense1)
    output = keras.layers.Dense(unique_speakers, activation='softmax', name='speaker')(drp2)
    model = keras.Model(inputs=audio_input, outputs=output)
    model.compile(loss=keras.losses.sparse_categorical_crossentropy,
                  optimizer=keras.optimizers.Adam(),
                  metrics=['acc'])
    return model

def layer_added(output_based_network, unique_speakers, activation='sigmoid'):
    ''' Add layer predict for Transfer learning, return those layer
    '''
    dropout_rate = .25
    regularazation = 0.001
    x = output_based_network
    x = keras.layers.Flatten()(x)
    x = keras.layers.Dropout(dropout_rate)(x)
    x = keras.layers.Dense(unique_speakers * 2, activation='relu',
                  kernel_regularizer=keras.regularizers.l2(regularazation))(x)
    x = keras.layers.Dropout(dropout_rate)(x)
    x = keras.layers.Dense(unique_speakers, activation=activation, name='speaker')(x)
    return x