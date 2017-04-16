# Problem specification

Problem is to identify the position of vehicles within images.
These vehicles are of various classes.

 - A
     - Motorcycle
 - B
     - Light short rear - light coloured vehicles with a short end
 - C
     - Light long rear - light coloured vehicles with a longer end
 - D
     - Dark short rear - as above but dark
 - E
     - Dark long rear - as above but dark
 - F
     - Red short rear - as above but red
 - G
     - Red long rear - as above but red
 - H
     - Light van
 - I
     - Red and white bus

When generating the ground truth, the observations were classified as low or high confidence.
The training examples only contain the high confidence examples,
so it has eliminated cases that couldn't be determined accurately.

## Image file format

Here is the file format for submission.
It is also the format of `trainingObservations.csv`.

    id,image,class,detections 
    TQ2379_0_0_A,TQ2379_0_0.jpg,A,None
    TQ2379_0_0_B,TQ2379_0_0.jpg,B,1776:520|1824:125 
    TQ2379_0_0_C,TQ2379_0_0.jpg,C,1760:456F

So a csv with the id, the image, 
and a pipe delimited field that contains the (x,y) coordinates of the centre of the vehicle in the image.
If there are more than one type of that vehicle in the image,
this is what causes the pipe delimited set of records.

## Acceptance boundaries

There are _acceptance boundaries_.
Which are the radius from the centre point to the edge of the acceptance boundary.
If you predict a position within that acceptance boundary,
you get a correct classification.

|   Class           |   Acceptance Radius   |
|-------------------|-----------------------|
|   A (motorcycle)  |   12 pixels (60cm)    |
|   B-G (cars)      |   30 pixels (150cm)   |
|   H (van)         |   40 pixels (200cm)   |
|   I (bus)         |   45 pixels (225cm)   |

## Scoring

Scoring is done via the jaccard index.

The low confidence classifications mentioned above come into the scoring.
They won't mind if you identify something that is a low confidence vehicle.

-------

# Notes on solving the problem

This is going to be a bit trickier than just throwing a CNN at it.
The problem isn't to identify if this is a picture of something,
instead it is to find where those vehicles are in the image.

[0] suggests that this is still an open problem in computer vision,
and links to the paper about _overfeat_ [1].

Gravity isn't important in these images, in fact the orientation of them isn't important.
What translations of the images should we do?

[0] http://stackoverflow.com/questions/28178054/does-convolutional-neural-network-possess-localization-abilities-on-images

[1] https://arxiv.org/pdf/1312.6229v4.pdf

[2] https://lmb.informatik.uni-freiburg.de/Publications/2016/OB16a/oliveira16icra.pdf

[3] https://www.cs.toronto.edu/~vmnih/docs/Mnih_Volodymyr_PhD_Thesis.pdf
