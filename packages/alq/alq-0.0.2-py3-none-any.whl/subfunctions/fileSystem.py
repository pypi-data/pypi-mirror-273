
from __future__ import annotations
from .configuration import Configuration
from .owncloud import Owncloud
import os 
import json 
import uuid
import hashlib




def get_machine_uuid():
    # 获取MAC地址
    mac = uuid.getnode()
    # 将MAC地址转换为字符串
    mac_str = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
    # 使用SHA-256哈希算法生成唯一标识码
    unique_id = hashlib.sha256(mac_str.encode()).hexdigest()
    return unique_id



class FileSystem:
    """ logical file system on a cloud
    """    

    def __init__(self):
        self._conf = Configuration() 
        self._oc = Owncloud()
        self._ALQ_RemoteDir = "/ALQ_REMOTE_DATA"
        self._ALQ_RemoteConfig = f"{self._ALQ_RemoteDir}/setting.txt"
        self._ALQ_RemoteSync = f"{self._ALQ_RemoteDir}/sync"
        self._mkdirsIfNotExist( self._ALQ_RemoteDir )

    def _mkdirsIfNotExist(self,dirpath):
        # dirpath = /like/this/one 
        segs = [ s for s in dirpath.strip().split("/") if len(s)>0  ]
        p = '' 
        for seg in segs:
            p += "/" + seg 
            if not self._isPathExist(p):
                self._oc.mkdir( p )

    def _getConfigDict(self):
        if self._isPathExist(self._ALQ_RemoteConfig):
            confDict = json.loads(self._oc._getClient().get_file_contents(self._ALQ_RemoteConfig).decode()) 
            return confDict
        else:
            return {} 
        
    def _setConfigDict(self,dataDict):
        self._oc._getClient().put_file_contents( remote_path = self._ALQ_RemoteConfig, data = json.dumps(dataDict))

    def _isPathExist(self,path):
        return self._oc._isPathExist(path) 

    def _getSyncTags(self):
        conf = self._getConfigDict() 
        syncTags = conf.get('syncTags',{}) 
        return syncTags

    def sync(self):
        # tagItem ->   tagName : {  'pcdir':[ 'mid_cwd',... ]   }, tagName is also the path of on the cloud
        conf = self._getConfigDict() 
        if 'syncTags' not in conf:
            conf['syncTags'] = {} 
            
        mid = get_machine_uuid() 
        cwd = os.getcwd() 
        localTag = f"{mid}_{cwd}" 
        tag = None
        for syncTag in conf['syncTags']:
            if localTag in conf['syncTags'][syncTag]['pcdir']:
                tag = syncTag 
                break 
        if tag is None:
            print("This is the first sync in this dir. Which of the following target do you want to link?")
            for syncTag in conf['syncTags']:
                print(f" {syncTag} ") 
            tag = input("Please type the syncTag name. If you type a new one that is not in the list, a new point will be created for you.")
        remotePath = self._ALQ_RemoteSync + "/" + tag 
        if tag not in conf['syncTags']:
            conf['syncTags'][tag] = { 'pcdir':[] } 
            self._mkdirsIfNotExist( remotePath ) 
        if localTag not in conf['syncTags'][tag]['pcdir']:
            conf['syncTags'][tag]['pcdir'].append(localTag) 
        self._setConfigDict(conf)
        self._oc.sync(localPath=cwd,remotePath=remotePath)


    def test(self):
        oc = self._oc._getPublicDirClient() 


        


#         public_link = 'http://domain.tld/owncloud/A1B2C3D4'

# oc = owncloud.Client.from_public_link(public_link)
# oc.drop_file('myfile.zip')


    

