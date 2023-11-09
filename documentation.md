## Pipeline
### Face Detection:
Pre trained retinaface model is used to detect the faces in the input image. The detector model is able to detect all the faces in the image perfectly. <br>
### Face Recognition:
The detected faces are aligned properly and converted into a 512 dimensional vector using pretrained Arcface model. The faces are embedded into a 512 dimensional vector space. This model achieves SOTA performance using only 128 bytes per face. <br>
### Face Matching: 
The vector embeddings of all students in the class are stored beforehand. In the input picture, the faces are detected and compared with the precalculated face embeddings. The cosine distance between the embeddings are minimized to find the roll number. <hr>
### Image Processing:
The backend receives the image into the folder `uploads/`. It is fetched from there, and the ML model processes it and returns an array of roll numbers of students that are present in that image. Next, a function opens a `.csv` file (creates one if it doesn't exist) and updates the attendance of students


