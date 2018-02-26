'''
# --------------------------------------------------------
# UIT Dataset - UIT Camera capturing (multiple cameras)
#
#   Extract frame from UIT camera stream
#
#  Additional Libaries:
#        python-opencv
#        schedule - scheduluing tasks - install: pip install schedule
#        pydrive - google drive lib - install: pip install pydrive
#
#
#
# @author: Hoang Huu Tin
# --------------------------------------------------------
'''

import cv2
import os
import argparse
import time
from threading import Thread

import schedule        # install by: pip install schedule

from config import CFG, load_cfg_from_file, format_imagefilename
from load_camera import CAMERA_LIST, load_camera_from_file
import sys

def checkCamera(link):
    '''check to see if capturing camera work'''
    vidcap = cv2.VideoCapture(link)
    success, image = vidcap.read()  
    
    cv2.imwrite('test.jpg', image)

    print("Camera info: ")
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    # Get fps of video
    if int(major_ver)  < 3 :
        fps = int(round(vidcap.get(cv2.cv.CV_CAP_PROP_FPS)))
        print ("\tCamera\'s fps: {0}".format(fps))
    else :
        fps = int(round(vidcap.get(cv2.CAP_PROP_FPS)))
        print ("\tCamera\'s fps: {0}".format(fps))
    print('\tCamera\'s width = {}'.format(int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))))
    print('\tCamera\'s height = {}'.format(int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    
    vidcap.release()

    return success

def ExtractFrame_FromCameraLink(camera_link, camera_name = 'test'):
    '''
        Extract keyframes from camera stream with sampling rate (number of frames will be taken per second)
        Example:
            sampling rate = 0.5
                => extract 1 keyframe after 2 seconds
    '''

    ############################# INIT local folders ############################################## 
    
    # Get date info
    date = time.strftime(CFG.DATE_FORMAT)
    start_time = time.strftime("%H:%M:%S")    # Use for log
    
    sampling_rate = float(CFG.SAMPLING_RATE)

    if not os.path.exists(camera_name):
        os.mkdir(camera_name)
  
    # Create sub-folder for each day in local disk
    folder_day = date
    if not os.path.exists(camera_name + '/' + folder_day):
        os.mkdir(camera_name + '/' + folder_day)
    
    # End time by integer format
    end_t = int(CFG.end_time.replace(':', ''))
  
    
    ############################# Calculate framestep ############################################## 
    # opencv video capture
    vidcap = cv2.VideoCapture(camera_link)
    success,image = vidcap.read()
    success = True
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    # Get fps of video
    if int(major_ver)  < 3 :
        fps = int(round(vidcap.get(cv2.cv.CV_CAP_PROP_FPS)))
    else :
        fps = int(round(vidcap.get(cv2.CAP_PROP_FPS)))
        
    framestep = max(1, min(int(round(fps / sampling_rate)), int(fps)))
    
    
    print("="*40)
    print('Extract frames from UIT CAMERA')
    print("Date: {}".format(time.strftime("%d/%m/%Y")))
    print("Camera Link: {}".format(camera_link))
    print("Sampling rate: {} frames/sec".format(sampling_rate))
    print ("Camera\'s fps: {0}".format(fps)) 
    print('framestep = {} - extract one frame after each framestep'.format(framestep))

        
    # count keyframe
    count_kf = 0
    # count loop
    count = 0
    
    ############################# CAPTURING LOOP ############################################## 
    # loop through all frame, only get frame with sampling_rate
    while success:
        success,image = vidcap.read()
         
        if (count % framestep == 0):
            count_kf += 1  
            
            if (count_kf % 20 == 0) or (count_kf == 1):    
                print('\t{}: Extracting at time: {}'.format(count_kf, time.strftime("%H:%M:%S")))
            
            time_hms = time.strftime(CFG.TIME_FORMAT)
            imgfilepath = camera_name + "/" + folder_day + "/" 
            imgfilepath += format_imagefilename(camera_link, camera_name, date, time_hms, count_kf)
            cv2.imwrite(imgfilepath, image, [int(cv2.IMWRITE_JPEG_QUALITY), CFG.IMAGE_QUALITY])
                
        # Check end time
        cur_t = int(time.strftime("%H%M"))
        if cur_t >= end_t:
            break
        
        count += 1

    vidcap.release()
    
    print("="*40)
    print('\nDone!\nDay: {}\nTotal frames ={}'.format(date, count_kf))
    print('Local folder: {}'.format(folder_day))

    # Writing Log
    log_filename = date + '_' + camera_name
    log_path = CFG.LOGS_PATH + log_filename
    with open(log_path, "a") as log:
        log.write("="*40 + '\r\n')
        log.write("Date: {}\r\n".format(date))
        log.write('Camera name: {}\r\n'.format(camera_name))
        log.write('Camera link: {}\r\n'.format(camera_link))
        log.write('Sampling rate: {} frames/s\r\n'.format(sampling_rate))
        log.write('Start time: {}\r\n'.format(start_time))
        log.write('End time: {}\r\n'.format(CFG.end_time))
        log.write('Image quality: {}\r\n'.format(CFG.IMAGE_QUALITY))
        log.write('\r\nTotal captured frames = {}\r\n'.format(count_kf))
        
def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Keyframes Extraction from Video')
    parser.add_argument('--cfg', dest='cfg_file',
                        help='optional config file (.yml file)',
                        default=None, type=str)
    parser.add_argument('--camera', dest='camera_file',
                        help='camera info file (.xml file)',
                        default=None, type=str)

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return args

def main():
    
    args = parse_args()
    print('Called with args:')
    print(args)

    if args.cfg_file is not None:
        load_cfg_from_file(args.cfg_file)
    if args.camera_file is not None:
        load_camera_from_file(args.camera_file)

    # Print screen
    print("="*20 + 'Capturing frames from UIT CAMERA' + "="*20)
    print('Camera name: {}'.format(CFG.camera_name))
    print('Camera link: {}'.format(CFG.camera_link))
    print('Sampling rate: {} frames/s'.format(CFG.sampling_rate))
    print('Start time: {}'.format(CFG.start_time))
    print('End time: {}'.format(CFG.end_time))
    print('Image quality: {}'.format(CFG.image_quality))
        
    print('\nChecking capturing camera...')
    if checkCamera(args.camera_link):
        print('Capturing status: OK!')
        print('Check file test.jpg for testing result.')
    else:
        print('Something error!')    # Dummy code, above exception in checkCamera() will print error message instead of this
        return
        
    print('\nCurrent system time is: {}'.format(time.strftime("%H:%M:%S")))
    print('Waiting to start time ...')
    
    # DEBUG
    #LINK = "rtsp://test:12345@192.168.75.27:554"
    #camera_name = "Front_MMLAB"
    #end_t = int(args.end_time.replace(':', ''))

    schedule.every().day.at(CFG.start_time).do(ExtractFrame_FromCameraLink, args.camera_link, 
                          args.camera_name)
    
    while True:
        schedule.run_pending()
        time.sleep(1) # wait 1s
    

if __name__ == '__main__':
    main()