
from __future__ import annotations
from .configuration import Configuration
import os 
import tempfile
import shutil
import subprocess
import owncloud
from six.moves.urllib import parse
import json
from pathlib import Path


def run_command(command):
    """Execute the command and capture stdout."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(),stderr.decode()


class Client2(owncloud.Client):

    @classmethod
    def from_public_link(cls, public_link, folder_password='', **kwargs):
        public_link_components = parse.urlparse(public_link)
        url = public_link_components.scheme + '://' + public_link_components.hostname
        if public_link_components.port:
            url += ":" + str(public_link_components.port)
        folder_token = public_link_components.path.split('/')[-1]
        anon_session = cls(url, **kwargs)
        anon_session.anon_login(folder_token, folder_password=folder_password)
        return anon_session




class Owncloud:
    """ 8096 at 7
    """    

    def __init__(self):
        self._conf = Configuration() 
        self._host = "http://192.168.1.7:8096"
        self._sharingUrlPath = f"{self._host}/s/iJCUedZ0F4d6cXQ"
        self._sharingPath = f"{self._host}/s/w8Xs5bq8BHx7QZa"
        self._softwarePath = f"{self._host}/s/jn7yzjzPbs8uEA4"

    def _downloadBinFileIfNotExist(self):
        homeDir = str(Path.home()) 
        alqDir = os.path.join(homeDir, ".alq" )
        binPath = os.path.join(alqDir,'ownCloud.AppImage')
        if not os.path.exists(alqDir):
            os.makedirs(alqDir) 
        if not os.path.exists(binPath):
            oc = Client2.from_public_link(self._softwarePath) 
            print("install owncloud-client for you, please wait...")
            oc.get_file(remote_path='/ownCloud.AppImage',local_file=binPath)
            os.chmod(binPath, 0o775)
        return binPath

    def _owncloudcli_rcmd(self,rcmd):
        bin = self._downloadBinFileIfNotExist()
        cmd = f"{bin} --cmd {rcmd}"
        os.system(cmd) 

    def _get_owncloudcli_rcmdWithConf(self,rcmd):
        bin = self._downloadBinFileIfNotExist()
        username,password = self._getUserPass()
        url = self._host
        cmd = f"{bin} --cmd -u {username} -p {password} --server {url} {rcmd} "
        return cmd
    
    def _getRemoteConfig(self):
        ALQ_RemoteDir = "ALQ_REMOTE_DATA" 
        ALQ_RemoteConfig = "/ALQ_REMOTE_DATA/setting.txt"
        oc = self._getClient()
        if not self._isPathExist(ALQ_RemoteDir):
            self.mkdir(ALQ_RemoteDir) 
        if self._isPathExist(ALQ_RemoteConfig):
            confDict = json.loads(oc.get_file_contents(ALQ_RemoteConfig).decode()) 
            return confDict
        else:
            return {} 
        
    def _setRemoteConfig(self,dataDict):
        ALQ_RemoteConfig = "/ALQ_REMOTE_DATA/setting.txt"
        data = self._getRemoteConfig() 
        oc = self._getClient()
        oc.put_file_contents( remote_path = ALQ_RemoteConfig, data = json.dumps(dataDict))



    def config(self,username:str,password:str):
        self._conf._set(section='owncloud',key='username',val=username) 
        self._conf._set(section='owncloud',key='password',val=password) 
        # self.conf._set(section='owncloud',key='url',val="http://192.168.1.7:8096") #http://192.168.1.7:8096/remote.php/webdav/ 
        # return self 
        return "set done!"
    
    def _getUserPass(self):
        oConfig = self._conf._getSectionDict(section="owncloud")
        username = oConfig.get('username',None)
        password = oConfig.get('password',None) 
        return username,password
    
    def _getClient(self):
        oc = owncloud.Client(self._host)
        username,password = self._getUserPass()
        if not (username is not None and password is not None):
            raise Exception("owncloud is not configurated") 
        oc.login(username, password) 
        return oc 
    
    def _getPublicDirClient(self):
        path = f"{self._host}/s/w8Xs5bq8BHx7QZa"
        oc = Client2.from_public_link(path) 
        return oc 

    
    def mkdir(self,dirName):
        oc = self._getClient() 
        oc.mkdir(dirName)

    def putfile(self,remotePath,localFile):
        self._getClient().put_file(remotePath, localFile)

    def delete(self,remotePath:str):
        ''' can be file or directory '''
        self._getClient().delete(remotePath)

    def _SharingPath(self):
        return "ALQ_sharing_dir"
    
    # def sharefile2user(self,filepath,user):
    #     # link_info = self._getClient().share_file_with_link(filepath)
    #     # return f"public link: {link_info.get_link()}"
    #     link_info = self._getClient().share_file_with_user( filepath )
    #     return f"public link: {link_info.get_link()}"

    def shareRemoteFile(self,remotepath):
        link_info = self._getClient().share_file_with_link(remotepath)
        return f"{link_info.get_link()}"


    def _uploadLocalFileOrDirectory2RemotePath(self,localPath:str,remoteDirPath:str): 
        lp = os.path.abspath(localPath) 
        basename = os.path.basename(lp)
        if not os.path.exists(lp):
            raise Exception("input path not found") 
        sharingDir = remoteDirPath
        try:
            self.delete( sharingDir ) 
        except:
            pass 
        self.mkdir( sharingDir ) 
        if os.path.isdir( lp ):
            # dir 
            remotePath = sharingDir + '/' +  f"d_{basename}.zip"
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_file = os.path.join(temp_dir, f"{basename}.zip")
                shutil.make_archive(os.path.splitext(zip_file)[0], 'zip', lp) 
                self.putfile( remotePath=remotePath, localFile=zip_file )
        else:
            # single file 
            remotePath = sharingDir + '/' + "f_" +  basename
            self.putfile( remotePath=remotePath, localFile=localPath )
        return remotePath


    # def sendshare_deprecated(self,localPath:str):
    #     '''
    #     share a local file or directory to public, other can download it by:
    #        getsharefrom <username> 
    #     '''
    #     dataPathDir = self._SharingPath() 
    #     remotePath = self._uploadLocalFileOrDirectory2RemotePath(localPath=localPath,remoteDirPath=dataPathDir) 
    #     sharedURL = self.shareRemoteFile(remotepath=remotePath) 
    #     metaDir = self._sharingUrlPath
    #     username = self._conf._getSectionDict(section="owncloud").get('username',None)
    #     if username is None:
    #         raise Exception("credition for owncloud is not set") 
    #     metaFileName = f"publicsharing_{username}.txt"
    #     with tempfile.TemporaryDirectory() as temp_dir:
    #         temp_file_path = os.path.join(temp_dir, metaFileName)
    #         with open(temp_file_path, 'w') as temp_file:
    #             temp_file.write(sharedURL)
    #         oc = Client2.from_public_link(metaDir)
    #         oc.drop_file(temp_file_path)

    def sendshare(self,localPath:str):
        '''
        share a local file or directory to public, other can download it by:
           getsharefrom <username> 
        '''
        username,password = self._getUserPass() 
        if not ( username is not None and password is not None  ):
            raise Exception('owncloud is not set')
        lp = os.path.abspath(localPath) 
        basename = os.path.basename(lp)
        poc = self._getPublicDirClient()
        if os.path.isdir( lp ):
            # dir
            meta = {
                'isdir':True, 
                'filename':f"{basename}",
            } 
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_file = os.path.join(temp_dir, f"{basename}.zip")
                shutil.make_archive(os.path.splitext(zip_file)[0], 'zip', lp) 
                poc.drop_file(zip_file)
            poc.move( f"{basename}.zip" , f"share_{username}_data" )
        else:
            meta = {
                'isdir':False, 
                'filename':f"{basename}",
            }
            # single file 
            poc.drop_file(lp) 
            poc.move( f"{basename}" , f"share_{username}_data" )
        poc.put_file_contents(remote_path=f"share_{username}_meta.txt",data=json.dumps(meta))
        return "done!"

    def getsharefrom(self,username:str):
        poc = self._getPublicDirClient() 
        metaFile = f"share_{username}_meta.txt" 
        dataFile = f"share_{username}_data"
        meta = json.loads(poc.get_file_contents(metaFile).decode())
        if meta['isdir']:
            localPath = os.path.join( os.getcwd(),meta['filename'] ) 
            with tempfile.TemporaryDirectory() as temp_dir:
                localZipFile = os.path.join(temp_dir, f"{meta['filename']}.zip")
                poc.get_file(remote_path=dataFile,local_file=localZipFile)  
                shutil.unpack_archive(localZipFile, localPath)
        else:
            localPath = os.path.join( os.getcwd(),meta['filename'] ) 
            poc.get_file(remote_path=dataFile,local_file=localPath)
        print(f"download data to: {localPath}")

    def _isPathExist(self,path):
        try:
            oc = self._getClient() 
            oc.file_info(path)
            return True 
        except:
            return False
        

    def test(self):
        self._setRemoteConfig({1:2})


    def sync(self,localPath,remotePath):
        self.rcmd( rcmd =  f"{localPath} {self._host} {remotePath}"  ) 

    def rcmd(self,rcmd):
        cmd = self._get_owncloudcli_rcmdWithConf(rcmd)
        # print(f"debug: cmd = {cmd}") 
        stdout,stderr = run_command(cmd)
        stdinfo = stdout + "\n" + stderr
        return stdinfo


