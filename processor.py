#
# as an example: process an mp4 file
#
import cv2
import pandas as pd
from glob import glob
from tqdm import tqdm
import time

# for OCI Vision client
import oci
from oci.ai_vision import AIServiceVisionClient

from oci_vision_utilities import OCIVisionImage

from config import LOCAL_DIR, LOCAL_DIR_OUT

# color map for logos
logo_names = ["Mobil1", "Oracle", "RedBull", "Siemens"]

label_map = {}
# the label returned from OCI Visio is Mobil1 and not Mobil
label_map["Mobil1"] = [169, 23, 69]  # blue
label_map["Oracle"] = [64, 57, 144]  # red [169, 23, 69]
label_map["RedBull"] = [112, 168, 162]  # green
label_map["Siemens"] = [169, 10, 60]  # ?

#
# some functions
#

# trasform the list as a string with logos separated by ,
def get_list_as_string(p_list):
    logo_str = ",".join([str(item) for item in p_list])

    return logo_str


# the name for the image file, with _bb added
def get_new_file_name(old_name):
    return old_name.split("/")[-1].split(".")[0] + "_bb.jpg"


class Processor:
    # removed start and duration, simplified

    def __init__(self):
        self.ENDPOINT = "https://vision.aiservice.eu-frankfurt-1.oci.oraclecloud.com"
        self.config = config = oci.config.from_file()
        # the OCI Vision model we're using
        self.MODEL_ID = "ocid1.aivisionmodel.oc1.eu-frankfurt-1.amaaaaaangencdyarrrcfnwo2yly3goldt4zwvvcs2bkerzwfrbntli74sta"

        # default
        self.EVERY = 1

    def extract_images(self, video_file_name):
        print("Extracting images from video...")

        # to build frame name, remove ".mp4"
        only_name = video_file_name.split(".")[0]
        # file is in local dir
        vidcap = cv2.VideoCapture(str(LOCAL_DIR / video_file_name))

        # get fps
        self.fps = int(vidcap.get(cv2.CAP_PROP_FPS))

        # count total number of frames
        tot_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        # first frame
        success, image = vidcap.read()

        count = 0
        with tqdm(total=tot_frames) as pbar:
            while success:
                frame_name = f"{only_name}{count:05d}.jpg"

                # frame written, as jpg, in local dir
                cv2.imwrite(str(LOCAL_DIR / frame_name), image)

                # read next frame
                success, image = vidcap.read()
                count += 1
                pbar.update(1)

        print(f"OK, extracted {count} imgs...")

        vidcap.release()

    def build_bb_film(self, video_file_name):
        # name without mp4
        only_name = video_file_name.split(".")[0]
        # take the list of files
        frame_bb_list = sorted(glob(str(LOCAL_DIR_OUT / f"{only_name}*.jpg")))

        print(f"We have {len(frame_bb_list)} frames..")
        print()

        # take a sample image to compute height, width
        img = cv2.imread(frame_bb_list[0])
        height, width, layers = img.shape

        new_video_name = only_name + "_bb.mp4"
        new_video_path_name = str(LOCAL_DIR_OUT / new_video_name)
        # H264 is crucial to be able to display in this app
        video = cv2.VideoWriter(
            new_video_path_name,
            fourcc=cv2.VideoWriter_fourcc(*"H264"),
            fps=int(self.fps / self.EVERY),
            frameSize=(width, height),
        )

        print("Building the new video, with annotation...")
        print()
        with tqdm(total=len(frame_bb_list)) as pbar:
            for f_name in frame_bb_list:
                img = cv2.imread(f_name)

                video.write(img)

                pbar.update(1)

        video.release()

    def process_images(self, video_file_name, every, threshold):
        # set evey from the slider
        self.EVERY = every

        # at this point we have to process, with OCI Vision model, each frame

        # get the list of names of the frames' files
        only_name = video_file_name.split(".")[0]
        frame_list = glob(str(LOCAL_DIR / f"{only_name}*.jpg"))

        # create oci vision client
        ai_service_vision_client = AIServiceVisionClient(
            config=self.config, service_endpoint=self.ENDPOINT
        )

        print("Processing images from video...")

        # the dict with results
        dict_res = {}

        # init counters
        for logo in logo_names:
            dict_res[logo] = 0

        i = 0
        tot_counted = 0
        for f_path_name in tqdm(frame_list):
            # process only every frames
            if i % self.EVERY == 0:
                # be careful with the threshold... too low and you have many fp
                oci_image = OCIVisionImage(
                    f_path_name,
                    self.MODEL_ID,
                    ai_service_vision_client,
                    label_map,
                    threshold,
                )

                # here we call OCI vision
                oci_image.analyze_image()

                # get logos identified in frame
                logos_str = get_list_as_string(oci_image.get_list_logos())

                for logo in logo_names:
                    if logo in logos_str:
                        # ok, count
                        dict_res[logo] += 1
                        tot_counted += 1

                # add the BB and save the annotated image
                im_bb = oci_image.get_image_with_bb()

                new_path_name = str(LOCAL_DIR_OUT / get_new_file_name(f_path_name))
                cv2.imwrite(new_path_name, im_bb)

            i += 1

        # remaining are no logo!
        dict_res["no logo"] = int(len(frame_list) / self.EVERY) - tot_counted

        # results are returned as a dictionary
        # where key is the logo name
        # and value is count
        return dict_res
