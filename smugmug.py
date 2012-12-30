from rauth.service import OAuth1Service
import requests, httplib, httplib2, hashlib, urllib, time, sys, os
import ConfigParser

class SmugMug(object):
	smugmug_api_uri = 'https://api.smugmug.com/services/api/json/1.3.0/'
	smugmug_upload_uri = 'http://upload.smugmug.com/'
	smugmug_request_token_uri = 'https://api.smugmug.com/services/oauth/getRequestToken.mg'
	smugmug_access_token_uri = 'https://api.smugmug.com/services/oauth/getAccessToken.mg'
	smugmug_authorize_uri = 'https://api.smugmug.com/services/oauth/authorize.mg'
	smugmug_api_version = '1.3.0'
	smugmug_config = 'smugmug.cfg'
	
	smugmug_service = None
	verbose = False
	consumer_key = None
	consumer_secret = None
	request_token = None
	request_token_secret = None
	access_token = None
	access_token_secret = None


	def __init__(self, verbose = False):
		"""Constructor. 
		Loads the config file and initialises the smugmug service
		"""

		self.verbose = verbose
		
		config_parser = ConfigParser.RawConfigParser()
		config_parser.read(SmugMug.smugmug_config)
		try:
			self.consumer_key = config_parser.get('SMUGMUG','consumer_key')
			self.consumer_secret = config_parser.get('SMUGMUG','consumer_secret')
			self.access_token = config_parser.get('SMUGMUG','access_token')
			self.access_token_secret = config_parser.get('SMUGMUG','access_token_secret')
		except:
			raise Exception("Config file is missing or corrupted. Run 'python smugmug.py'")

		self.smugmug_service = OAuth1Service(
			name='smugmug',
			consumer_key=self.consumer_key,
			consumer_secret=self.consumer_secret,
			request_token_url=self.smugmug_request_token_uri,
			access_token_url=self.smugmug_access_token_uri,
			authorize_url=self.smugmug_authorize_uri)

	@staticmethod
	def decode(obj, encoding='utf-8'):
		if isinstance(obj, basestring):
			if not isinstance(obj, unicode):
				obj = unicode(obj, encoding)
		return obj

	def get_authorize_url(self):
		"""Returns the URL for OAuth authorisation"""
		self.request_token, self.request_token_secret = self.smugmug_service.get_request_token(method='GET')
		authorize_url = self.smugmug_service.get_authorize_url(self.request_token, Access='Full', Permissions='Add')
		return authorize_url


	def get_access_token(self):
		"""Gets the access token from SmugMug"""
		response = self.smugmug_service.get_access_token('POST',
                                    request_token=self.request_token,
                                    request_token_secret=self.request_token_secret)
		data = response.content
		self.access_token = data['oauth_token']
		self.access_token_secret = data['oauth_token_secret']
		return self.access_token, self.access_token_secret

	def request_once(self, method, url, params={}, headers={}, files={}, data=None, header_auth=False):
		"""Performs a single request"""
		if self.verbose == True:
			print 'REQUEST:\nmethod='+method+'\nurl='+url+'\nparams='+str(params)+'\nheaders='+str(headers)
		response = self.smugmug_service.request(method=method,
						uri=url,
						params=params,
						headers=headers,
						files=files,
						data=data,
						access_token=self.access_token,
						access_token_secret=self.access_token_secret,
						header_auth=header_auth)
		if self.verbose == True:
			print 'RESPONSE:\n' + str(response.content)
		return response


	def request(self, method, url, params={}, headers={}, files={}, data=None, header_auth=False, retries=5, sleep=5):
		"""Performs requests, with multiple attempts if needed"""
		retry_count=retries
		while retry_count > 0:
			try:
				result = self.request_once(method, url, params, headers, files, data, header_auth)
				if 'stat' in result.content and result.content['stat'] == "ok":
					return result
			except (requests.ConnectionError, requests.HTTPError, requests.URLRequired, requests.TooManyRedirects, requests.RequestException, httplib.IncompleteRead) as e:
				if self.verbose == True:
					print sys.exc_info()[0]
			if self.verbose == True:
				print 'Retrying (' + str(retry_count) + ')...'
			time.sleep(sleep)
			retry_count -= 1
		print 'Error: Too many retries, giving up.'
		sys.exit(1)

	## Album

	def get_album_names(self):
		"""Get a list of all albums in the account"""
		response = self.request('GET', self.smugmug_api_uri, params={'method':'smugmug.albums.get'})
		albums = []
		for album in response.content['Albums'] :
			albums.append(album['Title'])
		return albums

	def get_album_id(self, album_name):
		"""Get album id"""
		if album_name == None:
			raise Exception("Album name cannot be None")

		album_id = None
		response = self.request('GET', self.smugmug_api_uri, params={'method':'smugmug.albums.get'})

		for album in response.content['Albums'] :
			if SmugMug.decode(album['Title']) == SmugMug.decode(album_name):
				album_id = album['id']
				break
		return album_id


	def get_album_key(self, album_id):
		"""Get album key"""
		if album_id == None:
			raise Exception("Album ID cannot be None")

		album_key = None
		response = self.request('GET', self.smugmug_api_uri, params={'method':'smugmug.albums.get'})

		for album in response.content['Albums'] :
			if album['id'] == album_id:
				album_key = album['Key']
				break
		return album_key


	def get_album_images(self, album_id):
		"""Get list of file names in an album"""
		if album_id == None:
			raise Exception("Album ID cannot be None")
		album_key = self.get_album_key(album_id)
		images = []
		response = self.request('GET', self.smugmug_api_uri,
				params={'method':'smugmug.images.get', 'AlbumID':album_id, 'AlbumKey':album_key, 'Extras':'FileName'})
		for image in response.content['Album']['Images'] :
			images.append(image['FileName'])
		return images


	def get_album_images_info(self, album_id):
		"""Get a information for all images in an album"""
		if album_id == None:
			raise Exception("Album ID cannot be None")
		album_key = self.get_album_key(album_id)
		images = []
		response = self.request('GET', self.smugmug_api_uri,
				params={'method':'smugmug.images.get', 'AlbumID':album_id, 'AlbumKey':album_key, 'Extras':'FileName,OriginalURL,MD5Sum,Size'})
		for image in response.content['Album']['Images'] :
			images.append({'name':image['FileName'], 'original_url':image['OriginalURL'], 'md5_sum':image['MD5Sum'], 'size':image['Size']})
		return images


	def create_album(self, album_name, password = None, category_id = None, template_id = None):
		"""Create a new album"""
		params = {'method':'smugmug.albums.create', 'Title':album_name, 'Originals' : '1', 'Filenames' : '1'}
	
		if category_id != None:
			params['CategoryID'] = category_id
		if template_id != None:
			params['AlbumTemplateID'] = template_id
		if password != None:
			params['Password'] = password

		response = self.request('GET', self.smugmug_api_uri, params=params)

		album_id = response.content['Album']['id']
		return album_id

	
	def get_album_info(self, album_id):
		"""Get info for an album"""
		info = dict()
		album_key = self.get_album_key(album_id)
		response = self.request('GET', self.smugmug_api_uri, params={'method':'smugmug.albums.getInfo', 'AlbumID':album_id, 'AlbumKey':album_key})
		info['album_id'] = response.content['Album']['id']
		info['album_name'] = response.content['Album']['Title']
		info['category_id'] = response.content['Album']['Category']['id']
		info['category_name'] = response.content['Album']['Category']['Name']
		info['password'] = response.content['Album']['Password']
		return info

	## Category

	def get_category_names(self):
		"""Get a list of all categories in the account"""
		response = self.request('GET', self.smugmug_api_uri, params={'method':'smugmug.categories.get'})
		categories = []
		for category in response.content['Categories'] :
			categories.append(category['Name'])
		return categories

	def get_category_id(self, category_name):
		"""Get category id"""
		category_id = None
		response = self.request('GET', self.smugmug_api_uri,
				params={'method':'smugmug.categories.get'})

		for category in response.content['Categories'] :
			if category['Name'] == category_name:
				category_id = category['id']
				break
		return category_id


	## Template

	def get_template_names(self):
		"""Get a list of all album templates in the account"""
		response = self.request('GET', self.smugmug_api_uri, params={'method':'smugmug.albumtemplates.get'})
		templates = []
		for template in response.content['AlbumTemplates'] :
			templates.append(template['Name'])
		return templates


	def get_template_id(self, template_name):
		"""Get template id"""
		template_id = None
		response = self.request('GET', self.smugmug_api_uri,
				params={'method':'smugmug.albumtemplates.get'})

		for template in response.content['AlbumTemplates'] :
			if template['Name'] == template_name:
				template_id = template['id']
				break
		return template_id


	## Image

	def upload_image(self, image_data, image_name, image_type, album_id):
		"""Upload an image"""
		response = self.request('POST', self.smugmug_upload_uri,
			data=image_data,
			header_auth = True,
			headers={'X-Smug-AlbumID':str(album_id), 
				'X-Smug-Version':self.smugmug_api_version, 
				'X-Smug-ResponseType':'JSON',
				'Content-MD5': hashlib.md5(image_data).hexdigest(),
				'X-Smug-FileName':image_name,
				'Content-Length' : str(len(image_data)),
				'Content-Type': image_type})
		return response.content


	def download_image(self, image_info, image_path, retries=5):
		"""Download an image"""
		count = retries
		image_url = image_info['original_url']
		image_url = httplib2.iri2uri(image_url)
		image_path_temp = image_path + "_temp"
		while count > 0:
			count -= 1
			# Doing the actual downloading
			urllib.urlretrieve (image_url, image_path_temp)
			
			# Checking the image			
			image_data = SmugMug.load_image(image_path_temp)
			image_md5sum = hashlib.md5(image_data).hexdigest()
			image_size = str(len(image_data))
			if image_md5sum != image_info['md5_sum']:
				raise "MD5 sum doesn't match."
			elif image_size != str(image_info['size']):
				raise "Image size doesn't match."
			else:
				os.rename(image_path_temp, image_path)
				break

			if count > 0:
				print "Retrying..."
			else:
				raise "Error: Too many retries."
				sys.exit(1)

	@staticmethod
	def load_image(image_path):
		"""Load the image data from a path"""
		try:
			image_data = open(image_path, 'rb').read()
			return image_data
		except IOError as e:
			raise "I/O error({0}): {1}".format(e.errno, e.strerror)
		return None


if __name__ == '__main__':
	print "# Welcome! We are going to go through some steps to set up this SmugMug photo manager and make it connect to the API."
	print "# Step 1: Go to http://wiki.smugmug.net/display/API and apply for an API key. This gives you unique identifiers for connecting to SmugMug."
	print "# When done, you can find the API keys in your SmugMug profile."
	print "# Enter them here and they will be saved to the config file (" + SmugMug.smugmug_config + ") for later use."
	consumer_key = raw_input("Key: ")
	consumer_secret = raw_input("Secret: ")

	config = ConfigParser.SafeConfigParser()
	config.add_section('SMUGMUG')
	config.set('SMUGMUG', 'consumer_key', consumer_key)
	config.set('SMUGMUG', 'consumer_secret', consumer_secret)
	config.set('SMUGMUG', 'access_token', '')
	config.set('SMUGMUG', 'access_token_secret', '')
	with open(SmugMug.smugmug_config, 'wb') as configfile:
		config.write(configfile)

	smugmug = SmugMug()
	authorize_url = smugmug.get_authorize_url()
	print "# Step 2: Visit this address in your browser and authenticate your new keys to access your SmugMug account: " + authorize_url
	raw_input("Press ENTER when you're finished: ")

	access_token, access_token_secret = smugmug.get_access_token()

	config = ConfigParser.SafeConfigParser()
	config.add_section('SMUGMUG')
	config.set('SMUGMUG', 'consumer_key', consumer_key)
	config.set('SMUGMUG', 'consumer_secret', consumer_secret)
	config.set('SMUGMUG', 'access_token', access_token)
	config.set('SMUGMUG', 'access_token_secret', access_token_secret)

	with open(SmugMug.smugmug_config, 'wb') as configfile:
		config.write(configfile)

	print "Great! All done!"
