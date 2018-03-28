from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

os.chdir("WavFiles")

def AudioTokenizer(filename):
    sound_file = AudioSegment.from_wav(filename)
    audio_chunks = split_on_silence(sound_file,min_silence_len=100, silence_thresh=-22)

    for i, chunk in enumerate(audio_chunks):
        out_file = filename[:-4]+ ".{0}.wav".format(i)
        chunk.export(out_file, format="wav")

