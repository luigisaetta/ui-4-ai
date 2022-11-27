import pathlib

# this is the dir the streamlit app is launched from
APP_DIR = pathlib.Path(__file__).parent.absolute()
LOCAL_DIR = APP_DIR / "local"
LOCAL_DIR_OUT = APP_DIR / "out"

# the name of a file for logo image
# to be put in APP_DIR
LOGO = "logo.png"

# the list of file type supported (and that can be loaded)
FILE_TYPE_SUPPORTED = ["mp4"]

# parameters for model
OCI_MODEL_ENDPOINT = "https://vision.aiservice.eu-frankfurt-1.oci.oraclecloud.com"
OCI_MODEL_ID = "ocid1.aivisionmodel.oc1.eu-frankfurt-1.amaaaaaangencdyarrrcfnwo2yly3goldt4zwvvcs2bkerzwfrbntli74sta"
