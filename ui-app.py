#
# L. Saetta, 2022
#

# check what imports you really need
import time
from PIL import Image
import pandas as pd
import streamlit as st

# all configs should be put in config.py
from config import APP_DIR, LOGO, FILE_TYPE_SUPPORTED

#
# Configs
#

# put here the list of supported file type
file_type_supported = FILE_TYPE_SUPPORTED

#
# Here we load once the model
#
@st.experimental_singleton
def load_model(model_name):
    # put here all the code needed to load the model, if needed
    model = None

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

# Render input type selection on the sidebar & the form
input_type = st.sidebar.selectbox("Input Type", ["File"])

with st.sidebar.form("input_form"):
    # see list of supported file type
    input_file = st.file_uploader("File", type=file_type_supported)

    # add a radio button
    process_mode = st.radio(
        label="Process mode", options=["Yes", "No"], horizontal=True
    )

    process = st.form_submit_button(label="Process")

if process:
    # shows a spinner indicator
    with st.spinner("Work in progress..."):
        t_start = time.time()

        print("Do something useful...")
        print(f"Process mode is {process_mode}")
        # simulate
        time.sleep(2)

        t_ela = round(time.time() - t_start, 1)

        print()
        print(f"Elapsed time: {t_ela} sec.")
