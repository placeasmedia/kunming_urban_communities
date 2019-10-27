# -*- coding: utf-8 -*-
'''
Download Baidu panoroma pictures
'''

import csv
import urllib
import os
import sys
import time
import datetime
import random
import requests
import shutil
import timeit

write_dir = './baidu/'
GPS_points = 'km_search_pts_1.csv'

API_count = 0

start = timeit.default_timer()

def _download_img(IMAGE_BASE_LINK, lat, lng, pitch, heading, gid):
    url = IMAGE_BASE_LINK
    url += '&location='+ str(lng) + ',' + str(lat)
    url += '&pitch=' + str(pitch)
    url += '&heading=' +str(heading)
    # url += '&coordtype=wgs84ll'
    url += '&coordtype=gcj02'
    url += '&ak=APIKey'
    url += '&width=1024'
    url += '&height=512'
    url += '&fov=90'
    print url

    try:
        imagelink = gid + '_' + str(heading) + '_' + str(pitch) + '.jpg'
        imgdirectory = gid
        if os.path.exists(write_dir + '/' + imgdirectory):
            print write_dir + '/' + imgdirectory
            pass
        else:
            os.mkdir(write_dir + '/' + imgdirectory, 0755)
        imgpath = write_dir + '/' + imgdirectory + '/' + imagelink
        print "image saving path..."
        print imgpath
        if os.path.isfile(imgpath):
            print imgpath
            return 'NA'
        else:
            urllib.urlretrieve(url, imgpath)
    except:
        time.sleep(random.uniform(1, 2))
        try:
            imagelink = gid + '_' + str(heading) + '_' + str(pitch) + '.jpg'
            imgdirectory = gid
            if os.path.exists(write_dir + '/' + imgdirectory):
                print write_dir + '/' + imgdirectory
                pass
            else:
                os.mkdir(write_dir + '/' + imgdirectory, 0755)

            imgpath = write_dir + '/' + imgdirectory + '/' + imagelink
            print imgpath
            if os.path.is_file(imgpath):
                print imgpath
                return 'NA'
            else:
                try:
                    urllib.urlretrieve(url, imgpath)
                except:
                    try:
                        r = requests.get(url, stream=True)
                        with open(imgpath, 'w') as f:
                            shutil.copyfileobj(r.raw, f)
                    except:
                        try:
                            r = requests.get(url, timeout=20, stream=True)
                            with open(imgpath, 'w') as f:
                                shutil.copyfileobj(r.raw, f) 
                        except:
                            return 'NA'

        except:
            return 'NA'

    return imgpath


if __name__ == "__main__":

    IMAGE_BASE_LINK = 'https://api.map.baidu.com/panorama/v2?'

    # test if it reaches API limit per day
    if API_count < 100:
        pass
    else:
        stop = timeit.default_timer()
        resttime = 24*60*60 - (stop - start)
        if resttime > 0:
            time.sleep(resttime)
        API_count = 0

    with open('./' + GPS_points,'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            gid = row[0]
            latitude = row[2]
            longitude = row[1]

            current_time = str(datetime.datetime.now())
            current_date = current_time.split(' ')[0]

            # initial heading
            heading = 45
            pitch = 15
            turn = 0
            while turn < 4:
                imgpath = _download_img(IMAGE_BASE_LINK, latitude, longitude, pitch, heading, gid)
                if imgpath == 'NA':
                    pass
                else:
                    print(gid, latitude, longitude, pitch, heading, imgpath)
                heading += 90
                turn += 1
                time.sleep(random.uniform(0, 1))

    print("done!")
