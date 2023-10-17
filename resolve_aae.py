import os
import time
import shutil
import logging
import pathlib
import argparse
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
log = logging.getLogger()

# Meta
SCRIPT_TITLE = "ResolveAAE 0.1"


def underline(s, c='-'):
    """Returns as many c as s is long.
    """
    return(c * len(s))


def handle_file(file, source_path, error_list, dry_run):
    """Handles one file.
    """
    source_filename = os.path.join(source_path, file)
    log.debug(f"Handling file {source_filename}...")

    # 1. Get path, full filename, and filename parts
    sourceFile = {}
    sourceFile["path"] = pathlib.Path(source_filename).parent.resolve()
    sourceFile["name"] = os.path.splitext(os.path.basename(source_filename))[0]
    sourceFile["name_prefix"], sourceFile["name_postfix"] = sourceFile["name"].split("_")
    sourceFile["name_prefix"] = sourceFile["name_prefix"] + "_"
    sourceFile["extension"] = ""

    # 2. Check if the image file "fileName_1234" exists with extension JPG or PNG
    for extension in (".JPG", ".JPEG", ".PNG"):
        filename_std = (sourceFile["path"] / sourceFile["name"]).with_suffix(extension)
        if os.path.exists(filename_std):
            sourceFile["extension"] = extension
            break

    # Cancel if no image file with proper extension could be found
    if not sourceFile["extension"]:
        return False

    # 2. Cancel if no file "fileName_E1234.[extension]" exists
    filename_e = (sourceFile["path"] / pathlib.Path(sourceFile["name_prefix"] + "E" + sourceFile["name_postfix"]).with_suffix(sourceFile["extension"]))
    if not os.path.exists(filename_e):
        return False

    # 3. Delete filename_std, and .AAE file
    os.remove(filename_std)
    os.remove(source_filename)

    # 4. Rename filename_e to filename_std
    os.rename(filename_e, filename_std)

    return True


def iterate_folder(source_path, dry_run):
    """Iterate files in a folder, and process them
    """
    error_list = []
    file_count = 0

    # Iterate folder
    for file in os.listdir(source_path):
        # Check file suffix
        if file.lower().endswith(".aae"):
            # Move file
            if handle_file(file, source_path, error_list, dry_run):
                # If moved, increase counter
                file_count += 1

    return file_count, error_list


def main():
    """Everything starts here.
    """
    # Setup arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path", metavar="SOURCEPATH", type=str, default=None, help="Path to the folder containing the files to resolve")

    # Parse arguments
    args = parser.parse_args()
    source_path = args.source_path

    # Welcome
    print("\n%s" % SCRIPT_TITLE)
    print("%s" % underline(SCRIPT_TITLE))
    print("source_path : %s" % source_path)
    print('')

    # Check if path exists
    if not os.path.isdir(source_path):
        log.error("%s is not a valid directory!" % source_path)
        return

    # Work it!
    files_processed, error_list = iterate_folder(source_path, False) #dry_run)

    # Summary: Files moved
    if files_processed > 0:
        print(f"{files_processed} files processed.")
    else:
        print("No files were moved.")

    # Summary: Errors occurred
    if len(error_list) > 0:
        log.error(f"{len(error_list)} errors have occurred" % len(error_list))
        print('')
        for errorString in error_list:
            log.error(errorString)
    print('')


if __name__ == "__main__":
    main()