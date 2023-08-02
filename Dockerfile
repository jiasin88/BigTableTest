
FROM python:3.9

#WORKDIR /app

RUN git clone https://github.com/jiasin88/BigTableTest.git .
#COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

#COPY . .


CMD ["python","write.py"]
#CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
