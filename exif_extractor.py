import os
import logging
from PIL import Image, ExifTags

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

path = os.path.join(os.getcwd(), 'sample_photos', 'exif-samples', 'jpg', 'gps')


def dms_to_decdeg(value, reference):
    """Accepts Tuple of Tuples ((Deg)(Min)(Secs)) and GPS Reference then Converts to Decimal Degrees (Lat/Lon)
        Reference: https://www.youtube.com/watch?v=w-spWmiEyME&list=PLO6KswO64zVu7S4bqQoHWR5516aCUEnda&index=18"""
    if not value:
        return
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    decdeg = d + (m / 60.0) + (s / 3600.0)

    if reference == "W" or reference == "S":
        return decdeg*-1
    else:
        return decdeg


def get_exif(pil_img):
    _exif = {}
    try:
        _exif = {ExifTags.TAGS[k]: v for k, v in pil_img._getexif().items() if k in ExifTags.TAGS}
    except AttributeError:
        # logger.debug('File has no EXIF data associated with it.')
        print('File has no EXIF data')

    return _exif


def get_gps_dms(exif_data):
    """Returns Tuple consisting of (GPSLatitudeReference 'N/S')(GPSLatitude DegMinSecs)
    (GPSLongitudeReference 'E/W')(GPSLongitude DegMinSecs) from exif_data"""
    img_gps = {}
    lat_ref = ''
    lat = 0.0
    long_ref = ''
    long = 0.0
    try:
        for key in exif_data['GPSInfo'].keys():
            decoded_value = ExifTags.GPSTAGS.get(key)
            img_gps[decoded_value] = exif_data['GPSInfo'][key]
            # logger.info(exif['GPSInfo'[key]])
        long_ref = img_gps.get('GPSLongitudeRef')
        lat_ref = img_gps.get('GPSLatitudeRef')

        long = img_gps.get('GPSLongitude')
        lat = img_gps.get('GPSLatitude')
    except AttributeError:
        # logger.debug('Image has no GPSInfo metadata: {}'.format())
        pass

    return lat_ref, lat, long_ref, long


if __name__ == '__main__':

    for image in os.listdir(path):
        if image.endswith('.jpg'):
            pil_img = Image.open(os.path.join(path, image))
        else:
            continue
        print(image)
        exif = get_exif(pil_img)
        # print(exif)


        # Print GPS Data from EXIF
        lat_ref, lat, long_ref, long = get_gps_dms(exif)
        print('Latitude Reference: {} Latitude: {}'.format(lat_ref, lat))
        print('Longitude Reference: {} Longitude: {}'.format(long_ref, long))
        print("Decimal Latitude: {}".format(dms_to_decdeg(lat, lat_ref)))
        print("Decimal Longitude: {}".format(dms_to_decdeg(long, long_ref)))


