# renamexif
Rename image files based on EXIF data

## Usage
usage: renamexif.py [-h] [-l | -m] input output

Default:  
Name by datetime as first value, then location and camera model.


### Options
<p>[-l] [--loc] name by location, then datetime and camera model</p>
<p>[-m] [--model] name by camera model, then datetime and location</p>


### Positional arguments
<p>input: input directory where the image files are located.</p>
<p>output: output directory. If it does not exist it will be created.</p>
