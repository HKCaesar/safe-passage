from PIL import Image
import os
import shutil
import csv
from tqdm import tqdm
from itertools import groupby
import random
import math

chipdir = 'data/images/chips'
imagedir = 'data/images/training'
# in pixels
boxsize = 150


def setupDirectories():
    """Set up the directories that will hold the chips. Remove the old chips if
    they exist."""
    shutil.rmtree(chipdir, ignore_errors=True)
    os.mkdir(chipdir)
    for classname in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'other']:
        os.mkdir(os.path.join(chipdir, classname))


def makeChips(observationcsv):
    """Given a csv file containing the observations, make the image chips from
    the file."""
    with open(observationcsv) as f:
        reader = csv.DictReader(f)
        for filename, group in tqdm(groupby(reader, lambda x: x['image'])):
            image = Image.open(os.path.join(imagedir, filename))
            coords = []
            for observation in group:
                if observation['detections'] != 'None':
                    # if the detections field is None then no vehicles of this
                    # type were observed
                    obs_coords = processObservation(observation, image)
                    coords = coords + obs_coords
                    #coords.append(obs_coords)
            makeRandomChips(observation, 4, coords, image)



def processObservation(observation, image):
    """An observation is a row in the observation file. This might contain
    multiple detections of vehicles. Extract each of those observations into a
    separate image chip and save."""
    coords = []
    for i, detection in enumerate(observation['detections'].split('|')):
        # the x and y coords are separated by a colon
        x, y = [float(i) for i in detection.split(':')]
        coords.append((x, y))
        # crop the image based on the bounding box calculation.
        bbox = formBBox(x, y)
        cropped = image.crop(bbox)
        # save the cropped image to the right directory. If there are multiple
        # observations of the same class in the image they will be numbered to
        # separate them.
        filename = formFilename(observation, i)
        cropped.save(
            os.path.join(chipdir, observation['class'], filename + '.jpg')
        )
    return coords


def makeRandomChips(observation, N, coords, image):
    """Make N random chips from the image that are from the image that are not near anything
    listed in coords."""
    for i in range(N):
        overlap = True
        rand_x = random.randint(boxsize // 2, image.width - (boxsize//2))
        rand_y = random.randint(boxsize // 2, image.height - (boxsize//2))
        while overlap:
            overlap = checkForOverlap(rand_x, rand_y, coords)
            rand_x = random.randint(boxsize // 2, image.width - (boxsize//2))
            rand_y = random.randint(boxsize // 2, image.height - (boxsize//2))
        bbox = formBBox(rand_x, rand_y)
        cropped = image.crop(bbox)
        filename = os.path.join(
            chipdir,
            'other',
            observation['id'] + "_" + str(i) + ".jpg"
        )
        cropped.save(filename)


def formBBox(x, y):
    """Find the bounding box, given a x and y coordinate."""
    # this tuple can be passed direct into the Image.crop function
    return (
        x - boxsize // 2,
        y - boxsize // 2,
        x + boxsize // 2,
        y + boxsize // 2
    )


def formFilename(observation, observationnumber):
    """From an observation, find the filename that I want to save it in."""
    return observation['id'] + "_" + observation['class'] + "_" + \
        str(observationnumber)


def checkForOverlap(x, y, coords):
    """Checks if the x and y coordinates given are in the coords list."""
    def distance(x, y, coord):
        """Return the distance between the x, y coordinate and the coord
        tuple."""
        return math.sqrt((x - coord[0])**2 + (y - coord[1])**2)
    distances = [distance(x, y, c) for c in coords]
    if len(distances) > 0:
        return min(distances) > 150
    return False


if __name__ == "__main__":
    setupDirectories()
    makeChips('data/trainingObservations.csv')
