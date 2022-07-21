# sortfiles
Simple Python script to sort files into a structure of subfolders by date of last modification. Very handy for sorting e.g. photos and videos.

## Usage
`sortfiles.py SOURCEPATH [-h] [--dest DESTPATH] [--pattern PATTERN] [--dry]`

### Arguments:
* `SOURCEPATH`  
Path to the folder where the unsorted files are located.

* `--dest`, `-d`  
_Optional_ path to a folder where the resulting folder and file structure will be created. If not specified, `SOURCEPATH` will be used.

* `--pattern`, `-p`  
_Optional_ pattern of file endings to process. Choose from preset pattern lists (e.g. "images", "movies", or "default"), or provide a comma-separated list of file endings (e.g. ".jpg,.bmp,.tif,.gif,.heic").

* `--dry`  
_Optionally_, perform a dry run. This will give you a preview of what `sortfiles.py` would do, but it does not actually move any files, nor create any folders.

* `-h`, `--help`  
Print the help.

### Examples
`python sortfiles.py "/Users/my_name/Pictures/New Pictures" --pattern=images`  
Sort image files from `"/Users/my_name/Pictures/New Pictures"` into subfolders.

`python sortfiles.py "/Users/my_name/Pictures/New Pictures" --pattern=images,movies`  
Sort image and movie files from `"/Users/my_name/Pictures/New Pictures"` into subfolders.

`python sortfiles.py "/Users/my_name/Documents/Unsorted Docs" --dest="/Archive/Documents" --pattern=documents`  
Sort document files from `"/Users/my_name/Documents/Unsorted Docs"` into a folder structure located in `"/Archive/Documents"`.