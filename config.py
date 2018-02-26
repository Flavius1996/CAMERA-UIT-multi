'''
Configuration for camera UIT:
    + Python objects
    + load config from yml file
'''

from easydict import EasyDict as edict


############################# DEFAULT OPTIONS #########################
__C = edict()
# Consumers can get config by:
#   from config import CFG
CFG = __C

# Where to store captured frames?
__C.STORE_PATH = './CAMERA_UIT'

# Where to store logs?
__C.LOGS_PATH = './logs'

# Number of frames per second
__C.SAMPLING_RATE = 5

# Captured jpeg images quality - max=100% (non compression)
__C.IMAGE_QUALITY = 100

# Image Filename format
__C.IMAGE_FILENAME_STRINGFORMAT = '"{}_{}_{}__{}".format(camera_name, date, time, count)'
# Date, time format in filename
__C.DATE_FORMAT = "%d%m%Y"
__C.TIME_FORMAT = "%H-%M-%S"


##### CAPTURING METHOD 1: Scheduling capturing
# Start capturing time of day
  # FORMAT: HH:MM  (24H format)
__C.START_TIME = '07:00'

# End capturing time
__C.END_TIME = '08:00'

# Start capturing date
  # FORMAT: dd/MM/YYYY
__C.START_DATE = '25/02/2018'

# End capturing date
__C.END_DATE = '28/02/2018'

##### CAPTURING METHOD 2: Start capturing immediately and end after CAPTURING_TIME minutes
  # Set 0 for disable method 2, otherwise method 1 will be disable
__C.CAPTURING_TIME = 0



############################ CONFIG FUNCTIONS ################################
def _merge_a_into_b(a, b):
    """Merge config dictionary a into config dictionary b, clobbering the
    options in b whenever they are also specified in a.
    """
    if type(a) is not edict:
        return

    for k, v in a.items():
        # a must specify keys that are in b
        if not k in b:
            raise KeyError('{} is not a valid config key'.format(k))

        # the types must match, too
        old_type = type(b[k])
        if old_type is not type(v):
            raise ValueError(('Type mismatch ({} vs. {}) '
                            'for config key: {}').format(type(b[k]),
                                                        type(v), k))

        # recursively merge dicts
        if type(v) is edict:
            try:
                _merge_a_into_b(a[k], b[k])
            except:
                print('Error under config key: {}'.format(k))
                raise
        else:
            b[k] = v
            
def load_cfg_from_file(filepath):
    """Load a config yml file and merge it into the default options."""
    import yaml
    with open(filepath, 'r') as f:
        yaml_cfg = edict(yaml.load(f))

    _merge_a_into_b(yaml_cfg, __C)

    # Normalize
    if CFG.STORE_PATH[-1] != '/' or CFG.STORE_PATH[-1] != '\\':
        CFG.STORE_PATH += '/'
        
    if CFG.LOGS_PATH[-1] != '/' or CFG.LOGS_PATH[-1] != '\\':
        CFG.LOGS_PATH += '/'
    


def format_imagefilename(camera_link, camera_name, date, time, count):

    camera_ip = camera_link.split('@')[-1].split(':')[0]

    stringformat = CFG.IMAGE_FILENAME_STRINGFORMAT

    filename = eval(stringformat) + '.jpg'

    return filename



#### DEBUG ####
print(CFG)
print()
file = './cfgs/test.yml'
load_cfg_from_file(file)
print(CFG)
print(format_imagefilename('rtsp://test:12345@192.168.75.27:554', 'test','26022018', '12:04', 5))