# -*- coding: utf-8 -*-

import random
import requests
import datetime
import sys
import sqlite3
import os
import urllib
import time
import sqlite3

reload(sys)
sys.setdefaultencoding('utf-8')
USER_AGENTS_FILE = 'user_agents.txt'

# Helper function to return UNIX time.
def get_unix_time(year, month, day, hours, minutes):
	return datetime.datetime(year, month, day, hours, minutes).strftime('%s')

# Helper function to oad user agents.
def load_user_agents(uafile=USER_AGENTS_FILE):
    """
    uafile : string
        path to text file of user agents, one per line
    """
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1-1])
    random.shuffle(uas)
    return uas

# Get a new proxy.
def get_new_proxy():
	url = 'http://gimmeproxy.com/api/getProxy?get=true&anonymityLevel=1&maxCheckPeriod=3600'
	r = requests.get(url)
	rjson = r.json()
	print rjson
	return rjson.get("ip")

def load_init_proxies():
	fin = open('ip_list.tsv', 'rb')
	print('hello')
	for line in fin:
		print line.strip()

# Filter request through proxy
def proxy_request(url, uas, proxy_ip):
	proxy = {"http": proxy_ip}
	ua = random.choice(uas)
	headers = {"Connection" : "close", "User-Agent" : ua}
	r = requests.get(url, proxies=proxy, headers=headers)
	return r

# Construct baseline URL with input.
def construct_url(token, lat, lon, starttime, endtime):
	url = 'https://api.weibo.com/2/place/nearby_timeline.json?'
	url += 'access_token=' + str(token)
	url += '&lat=' + str(lat)
	url += '&long=' + str(lon)
	url += '&range=11000'
	#url += '&starttime=' + str(starttime)
	#url += '&endtime=' + str(endtime)
	url += '&count=50'
	
	return url

# Get data for URL.
def get_url_request(url, uas, proxy_ip):
	remaining = True 
	current_statuses = []
	page_num = 1
	while remaining:
		try:
			url_data = proxy_request(url, uas, proxy_ip)
			url_data_json = url_data.json()
			#print url_data_json.get('error_code')
			statuses = url_data_json.get('statuses')
			#print len(statuses)
			for status in statuses:
				current_statuses.append(status)
		except Exception as e:
			return current_statuses
		#print len(current_statuses)

		if len(statuses) < 50:
			remaining = False
		else:
			page_num += 1
	return current_statuses


def check_get_token_index(token_list, token_index, token_count_dict, token_time_dict):
	#print 'CHECKING TOKEN'
	# Check if current token is still usable
	current_token = token_list[token_index]
	current_token_count = token_count_dict[current_token]
	#print(token_count_dict)
	#print current_token_count
	if (current_token_count < 150) and (abs(token_time_dict[current_token] - datetime.datetime.now()) > datetime.timedelta(hours=1)):
		return token_index

	# update index - first step
	if token_index == (len(token_list) - 1):
		new_token_index = 0
	else:
		new_token_index = token_index + 1

	# while loop to find eligible token
	found = False
	while not found:
		# check if token is eligible
		new_token = token_list[new_token_index]
		new_token_count = token_count_dict[new_token]
		new_token_time = token_time_dict[new_token]
		current_time = datetime.datetime.now()
		token_time_diff = abs(current_time - new_token_time)
		if (new_token_count == 0) and (token_time_diff > datetime.timedelta(hours=1)):
			found = True
			token_time_dict[new_token] = current_time

		if new_token_index == (len(token_list) - 1):
			new_token_index = 0
		else:
			new_token_index += 1

	# If current token isn't usable, update its values.
	token_count_dict[current_token] = 0
	token_time_dict[current_token] = datetime.datetime.now()

	#print 'FINISHED CHECKING TOKEN'
	return new_token_index


def check_get_proxy(proxy_ip, proxy_count_dict, proxy_time_dict):
	#print 'CHECKING PROXY'
	#print proxy_count_dict
	if (proxy_count_dict[proxy_ip] < 1000) and (abs(proxy_time_dict[proxy_ip] - datetime.datetime.now()) > datetime.timedelta(hours=1)):
		return proxy_ip

	proxy_list = proxy_count_dict.keys()
	found = False
	for proxy in proxy_list:
		proxy_count = proxy_count_dict[proxy]
		proxy_time = proxy_time_dict[proxy]
		current_time = datetime.datetime.now()
		proxy_time_diff = abs(current_time - proxy_time)
		if (proxy_count == 0) and (proxy_time_diff > datetime.timedelta(hours=1)):
			found = True
			#proxy_time_dict[proxy] = current_time
			new_proxy_ip = proxy
			break

	'''if not found:
		new_proxy_ip = get_new_proxy()
		proxy_count_dict[new_proxy_ip] = 0
		proxy_time_dict[new_proxy_ip] = datetime.datetime.min'''

	proxy_count_dict[proxy_ip] = 0
	proxy_time_dict[proxy_ip] = datetime.datetime.now()

	#print 'FINISHED CHECKING PROXY'
	return new_proxy_ip


def construct_get_url_request(token_list, token_index, token_count_dict, token_time_dict, lat, lon, starttime, endtime, proxy_ip, proxy_count_dict, proxy_time_dict, uas):
	# Wrap in for loop.
	remaining = True
	current_statuses = []
	page_num = 1
	while remaining:
		# Check token.
		token_index = check_get_token_index(token_list, token_index, token_count_dict, token_time_dict)
		# Construct url.
		token = token_list[token_index]
		url = construct_url(token, lat, lon, starttime, endtime) + '&page=' + str(page_num)
		#print url 

		# Check proxy.
		proxy_ip = check_get_proxy(proxy_ip, proxy_count_dict, proxy_time_dict)

		#print "Current URL: " + str(url)
		#print "Current token:" + str(token)
		#print "Current proxy:" + str(proxy_ip)


		# Request using proxy.
		found = False
		while not found:
			try:
				url_data = proxy_request(url, uas, proxy_ip)
				url_data_json = url_data.json()
				if type(url_data_json) != type(dict()):
					return current_statuses
				token_count_dict[token] += 1
				proxy_count_dict[proxy_ip] += 1
				error_code = str(url_data_json.get('error_code'))
				#print 'Error code: ' + error_code

				if error_code == '10023':
					# reset the current token
					token_count_dict[token] = 0
					token_time_dict[token] = datetime.datetime.now()
					# get a new token
					token_index += 1
					token = token_list[token_index]
					url = construct_url(token, lat, lon, starttime, endtime) + '&page=' + str(page_num)
				else:
					found = True
					statuses = url_data_json.get('statuses')
					for status in statuses:
						current_statuses.append(status)
			except Exception as e:
				return current_statuses
		#print "Now at this many statuses: " + str(len(current_statuses))

		# Update proxy and token counts.
		#token_count_dict[token] += 1
		#proxy_count_dict[proxy_ip] += 1

		# Check termination.
		if len(statuses) < 50 or page_num == 400:
			remaining = False
		else:
			page_num += 1
		#print proxy_count_dict
		#print token_count_dict

	# Return found statuses.
	#print "Found " + str(len(current_statuses)) + " in total at the original URL"
	return current_statuses


# Convert larger list of maps into smaller list of relevant maps.
def output_statuses_to_maps(statuses, search_lat, search_lon, token):
	status_maps = []
	user_maps = []
	current_time = str(datetime.datetime.now())
	current_date = current_time.split(' ')[0]
	for status in statuses:
		status_map = dict()
		# add fields into map
		status_map['post_id'] = str(status['id'])
		status_map['text'] = status['text']
		try:
			status_map['post_lat'] = str(status['annotations'][0]['place']['lat'])
			status_map['post_lon'] = str(status['annotations'][0]['place']['lon'])
		except Exception as e:
			status_map['post_lat'] = search_lat
			status_map['post_lon'] = search_lon
		status_map['search_lat'] = str(search_lat)
		status_map['search_lon'] = str(search_lon)
		status_map['images'] = str(status['pic_ids'])
		status_map['num_comments'] = str(status['comments_count'])
		status_map['num_reposts'] = str(status['reposts_count'])
		status_map['num_likes'] = str(status['attitudes_count'])
		status_map['creation_date'] = str(status['created_at'])
		status_map['access_date'] = current_time
		status_map['token'] = str(token)
		dump_status_json(status_map['post_id'], str(status))

		user = status.get('user')
		if user:
			status_map['user_id'] = str(user['id'])
			user_map = dict()
			user_map['key_field'] = '(' + str(user['id']) + ',' + current_date + ')'
			user_map['id'] = str(user['id'])
			user_map['name'] = user['name']
			user_map['num_favorites'] = str(user.get('favourites_count'))
			user_map['num_followers'] = str(user.get('followers_count'))
			user_map['num_friends'] = str(user.get('friends_count'))
			user_map['num_statuses'] = str(user.get('statuses_count'))
			user_map['gender'] = str(user.get('gender'))
			user_map['city'] = str(user.get('city'))
			user_map['province'] = str(user.get('province'))
			user_map['location'] = user.get('location')
			user_map['creation_date'] = str(user['created_at'])
			user_map['credit_score'] = str(user['credit_score'])
			user_map['verified'] = str(user['verified'])
			user_map['access_date'] = current_time
			user_maps.append(user_map)
			dump_user_json(user_map['key_field'], str(user))
		else:
			status_map['user_id'] = str('NaN')

		status_maps.append(status_map)
		
	return (status_maps, user_maps)

def dump_status_json(post_id, post_json):
	write_dir = './Geotag/Text/'
	sqlite_file = 'geotagposts.sqlite'
	conn = sqlite3.connect(write_dir + sqlite_file, timeout=75)
	c = conn.cursor()
	table_name = 'postsdump'
	table_fields = '(id, json)'
	values_string = 'VALUES(?,?)'
	database_command = 'INSERT INTO ' + table_name + ' ' + values_string
	database_values = (post_id, post_json)
	try:
		c.execute(database_command, database_values)
	except Exception as e:
		pass
	conn.commit()
	conn.close()

def dump_user_json(user_key, user_json):
	write_dir = './Geotag/Text/' 
	sqlite_file = 'geotagposts.sqlite'
	conn = sqlite3.connect(write_dir + sqlite_file, timeout=75)
	c = conn.cursor()
	table_name = 'usersdump'
	table_fields = '(key, json)'
	values_string = 'VALUES(?,?)'
	database_command = 'INSERT INTO ' + table_name + ' ' + values_string
	database_values = (user_key, user_json)
	try:
		c.execute(database_command, database_values)
	except Exception as e:
		pass
	conn.commit()
	conn.close()

def write_status_to_db(post):
	write_dir = './Geotag/Text/' 
	sqlite_file = 'geotagposts.sqlite'
	conn = sqlite3.connect(write_dir + sqlite_file, timeout=75)
	c = conn.cursor()
	table_name = 'posts'
	table_fields = '(post_id, user_id, text, post_lat, post_lon, search_lat, search_lon, images, num_comments, num_reposts, num_likes, creation_date, access_date, token)'
	values_string = 'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
	database_command = "INSERT INTO " + table_name + ' ' + values_string
	database_values = (post['post_id'], post['user_id'], post['text'], post['post_lat'], post['post_lon'], post['search_lat'], post['search_lon'], post['images'], post['num_comments'], post['num_reposts'], post['num_likes'], post['creation_date'], post['access_date'], post['token'])
	try:
		c.execute(database_command, database_values)
	except Exception as e:
		pass
	conn.commit()
	conn.close()

def write_user_to_db(user):
	write_dir = './Geotag/Text/' 
	sqlite_file = 'geotagposts.sqlite'
	conn = sqlite3.connect(write_dir + sqlite_file, timeout=75)
	c = conn.cursor()
	table_name = 'users'
	table_fields = '(key, id, name, num_favorites, num_followers, num_friends, num_statuses, gender, city, province, location, creation_date, credit_score, verified, access_date)'
	values_string = 'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
	database_command = 'INSERT INTO ' + table_name + ' ' + values_string
	database_values = (user['key_field'], user['id'], user['name'], user['num_favorites'], user['num_followers'], user['num_friends'], user['num_statuses'], user['gender'], user['city'], user['province'], user['location'], user['creation_date'], user['credit_score'], user['verified'], user['access_date'])
	try:
		c.execute(database_command, database_values)
	except Exception as e:
		pass
	conn.commit()
	conn.close()


total_counter = 0
token_file = sys.argv[1]
tokenfp = open(token_file, 'rb')
token_list = []
for line in tokenfp:
	token_list.append(line.strip())

token_count_dict = dict()
token_time_dict = dict()
current_time = datetime.datetime.now()
for token in token_list:
	token_count_dict[token] = 0
	token_time_dict[token] = datetime.datetime.min 

proxy_file = sys.argv[2]
location_file = sys.argv[3]
max_token_index = len(token_list)
token_index = 0

#load proxies
fin = open(proxy_file, 'rb')
proxy_count_dict = dict()
proxy_time_dict = dict()
for line in fin:
	proxy_ip = line.strip()
	proxy_count_dict[proxy_ip] = 0
	proxy_time_dict[proxy_ip] = datetime.datetime.min

# select proxy randomly
print proxy_count_dict.keys()
proxy_ip = sorted(proxy_count_dict.keys())[0]
print proxy_ip

#proxy_list = [proxy_ip]
#proxy_index = 0

uas = load_user_agents('user_agents.txt')

fp = open(location_file, 'rb')
skip_index = int(sys.argv[4])
for _ in range(skip_index):
	fp.readline()
for line in fp:
	token_index = check_get_token_index(token_list, token_index, token_count_dict, token_time_dict)
	proxy_ip = check_get_proxy(proxy_ip, proxy_count_dict, proxy_time_dict)

	# comment out this section if you want to download all the coordinates
	line_array = line.strip().split(',')
	token = token_list[token_index]
	lat = str(line_array[2])
	lon = str(line_array[3])
	
	# comment out this section if you want to download urban coordinates
	'''line_array = line.strip().split('\t')
	token = token_list[token_index]
	lat = str(line_array[0])
	lon = str(line_array[1])'''
	print('Current latitude: ' + lat + ', current longitude: ' + lon)
	starttime = str(get_unix_time(2016, 10, 1, 0, 0))
	endtime = str(get_unix_time(2016, 11, 1, 0, 0))

	statuses = construct_get_url_request(token_list, token_index, token_count_dict, token_time_dict, lat, lon, starttime, endtime, proxy_ip, proxy_count_dict, proxy_time_dict, uas)
	#print ('Found this many statuses: ' + str(len(statuses)))
	total_counter += len(statuses)
	print ('The total counter is now at: ' + str(total_counter)) + ' at ' + str(datetime.datetime.now())
	status_user_maps = output_statuses_to_maps(statuses, lat, lon, token)
	status_maps = status_user_maps[0]
	user_maps = status_user_maps[1]
	for status in status_maps:
		#print status
		write_status_to_db(status)
	for user in user_maps:
		#print user
		write_user_to_db(user)
	sys.stdout.flush()
