import glob
from os.path import exists
import re
from subprocess import call
import shutil
import datetime

DATA_PATH = "../data/noaa/"

def load_noaa_data():
    if not exists(DATA_PATH):
        call([
             "wget", "-r",
             "ftp://ftp.swpc.noaa.gov/pub/indices/old_indices/",
        ])
        result_path = "ftp.swpc.noaa.gov/pub/indices/old_indices/"
        shutil.copytree(result_path, DATA_PATH)
        shutil.rmtree("ftp.swpc.noaa.gov")

    all_data = sum(map(lambda x: open(x).readlines(), glob.glob(DATA_PATH + "/*DSD*")), [])

    result = {}

    for row in all_data:
        old_date = re.match("^(\d{2})\s([A-Za-z]{3})\s(\d{2})", row)
        new_date = re.match("^(\d{4})\s(\d{2})\s(\d{2})", row)
        date = None

        if old_date is not None:
            date = datetime.datetime.strptime(old_date.group(0), "%d %b %y").strftime("%Y-%m-%d")
        elif new_date is not None:
            date = datetime.datetime.strptime(new_date.group(0), "%Y %m %d").strftime("%Y-%m-%d")

        if date is not None:
            s = re.split("\s+", row)

            def safe_int(x):
                try:
                    return int(x)
                except:
                    return None


            subres = {
                'radio_flux': safe_int(s[3]),
                'sunspot_number': safe_int(s[4]),
                'sunspot_area': safe_int(s[5])
            }
            if len(s) > 9:
                subres['new_regions'] = safe_int(s[6])
            result[date] = subres

    return result

