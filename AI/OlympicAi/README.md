# Overview of files

## Requirements
### Conda
Make sure you have conda installed, and running environment with python version 3.9.
Later pythonversions may be incompatible with MediaPipe.
Create a new conda environment with 'conda create -n {nameOfEnv} python=3.9 -y'
Activate environment by first running 'source activate base' then 'conda activate {nameOfEnv}'

### Necessary libraries

To run this directory make sure to download/pip install the following libraries:

1. MediaPipe
    - Install this by running first 'pip install mediapipe ipykernel'
    - then 'python -m ipykernel install --user --name=MediaPipe --display-name "Python (MediaPipe)"'
2. OpenCV
3. FastAPI
4. NumPy
5. Uvicorn


## AI folder

### MediaPipe.py

This file is the MediaPipe model where we introduce the class "MediaPipeVideoProcessor". 
This file is created to use the MediaPipe model, and create necessary functions to either extract necessary information from uploaded videos, or determine how to process the videos.

### test.py

This is a simple file to test different methods created in "MediaPipe.py" to see if it works as intended

### Utils.py

This file is created to have supporting functions for "MediaPipe.py". The intent is to structure helper functions here to help make "MediaPipe.py" well structured and easy to understand by avoiding doing everything inside some functions.



## Backend folder

This folder contains the file "main.py" which is the file that contains different FastAPI methods.



## MoveNet folder

This folder is created for our potentially alternative model called MoveNet. There have not been any work done here yet, just some tutorials. This folder might be depricated in later stages if we decide to to experiment with it



## Videos folder

Potentially a temporary folder. Will be used to store videos for either training, or store generated videos. 






# How to start FastAPI localhost

Run the following command in powershell given that you have the necessary libraries. The following prompt is based on if you are in the "OlympicAI" folder:

uvicorn backend.main:app --reload 