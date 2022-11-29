import pyaudio
import numpy as np

CHUNK = 2 ** 10
RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


p = pyaudio.PyAudio()
for index in range(p.get_device_count()):
    desc = p.get_device_info_by_index(index)
    print("DEVICE: {device}, INDEX: {index}, RATE: {rate} ".format(
        device=desc["name"], index=index, rate=int(desc["defaultSampleRate"])))

stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                frames_per_buffer=CHUNK, input_device_index=1)

frames = []

while (True):
    datasrc = stream.read(CHUNK)
    # data = np.fromstring(datasrc, dtype=np.int16)
    data = np.frombuffer(datasrc, dtype=np.int16)
    frames.append(datasrc)
    if np.average(np.abs(data)) > 100 :
        print(int(np.average(np.abs(data))))

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()