#!/usr/bin python
# -*- coding: UTF-8 -*-

import logging
import os
import ConfigParser
import shutil
import datetime
import glob
import hashlib

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s : %(name)s -- %(message)s')
logger = logging.getLogger(__name__)
logger.info('Starting backup...')

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
logger.debug('PROJECT_PATH = {0}'.format(PROJECT_PATH))

config = ConfigParser.ConfigParser()
config.read(PROJECT_PATH + '/calendar_backup.cfg')

BACKUP_DIR = config.get('settings', 'backup_dir')
logger.debug('BACKUP_DIR = {0}'.format(BACKUP_DIR))

CALS = config.get('calendars', 'ics_list').split(',')
logger.debug('CALS = {0}'.format(CALS))

now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

for cal in CALS:
    SRC = cal.replace('"', '')
    logger.debug('SRC = {0}'.format(SRC))
    DST = BACKUP_DIR + os.path.basename(cal) + '.' + now + '.backup'
    DST = DST.replace('"', '')
    logger.debug('DST = {0}'.format(DST))
    
    z = BACKUP_DIR + os.path.basename(cal) + '*.backup'
    z = z.replace('"','')
    logger.debug('z = {0}'.format(z))
    
    filelist = glob.glob(z)
    logger.debug('filelist = {0}'.format(filelist))
    
    shutil.copy(SRC, DST)
    
    if (len(filelist)>1):
        old_backup = filelist[-2]
        logger.debug('old_backup = {0}'.format(old_backup))
        
        with open(DST, 'r') as content_file:
            content = content_file.read()
        
        new_hash = hashlib.md5()
        new_hash.update(content)
        new_hash = new_hash.hexdigest()
        logger.debug('new_hash = {0}'.format(new_hash))
        
        with open(old_backup, 'r') as content_file:
            content = content_file.read()
            
        old_hash = hashlib.md5()
        old_hash.update(content)
        old_hash = old_hash.hexdigest()
        logger.debug('old_hash = {0}'.format(old_hash))
        
        if (new_hash == old_hash):
            os.remove(DST)
