import os,sys
from pocketsphinx import AudioFile, get_model_path, get_data_path, Decoder
import pocketsphinx as ps



def recog(MODELDIR,wavfile):

    #print(MODELDIR)
    
    config = Decoder.default_config()
    config.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
    config.set_string('-lm', os.path.join(MODELDIR, 'en-us.lm.bin'))
    config.set_string('-dict', os.path.join(MODELDIR, 'cmudict-en-us.dict'))

    # Decode streaming data.
    decoder = Decoder(config)

    decoder.start_utt()
    wav_stream=open(wavfile,"rb")
    while True:
        buffer = wav_stream.read(1024)
        if buffer:
            decoder.process_raw(buffer,False,False)
        else:
            break
    decoder.end_utt()
    for seg in decoder.seg():
        print(seg.word)
             
    


model_path = get_model_path()
#data_path = get_data_path()
recog(model_path,"/home/pi/Desktop/KURF/LDC93S1.wav")
#wav_file=os.path.join("/home/pi/Desktop/KURF", 'LDC93S1.wav')
#hmm=os.path.join(model_path, 'en-us')
#lm=os.path.join(model_path, 'en-us.lm.bin')
#dictd=os.path.join(model_path, 'cmudict-en-us.dict')
#print(recog(model_path,wav_file))

"""
config = {
    'verbose': False,
    'audio_file': os.path.join("/home/pi/Desktop/KURF", 'LDC93S1.wav'),
    'buffer_size': 2048,
    'no_search': False,
    'full_utt': False,
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'dict': os.path.join(model_path, 'cmudict-en-us.dict')
}
#print(data_path)
#audio = AudioFile(**config)
#for phrase in audio:
#    print(phrase)
"""