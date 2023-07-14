import sounddevice as sd
import noisereduce as nr
import numpy as np
from scipy.io.wavfile import write, read

fs=44100
second=int(input("Enter time duration in seconds: "))
# loop=int(input("Enter number of loop: "))
# # loop+=10
email = str(input("Enter email: "))
for i in range(1):
    print("Loop "+str(i))
    input("Press Enter to continue...")
    
    print("Start recording.....")
    record_voice=sd.rec(int(second*fs),samplerate=fs,channels=2)
    sd.wait()
    write(f"{email}-signin-raw.wav",fs,record_voice)
    
    print("Please waiting reduce noise....")
    # load data
    rate, data = read(f"{email}-signin-raw.wav")
    orig_shape = data.shape
    data = np.reshape(data, (2, -1))
    # perform noise reduction
    # optimized for speech
    reduced_noise = nr.reduce_noise(
        y=data,
        sr=rate,
        stationary=True
    )
    write(f"audio/{email}/{email}-signin.wav",rate,reduced_noise.reshape(orig_shape))
    print("Finished.....")  
    input("Press Enter to continue...")

print("Done!!! \nPlease check your output file")