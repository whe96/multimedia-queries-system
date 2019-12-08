# CS576Final

# Frontend
  ### Views using Web
  ### Communication with backend
  ### Controls/Features
# Backend
### Pipeline
* Video query
* Multi-threads response to extract different features and compare
* Overall comparing strategy with dataset videos
* Response
### Goal
All feature extractions and comparison should be done within 5 seconds. The features need to be tested seperately to verify its accuracy (from human eyes). The dimensions of features shall be discussed later. Please write sample codes to setup and extract features and compare.
### Features
PyTorch Prefered
#### Color 
[Color Histogram](https://www.geeksforgeeks.org/opencv-python-program-analyze-image-using-histogram/)

Test on all 001.rgb images

|  | flower| interview| movie| music| sports|starcraft|traffic|
|:-----:|:-----:| :-------:| :----:| :-----:| :-----:| :-----:| :-----:| 
|flower| 1| 0.534|0.299|0.297|0.622|0.296|0.820|
|interview| |1.0| 0.001| 0.000|0.76|0.000|0.306
|movie| | |1.0|0.999 |0.126|0.999|0.741|
|music| | | |1.0|0.112|0.999|0.741|
|sports| | | | | 1.0 |0.112|0.298|
|starcraft| | | | | |1.0|0.741|
|traffic| | | | | | |1.0|



#### Frame Feature
ResNet 18
#### Multi-frame Feature 
R(2+1)D
#### Frame Motion Feature
LK or Dense Optical Flow (OpenCV)
#### Audio
MFCC (torchaudio)
#### Object Detection
### TODO
- [ ] Web (Zequn)
- [ ] Backend ComunicationPart (Zequn)
- [ ] Comparing Strategy
- [ ] Color (Zequn)
- [ ] Frame Feature (Jiarong) 
- [ ] Multi-frame Feature (Jiarong)
- [ ] Frame Motion Feature (Jiarong)
- [ ] Audio (Wenda)
- [ ] Object Detection (Wenda)
  
  
