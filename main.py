

import multiprocessing as mp
import sys
import os
import subprocess

#----------#File recognition#----------#
def stt_file(files_path, path, new_path):
    for file in files_path:
        subprocess.Popen(
            ['ffmpeg'
            , '-loglevel'
            , 'quiet'
            , '-i'
            ,file
            ,'-ar'
            , '16000'
            , '-ac'
            , '1'
            , '-f'
            , 's16le'
            , file.replace(path, new_path)
            ])
 
#----------#Collect files#----------#
def collect_files(dict_path):
    print('Collecting files')
    file_collection = []
    for subdir, dirs, files in os.walk(dict_path):
        print(subdir)
        for f in files:
            if f.endswith('.wav'):
                file_collection.append(os.path.join(subdir, f))
                
    return file_collection

if __name__ == "__main__":
    path='files/'
    new_path='new_files/'

    file_collection = collect_files(path)       #функция получения файлов

    count_t=5                                   #кол-во потоков
    count_p=len(file_collection)//count_t+1     #кол-во для обработке в одном потоке
    procs=list()                                #Массив процессов
    list_path=[]                                #Список файлов для отправки в поток
    count=0                                     #Кол-во файлов в потке
    for file_path in file_collection:
        count+=1 
        list_path.append(file_path)
        if count_p==count:
            proc=mp.Process(target=stt_file, args=(list_path))
            procs.append(proc)
            proc.start()
            count=0
            list_path=[]
    
    proc=mp.Process(target=stt_file, args=(list_path))
    procs.append(proc)
    proc.start()

    for proc in procs:
        proc.join()

