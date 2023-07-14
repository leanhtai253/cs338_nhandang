import os
import numpy as np
import tensorflow as tf
from tensorflow import keras

from model import layer_added
from get_path_and_label import load_data
from extract_mfcc_features import create_audio_ds 

BATCH_SIZE = 32

def get_run_dir(root_logdir):
    import time
    run_id = time.strftime("run%Y_%m_%d-%H_%M_%S")
    return os.path.join(root_logdir, run_id)

def load_path(path):
    list_paths=[]
    for r, d, f in os.walk(path):
        for file in f:
            if '.wav' in file: 
                list_paths.append(os.path.join(r, file))
    return list_paths

def get_train_val_ds(list_path, old_list_path, train_rate=0.7, batch_size=32):
    list_ds, _ = load_data(list_path)
    audio_ds = create_audio_ds(list_ds)

    old_audio = tf.data.experimental.load(old_list_path)

    n_take = len(list_ds)*5
    old_audio_take = old_audio.shuffle(len(old_audio)).take(n_take)
    labeled_0 = tf.data.Dataset.from_tensor_slices(np.repeat(0, n_take))
    old_audio_labeled_0 = tf.data.Dataset.zip((old_audio_take, labeled_0))
    

    labeled_1 = tf.data.Dataset.from_tensor_slices(np.repeat(1,len(list_ds)))
    user_audio_labeled_1 = tf.data.Dataset.zip((audio_ds,labeled_1))
    total_ds = user_audio_labeled_1.concatenate(old_audio_labeled_0)
    
    data_size = sum([1 for _ in total_ds])
    train_size = int(data_size * train_rate)
    val_size = data_size - train_size
    total_ds = total_ds.shuffle(data_size, seed=42)
    train_ds = total_ds.take(train_size).shuffle(1000).batch(batch_size).prefetch(1)
    val_ds = total_ds.skip(train_size).take(val_size).batch(batch_size).prefetch(1)
    return train_ds, val_ds

def training_model(new_data_dir, audio_ds_path, base_model_path, log_dir, user_model_dir):

    user_file_paths = load_path(new_data_dir)
    train_set, dev_set = get_train_val_ds(user_file_paths, audio_ds_path, 0.7, BATCH_SIZE)
    
    old_model = keras.models.load_model(base_model_path)
    output_layer = layer_added(old_model.layers[-6].output, 1, 'sigmoid')
    new_model = keras.Model(old_model.input, output_layer)
    new_model.layers[-6].set_weights(old_model.layers[-6].get_weights())
    # new_model.summary()
    new_model.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(), metrics=['binary_accuracy'])
    
    # Freeze the first layers, before train it
    for layer in new_model.layers[:-5]:
        layer.trainable = False

    run_logdir = get_run_dir(log_dir)
    tensorboard_cb = keras.callbacks.TensorBoard(run_logdir, update_freq='batch')
    history = new_model.fit(train_set, epochs=8, validation_data=dev_set, callbacks=[tensorboard_cb])

    user_key = new_data_dir.split('/')[-1]
    model_name = user_key + '_model.h5'
    weights_name = user_key + '_weights.h5'
    new_model.save(os.path.join(user_model_dir, user_key, model_name))
    # new_model.save_weights(os.path.join(user_weigths_dir, user_key, weights_name))