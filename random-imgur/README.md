random-imgur
============

random-imgur is a python script to download random images from the popular site Imgur.com. This script is multi-threaded, and has options configurable from the command line. This script has been updated to run on Python 3.0+.


### Usage
To run with default options:

    random_imgur.py

To view additional command line options:

    random_imgur.py --help

    usage: random_imgur.py [-h] [-i IMAGES] [-t THREADS] [-min MIN_SIZE]
                       [-o OUTPUT] [-e ERRORS]

    optional arguments:
      -h, --help            show this help message and exit
      -e ERRORS, --errors ERRORS
                        Toggle error messages on and off. (Default: True)
      -i IMAGES, --images IMAGES
                        Number of images to download. (Default: 25)
      -min MIN_SIZE, --min-size MIN_SIZE
                        Minimum image size in bytes. (Default: 20480)
      -o OUTPUT, --output OUTPUT
                        Output folder name. (Default: output)
      -t THREADS, --threads THREADS
                        Number of threads to spawn. (Default: 5)

