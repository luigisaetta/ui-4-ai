import pathlib

# this is the dir the streamlit app is launched from
APP_DIR = pathlib.Path(__file__).parent.absolute()

# the name of a file for logo image
# to be put in APP_DIR
LOGO = "logo.png"

# the list of file type supported (and that can be loaded)
FILE_TYPE_SUPPORTED = ["csv"]
