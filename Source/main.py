import random
import math
from text_wave_handler import TextWaveHandler

file = open("presidents.txt","r")
s = file.read()
file.close()

wh = TextWaveHandler(max_size=16,radius=2)
wh.read_text(s)
wh.generate_wave()
wh.produce(20)