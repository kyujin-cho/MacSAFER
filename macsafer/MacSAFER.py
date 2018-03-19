import subprocess
import os
import sys
import getpass

knownPlugins = {
    "Ahnlab Safe Transaction": "/Applications/AhnLab/ASTx/Uninstaller.app/Contents/MacOS/astxUninstaller",
    "TouchEnEx": "/Applications/CrossEX/touchenex/UnInstallCrossEX.app/Contents/MacOS/UnInstallCrossEX",
    "CrossWeb": "/Applications/CrossWeb/UninstallCrossWeb.app/Contents/MacOS/UninstallCrossWeb",
    "CrossWebEX": "/Applications/CrossWebEX/UnInstallCrossEX.app/Contents/MacOS/UnInstallCrossEX",
    "Delfino": "/Applications/Delfino/Uninstaller.app/Contents/MacOS/Uninstaller",
    "Ahnlab Online Security": "/Applications/AhnLab/ASP/Firewall/Uninstaller.app/Contents/MacOS/ahnlabfwUninstaller",
    "INISAFE MoaSign Ex": "/Applications/INISAFE MoaSign EX Uninstaller.app/Contents/MacOS/INISAFE MoaSign EX Uninstaller",
    "INISAFE MoaSign S": "/Applications/INISAFE MoaSign S Unintaller.app/Contents/MacOS/INISAFE MoaSign S Unintaller",
    "nProtect Online Security V1": "/Applications/nProtect/nProtect Online Security V1/NOS/nosuninst.app/Contents/MacOS/nosuninst",
    "nProtect Netizen": "/Applications/nProtect Netizen/netizen Uninstaller.app/Contents/MacOS/netizen Uninstaller",
    "NWS IPInside": "/Applications/NWS_IPinside/NWSUninstaller.app/Contents/MacOS/NWSUninstaller",
    "IPInside": "/Applications/IPinside.app/Contents/MacOS/IPinside",
    "RaonK": "/Applications/raonk/uninstall.app/Contents/MacOS/uninstall.sh",
    "AnySign for PC": "/Applications/SoftForum/Uninstaller_AnySign4PC.app/Contents/MacOS/Uninstaller",
    "Veraport": "/Applications/Veraport/veraport.app/Contents/MacOS/veraport"
}

customDeleteFiles = {
    "UniCRSV2": [
        "/Library/Internet Plug-Ins/npUniCRSV2Plugin.plugin"
    ],
    "UniSignWeb": [
        "/Library/Internet Plug-Ins/npUniSignWebPlugin.plugin"
    ],
    "Printmade3": [
        "/Library/Internet Plug-Ins/Printmade3",
        "/Library/Internet Plug-Ins/Printmade3NPPlugin.plugin"
    ],
    "CrossEX": [
        "/Applications/CrossEX"
    ],
    "AhnLab": [
        "/Applications/AhnLab"
    ],
    "Veraport": [
        "/Applications/Veraport",
        "/Library/Internet Plug-Ins/Veraport.plugin"
    ],
    "I3GManager": [
        "/Library/Internet Plug-Ins/NPI3GManager.plugin"
    ],
    "MarkAny": [
        "/Applications/MaSafeViewer.app",
        "/Applications/MDMBroker.app"
    ],
    "NTS": [
       "/Applications/NTSFileCryptNP.app",
        "/Applications/NTSMagicLineNP.app",
        "/Applications/NTSMagicXMLSecurityNP.app" 
    ]
}

def run():
    loaded = {
        'App': {},
        'File': {}
    }

    if sys.platform != 'darwin':
        print('This program works on macOS only.')
        return 1

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
