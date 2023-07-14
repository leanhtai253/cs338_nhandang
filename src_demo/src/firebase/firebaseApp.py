import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import storage as gg_storage
import os 
class FirebaseApp:
    cred = credentials.Certificate({})
    firebase_admin.initialize_app(cred, {})
    bucket = storage.bucket()
    bucketName = ""
    def bucket_metadata(self):
        """Prints out a bucket's metadata."""
        # bucket_name = 'your-bucket-name'
        print(f"ID: {self.bucket.id}")
        print(f"Name: {self.bucket.name}")
        print(f"Storage Class: {self.bucket.storage_class}")
        print(f"Location: {self.bucket.location}")
        print(f"Location Type: {self.bucket.location_type}")
        print(f"Cors: {self.bucket.cors}")
        print(f"Default Event Based Hold: {self.bucket.default_event_based_hold}")
        print(f"Default KMS Key Name: {self.bucket.default_kms_key_name}")
        print(f"Metageneration: {self.bucket.metageneration}")
        print(
            f"Public Access Prevention: {self.bucket.iam_configuration.public_access_prevention}"
        )
        print(f"Retention Effective Time: {self.bucket.retention_policy_effective_time}")
        print(f"Retention Period: {self.bucket.retention_period}")
        print(f"Retention Policy Locked: {self.bucket.retention_policy_locked}")
        print(f"Requester Pays: {self.bucket.requester_pays}")
        print(f"Self Link: {self.bucket.self_link}")
        print(f"Time Created: {self.bucket.time_created}")
        print(f"Versioning Enabled: {self.bucket.versioning_enabled}")
        print(f"Labels: {self.bucket.labels}")

    def get_blob(self, username, fileNum):
        if fileNum < 10: fileNumStr = f'00{fileNum}'
        else: fileNumStr = f'0{fileNum}'
        blobName = f'audio/{username}/{fileNumStr}'
        blob = self.bucket.blob(blobName)
        return blob
    
    def get_blob_signin(self, username):
        blobName = f'audio/{username}-signin'
        blob = self.bucket.blob(blobName)
        return blob

    def download_blob(self, username, fileNum):
        user_audio_dir = f'src/audio_data/user_audio_ds/{username}'
        for i in range(1, 11):
            if i < 10: iStr = f'00{i}'
            else: iStr = f'0{i}'
            blobName = f'{username}-{iStr}'
            blob = self.get_blob(username, i)
            if not os.path.isdir(user_audio_dir):
                os.makedirs(user_audio_dir)
            try:
                blob.download_to_filename(f'src/audio_data/user_audio_ds/{username}/{blobName}.wav')
                print(f"Successfully downloaded {blobName}")
            except Exception as e:
                print(f"Error downloading {blobName}")
                print(e)

    def download_blob_signin(self, username):
        blob = self.get_blob_signin(username=username)
        username = username.split('@')[0].replace('.','')
        user_audio_dir = f'src/model/audio/{username}'
        blobName = f'audio/{username}-signin.wav'
        if not os.path.isdir(user_audio_dir):
            os.makedirs(user_audio_dir)
        try:
            blob.download_to_filename(f'{user_audio_dir}/{username}.wav', raw_download=True)
            # blob.download_to_file(f'{user_audio_dir}/{username}.wav')
            print(f"Successfully downloaded {blobName}")
        except Exception as e:
            print(f"Error downloading {blobName}")
            print(e)

    def upload_blob(self, username, file, fileNum):
        if fileNum < 10: fileNumStr = f'00{fileNum}'
        else: fileNumStr = f'0{fileNum}'
        blobName = f'audio/{username}/{fileNumStr}'
        blob = self.bucket.blob(blob_name=blobName)
        try:
            blob.upload_from_file(file_obj=file)
            print(f"Successfully uploaded for {username}/{fileNum}")
        except Exception as e:
            print(f"Error uploading for {username}/{fileNum}")
            print(e)

    def upload_blob_signin(self, username, file):
        blobName = f'audio/{username}-signin.wav'
        blob = self.bucket.blob(blob_name=blobName)
        try:
            blob.upload_from_file(file_obj=file)
            print(f"Successfully uploaded for {username}-signin")
        except Exception as e:
            print(f"Error uploading for {username}-signin")
            print(e)

    def check_blob_exists(self, username, fileNum):
        if fileNum < 10: fileNumStr = f'00{fileNum}'
        else: fileNumStr = f'0{fileNum}'
        blobName = f'audio/{username}/{fileNumStr}'
        blob = self.bucket.blob(blob_name=blobName)
        return blob.exists()
    
    def get_latest_blobNum(self, username):
        num = 10
        while num > 0:
            if self.check_blob_exists(username=username, fileNum=num):
                return num
            num -= 1
        return num
        