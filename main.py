__author__ = "Dermul Bart"
__copyright__ = "Copyright 2022 - ask before you participate"
__credits__ = ["Dermul Bart"]
__license__ = "GNU"
__version__ = "1"
__maintainer__ = "Dermul Bart"
__email__ = "bart.dermul@gmail.com"
__status__ = "Production"

from HornetTracker import app

context = ('cert.pem', 'key.pem')
if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=4443, ssl_context=context)
    app.run(host="0.0.0.0", port=8080)
