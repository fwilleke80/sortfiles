import os
import time
import shutil
import argparse
import logging
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
log = logging.getLogger()


PATTERNS = {
    'images' : ('.bmp', '.BMP', '.PNG', '.png', '.JPG', '.jpg', '.jpeg', '.JPEG', '.TIF', '.tif', '.tiff', '.TIFF', '.CR2', '.cr2', '.aae', '.AAE', '.xmp', '.XMP'),
    'movies' : ('.MP4', '.mp4', '.MOV', '.mov', '.avi', '.AVI', '.mpg', '.MPG', '.mpeg', '.mpeg'),
    'default' : ('.bmp', '.BMP', '.PNG', '.png', '.JPG', '.jpg', '.jpeg', '.JPEG', '.TIF', '.tif', '.tiff', '.TIFF', '.CR2', '.cr2', '.aae', '.AAE', '.xmp', '.XMP', '.MP4', '.mp4', '.MOV', '.mov', '.avi', '.AVI', '.mpg', '.MPG', '.mpeg', '.mpeg')
}


def handle_file(file, source_path, dest_path, folder_list, error_list, dry_run):
    source_filename = os.path.join(source_path, file)
    log.debug('Handling file %s...' % source_filename)

    # 1. Get file modification date
    file_date = time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(source_filename)))
    log.debug("-> Date: %s" % file_date)

    # Create target folder name
    target_folder = os.path.join(dest_path, file_date)
    log.debug('-> Target folder: ' + str(target_folder))

    # Add target folder to list, if it's not already in there
    if file_date not in folder_list:
        folder_list.append(file_date)

    # 2. Check if targetFolder already exists
    if not os.path.isdir(target_folder):
        # Create it, if necessary
        log.debug('-> -> Creating folder')
        try:
            if dry_run == False:
                os.makedirs(target_folder)
        except Exception:
            error_list.append('Could not create folder: ' + str(target_folder))
            return False

    # 3. Move file to target folder
    log.debug('-> Moving file...')
    if dry_run:
        log.info('DRY RUN: Moving %s --> %s' % (source_filename, target_folder))
    try:
        if not dry_run:
            shutil.move(source_filename, target_folder)
    except Exception:
        error_list.append('File already exists: ' + os.path.join(target_folder, file))
        return False
    return True


def iterate_folder(source_path, dest_path, file_pattern, dry_run):
    folder_list = []
    error_list = []
    file_count = 0

    # Iterate folder
    for file in os.listdir(source_path):
        # Check file suffix
        if file.endswith(file_pattern):
            # Move file
            if handle_file(file, source_path, dest_path, folder_list, error_list, dry_run):
                # If moved, increase counter
                file_count += 1

    return file_count, folder_list, error_list


def main():
    # Prepare argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path", metavar="SOURCEPATH", type=str, default=None, help="Path to the folder containing the unsorted files")
    parser.add_argument("--dest", "-d", dest="dest_path", metavar="DESTPATH", type=str, default=None, help="Path to the folder where the resutls should be moved. If not specified, SOURCEPATH will be used.")
    parser.add_argument("--pattern", "-p", metavar="PATTERN", type=str, default="default", help="Patterns of files that should be moved")
    parser.add_argument("--dry", action="store_true", help="Set this to perform a dry run without actually moving any files.")
    args = parser.parse_args()

    # Get arguments
    source_path = args.source_path
    dest_path = args.dest_path if args.dest_path else args.source_path
    if str(args.pattern).lower() in PATTERNS.keys():
        file_pattern = tuple(PATTERNS[args.pattern])
    else:
        file_pattern = tuple(str(args.pattern).split(","))
    dry_run = args.dry

    # Welcome
    print("SortFiles 1.0\n")
    print("source_path: %s" % source_path)
    print("dest_path: %s" % dest_path)
    print("file_pattern: %s" % str(file_pattern))
    print("dry_run: %s" % dry_run)

    if not os.path.isdir(source_path):
        log.error("%s is not a valid directory!" % source_path)
        return

    # Work it!
    files_moved, folder_list, error_list = iterate_folder(source_path, dest_path, file_pattern, dry_run)

    # Summary: Files moved
    print("%i files moved into %i folders:" % (files_moved, len(folder_list)))
    for folder in folder_list:
        print(folder)

    # Summary: Errors occurred
    if len(error_list) > 0:
        log.error("%i errors have occurred" % len(error_list))
        print('')
        for errorString in error_list:
            log.error(errorString)
    else:
        log.info("No errors occurred.")


if __name__ == "__main__":
    main()