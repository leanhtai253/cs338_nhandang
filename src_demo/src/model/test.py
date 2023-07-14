import os
import tensorflow as tf
from tensorflow import keras

from .extract_mfcc_features import create_audio_ds

def predict_score(sample_test_path, user_key, user_model_dir, user_weigths_dir=None):

    sample_ds = tf.data.Dataset.from_tensor_slices([sample_test_path])
    sample_input = create_audio_ds(sample_ds).batch(1)

    model_name = user_key + '_model.h5'
    # weights_name = user_key + '_weights.h5'

    model = keras.models.load_model(os.path.join(user_model_dir, user_key, model_name))
    # model = keras.models.load_model(user_model_dir)
    # model.load_weights(os.path.join(user_weigths_dir, weights_name))
    pred_score = model.predict(sample_input)

    # if pred >= 0.9:
    #     print('Verify done!')
    # else:
    #     print('Wrong! Please try again!')
    
    return pred_score


if __name__ == 'main':
    username = 'nghia.nguyen@vah.com.au'
    print(username)
    user_audio_path = f'src/model/audio/{username}/{username}.flac'
    user_model_dir = f'src/model/models'
    score = predict_score(sample_test_path=user_audio_path, user_key=username, user_model_dir=user_model_dir)
    print(score)