import sounddevice as sd
import noisereduce as nr
import numpy as np
from scipy.io.wavfile import write, read

fs=44100
second=int(input("Enter time duration in seconds: "))
loop=int(input("Enter number of loop: "))
# loop+=10
for i in range(loop):
    print("Loop "+str(i))
    input("Press Enter to continue...")
    
    print("Start recording.....")
    record_voice=sd.rec(int(second*fs),samplerate=fs,channels=2)
    sd.wait()
    write("nghiahieu@gm.com-"+str(i+11)+"-raw.wav",fs,record_voice)
    
    print("Please waiting reduce noise....")
    # load data
    rate, data = read("nghiahieu@gm.com-"+str(i+11)+"-raw.wav")
    orig_shape = data.shape
    data = np.reshape(data, (2, -1))
    # perform noise reduction
    # optimized for speech
    reduced_noise = nr.reduce_noise(
        y=data,
        sr=rate,
        stationary=True
    )
    write("nghiahieu@gm.com-"+str(i+11)+".wav",rate,reduced_noise.reshape(orig_shape))
    print("Finished.....")  
    input("Press Enter to continue...")

print("Done!!! \nPlease check your output file")