import smuploader
import argparse, os

def main():
	parser = argparse.ArgumentParser(description='Upload multiple albums to SmugMug.')
	parser.add_argument('rootdir', metavar='ROOTDIR', type=str, help='the root directory that contains album directories')
	parser.add_argument('-t', '--template', dest='template', metavar='TEMPLATE_NAME', type=str, help='set album template name')
	parser.add_argument('-p', '--password', dest='password', metavar='PASSWORD', type=str, help='set album password')
	parser.add_argument('-c', '--category', dest='category', metavar='CATEGORY_NAME', type=str, help='set category name')
	parser.add_argument('-r', '--resume', dest='resume', action='store_true', default=False, help='if album already exists, add photos in there. default: false')	
	parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='verbose output')	
	args = parser.parse_args()
	
	root_dir = args.rootdir
	directory_names = []

	for directory_name in os.listdir(root_dir):
		directory_path = os.path.join(root_dir, directory_name)
		if os.path.isdir(directory_path) == True:
			directory_names.append(directory_name)

	for directory_name in sorted(directory_names):
		file_paths = []
		directory_path = os.path.join(root_dir, directory_name)
		for file_name in os.listdir(directory_path):
			file_path = os.path.join(directory_path, file_name)
			if os.path.isfile(file_path):
				file_paths.append(file_path)
		file_paths.sort()
		smuploader.main(album_name = directory_name, category_name = args.category, template_name = args.template, password = args.password, resume = args.resume, verbose = args.verbose, image_paths = file_paths)

	print "Batch upload done."

if __name__ == '__main__':
	main()
