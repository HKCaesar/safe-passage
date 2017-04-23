
For this challenge.

https://www.datasciencechallenge.org/challenges/1/safe-passage/

Grab the data from there and put it in the right directories.

# Directory structure

    .
    ├── competition-instructions
    └── data
        └── images
            ├── test
            └── training

the `data` directory has the file `trainingObservations.csv` in it.

The `test` and `training` directories should have the unzipped jpg files in them.

I've saved the competition instructions and an analysis of them in the [competition-instructions](competition-instructions/readme.md) markdown file.

```bash
python src/form_chips.py
```

```bash
python retrain.py --image_dir data/images/chips
```
