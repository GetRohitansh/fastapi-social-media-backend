FROM python:3.10

# working directory set by WORKDIR
WORKDIR /usr/src/app

# ./ means in WORKDIR (working directory)
COPY requirements.txt ./ 

RUN pip install -r requirements.txt

# copy all from existing directory to WORKDIR
COPY . . 


# Why copy two times, because for optimization
# requirements takes longest time to install
# in docker each line is layer and it runs layer by layer ans stores result of each in cache
# hence if we change source code is comes directly to last COPY . . layer
# docker knows which file is changed this way

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]