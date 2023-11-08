# importing the pandas library 
import pandas as pd 
  
# reading the csv file 
df = pd.read_csv("test.csv") 
for row in df.iterrows():
    print(row[1]['Roll number'])
  
# updating the column value/data 
df['Attendance'] = '1' 
  
# writing into the file 
df.to_csv("test.csv", index=False) 
  
# print(df) 