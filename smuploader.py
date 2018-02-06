from smugmug import SmugMug
import argparse, sys, os, mimetypes

def upload_images(album_name, folder_name, template_name, password, resume, verbose, image_paths):
    if album_name == None:
        print 'Error: Album name not specified.'
        sys.exit(1)

    if len(image_paths) == 0:
        print 'Error: No images specified for uploading.'
        sys.exit(1)

    smugmug = SmugMug(verbose=verbose)

    # Finding / creating the album
    album_id = smugmug.get_album_id(album_name)
    if album_id == None:
        # Getting folder id
        folder_id = None
        if folder_name != None:
            folder_id = smugmug.get_folder_id(folder_name)
            if folder_id == None:
                print 'Error: Could not find folder named \'' + folder_name + '\''
                sys.exit(1)
        # Getting template id
        template_id = None
        if template_name != None:
            template_id = smugmug.get_template_id(template_name)
            if template_id == None:
                print 'Error: Could not find album template named \'' + template_name + '\''
                sys.exit(1)
        # Creating a new album
        smugmug.create_album(album_name = album_name, folder_id = folder_id, template_id = template_id, password = password)
        print 'Created new album \''+album_name+'\''
        album_id = smugmug.get_album_id(album_name)
    elif album_id != None and resume == True:
        print 'Uploading to existing album \'' + album_name + '\''
    else:
        print 'Error: Album already exists. Use \'--resume\' to add to existing album.'
        sys.exit(1)


    # Uploading the images
    total = len(image_paths)
    count = 0
    album_image_names = smugmug.get_album_image_names(album_id)

    for image_path in image_paths:
        if verbose == True:
            print '----------------------------------------------------'
        count += 1
        image_name = os.path.basename(image_path)
        sys.stdout.write('Uploading ' + album_name + '/' + image_name + ' [' + str(count) + '/' + str(total) + ']... ')
        sys.stdout.flush()
        if verbose == True:
            print ''
        if image_name in album_image_names:
            print 'File already exists, skipping.'
            sys.stdout.flush()
        else:
            # Loading the image data
            try:
                image_data = open(image_path, 'rb').read()
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                raise
        
            # Finding the mime type
            image_type = mimetypes.guess_type(image_path)[0]
        
            # Uploading image
            result = smugmug.upload_image(image_data=image_data, image_name=image_name, image_type=image_type, album_id=album_id)
        
            if result['stat'] != 'ok':
                print 'Error: Upload failed for file \'' + image + '\''
                print 'Printing server response:'
                print result
                sys.exit(1)
            print 'Done'

    # Small additional check if the number of images matches
    album_images = smugmug.get_album_images(album_id)
    if len(image_paths) != len(image_paths):
        print 'Warning: You selected ' + str(len(args.images)) + ' images, but there are ' + str(len(existing_images)) + ' in the online album.'


    print 'Album done: \''+album_name+'\''


def list_files(dir_path):
    """Get paths for all files in a directory"""
    file_paths = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            file_paths.append(file_path)
    file_paths.sort()
    return file_paths

def main(args):
    """Run the uploading"""
    
    # Determine whether the input contains files or directories
    contains_dirs = False
    contains_files = False
    for source in args.source:
        if os.path.isdir(source) == True:
            contains_dirs = True
        if os.path.isfile(source) == True:
            contains_files = True

    # If it contains both files or directories, raise an error
    if contains_dirs and contains_files:
        raise "Input contains both directories and files"

    # If only files
    elif contains_files:
        upload_images(album_name = args.album, folder_name = args.folder, template_name = args.template, password = args.password, resume = args.resume, verbose = args.verbose, image_paths = args.source)
    # If only directories
    elif contains_dirs:
        # If a single directory, and the album name is set
        if len(args.source) == 1 and args.album != None:
            image_paths = list_files(args.source[0])
            album_name = args.album
            upload_images(album_name = album_name, folder_name = args.folder, template_name = args.template, password = args.password, resume = args.resume, verbose = args.verbose, image_paths = image_paths)
        # Otherwise, ignore the album name and upload all directories with their own names
        else:
            for source in args.source:
                image_paths = list_files(source)
                album_name = os.path.basename(os.path.normpath(source))
                upload_images(album_name = album_name, folder_name = args.folder, template_name = args.template, password = args.password, resume = args.resume, verbose = args.verbose, image_paths = image_paths)
        print "All albums done!"
            

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Upload images to SmugMug.')
    parser.add_argument('source', metavar='SOURCE', type=str, nargs='+', help='files/dirs to upload')
#    parser.add_argument('--config', dest='configconfig', action='store_true', default=False, help='run configuration')
    parser.add_argument('-a', '--album', dest='album', metavar='ALBUM_NAME', type=str, help='set album name')
    parser.add_argument('-t', '--template', dest='template', metavar='TEMPLATE_NAME', type=str, help='set album template name')
    parser.add_argument('-p', '--password', dest='password', metavar='PASSWORD', type=str, help='set album password')
    parser.add_argument('-f', '--folder', dest='folder', metavar='FOLDER_NAME', type=str, help='set folder name')
    parser.add_argument('-c', '--category', dest='folder', metavar='FOLDER_NAME', type=str, help='set folder name, alias for backwards compatibility')
    parser.add_argument('-r', '--resume', dest='resume', action='store_true', default=False, help='if album already exists, add photos in there. default: false')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='verbose output')
    args = parser.parse_args()
    
    main(args)
    

