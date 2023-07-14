import tensorflow as tf
from sklearn import preprocessing

# def is_valid(file_path):
#     ''' returns True if a regular files. False for hidden files.
#     Also, True is a known user with a name, False if anon.
#     '''
#     file_name = tf.strings.split(file_path, '/')[-1]
#     if tf.strings.substr(file_name, 0, 1) == tf.constant(b'.'):
#         return False
#     sc = tf.strings.split(file_path, '/')[-3]
#     speaker = tf.strings.split(sc, '-')[0]
#     return not tf.strings.substr(speaker, 0, 9) == tf.constant(b'anonymous')

def extract_speaker(file_path):
    ''' extract speaker name from the file path '''
    sc = tf.strings.split(file_path, '/')[-1]
    return tf.strings.split(sc, '-')[0]

def encoding_speaker(speaker_ds):
    '''
    '''
    # create one-hot vector dataset from speakers
    speaker_encoder = preprocessing.LabelEncoder()
    speaker_idx = speaker_encoder.fit_transform([bytes.decode(s.numpy()) for s in speaker_ds])
    encoded_speaker_ds = tf.data.Dataset.from_tensor_slices(speaker_idx)
    unique_speakers = len(speaker_encoder.classes_)
    return encoded_speaker_ds, speaker_encoder, unique_speakers

def load_data(list_path):
    '''
    Return dataset which containing audio tensors and label
    '''
    list_ds = tf.data.Dataset.list_files(list_path,shuffle=False)
    # list_ds = list_ds.filter(is_valid)
    # for f in list_ds.take(3):
    #    print(f.numpy())

    # each folder under root contains audio files for a speaker.
    # the folder name is the name of the speaker plus date and three digit code separated by dash.
    # let's print few sample speaker names.
    speaker_ds = list_ds.map(extract_speaker)
    # for speaker in speaker_ds.take(3):
    #    print(speaker)
    return list_ds, speaker_ds

def train_dev_test_split(labeled_ds, batch_size=32):
    '''
    Split dataset to train, validation and test set
    '''
    # create train, validation and test datasets.
    data_size = sum([1 for _ in labeled_ds])
    train_size = int(data_size * 0.7)
    val_size = int(data_size * 0.2)
    test_size = data_size - train_size - val_size
    print('all samples: {}'.format(data_size))
    print('training samples: {}'.format(train_size))
    print('validation samples: {}'.format(val_size))
    print('test samples: {}'.format(test_size))

    # create batched datasets
    labeled_ds = labeled_ds.shuffle(data_size, seed=42)
    train_ds = labeled_ds.take(train_size).shuffle(1000).batch(batch_size).prefetch(1)
    val_ds = labeled_ds.skip(train_size).take(val_size).batch(batch_size).prefetch(1)
    test_ds = labeled_ds.skip(train_size + val_size).take(test_size).batch(batch_size).prefetch(1)
    return train_ds, val_ds, test_ds