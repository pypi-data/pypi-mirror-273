import numpy as np
import cv2
import os
from patchify import patchify, unpatchify
from typing import *
from data.data_processing import roi_extraction_coords_direct, padder, set_outside_pixels_to_zero


import logging
# Create a logger object
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.INFO)
# Create a handler for writing to a file
file_handler = logging.FileHandler('log.txt')

# Create a handler for writing to the console
console_handler = logging.StreamHandler()

# Create a formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Create a logger for this module
logger = logging.getLogger(__name__)


def create_folder(folder_name: str) -> None:
    """
    Create a folder if it doesn't exist.

    Author: Vlad Matache 224108@buas.nl
    :param folder_name: Name of the folder to create.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    else:
        print(f"Folder '{folder_name}' already exists.")


def check_input_type(input_data: any) -> str:
    """
    Check the type of the input data.

    Author: Vlad Matache, 224108@buas.nl
    :param input_data: Input data to check.
    """
    if type(input_data) is str:
        return "str"
    elif type(input_data) is np.ndarray:
        return "np.ndarray"
    else:
        return "unspported"


def load_image(image_path: str, verbose: bool = True) -> np.ndarray:
    """
    Load an image from a given path.

    Author: Vlad Matache, 224108@buas.nl
    :param image_path: Path of the image to load.
    :param verbose: Print additional information.
    :return: Loaded image.
    """
    if check_input_type(image_path) != "str":
        logger.error(f"Unsupported input type: {check_input_type(image_path)}")
    else:
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Image not found at: {image_path}")
        elif len(image.shape) != 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        if verbose:
            logger.info(f"Loaded image with shape: {image.shape}")
        return image


def load_images_from_folder(folder_path: str, verbose: bool = True) -> tuple[list, list]:
    """
    Load images from a given folder.

    Author: Vlad Matache, 224108@buas.nl
    :param folder_path: Path of the folder containing the images.
    :param verbose: Print additional information.
    :return: List of loaded images.
    """
    if check_input_type(folder_path) != "str":
        logger.error(
            f"Unsupported input type: {check_input_type(folder_path)}")
    else:
        images = []
        filenames = []
        paths = []
        for filename in os.listdir(folder_path):
            image = load_image(os.path.join(folder_path, filename), verbose)
            images.append(image)
            filenames.append(filename)
            paths.append(os.path.join(folder_path, filename))
        if verbose:
            logger.info(
                f"Loaded {len(images)} images from folder: {folder_path}")
        return images, filenames, paths
