Bioteksa Backend 
=======

This code is for  Bioteksa
Tested with Python 3.7.3 (default, Jun 20 2022, 17:56:55) 

Set it up
------
Export the following environment variables 
```
export LD_LIBRARY_PATH=/home/wsgi/Python-3.7.3/lib
export BIO_API_HOST=mysql://biobotTest:shinyWhal322@biobottest.ccttyurgugvu.us-east-1.rds.amazonaws.com/biobot_first_release
```

Create a virtual environment and install the requirements

    $ python3 -m venv ./backendenv
    $ source ./backendenv/bin/activate
    $ pip install --upgrade pip
    $ pip install -r requirements.txt

Start the development server

    $ chmod +x ./run
    $ ./run

Check the service at http://127.0.0.1:8001/

To run into production use the following Apache2 file:
```
biobackend.conf
```




