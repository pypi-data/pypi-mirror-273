__version__= '0.7.0 2023-09-25'
import os,time
timer = time.perf_counter
import numpy as np

print(f'importing apstrimAccess')
from apstrim import scan
print(f'APScan: {scan.__version__}')
#from .apstrim.scan import APScan, __version__ as scanVersion
#from apstrim import scan as APScan
#print(f'APScan: {APScan.__version__}')
#import apstrim
#print(help(apstrim))

class Access():
    """Interface to Process Variables, from apstrim file.
    The pvName should be a tuple: (deviceName,parameterName)
    """
    __version__ = __version__
    Dbg = 1
    scan.APScan.Verbosity = Dbg
    timeInterval = 9e9
    startTime = None
    timestamp = time.time()
    result = {}

    def __init__(self, verbosity = 1):
        self.Dbg = verbosity
        scan.APScan.Verbosity = verbosity
        print('>apstrimAccess.__init__')

    def info(*devParNames):
        print(f'>info({devParNames})')
        return

    def get(*devParNames, **kwargs):
        print(f'>get({devParNames}), {Access.result.keys()}')
        devParName = devParNames[0]
        result = Access.result.get(devParName)
        if result is None:
            #result = {devParName:{'value': np.random.rand(100), 'timestamp':Access.timestamp}}

            # 
            fileName = os.path.expanduser(devParName[0])
            print(f'>APScan({fileName})')
            apscan = scan.APScan(fileName)
            ts = timer()
            pvIndexes = [0]#devParName[1]
            extracted = apscan.extract_objects(Access.timeInterval,
                pvIndexes, Access.startTime)
            print(f'Total (reading + extraction) time: {round(timer()-ts,3)}')
            print(f'extracted: {extracted}')
            result = 
            #print(f'result: {Access.result}')
            Access.result[devParName] = result
        return result

    def set(devPar_Value):
        print(f'>set({devPar_Value})')

    def subscribe(callback, *devParNames):
        print(f'>subscribe({callback, devParNames})')

    def unsubscribe():
        print(f'>subscribe({callback, devParNames})')
