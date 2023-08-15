# renamexif
Rename image files based on EXIF date

## Usage
usage: renamexif.py [-h] [-l | -m] input output

Default:  
Name by datetime as first value, then location and camera model.


### Options
[-l] [--loc] name by location, then datetime and camera model
[-m] [--model] name by camera model, then datetime and location


### Positional arguments
input: input directory where the image files are located.
output: output directory. If it does not exist it will be created.
