from smugmug import SmugMug
import argparse, sys, os, hashlib

def download_album(album_name, path, resume = False, verbose = False):
    """
    Download an album from smugmug to the local path
    """
    if album_name == None:
        raise "Error: Album name not specified"
        sys.exit(1)
    
    if path == None:
        raise "Error: Path is not specified"
        sys.exit(1)

    smugmug = SmugMug(verbose)

    print("#### Processing album: " + album_name)

    album_id = smugmug.get_album_id(album_name)
    if album_id == None:
        raise "Error: Album does not exist at SmugMug. Skipping."

    # Creating the album
    album_path = os.path.join(path, album_name)
    if os.path.exists(album_path):
        if resume == False:
            print("Error: Local album \'" + album_name + "\' already exists and resuming is not enabled.")
            sys.exit(1)
        else:
            print("Local album already exists. Adding images.")
    else:
        print("Creating new local album.")
        os.makedirs(album_path)

    images = smugmug.get_album_images(album_id)
    count = 0
    total = len(images)
    for image_info in images:
        count += 1
        image_name = image_info['FileName']
        image_path = os.path.join(album_path, image_name)
        sys.stdout.write('Downloading ' + album_name.encode('utf-8') + '/' + image_name.encode('utf-8') + ' [' + str(count) + '/' + str(total) + ']... ')
        sys.stdout.flush()
        if verbose == True:
            print('')

        if os.path.exists(image_path):
            if resume == True:
                print("Already exists. Skipping.")
            else:
                raise Exception("Error: File already exists and resuming is not enables.")
        else:
            smugmug.download_image(image_info = image_info, image_path = image_path)
            print("Done")
    print("Done downloading album '" + album_name + "'")


def download_all(path, resume, verbose):
    """
    Download all albums in an account
    """
    smugmug = SmugMug(verbose)

    album_names = []

    albums = smugmug.get_album_names()
    for album_name in albums:
        download_album(album_name = album_name, path = path, resume = resume, verbose = verbose)
    print("Finished downloading all albums!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download images from SmugMug.')
    parser.add_argument('path', metavar='PATH', type=lambda s: unicode(s, 'utf8'), help='path where the albums are downloaded')
    parser.add_argument('-a', '--album', dest='album', metavar='ALBUM_NAME', type=lambda s: unicode(s, 'utf8'), help='album to download')
    parser.add_argument('--getall', dest='getall', action='store_true', default=False, help='download all albums')
    parser.add_argument('-r', '--resume', dest='resume', action='store_true', default=False, help='if album already exists, add photos in there. default: false')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False, help='verbose output')
    args = parser.parse_args()

    if args.getall == True:
        download_all(path = args.path, resume = args.resume, verbose = args.verbose)
    else:
        download_album(album_name = args.album, path = args.path, resume = args.resume, verbose = args.verbose)

