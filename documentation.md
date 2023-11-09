# attendance-marker - Documentation

## Tech Stacks Used
1. Flask
2. Deepface
3. TailwindCSS
4. HTML

## Pipeline
### Face Detection:
Pre trained retinaface model is used to detect the faces in the input image. The detector model is able to detect all the faces in the image perfectly. <br>
### Face Recognition:
The detected faces are aligned properly and converted into a 512 dimensional vector using pretrained Arcface model. The faces are embedded into a 512 dimensional vector space. This model achieves SOTA performance using only 128 bytes per face. <br>
### Face Matching: 
The vector embeddings of all students in the class are stored beforehand. In the input picture, the faces are detected and compared with the precalculated face embeddings. The cosine distance between the embeddings are minimized to find the roll number. <hr>

### Image Processing:
The backend receives the image into the folder `uploads/`. It is fetched from there, and the ML model processes it and returns an array (`list` in Python) of roll numbers of students that are present in that image. Next, a function opens a `.csv` file (creates one if it doesn't exist, from another standard file `sheets/reference.csv`) and updates the attendance of students using the data returned in the array. This involves the use of the pandas library and a Python `dict`. This CSV file will store the attendance of a particular day.
### Attendance Update:
The file `sheets/total_attendance.csv` stores the total attendance over all days. During a function call, this is converted into a pandas DataFrame and is updated with the attendance data obtained from the image. This is done with the help of a hash table or a Python `dict` and a pandas DataFrame.
### Conversions to PDF:
From the above processes, `.csv` files are read using pandas DataFrames and correspondingly PDF files are generated for the same with the use of the reportlab library of Python.


