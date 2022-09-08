# this file contains formatter and small usefull functions to limit lines in the code

def longlatformatter(latlong):
    if isinstance(latlong, float or int):
        return latlong
    else:
        if isinstance(latlong, str):
            formattedlatlong = latlong.replace(",",".")
            return float(formattedlatlong)