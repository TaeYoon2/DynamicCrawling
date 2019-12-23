import os
from pydub import AudioSegment

SAVE_ROOT = "/mnt/data1/sunkist/projects/bible_text/"
mp3_path = os.path.join(SAVE_ROOT, "1/mp3s" , "123_85_14.mp3")
song = AudioSegment.from_mp3(mp3_path)
print(song.frame_rate)