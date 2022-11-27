# A User Interface for AI (ui-4-ai)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repo contains the work I have done to build (initially for myself) a reusable UI application 
that can be used to demo almost any AI solution. 

The app is based on the **Streamlit** library

## Template and demo
In this repo you will find:
* a [template](https://github.com/luigisaetta/ui-4-ai/blob/main/ui-app.py) that can be used as starting point to build the UI for your demo
* a [demo](https://github.com/luigisaetta/ui-4-ai/blob/main/ui-app-demo.py) example, based on **OCI Vision Service**

To run the template you only need, in addition to ui-app.py, the file config.py

## Features
* how to manage the upload of a file to be processed
* Various widgets (slider, radio, selectbox)
* singleton, to load model once

## Python libraries needed
* Streamlit
* PIL (if you work with images)

The code has been tested with **Python 3.10**


