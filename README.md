# attendance-marker
<strong>A web application for recording class attendance with computer vision.</strong>

## Team Details
* Naren Kumar Sai Kaja (220001049)
* S Ruthvik (220001064)
* P C Uma Mahesh (220001052)

## Installation and Localhost
* Clone this repository using:
  ```
  git clone https://github.com/Naren-Sai-17/attendance-marker
  cd attendance-marker
  ```
* Install requirements using pip:
  ```
  pip install -r requirements.txt
  ```
* Start the local server:
  ```
  python main.py
  ```
* The website can now be viewed [here](http://127.0.0.1:5000). If that doesn't work, click the link specified in the terminal.

## How To Use
* Select the date on which the attendance is to be recorded, as shown below.
* Click on "Process Image".
* The attendance for that particular date will be updated in the backend and a success message indicating the same will be displayed. 
* You can also view a preview of the total attendance of the class recorded till date as below:

## Pipeline
### Face Detection:
Pre trained retinaface model is used to detect the faces in the input image. The detector model is able to detect all the faces in the image perfectly. <br>
### Face Recognition:
The detected faces are aligned properly and converted into a 512 dimensional vector using pretrained Arcface model. The faces are embedded into a 512 dimensional vector space. This model achieves SOTA performance using only 128 bytes per face. <br>
### Face Matching: 
The vector embeddings of all students in the class are stored beforehand. In the input picture, the faces are detected and compared with the precalculated face embeddings. The cosine distance between the embeddings are minimized to find the roll number. <hr>
### Image Processing:
The backend receives the image into the folder `uploads/`. It is fetched from there, and the ML model processes it and returns an array of roll numbers of students that are present in that image. Next, a function opens a `.csv` file (creates one if it doesn't exist) and updates the attendance of students


