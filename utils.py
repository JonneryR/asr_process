import wave
import numpy as np
from pydub import AudioSegment

# read pcm as numpy array
def read_pcm_array(file_path, sr=16000, ch=1, sw=2, format='np'):
    voice_data = AudioSegment.from_file(file=file_path, sample_width=sw, frame_rate=sr, channels=ch)
    pcm_data = np.array(voice_data.get_array_of_samples()) / 32768.0
    if format == 'tr':
        import torch as tr
        pcm_data = tr.from_numpy(pcm_data)
    elif format == 'tf':
        import tensorflow as tf
        pcm_data = tf.convert_to_tensor(pcm_data)
    return pcm_data


# pcm to wav
def pcm2wav(pcm_file, wav_file, channels=1, bits=16, sample_rate=16000):
    pcmf = open(pcm_file, 'rb')
    pcmdata = pcmf.read()
    pcmf.close()
    if bits % 8 != 0:
        raise ValueError("bits % 8 must == 0. now bits:" + str(bits))
    wavfile = wave.open(wav_file, 'wb')
    wavfile.setnchannels(channels)
    wavfile.setsampwidth(bits // 8)
    wavfile.setframerate(sample_rate)
    wavfile.writeframes(pcmdata)
    wavfile.close()


# wav to pcm
def wav2pcm(wavfile, pcmfile, data_type=np.int16):
    f = open(wavfile, "rb")
    f.seek(0)
    f.read(44)
    data = np.fromfile(f, dtype= data_type)
    data.tofile(pcmfile)
