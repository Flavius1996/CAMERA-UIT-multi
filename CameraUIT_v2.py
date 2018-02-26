'''
# --------------------------------------------------------
# UIT Dataset - UIT Camera capturing (multiple cameras)
#
#   Extract frame from UIT camera stream
#
#  Additional Libaries:
#        opencv-python
#        schedule - scheduluing tasks - install: pip install schedule
#        easydict
#
#
# @author: Hoang Huu Tin
# --------------------------------------------------------
'''

import cv2
import os
import argparse
import time, datetime
from threading import Thread

import schedule        # install by: pip install schedule

from config import CFG, load_cfg_from_file, format_imagefilename
from load_camera import CAMERA_LIST, load_camera_from_file
import sys

def checkCamera(link, name):
    '''check to see if capturing camera work'''
    vidcap = cv2.VideoCapture(link)
    success, image = vidcap.read()  
    
    date = time.strftime(CFG.DATE_FORMAT)
    time_hms = time.strftime(CFG.TIME_FORMAT)
    name = format_imagefilename(link, name, date, time_hms, 0) 
    test_img_path = './test_imgs' + name

    cv2.imwrite(test_img_path, image)

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

def ExtractFrame_FromCameraLink(camera_link, camera_name, start_datetime, end_datetime):
    '''
        Extract keyframes from camera stream with sampling rate (number of frames will be taken per second)
        Example:
            sampling rate = 0.5
                => extract 1 keyframe after 2 seconds
    '''

    ############################# INIT local folders ############################################## 
    
    # START TIME TRIGGER
    now = datetime.datetime.now()
    if now < start_datetime:
        return

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
            
            if (count_kf % 100 == 0) or (count_kf == 1):    
                print('\t[{}] - frame {}: Extracting at time: {}'.format(camera_name, count_kf, time.strftime("%H:%M:%S")))
            
            time_hms = time.strftime(CFG.TIME_FORMAT)
            imgfilepath = camera_name + "/" + folder_day + "/" 
            imgfilepath += format_imagefilename(camera_link, camera_name, date, time_hms, count_kf)
            cv2.imwrite(imgfilepath, image, [int(cv2.IMWRITE_JPEG_QUALITY), CFG.IMAGE_QUALITY])
                
        # Check end time
        cur_t = datetime.datetime.now()
        if cur_t > end_datetime:
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

def INIT():
    '''Initialize'''

    if not os.path.exists(CFG.STORE_PATH):
        os.mkdir(CFG.STORE_PATH)

    if not os.path.exists(CFG.LOGS_PATH):
        os.mkdir(CFG.LOGS_PATH)

    if not os.path.exists('./test_imgs'):
        os.mkdir('./test_imgs')

def main():
    
    args = parse_args()
    print('Called with args:')
    print(args)

    if args.cfg_file is not None:
        load_cfg_from_file(args.cfg_file)
    if args.camera_file is not None:
        load_camera_from_file(args.camera_file)

    INIT()

    # Print screen
    print("="*20 + 'Capturing frames from UIT CAMERA' + "="*20)
    print('Store path: {}'.format(CFG.STORE_PATH))
    print('Logs path: {}'.format(CFG.LOGS_PATH))
    print('Sampling rate: {} frames/s'.format(CFG.SAMPLING_RATE))
    print('Image quality: {}'.format(CFG.IMAGE_QUALITY))
    print('Filename format: {}'.format(CFG.IMAGE_FILENAME_STRINGFORMAT))
    print('Date format: {}'.format(CFG.DATE_FORMAT))
    print('Time format: {}'.format(CFG.TIME_FORMAT))
    print('Start time: {}'.format(CFG.START_TIME))
    print('End time: {}'.format(CFG.END_TIME))
    
    
    print('\nChecking capturing cameras...')
    for camera in CAMERA_LIST:
        print('Camera: {}'.format(camera['name']))
        print('Link: {}'.format(camera['link']))
        if checkCamera(camera['link'], camera['name']):
            print('Status: OK!')
            print()
        else:
            # Dummy code, above exception in checkCamera() will print error message instead of this
            print('Something error!')    
            return
    print('Check test images in ./test_imgs folder.')

    if CFG.CAPTURING_TIME != 0:
        # CAPTURING METHOD 2: start rightnow, end after X minutes
        plus_minute = int(CFG.CAPTURING_TIME)
        start_datetime = datetime.datetime.now()
        end_datetime = start_datetime + datetime.timedelta(minutes = plus_minute)

        for camera in CAMERA_LIST:
            thread1 = Thread(target = ExtractFrame_FromCameraLink, args = (camera['link'], camera['name'], start_datetime, end_datetime))
            thread1.start()

    else:
        # CAPTURING METHOD 1: scheduling task
        print('\nCurrent system time is: {}'.format(time.strftime("%H:%M:%S")))
        print('Waiting to start time ...')
        
        schedule.every().day.at(CFG.start_time).do(ExtractFrame_FromCameraLink, args.camera_link, 
                              args.camera_name)
        
        while True:
            schedule.run_pending()
            time.sleep(1) # wait 1s
    

if __name__ == '__main__':
    main()