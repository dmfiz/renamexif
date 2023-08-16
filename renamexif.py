from geopy.geocoders import Nominatim, GeoNames
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import argparse
import sys



def parse_args():
    parser = argparse.ArgumentParser(description="Rename image files based on EXIF date. Name by datetime as first value, then location and camera model")
    group = parser.add_mutually_exclusive_group()

    # This is the default
    #group.add_argument("-d", "--datetime", help="name by datetime as first value, then location and camera model")

    # Mutually exclusive arguments
    group.add_argument("-l", "--loc", help="name by location, then datetime and camera model", action="store_true")
    group.add_argument("-m", "--model", help="name by camera model, then datetime and location", action="store_true")

    # positional arguments for input and output directories
    parser.add_argument("input", help="input directory")
    parser.add_argument("output", help="output directory")

    args = parser.parse_args()
    return args


def generate_filename(exif):

    # Get arguments from argparse
    args = parse_args()

    # Take the date and camera model from exif data
    date_taken = exif["DateTime"].replace(":", "").replace(" ", "-")
    camera_model = exif["Model"]

    # For debuggind purposes
    #print(date_taken)
    #print(camera_model)

    # Try/Except because otherwise we get a KeyError
    try:
        north = exif["GPSInfo"][2]
        east = exif["GPSInfo"][4]

        # Initial Coordinates are Degrees, Minutes, and Seconds. We need to convert them to decimal
        lat = float(((((north[0] * 60) + north[1]) * 60) + north[2]) / 60 / 60)
        long = float(((((east[0] * 60) + east[1]) * 60) + east[2]) / 60 / 60)


        # Neither Nominatim nor GeoNames deliver sufficient good location names so I leave both options included to make a quick change possible
        #loc_name = geocode_nominatim(lat, long)
        loc_name = geocode_geonames(lat, long)


    # In case of KeyError we define loc_name manually as None
    except KeyError:
        loc_name = None

    # No flag. Default variant of program
    if not args.loc and not args.model and loc_name is not None:
        return f"img_{date_taken}_{loc_name}_{camera_model}.jpg"
    elif not args.loc and not args.model and loc_name is None:
        return f"img_{date_taken}_{camera_model}.jpg"

    # Flag --loc
    elif args.loc and loc_name is not None:
        return f"img_{loc_name}_{date_taken}_{camera_model}.jpg"

    # Flag --model
    elif args.model and loc_name is not None:
        return f"img_{camera_model}_{date_taken}_{loc_name}.jpg"
    elif args.model and loc_name is None:
        return f"img_{camera_model}_{date_taken}.jpg"


def geocode_nominatim(lat, long):

    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse(f"{lat}, {long}", zoom=11)
    loc_name = str(locname.address).partition(",")[0]

    # For debugging purposes
    #print(f"Nominatim: {loc_name}")

    return loc_name


def geocode_geonames(lat, long):

    geo = GeoNames(username="dmfiz")
    location = geo.reverse(query=(lat, long), exactly_one=True, timeout=5, lang="local", find_nearby_type="findNearbyPlaceName")
    loc_name = str(location).partition(",")[0]

    # For debugging purposes
    #print(f"GeoNames: {location_name}")

    return loc_name


def main():

    # Get arguments from argparse
    args = parse_args()

    # Path works for Linux and Windows
    input_path = Path(args.input)
    output_path = Path(args.output)

    # Check if provided input directory exists
    if input_path.is_dir():

        # If output directory does not exist we create it including all missing parent directories
        if not output_path.is_dir():
            output_path.mkdir(parents=True)

        # glob all jpg (and jpeg) files in input directory
        glob_jpg = input_path.glob('*.jp*g')

        # Iterate over all image files
        for file in glob_jpg:
            with Image.open(file) as img:
                img.load()

                try:
                    exif = {
                    TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in TAGS
                    }

                # If no exif data available we skip the file
                except AttributeError:
                    image = img.save(f"{output_path}/{Path(file).name}")

                # If exif data available we proceed
                new_filename = generate_filename(exif)

                # For debugging purposes
                #print(file)
                #print(new_filename)

                # Save new image under new filename in output directory
                image = img.save(f"{output_path}/{new_filename}")




    else:
        sys.exit("The input directory doesn't exist")


if __name__ == "__main__":
    main()