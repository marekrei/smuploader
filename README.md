Smuploader
===========

This script is for uploading / downloading images from smugmug.com. It uses OAuth for authentication.


Requirements
------------

The following python modules need to be installed:

* requests [http://docs.python-requests.org]
* rauth [https://github.com/litl/rauth]

The **rauth** python library, which is used for authentication, relies on the **requests** library. At the time of writing this, the rauth library is not compatible with the latest version of requests (>= 1.0.0), although they are working on fixing that. To use the script, install an earlier version of requests, for example:

	pip install 'requests<0.20'


Files
-----

* smugmug.py - The core library for communicating with SmugMug
* smuploader.py - Tool for uploading images to your account
* smdownloader.py - Tool for dowloading images from your account
* test.py - Test the library


Usage
-----

You first need to configure the script, by running the following command and following instructions:

	python smugmug.py

After setup, you can run the following command to check if everything is working. It creates a new album into your smugmug account, uploads a sample image, and downloads it back again.

	python smugmug_test.py

Now you can start uploading. As input, you can give either images or directories. For example, upload a single image to a new gallery:

	python smuploader.py -a AlbumName path/to/image.jpg

Upload all images in the same dir to an album:

	python smuploader.py -a AlbumName path/to/album/*

Upload a whole directory, and set the album name from the dir name:

	python smuploader.py path/to/album/

Upload multiple directories, and set album names for directory names:

	python smuploader.py path/to/multiple/albums/*

Use the --help argument to get the list of all options, such as setting the password, template and category:

	python smuploader.py --help

You can also download an album from smugmug to your local machine:

	python smdownloader.py -a AlbumName path/to/destination/

Use quotes if the album name contains spaces:

	python smdownloader.py -a 'My Long Album Name' path/to/destination/

Finally, you can also download all the albums in your account:

	python smdownloader.py --getall path/to/destination/


Copyright and License
---------------------

This software is distributed under the GNU Affero General Public License version 3. It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. The authors are not responsible for how it performs (or doesn't). See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.

Copyright (c) 2012, Marek Rei (marek@marekrei.com)
