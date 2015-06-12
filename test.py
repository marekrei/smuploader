import random
import unittest, os, mimetypes, urllib, time
from smugmug import SmugMug

class TestSmugMug(unittest.TestCase):

	def test_album_creation(self):
		smugmug = SmugMug(verbose=True)
		albums = smugmug.get_album_names()

		# Let's create a name that doesn't exist yet
		album_name = 'SmugMug Test Album '
		index = 1
		while (album_name + str(index)) in albums:
			index += 1
		album_name += str(index)


		# Selecting the last category
		category_name = None
		for category in smugmug.get_category_names():
			category_name = category
		
		# Selecting the last template
		template_name = None
		for template in smugmug.get_template_names():
			template_name = template
		
		# Setting a password
		password = 'TestAlbumPassword'

		# Getting category id
		category_id = smugmug.get_category_id(category_name)
		self.assertTrue(category_name == None or int(category_id) > 0)

		# Getting template id
		template_id = smugmug.get_template_id(template_name)
		self.assertTrue(template_name == None or int(template_id) > 0)

		# Creating a new album
		smugmug.create_album(album_name, category_id = category_id, template_id = template_id, password = password)

		# Checking that the album was created
		albums = smugmug.get_album_names()
		self.assertTrue(album_name in albums)

		# Getting the id of the new album
		album_id = smugmug.get_album_id(album_name)
		self.assertTrue(album_id != None)
		self.assertTrue(int(album_id) > 0)

		# Checking properties
		album_info = smugmug.get_album_info(album_id)
		self.assertTrue(album_info['album_name'] == album_name)
		self.assertTrue(album_info['album_id'] == album_id)
		self.assertTrue(album_info['category_id'] == category_id)
		self.assertTrue(album_info['category_name'] == category_name)
		## self.assertTrue(album_info['password'] == password) ## Apparently password is not returned by the request any more

		# Let's load the sample photo
		image_path = 'sampleimage.jpg'
		try:
			image_data = open(image_path, 'rb').read()
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			raise

		image_name = os.path.basename(image_path)
		image_type = mimetypes.guess_type(image_path)[0]
		smugmug.upload_image(image_data=image_data, image_name=image_name, image_type=image_type, album_id=album_id)

		# Now let's check that the image is in the album
		album_images = smugmug.get_album_images(album_id)
		self.assertTrue(len(album_images) == 1)
		self.assertTrue(image_name in album_images)

		images_info = smugmug.get_album_images_info(album_id)
		self.assertTrue(len(images_info) == 1)

		# Have to wait a bit
		time.sleep(20)

		# Dowloading the image
		image_path2 = 'sampleimage2.jpg'
		smugmug.download_image(image_info = images_info[0], image_path = image_path2)

		# Checking that the new image is same as the old one
		try:
			image_data2 = open(image_path2, 'rb').read()
		except IOError as e:
			raise "I/O error({0}): {1}".format(e.errno, e.strerror)
		self.assertTrue(image_data == image_data2)
		

if __name__ == '__main__':
    unittest.main()
