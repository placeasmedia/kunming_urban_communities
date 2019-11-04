# -*- coding: utf-8 -*-
import sqlite3
import urllib
import os
import sys
import datetime

write_dir = '/scratch/users/cchang45/rural'
sqlite_file = 'geotag.sqlite'

def _retrieve_post():
    conn = sqlite3.connect(write_dir + sqlite_file, timeout=75)
    c = conn.cursor()

    select_sql = "select images, post_id, creation_date from posts where imgdate is null limit 20;"

    c.execute(select_sql)
    records = c.fetchall()

    conn.commit()
    conn.close()

    return records

def _update_post(post_id, imgdate):
    conn = sqlite3.connect(write_dir + sqlite_file, timeout=75)
    c = conn.cursor()
    # print post_id, imgdate
    try:
        c.execute("""update posts set imgdate = ? WHERE post_id = ?;""", (imgdate, post_id))
    except Exception as e:
        print e
        pass

    conn.commit()
    conn.close()

def _insert_pic(postid, img, imgpath):
    conn = sqlite3.connect(write_dir + sqlite_file, timeout=75)
    c = conn.cursor()
    table_name = 'pictures'
    table_fields = '(post_id, image, imgpath)'
    values_string = 'VALUES(?,?,?)'
    database_command = 'INSERT INTO ' + table_name + ' ' + values_string
    print database_command
    database_values = (postid, img, imgpath)
    print database_values
    try:
        c.execute(database_command, database_values)
    except Exception as e:
        print e
        pass
    conn.commit()
    conn.close()


def _download_img(imglink, post_id, date):
    try:
        imagelink = IMAGE_BASE_LINK1 + imglink + '.jpg'
        ## form a date path
        imgdirectory = 'Picture/' + date +'/' + post_id
        if os.path.exists(write_dir + imgdirectory):
            pass
        else:
            os.mkdir(write_dir + imgdirectory, 0755)
        imgpath = write_dir + imgdirectory + '/' + imglink + '.jpg'
        urllib.urlretrieve(imagelink, imgpath)
    except:
        try:
            imagelink = IMAGE_BASE_LINK2 + imglink + '.jpg'
            urllib.urlretrieve(imagelink, imgpath)
        except:
            try:
                imagelink = IMAGE_BASE_LINK3 + imglink + '.jpg'
                urllib.urlretrieve(imagelink, imgpath)
            except:
                try:
                    imagelink = IMAGE_BASE_LINK4 + imglink + '.jpg'
                    urllib.urlretrieve(imagelink, imgpath)
                except:
                    print imagelink
                    raise
    return imgdirectory

if __name__ == "__main__":

    ## Make DIR

    path = './Picture/'

    IMAGE_BASE_LINK1 = 'http://wx1.sinaimg.cn/large/'
    IMAGE_BASE_LINK2 = 'http://wx2.sinaimg.cn/large/'
    IMAGE_BASE_LINK3 = 'http://wx3.sinaimg.cn/large/'
    IMAGE_BASE_LINK4 = 'http://wx4.sinaimg.cn/large/'

    for n in range(1000000):
        records = _retrieve_post()
        for record in records:
            image = record[0]
            post_id = record[1]
            post_id = str(post_id)
            creation_date = record[2]
            creation_date = str(creation_date)
            creation_date = creation_date[0:19] + creation_date[25:30]
            datet = datetime.datetime.strptime(creation_date, '%a %b %d %H:%M:%S %Y')
            datet = datet.strftime("%Y-%m-%d")
            if len(image) == 2:
                # print post_id, datet
                datet = 'NA'
                _update_post(post_id, datet)
            elif len(image) == 37:
                image = str(image[3:35])
                # print image, datet
                imgdirectory = _download_img(image, post_id, datet)
                _update_post(post_id, datet)
                _insert_pic(post_id, image, imgdirectory)
            elif len(image) == 74:
                image1 = str(image[3:35])
                image2 = str(image[40:72])
                # print image1, image2, datet
                imgdirectory = _download_img(image1, post_id, datet)
                imgdirectory = _download_img(image2, post_id, datet)
                _update_post(post_id, datet)
                _insert_pic(post_id, image1, imgdirectory)
                _insert_pic(post_id, image2, imgdirectory)
            elif len(image) == 111:
                # print image
                image1 = str(image[3:35])
                image2 = str(image[40:72])
                image3 = str(image[77:109])
                # print image1, image2, image3, datet
                imgdirectory = _download_img(image1, post_id, datet)
                imgdirectory = _download_img(image2, post_id, datet)
                imgdirectory = _download_img(image3, post_id, datet)
                _update_post(post_id, datet)
                _insert_pic(post_id, image1, imgdirectory)
                _insert_pic(post_id, image2, imgdirectory)
                _insert_pic(post_id, image3, imgdirectory)
            elif len(image) == 148:
                # print image
                image1 = str(image[3:35])
                image2 = str(image[40:72])
                image3 = str(image[77:109])
                image4 = str(image[114:146])
                # print image1, image2, image3, image4, datet
                imgdirectory = _download_img(image1, post_id, datet)
                imgdirectory = _download_img(image2, post_id, datet)
                imgdirectory = _download_img(image3, post_id, datet)
                imgdirectory = _download_img(image4, post_id, datet)
                _update_post(post_id, datet)
                _insert_pic(post_id, image1, imgdirectory)
                _insert_pic(post_id, image2, imgdirectory)
                _insert_pic(post_id, image3, imgdirectory)
                _insert_pic(post_id, image4, imgdirectory)
            elif len(image) == 185:
                # print image
                image1 = str(image[3:35])
                image2 = str(image[40:72])
                image3 = str(image[77:109])
                image4 = str(image[114:146])
                image5 = str(image[151:183])
                # print image1, image2, image3, image4, image5, datet
                imgdirectory = _download_img(image1, post_id, datet)
                imgdirectory = _download_img(image2, post_id, datet)
                imgdirectory = _download_img(image3, post_id, datet)
                imgdirectory = _download_img(image4, post_id, datet)
                imgdirectory = _download_img(image5, post_id, datet)
                _update_post(post_id, datet)
                _insert_pic(post_id, image1, imgdirectory)
                _insert_pic(post_id, image2, imgdirectory)
                _insert_pic(post_id, image3, imgdirectory)
                _insert_pic(post_id, image4, imgdirectory)
                _insert_pic(post_id, image5, imgdirectory)
            elif len(image) == 222:
                # print image
                image1 = str(image[3:35])
                image2 = str(image[40:72])
                image3 = str(image[77:109])
                image4 = str(image[114:146])
                image5 = str(image[151:183])
                image6 = str(image[188:220])
                # print image1, image2, image3, image4, image5, image6, datet
                imgdirectory = _download_img(image1, post_id, datet)
                imgdirectory = _download_img(image2, post_id, datet)
                imgdirectory = _download_img(image3, post_id, datet)
                imgdirectory = _download_img(image4, post_id, datet)
                imgdirectory = _download_img(image5, post_id, datet)
                imgdirectory = _download_img(image6, post_id, datet)
                _update_post(post_id, datet)
                _insert_pic(post_id, image1, imgdirectory)
                _insert_pic(post_id, image2, imgdirectory)
                _insert_pic(post_id, image3, imgdirectory)
                _insert_pic(post_id, image4, imgdirectory)
                _insert_pic(post_id, image5, imgdirectory)
                _insert_pic(post_id, image6, imgdirectory)
            elif len(image) == 259:
                # print image
                image1 = str(image[3:35])
                image2 = str(image[40:72])
                image3 = str(image[77:109])
                image4 = str(image[114:146])
                image5 = str(image[151:183])
                image6 = str(image[188:220])
                image7 = str(image[225:257])
                # print image1, image2, image3, image4, image5, image6, image7, datet
                imgdirectory = _download_img(image1, post_id, datet)
                imgdirectory = _download_img(image2, post_id, datet)
                imgdirectory = _download_img(image3, post_id, datet)
                imgdirectory = _download_img(image4, post_id, datet)
                imgdirectory = _download_img(image5, post_id, datet)
                imgdirectory = _download_img(image6, post_id, datet)
                imgdirectory = _download_img(image7, post_id, datet)
                _update_post(post_id, datet)
                _insert_pic(post_id, image1, imgdirectory)
                _insert_pic(post_id, image2, imgdirectory)
                _insert_pic(post_id, image3, imgdirectory)
                _insert_pic(post_id, image4, imgdirectory)
                _insert_pic(post_id, image5, imgdirectory)
                _insert_pic(post_id, image6, imgdirectory)
                _insert_pic(post_id, image7, imgdirectory)
            elif len(image) == 296:
                # print image
                image1 = str(image[3:35])
                image2 = str(image[40:72])
                image3 = str(image[77:109])
                image4 = str(image[114:146])
                image5 = str(image[151:183])
                image6 = str(image[188:220])
                image7 = str(image[225:257])
                image8 = str(image[262:294])
                # print image1, image2, image3, image4, image5, image6, image7, image8, datet
                imgdirectory = _download_img(image1, post_id, datet)
                imgdirectory = _download_img(image2, post_id, datet)
                imgdirectory = _download_img(image3, post_id, datet)
                imgdirectory = _download_img(image4, post_id, datet)
                imgdirectory = _download_img(image5, post_id, datet)
                imgdirectory = _download_img(image6, post_id, datet)
                imgdirectory = _download_img(image7, post_id, datet)
                imgdirectory = _download_img(image8, post_id, datet)
                _update_post(post_id, datet)
                _insert_pic(post_id, image1, imgdirectory)
                _insert_pic(post_id, image2, imgdirectory)
                _insert_pic(post_id, image3, imgdirectory)
                _insert_pic(post_id, image4, imgdirectory)
                _insert_pic(post_id, image5, imgdirectory)
                _insert_pic(post_id, image6, imgdirectory)
                _insert_pic(post_id, image7, imgdirectory)
                _insert_pic(post_id, image8, imgdirectory)
            elif len(image) == 333:
                # print image
                image1 = str(image[3:35])
                image2 = str(image[40:72])
                image3 = str(image[77:109])
                image4 = str(image[114:146])
                image5 = str(image[151:183])
                image6 = str(image[188:220])
                image7 = str(image[225:257])
                image8 = str(image[262:294])
                image9 = str(image[299:331])
                # print image1, image2, image3, image4, image5, image6, image7, image8, image9, datet
                imgdirectory = _download_img(image1, post_id, datet)
                imgdirectory = _download_img(image2, post_id, datet)
                imgdirectory = _download_img(image3, post_id, datet)
                imgdirectory = _download_img(image4, post_id, datet)
                imgdirectory = _download_img(image5, post_id, datet)
                imgdirectory = _download_img(image6, post_id, datet)
                imgdirectory = _download_img(image7, post_id, datet)
                imgdirectory = _download_img(image8, post_id, datet)
                imgdirectory = _download_img(image9, post_id, datet)
                _update_post(post_id, datet)
                _insert_pic(post_id, image1, imgdirectory)
                _insert_pic(post_id, image2, imgdirectory)
                _insert_pic(post_id, image3, imgdirectory)
                _insert_pic(post_id, image4, imgdirectory)
                _insert_pic(post_id, image5, imgdirectory)
                _insert_pic(post_id, image6, imgdirectory)
                _insert_pic(post_id, image7, imgdirectory)
                _insert_pic(post_id, image8, imgdirectory)
                _insert_pic(post_id, image9, imgdirectory)


