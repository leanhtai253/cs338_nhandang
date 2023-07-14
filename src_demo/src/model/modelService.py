from .train import *
from .test import *
class ModelService:

    def check(username):
        user_audio_path = f'src/model/audio/{username}/{username}-signin.wav'
        # user_audio_path = f'src/model/audio/{username}/{username}-signin-real.wav'
        user_model_dir = f'src/model/models'
        score = predict_score(sample_test_path=user_audio_path, user_key=username, user_model_dir=user_model_dir)
        return score