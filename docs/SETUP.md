# Setting Up The Server #

## Setup ##

Do all your work in some specific directory that is convenient for you. I will
call the directory ROOT. On my local computer, this directory is
/home/twn/Projects/declassengine/

(1) Create an emtpy file inside declassengine called \_\_init__.py. On Linux or
Mac you can do this by running the following at the command line:

```
touch ROOT/__init__.py
```

(2) Next clone the api.git repository into the declassengine folder.

(3) This guide assumes that you have all the python dependencies already
which very well may not be true. The easiest way to satisfy dependencies is to
run the installation script SETUP_API.sh. The script will download all necessary
dependencies and configure the python path for your ROOT directory. It will
also create an environment variable called DECLASS_API pointing to the api
folder.

You can do this by modifying line #3 of SETUP_API.sh and replacing ROOT with the
location to your home directory. Once you do that, run:

```
sudo ./SETUP_API.sh
```

Note that you may have to run

```
sudo bash ./SETUP_API.sh
```

In fact, every time you re-launch the project from a new shell terminal,
you will have to call "sudo SETUP_API.sh" to configure the shell environment
variables.

The final directory structure should look like this (not all files/folders are
shown):

```
ROOT/
├── __init__.py
└── api/
    ├── __init__.py
    └── src/
        └── declass_api.py
```

Testing it out
--------------

If everything worked correctly, the script should download all missing dependencies
and should start the server.

You should see a message similar to  
* Running on http://0.0.0.0:5000/

and then recieve a nice greeting by entering http://0.0.0.0:5000/declass
into your browser.
