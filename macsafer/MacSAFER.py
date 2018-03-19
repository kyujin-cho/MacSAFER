import subprocess
import os
import sys
import getpass
import requests
import json
import sys

def run():
    if sys.platform != 'darwin':
        print('This program works on macOS only.')
        return 1
    print(sys.argv)
    data_url = 'https://raw.githubusercontent.com/thy2134/MacSAFER/master/plugins.json'
    json_datas = requests.get(data_url)
    if json_datas.status_code != 200:
        print('Error fetching plugin data!')
        print('URL =>', data_url)
        exit(1)
    knownPlugins, customDeleteFiles = None, None
    try:
        json_data = json.loads(json_datas.text)
        customDeleteFiles = json_data['customDeleteFiles']
        knownPlugins = json_data['knownPlugins']
    except:
        print('Error while loading data!')
        print('Response data =>')
        print(json_datas.text)
        exit(1)
    
    loaded = {
        'App': {},
        'File': {}
    }


    p = subprocess.Popen(['whoami'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    whoami = p.stdout.readline().decode('utf-8')
    is_root = (whoami == 'root\n')

    password = ''
    if not is_root:
        password = getpass.getpass('Password:')
        echo = subprocess.Popen(['echo', password], stdout=subprocess.PIPE).stdin
        (out, err) = subprocess.Popen(['sudo', '-S', 'ls'], stdin=echo, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if len(err) > 0:
            print('Authentication failed')
            return 1

    for key in knownPlugins.keys():
        if os.path.exists(knownPlugins[key]):
            loaded['App'][key] = knownPlugins[key]
        
    for key in customDeleteFiles:
        for item in customDeleteFiles[key]:
            if os.path.exists(item):
                if key not in loaded['File'].keys():
                    loaded['File'][key] = []
                loaded['File'][key].append(item)

    count = len(loaded['App'].keys()) + len(loaded['File'].keys())
    print('Found', count, 'software' + ('s' if count > 1 else ''))
    if count <= 0:
        return 0
    for (key, value) in loaded['App'].items():
        print(key, '=>', value)

    for (key, value) in loaded['File'].items():
        for item in value:
            print(key, '=>', item)

    yn = input('Deleting ' + str(count) + ' items. Continue? [Y/n]')
    if yn != '' and yn != 'Y':
        print('Aborting...')
        return 0

    for (key, value) in loaded['App'].items():
        print('Deleting', key)
        echo = subprocess.Popen(['echo', password], stdout=subprocess.PIPE).stdin
        p = subprocess.Popen(['sudo', '-S', value], stdin=echo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()


    for (key, value) in loaded['File'].items():
        for item in value:
            print('Deleting', key, 'at', item)
            echo = subprocess.Popen(['echo', password], stdout=subprocess.PIPE).stdin
            p = subprocess.Popen(['sudo', '-S', "rm", "-rf", item], stdin=echo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
