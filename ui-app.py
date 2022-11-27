#
# L. Saetta, 2022
# this one is the general template
#

# check what imports you really need
import time
from PIL import Image
import streamlit as st

# all configs should be put in config.py
from config import APP_DIR, LOGO, FILE_TYPE_SUPPORTED

# the first is the dir where theframe extracted are saved
# the second is where the annotaed images are created
from config import LOCAL_DIR, LOCAL_DIR_OUT

#
# but if you want put other configs here
#

file_type_supported = FILE_TYPE_SUPPORTED

#
# Functions
#

#
# Here we load once the model
# singleton actually execute only the first time...
#
@st.experimental_singleton
def load_model(model_name):
    # put here all the code needed to load the model, if needed
    model = None

    # simulate
    print("Loading model...")
    print()
    time.sleep(2)

    return model


# Set app wide config
# should we move the string to the config file?
st.set_page_config(
    page_title="AI powered app | UI",
    page_icon="🤖",
    layout="wide",
    menu_items={
        "Get Help": "https://luigisaetta.it",
        "Report a bug": "https://luigisaetta.it",
        "About": "This is a UI for AI.",
    },
)

# add a logo
image = Image.open(APP_DIR / LOGO)
img_widg = st.sidebar.image(image)

# for now input could be only File, but in future could be also a url
input_type = st.sidebar.selectbox("Input Type", ["File"])

with st.sidebar.form("input_form"):
    # see list of supported file type
    input_file = st.file_uploader("File", type=file_type_supported)

    # configs can be expanded
    extra_configs = st.expander("Configs")
    with extra_configs:
        # add a listbox
        model_type = st.selectbox("Model type", options=["model1", "model2"], index=0)

        # add a radio button
        process_mode = st.radio(
            label="Process mode", options=["Yes", "No"], horizontal=True
        )

        threshold = st.slider(
            "Threshold",
            min_value=0.1,
            max_value=0.9,
            value=0.5,
            step=0.1,
        )

        every = st.slider(
            "Process every (frame)",
            min_value=1,
            max_value=10,
            value=1,
            step=1,
        )

    process = st.form_submit_button(label="Process")

# tw ocolumns on the right of the sidebar for output
# 1:1 ratio of col1 width compared to col2, you can change it here
col1, col2 = st.columns(gap="large", spec=[1, 1])

if process:
    # pushed button...

    # check that a file to process as been uploaded
    if input_file:

        # first make a local copy of the file
        print("Making a local copy of input file...")

        file_path = LOCAL_DIR / input_file.name

        with open(file_path, "wb") as f:
            f.write(input_file.read())

        # if we need to load a model, executed only once
        print(f"Model type is {model_type}")
        model = load_model(model_type)


        t_start = time.time()

        print(f"Process mode is {process_mode}")

        #
        # here we do the main processing
        #
        with st.spinner("Processing..."):
            print("Do something useful here...")
            print()
            time.sleep(2)

        t_ela = round(time.time() - t_start, 1)

        print()
        print(f"Elapsed time: {t_ela} sec.")
        print()

        col1.subheader(f"Statistics...")

        col1.write("Output here:")

        # happy... has finished
        st.success("Elaborations finished", icon="✅")
    else:
        # no file? please, upload it
        st.error("Please upload a file!")
