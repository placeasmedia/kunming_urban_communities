'''
Collecting weibo by using Weibo nearby API and random points
generated within the city's limit 2013

save in postgresql
'''

import urllib2
import json
import csv
import codecs
import time, timeit
import numpy
import socket
import psycopg2
import psycopg2.extras
import csv, codecs, cStringIO
from httplib import BadStatusLine

# global timeout in seconds
socket.setdefaulttimeout(30)

url_nearby_timeline_base = 'https://api.weibo.com/2/place/nearby_timeline.json?'

Weibo_Base_Url = url_nearby_timeline_base


start_lat = 25.27
start_lng = 102.07
end_lat = 24.29
end_lng = 103.74
list_lat = numpy.arange(end_lat, start_lat, 0.004)
list_lng = numpy.arange(start_lng, end_lng, 0.004)

class APIError(StandardError):
    '''
    raise APIError if got failed json message.
    '''
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)

def _insert_weibo_sql(lat, lng, wid, uid, gender, followers_count, friends_count, statuses_count, weekday, month, day, year, daytimed,created_at, user_province, user_city, geo_enabled, content, source):
    _insert_sql = "INSERT INTO kunming (latitude, longitude, wid, uid, gender, followers_count, friends_count,statuses_count, "\
                  "weekday, month, day, year, daytime, created_at, province, city, geo_enable, content, source) VALUES"\
                  "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (lat, lng, wid, uid, gender, followers_count, \
                                                                                                friends_count, statuses_count, weekday, month, day, \
                                                                                                year, daytimed, created_at, user_province, user_city, geo_enabled, content, source)
    return _insert_sql
    
 
def _retrieve_record(field1, value1, field2, value2, field3, value3, field4, value4, field5, value5):
    '''
    retrieve record from database for checking duplicates
    '''
    conn_string = "host='localhost' dbname='weiboDB' user='postgres' password='postgres'"
    # print the connection string we will use to connect
    ##print "Retrieve records: connecting to database\n	->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()


    cursor.execute("SELECT * FROM kunming WHERE %s = \'%s\' and %s = \'%s\' and %s = \'%s\' and %s = \'%s\' and %s = \'%s\'" % (field1, value1, \
                                                                                                                                 field2, value2, \
                                                                                                                                 field3, value3,\
                                                                                                                                 field4, value4,\
                                                                                                                                 field5, value5))

    # retrieve the records from the database
    records = cursor.fetchall()

    return records

def _insert_record(lat,lng,wid,uid,gender,followers_count,friends_count,statuses_count,weekday,month, day, year,daytimed,created_at, user_province, user_city, geo_enabled, content, source):

        conn_string = "host='localhost' dbname='weiboDB' user='postgres' password='postgres'"
        # print the connection string we will use to connect
        ##print "Insert records: connecting to database to insert \n	->%s" % (conn_string)

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()

        # Insert into table without escaping values (not recommended)
        ##cursor.execute("INSERT INTO my_table (sku, price) VALUES ('" + sku + "', '" + str(cost) + "')")

        # Insert into table, properly escaping values (recommended)
        ##cursor.execute("INSERT INTO my_table (sku, price) VALUES (%s, %s)", (sku, cost,))
        weibo_sql = _insert_weibo_sql(lat,lng,wid,uid,gender,followers_count,\
                                      friends_count,statuses_count,weekday,month,\
                                      day, year, daytimed, created_at, user_province, user_city,\
                                      geo_enabled, content, source)

        print weibo_sql

        cursor.execute(weibo_sql)

        # Another example inserting and properly escaping, while casting to appropriate data types
        ##cursor.execute("INSERT INTO my_table (sku, price) VALUES (%(str)s, %(int)s)", (sku, cost,))
        # After we've inserted our row, we must then perform a commit() to save the transaction.
        conn.commit()


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


# Change API
def _reach_API_hour_limit(count):

    count = count % 1000
    # Customize your APIs

    if (count > 0) and (count < 150):
        access_token = '&access_token=API1'
    elif (count >= 150 and count < 300):
        access_token = '&access_token=API2'
    elif (count >= 300 and count < 450):
        access_token = '&access_token=API3'
    elif (count >= 450 and count < 600):
        access_token = '&access_token=API4'
    elif (count >= 600 and count < 750):
        access_token = '&access_token=API5'
    elif (count >= 750 and count < 900):
        access_token = '&access_token=API6'
    elif (count >=900 and count < 1000):
        access_token = '&access_token=API7'
    else:
        print "reach the limit, reset access token"
        count = 1
        # print "sleep an hour"
        time.sleep(3600)
        # reset
        access_token = '&access_token=API1'
        
        #time.sleep(2000)
        
    return (count, access_token)
    


if __name__ == '__main__':

    # Initialize global variables
    count = 1
    access_token = ''
    start = timeit.default_timer()
    
    for num1 in range(0, len(list_lat)):
        for num2 in range(0, len(list_lng)):

            print "processing point %s and %s" %(num1, num2)

            # Check if reach Weibo's limit
            count, access_token = _reach_API_hour_limit(count)
        
            # Geographical coordinates
            point_coordinates = 'long='+ str(list_lng[num2]) + '&lat=' + str(list_lat[num1])

            # Search radius, unit meter
            radius = '&range=1000'

            # sort by distance
            sort_by_distance = '&sort=1'

            # record per page
            record_per_page = '&count=50'

            # page: default (minimum) is 1
            page = '&page='

            try:

                # initial max_page_number
                max_page_number = 400
                countDuplicates = 0
                
                # the maximum pages set to 15 -- that is 150 posts in total
                for page_no in range(1, max_page_number):
                    
                    count,access_token = _reach_API_hour_limit(count)

                    if (countDuplicates > 48): # at lease 9 out of 10 tweets are duplicate
                        
                        print countDuplicates
                        print "too many duplicates, move to next point"
                        countDuplicates = 0
                        break

                    else:             
                        url = Weibo_Base_Url + point_coordinates + radius + sort_by_distance + record_per_page + access_token + page + str(page_no)
                        get_url = urllib2.urlopen(url, timeout=40)
                        get_url_u = get_url.read()
                        try:
                            get_tweets = json.loads(get_url_u)
                        except ValueError:
                            break

                        # increment count
                        count = count + 1
                        # record duplicated tweet
                        countDuplicates = 0
                
                        if (get_tweets):
                            results = get_tweets['statuses']
                            if (results):
                                print 'length of the results is...', len(results)

                                for n in range(len(results)):
                                    geo = results[n]['geo']
                                    if(geo):
                                        coordinates = geo['coordinates']
                                        lat = coordinates[0]
                                        lng = coordinates[1]

                                        ## time in Beijing time
                                        sent_time = results[n]['created_at']

                                        if len(sent_time) >= 30:
                                            weekday = sent_time[0:3]
                                            month = sent_time[4:7]
    
                                            if month == 'Jan':
                                                monthd = '01'
                                            elif month == 'Feb':
                                                monthd = '02'
                                            elif month == 'Mar':
                                                monthd = '03'
                                            elif month == 'Apr':
                                                monthd = '04'
                                            elif month == 'May':
                                                monthd = '05'
                                            elif month == 'Jun':
                                                monthd = '06'
                                            elif month == 'Jul':
                                                monthd = '07'
                                            elif month == 'Aug':
                                                monthd = '08'
                                            elif month == 'Sep':
                                                monthd = '09'
                                            elif month == 'Oct':
                                                monthd = '10'
                                            elif month == 'Nov':
                                                monthd = '11'
                                            else:
                                                monthd = '12'
                                            day = sent_time[8:10]

                                        
                                            daytime = sent_time[11:19]

                                            hour = daytime[0:2]
                                            minute = daytime[3:5]
                                            second = daytime[6:8]

                                        

                                            daytimed = int(hour) + int(minute)/60.0 + int(second)/3600.0

                                        
                                            timezone = sent_time[20:25]
                                            year = sent_time[26:30]

                                            created_at = '\'' + year + '_' + monthd + '_' + day + ' ' + daytime + ' ' + timezone + '\''
                                        else:
                                            weekday = 'NAN'
                                            month = 'NAN'
                                            day = 'NA'
                                            daytime = '0'
                                            timezone = 'NAN'
                                            year = 'NONE'
                                            print "Wrong format of sent_time! Sent_time is %s" %(sent_time)
                                            

                                        ## weibo id
                                        wid = results[n]['id']                                            

                                        ## user id
                                        uid = results[n]['user']['id']

                                        ## user name
                                        user_name = results[n]['user']['name']
                                            
                                        ## user location
                                        user_location = results[n]['user']['location']

                                        ## user_gender
                                        gender = results[n]['user']['gender']

                                        ## favorited: whether it is favorited
                                        favorited = results[n]['favorited']

                                        if favorited:
                                            favorited = 1
                                        else:
                                            favorited = 0

                                        ## whether truncated
                                        truncated = results[n]['truncated']

                                        if truncated:
                                            truncated = 1
                                        else:
                                            truncated = 0

                                        ## The reply's id
                                        in_reply_to_status_id = results[n]['in_reply_to_status_id']

                                        ## User's id of the replyer
                                        in_reply_to_user_id = results[n]['in_reply_to_user_id']

                                        ## user_follower_count
                                        followers_count = results[n]['user']['followers_count']

                                        ## user_friends_count
                                        friends_count = results[n]['user']['friends_count']

                                        ## user_status count
                                        statuses_count = results[n]['user']['statuses_count']
                                    
                                        ## user's province
                                        user_province = results[n]['user']['province']

                                        ## user's city
                                        user_city = results[n]['user']['city']

                                        ## whether geo_enabled
                                        geo_enabled = results[n]['user']['geo_enabled']

                                        if geo_enabled:
                                            geo_enabled = 1
                                        else:
                                            geo_enabled = 0

                                        ## whether verified
                                        verified = results[n]['user']['verified']

                                        if verified:
                                            verified = 1
                                        else:
                                            verified = 0

                                        ## verified type
                                        verified_type = results[n]['user']['verified_type']
                                            
                                        ## content
                                        content = results[n]['text']

                                        ## devide user use
                                        source = results[n]['source']


                                        field1 = 'latitude'
                                        field2 = 'longitude'
                                        field3 = 'daytime'
                                        field4 = 'uid'
                                        field5 = 'wid'
                                        record = _retrieve_record(field1, str(lat), field2, str(lng), field3, str(daytimed), field4, str(uid),field5, str(wid))

                                    
                                        if len(record) > 0:
                                            print "Duplicates removed"
                                            ##print 'latitude, longitude, and sent time are {0}, {1}, {2}'.format(str(lat), str(lng), str(daytimed))
                                            countDuplicates = countDuplicates + 1
                                                    
                                        else:
                                        #print content
                                            content = content.replace('\'','_')
                                            content = content.replace('\"','__')
                                            gender = '\'' + gender + '\''
                                            weekday = '\''  + weekday +'\''
                                            month = '\''  + month + '\''
                                            content = '\'' + content +'\''
                                            source = source[(source.find('>')+1):]
                                            source = source[:source.find('<')]
                                            source = source.replace('\'','_')
                                            source = source.replace('\"','__')
                                            source = '\'' + source + '\''
                                            if len(content) > 300:
                                                print "content is too long %s" %(content)
                                            elif len(source) > 80:
                                                print "source is too long %s"%(source)
                                            else:
                                                _insert_record(lat,lng,wid,uid,gender,followers_count,\
                                                               friends_count,statuses_count,weekday,month,\
                                                               day,year,daytimed,created_at, user_province, user_city,\
                                                               geo_enabled, content, source)
                                            print "access count is %s"%(count)
                    # if the page doesn't have any content
                    # break the inner loop
                        else:
                            break


                                    
            except urllib2.URLError, e:
                print "Url reading timeout!"
                print url
                count = count + 1
                if hasattr(e, "code") and e.code == 403:
##             if hasattr(e, "code") and e.code == 10023:
                    print('Warning: Url load error {} for url {}'.format(e.code, url))
                    time.sleep(60)
            except urllib2.HTTPError, e:
                print "Http reading timeout!"
                print url
            except socket.error:
                print "Socket Timeout!"
                print url
            except RuntimeError,e:
                print e.message
            except BadStatusLine:
                print "could not fetch %s" % url
    
    print 'done!'

