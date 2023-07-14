import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('study-with-mentors-firebase-adminsdk-uss11-7a0f31fcca.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'growth-me-381908.appspot.com'
})

bucket = storage.bucket()
print(bucket)
# 'bucket' is an object defined in the google-cloud-storage Python library.
# See https://googlecloudplatform.github.io/google-cloud-python/latest/storage/buckets.html
# for more details.