from PIL import Image
import os
import shutil
import csv
from tqdm import tqdm
from itertools import groupby

chipdir = 'data/images/chips'
imagedir = 'data/images/training'


def setupDirectories():
    """Set up the directories that will hold the chips. Remove the old chips if
    they exist."""
    shutil.rmtree(chipdir, ignore_errors=True)
    os.mkdir(chipdir)
    for classname in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
        os.mkdir(os.path.join(chipdir, classname))


def makeChips(observationcsv):
    """Given a csv file containing the observations, make the image chips from
    the file."""
    with open(observationcsv) as f:
        reader = csv.DictReader(f)
        for filename, group in tqdm(groupby(reader, lambda x: x['image'])):
            image = Image.open(os.path.join(imagedir, filename))
            for observation in group:
                if observation['detections'] != 'None':
                    # if the detections field is None then no vehicles of this
                    # type were observed
                    processObservation(observation, image)


def processObservation(observation, image):
    """An observation is a row in the observation file. This might contain
    multiple detections of vehicles. Extract each of those observations into a
    separate image chip and save."""
    for i, detection in enumerate(observation['detections'].split('|')):
        # the x and y coords are separated by a colon
        x, y = detection.split(':')
        # crop the image based on the bounding box calculation.
        bbox = formBBox(float(x), float(y))
        cropped = image.crop(bbox)
        # save the cropped image to the right directory. If there are multiple
        # observations of the same class in the image they will be numbered to
        # separate them.
        filename = formFilename(observation, i)
        cropped.save(
            os.path.join(chipdir, observation['class'], filename + '.jpg')
        )


def formBBox(x, y):
    """Find the bounding box, given a x and y coordinate."""
    # boxsize in pixels
    boxsize = 150
    # this tuple can be passed direct into the Image.crop function
    return (
        x - boxsize / 2,
        y - boxsize / 2,
        x + boxsize / 2,
        y + boxsize / 2
    )


def formFilename(observation, observationnumber):
    """From an observation, find the filename that I want to save it in."""
    return observation['id'] + "_" + observation['class'] + "_" + \
        str(observationnumber)


if __name__ == "__main__":
    setupDirectories()
    makeChips('data/trainingObservations.csv')
