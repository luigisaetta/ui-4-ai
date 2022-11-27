from oci.ai_vision import AIServiceVisionClient
from oci.ai_vision.models import AnalyzeImageDetails
from oci.ai_vision.models import ImageObjectDetectionFeature
from oci.ai_vision.models import InlineImageDetails
from oci.ai_vision.models import ObjectStorageImageDetails

import os
import base64
import json
import cv2


class OCIVisionImage:
    def __init__(
        self, path_name, model_id, ai_service_vision_client, label_map, threshold=0.5
    ):
        # the second parms is the OCID of the model
        self.MAX_RESULTS = 5
        self.MODEL_ID = model_id
        # it is used only to display bb
        self.THRESHOLD = threshold
        self.vision_client = ai_service_vision_client

        # color map for logos: one color for each logos
        self.label_map = label_map

        self.is_analyzed = False

        # read the image file with cv2
        self.path_name = path_name

        # store img as numpy array
        self.cv2_im = cv2.imread(self.path_name)
        # store the image as encoded string
        self.encoded_string = self.get_encoded_string()

        self.height, self.width, self.channels = self.get_image_size()

    def get_encoded_string(self):
        with open(self.path_name, "rb") as image_file:
            # we need to send as base64, UTF8

            return base64.b64encode(image_file.read()).decode("utf-8")

    def get_image_size(self):

        # Get Dimensions of Image
        height, width, channels = self.cv2_im.shape

        return height, width, channels

    # simplify the creation of the request to OCI Vision
    def prepare_request_4_vision(self):
        image_object_detection_feature = ImageObjectDetectionFeature()
        image_object_detection_feature.max_results = self.MAX_RESULTS

        # this is the ID of our custom model
        image_object_detection_feature.model_id = self.MODEL_ID

        # List of Features
        features = [image_object_detection_feature]

        # Create Analyze Image Object and set Image and Features
        analyze_image_details = AnalyzeImageDetails()
        inline_image_details = InlineImageDetails()

        inline_image_details.data = self.encoded_string
        analyze_image_details.image = inline_image_details
        analyze_image_details.features = features

        return analyze_image_details

    def analyze_image(self):
        # prepare the request
        analyze_image_details = self.prepare_request_4_vision()

        res = self.vision_client.analyze_image(
            analyze_image_details=analyze_image_details
        )

        self.is_analyzed = True
        self.raw_results = res.data

        # Extract Bounding Boxes from results
        # transform in JSON
        od_results = json.loads(str(self.raw_results))

        # store the od_bounding_boxes
        self.od_bounding_boxes = od_results["image_objects"]

        # create the sorted list of logos in the image
        list_logos = []

        if self.od_bounding_boxes is not None:
            for box in self.od_bounding_boxes:
                # using threshold also here
                if box["confidence"] >= self.THRESHOLD:
                    list_logos.append(box["name"])
        else:
            list_logos.append("")

        # remove duplicates and sort
        list_logos = sorted(list(set(list_logos)))

        self.list_logos = list_logos

    #
    # This 3 func give the result of analysis stored in the object
    #
    def get_raw_results(self):
        return self.raw_results

    def get_list_logos(self):
        return self.list_logos

    def get_image_with_bb(self):
        # set a threshold
        THRESHOLD = 0.5

        im_bb = self.cv2_im.copy()

        # Iterate over each Bounding Box and add to im_bb
        if self.od_bounding_boxes is not None:
            for box in self.od_bounding_boxes:
                if box["confidence"] >= self.THRESHOLD:
                    # Extract opposite coordinates for bounding box
                    # Un-Normalise the Data by scaling to the max image height and width
                    # Convert to Integer
                    pt1_x = int(
                        box["bounding_polygon"]["normalized_vertices"][0]["x"]
                        * self.width
                    )
                    pt1_y = int(
                        box["bounding_polygon"]["normalized_vertices"][0]["y"]
                        * self.height
                    )
                    pt2_x = int(
                        box["bounding_polygon"]["normalized_vertices"][2]["x"]
                        * self.width
                    )
                    pt2_y = int(
                        box["bounding_polygon"]["normalized_vertices"][2]["y"]
                        * self.height
                    )

                    # Build Points as Tuples
                    pt1 = (pt1_x, pt1_y)
                    pt2 = (pt2_x, pt2_y)

                    # Draw Bounding Boxes - Pass in Image, Top Left and Bottom Right Points, Colour, Line Thickness
                    cv2.rectangle(im_bb, pt1, pt2, self.label_map[box["name"]], 3)
                    # Plot Label just above the Top Left Point, Set Font, Size, Colour, Thickness
                    cv2.putText(
                        im_bb,
                        box["name"],
                        (pt1_x, pt1_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 0),
                        2,
                    )

        # return the image with bb
        return im_bb
