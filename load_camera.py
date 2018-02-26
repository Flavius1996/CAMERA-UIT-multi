'''
CAMERA information:
    + camera name (unique for each camera)
    + camera link
'''


import xml.etree.ElementTree as ET

CAMERA_LIST = []

def check_validname():
    '''check if all names in CAMERA_LIST is unique'''
    global CAMERA_LIST

    name_list = [t['name'] for t in CAMERA_LIST]
    duplicate = set([x for x in name_list if name_list.count(x) > 1])

    if (duplicate is not None and len(duplicate) == 0):
        return True
    else:
        raise ValueError('All camera \'name\' in the file must be unique. \
            \nThese name is duplicated: {}'.format(duplicate))


def load_camera_from_file(filepath):
    """Load camera info from xml file."""
    global CAMERA_LIST

    tree = ET.parse(filepath)
    data = tree.getroot()

    for camera in data:
        if 'name' not in camera.attrib:
            raise KeyError('Camera does\'t have attribute: \'name\'')

        temp = camera.attrib
        for att in camera:
            temp[att.tag] = att.text
        CAMERA_LIST.append(temp)

    check_validname()


# Debug
# load_camera_from_file('./camera_info/test.xml')
# print(CAMERA_LIST)