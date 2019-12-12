# CS576Final

# Frontend

# Backend
### Pipeline
* Video query
* Multi-threads response to extract different features and compare
* Overall comparing strategy with dataset videos
* Response
### Goal
All feature extractions and comparison should be done within 5 seconds. The features need to be tested separately to verify its accuracy (from human eyes). The dimensions of features shall be discussed later. Please write sample codes to setup and extract features and compare.
### Environment
* PyTorch
* Python3.7
### Evaluation on features
##### Self validation
1. Compute the similarity simiA between two random snippets in the same video video1.
2. Compute the similarity simiB between a snippet in video1 and a snippet in other class of videos.
3. Select videos other than video1 one time each to perform Step 2, and perform the same amount of trials in Step1.
4. The similarity margin in one iterations is avg(simiA)-avg(simiB). Do Step1-3 1000 times to compute the expectation of this similarity difference.

P.S. We use only 1000 iterations because it could get a fair expectation of this margin.
For color histogram, the margin with different iterations flows as followed, 

| |10|100|500|1000|5000|10000|
|---|---|---|---|---|---|---|
|margin(%)|29.6|27.5|29.3|29.1|28.9|29.0|

##### Test on new videos
Build new unseens test dataset for every category.

### Features
#### Color 
[Color Histogram](https://www.geeksforgeeks.org/opencv-python-program-analyze-image-using-histogram/)
margin:15%
self:95%
other:80%


#### Frame Feature
ResNet 18
margin:12.3%
self:96.7%
other:84.3%

#### Frame Motion Feature
Dense Optical Flow (OpenCV)
margin:19.5%
self:70.1%
other:51%

#### Audio
MFCC (torchaudio)
margin 9%
self: 98%
other:89%

  
