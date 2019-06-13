import os,sys
from pocketsphinx import AudioFile, get_model_path, get_data_path, Decoder
import pocketsphinx as ps
from argparse import ArgumentParser, SUPPRESS
import logging as log
#import pyaudio
import time

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-i','--file_location',help="Required if running on speech file. Path to speech file", default=None, type=str)
    args.add_argument('-t','--type_of_file',help="Required. Type format of the speech file in lower letter or live for live speech. Option: wav, live", required = True, type=str)
    return parser


def recog_wav(MODELDIR,wavfile):

    #print(MODELDIR)
    
    config = Decoder.default_config()
    config.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
    config.set_string('-lm', os.path.join(MODELDIR, 'en-us.lm.bin'))
    config.set_string('-dict', os.path.join(MODELDIR, 'cmudict-en-us.dict'))

    # Decode streaming data.
    decoder = Decoder(config)
    start = time.time()
    decoder.start_utt()
    wav_stream=open(wavfile,"rb")
    while True:
        buffer = wav_stream.read(1024)
        if buffer:
            decoder.process_raw(buffer,False,False)
        else:
            break
    decoder.end_utt()
    duration = time.time() - start
    print("Duration: " + str(duration)) #Benchmarking
    for seg in decoder.seg():
        print(seg.word)


def recog_live(MODELDIR):
    from pocketsphinx import LiveSpeech
    try:
        speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=os.path.join(MODELDIR, 'en-us'),
            lm=os.path.join(MODELDIR, 'en-us.lm.bin'),
            dic=os.path.join(MODELDIR, 'cmudict-en-us.dict')
        )
        for phrase in speech:
            print(phrase)
            
            
    except RuntimeError as e:
        log.error("Error occured. Please check the mic is connected. Here are the traceback")
        log.error(e)
        sys.exit(1)
    
    

def main():
    args = build_argparser().parse_args()
    model_path = get_model_path()
    #data_path = get_data_path()
    file_type = args.type_of_file
    file_loca = args.file_location
    if file_type == "live":
        recog_live(model_path)
    else:
        if file_loca == None:
            log.error("File name required if running on file to text mode")
            sys.exit(1)
        if file_type == "wav":
            recog_wav(model_path,file_loca)
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
if __name__ == "__main__":
    sys.exit(main() or 0)
