Smuploader
===========

This script is for uploading / downloading images from smugmug.com, using your command line. It uses OAuth for authentication.


Requirements
------------

The following python modules need to be installed:

* requests [http://docs.python-requests.org]
* rauth [https://github.com/litl/rauth]

You can install them using

	pip install rauth


Files
-----

* smugmug.py - The core library for communicating with SmugMug
* smuploader.py - Tool for uploading images to your account
* smdownloader.py - Tool for dowloading images from your account
* test.py - Test the library


Usage
-----

You first need to configure the script, by running the following command and following instructions. It will instruct you to generate a personal API access key.

	python smugmug.py

After setup, you can run the following command to check if everything is working. It creates a new album into your smugmug account, uploads a sample image, and downloads it back again. The script will show a lot of verbose output, and should conclude with OK or FAILED.

	python test.py

Now you can start uploading. As input, you can give either images or directories. For example, upload a single image to a new album:

	python smuploader.py -a AlbumName path/to/image.jpg

Upload a whole directory as an album:

	python smuploader.py path/to/album/

Upload a whole directory, and manually set a new album name:

	python smuploader.py -a AlbumName path/to/album/*
	
Upload a directory, set password to "pass" and category to "Photos":

	python smuploader.py -p pass -c Photos path/to/album/

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

This software is distributed under The MIT License (MIT)

Copyright (c) 2015 Marek Rei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

