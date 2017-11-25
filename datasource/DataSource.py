import sys,os
path = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(path, '../'))
from base import do, update
from PostgresSQL import Records

initializer = {'Records': Records}

def init(name, settings):
	return initializer[name](**settings)

def get_dbs(config):
	return update(config, {"dbs":{k:init(k, v) for k,v in config.items()}})