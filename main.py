import soundcard as sc
import soundfile as sf
import numpy as np
import os
import config
from threading import Thread
import time
from datetime import datetime

OUTPUT_FILE_NAME_SPEAKERS_FOLDER = "speakers"    # file name.
OUTPUT_FILE_NAME_MIC_FOLDER = "mic"    # file name.
SAMPLE_RATE = 48000              # [Hz]. sampling rate.
STEP_PER_SEC = 240

DO_RECORD = False 

def find_processes():
    p = os.popen(config.tasklist_query()).read().splitlines()
    is_it_running = 0
    for item in p:
        # Still needs condition because otherwise the console returns "No tasks are running for specific criteria"
        if config.ZOOM is True and item.find('CptHost.exe') > -1:
                is_it_running += 1
        if config.TEAMS is True and item.find('msteams.exe') > -1:
                is_it_running += 1
    
    return is_it_running

def input_do_record():
    global DO_RECORD
    while True:
        if find_processes()>0:
            DO_RECORD = True
        else:
            DO_RECORD = False
        time.sleep(1)

def record_both():
    global DO_RECORD
    while True:
        while not DO_RECORD:
                print('Not Recording')
                time.sleep(1)
        with (sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as speaker, 
            sc.get_microphone(id=str(sc.default_microphone().name)).recorder(samplerate=SAMPLE_RATE) as mic,
            open('temp_speaker.txt','ab') as f_speaker,
            open('temp_mic.txt','ab') as f_mic):

            print("Recording")

            data_speaker = speaker.record(numframes=SAMPLE_RATE//STEP_PER_SEC)
            data_mic = mic.record(numframes=SAMPLE_RATE//STEP_PER_SEC)
            np.savetxt(f_speaker,data_speaker)
            np.savetxt(f_mic,data_mic)
            
            while DO_RECORD:
                f_speaker.write(b"\n")
                f_mic.write(b"\n")
                data_speaker_sample = speaker.record(numframes=SAMPLE_RATE//STEP_PER_SEC)
                data_mic_sample = mic.record(numframes=SAMPLE_RATE//STEP_PER_SEC)
                np.savetxt(f_speaker,data_speaker_sample)
                np.savetxt(f_mic,data_mic_sample)

            print("Stop Recording")

        date_string = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")  
        with (open('temp_speaker.txt','r') as f_speaker,
            open('temp_mic.txt','r') as f_mic):
            sf.write(file=os.path.join(OUTPUT_FILE_NAME_SPEAKERS_FOLDER,date_string+".wav"), data=np.loadtxt(f_speaker,dtype=np.float64)[:, 0], samplerate=SAMPLE_RATE)
            sf.write(file=os.path.join(OUTPUT_FILE_NAME_MIC_FOLDER,date_string+".wav"), data=np.loadtxt(f_mic,dtype=np.float64), samplerate=SAMPLE_RATE)

        os.remove('temp_speaker.txt')
        os.remove('temp_mic.txt')


def run():
    if not os.path.exists(OUTPUT_FILE_NAME_SPEAKERS_FOLDER):
        os.mkdir(OUTPUT_FILE_NAME_SPEAKERS_FOLDER)
    if not os.path.exists(OUTPUT_FILE_NAME_MIC_FOLDER):
        os.mkdir(OUTPUT_FILE_NAME_MIC_FOLDER)

    record = Thread(target=record_both)
    record.daemon = True
    record.start()
    checker = Thread(target=input_do_record)
    checker.daemon = True
    checker.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    run()