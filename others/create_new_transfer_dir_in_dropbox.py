import ConfigParser
import datetime
import logging
import os

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s : %(name)s -- %(message)s')
logger = logging.getLogger(__name__)


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
logger.debug('PROJECT_PATH = {}'.format(PROJECT_PATH))

config = ConfigParser.ConfigParser()
config.read(os.path.join(PROJECT_PATH, 'create_new_transfer_dir_in_dropbox.conf'))

TRANSFER_DIR = config.get('settings', 'transfer_dir')
logger.debug('BACKUP_DIR = {}'.format(TRANSFER_DIR))

now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

NEW_DIR = os.path.join(TRANSFER_DIR, now)
os.makedirs(NEW_DIR)

logger.info("{} was created.".format(NEW_DIR))
