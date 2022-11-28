import pyaudio
import numpy as np

CHUNK = 2 ** 10
RATE = 44100

p = pyaudio.PyAudio()
for index in range(p.get_device_count()):
    desc = p.get_device_info_by_index(index)
    print("DEVICE: {device}, INDEX: {index}, RATE: {rate} ".format(
        device=desc["name"], index=index, rate=int(desc["defaultSampleRate"])))

stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                frames_per_buffer=CHUNK, input_device_index=1)

while (True):
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    if np.average(np.abs(data)) > 100 :
        print(int(np.average(np.abs(data))))

stream.stop_stream()
stream.close()

p.terminate()
