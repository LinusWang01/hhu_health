#based on Python3.6
FROM python:3.6
#copy source
ADD ./src /
# set workdir
WORKDIR /
# install dependency
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "check_in.py" ]
