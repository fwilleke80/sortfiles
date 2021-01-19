import os
import time
import shutil
import argparse
import logging
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
log = logging.getLogger()

# Meta
SCRIPT_TITLE = "SortFiles 1.1"

# Preset file endings
ENDINGS_IMAGES = ('.bmp', '.png', '.jpg', '.jpeg', '.tif', '.tiff', '.cr2', '.aae', '.xmp', '.heic')
ENDINGS_MOVIES = ('.mp4', '.mov', '.avi', '.mpg', '.mpeg', '.mkv')
PATTERNS = {
    'images' : ENDINGS_IMAGES,
    'movies' : ENDINGS_MOVIES,
    'default' : ENDINGS_IMAGES + ENDINGS_MOVIES
}


def underline(s, c='-'):
    """Return as many c as s is long
    """
    return(c * len(s))


def handle_file(file, source_path, dest_path, folder_list, error_list, dry_run):
    """Move one file
    """
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
    """Iterate files in a folder, and process them
    """
    folder_list = []
    error_list = []
    file_count = 0

    # Iterate folder
    for file in os.listdir(source_path):
        # Check file suffix
        if file.lower().endswith(file_pattern):
            # Move file
            if handle_file(file, source_path, dest_path, folder_list, error_list, dry_run):
                # If moved, increase counter
                file_count += 1

    return file_count, folder_list, error_list


def main():
    """Everything starts here.
    """
    # Setup arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path", metavar="SOURCEPATH", type=str, default=None, help="Path to the folder containing the unsorted files")
    parser.add_argument("--dest", "-d", dest="dest_path", metavar="DESTPATH", type=str, default=None, help="Path to the folder where the results should be moved. If not specified, SOURCEPATH will be used.")
    parser.add_argument("--pattern", "-p", metavar="PATTERN", type=str, default="default", help="Patterns of files that should be moved (either one of %s, or a comma separated list of endings [e.g. '.JPG,.BMP,.TIF'])" % PATTERNS.keys())
    parser.add_argument("--dry", action="store_true", help="Set this to perform a dry run without actually moving any files.")
    args = parser.parse_args()

    # Parse arguments
    source_path = args.source_path
    dest_path = args.dest_path if args.dest_path else args.source_path
    if str(args.pattern).lower() in PATTERNS.keys():
        file_pattern = tuple(PATTERNS[args.pattern])
    else:
        file_pattern = tuple(str(args.pattern).split(","))
    dry_run = args.dry

    # Welcome
    print("\n%s" % SCRIPT_TITLE)
    print("%s" % underline(SCRIPT_TITLE))
    print("source_path : %s" % source_path)
    print("dest_path   : %s" % dest_path)
    print("file_pattern: %s" % str(file_pattern))
    if dry_run:
        print("dry_run     : %s\n" % dry_run)
    print('')

    if not os.path.isdir(source_path):
        log.error("%s is not a valid directory!" % source_path)
        return

    # Work it!
    files_moved, folder_list, error_list = iterate_folder(source_path, dest_path, file_pattern, dry_run)

    # Summary: Files moved
    if files_moved > 0:
        print("%i files moved into %i folders:" % (files_moved, len(folder_list)))
        for folder in folder_list:
            print(folder)
    else:
        print("No files were moved.")

    # Summary: Errors occurred
    if len(error_list) > 0:
        log.error("%i errors have occurred" % len(error_list))
        print('')
        for errorString in error_list:
            log.error(errorString)


if __name__ == "__main__":
    main()