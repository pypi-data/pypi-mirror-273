
from __future__ import annotations
from pathlib import Path
import os 
import configparser
import pprint 



class ReadWriteini():

    def __init__(self,filePath:str):
        self.fp = filePath

    def get(self):
        if not os.path.exists( self.fp ):
            return {} 
        config = configparser.ConfigParser()
        config.read( self.fp )
        return self._config_to_dict( config )
    
    def set(self,data):
        conf = self._dict_to_config(data)
        with open(self.fp, 'w') as configfile:
            conf.write(configfile)

    @staticmethod
    def _config_to_dict(config):
        # by GPT 
        config_dict = {}
        for section in config.sections():
            config_dict[section] = {}
            for option in config.options(section):
                config_dict[section][option] = config.get(section, option)
        return config_dict

    @staticmethod
    def _dict_to_config(config_dict):
        # by GPT
        config = configparser.ConfigParser()
        for section, options in config_dict.items():
            config[section] = options
        return config



class Configuration:

    def __init__(self):
        self._wr = ReadWriteini( self._get_user_config_file() )

    @staticmethod
    def _get_user_config_file():
        HOME = str( Path.home() ) 
        Dir = os.path.join(HOME,'.config')
        filePath = os.path.join( Dir, 'alq_tool.ini' ) 
        try:
            os.makedirs(Dir)
        except:
            pass 
        return filePath

    def _set(self,section,key,val):
        data = self._wr.get()
        if section not in data:
            data[section] = {} 
        data[section][key] = val 
        self._wr.set(data) 
        return self
    
    def _getSectionDict(self,section,default={} ):
        data = self._wr.get()
        return data.get(section,default) 

    def print(self):
        """print all configurations
        """   
        res = [] 
        data = self._wr.get()
        for section in data:
            res.append(f"---[{section}]---")
            for k in data[section]:
                res.append(f"{k} = {data[section][k]}")
        return res


    

    

