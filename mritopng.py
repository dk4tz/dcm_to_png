#!/usr/bin/env python3
import os
import logging
import argparse
import pydicom
import png
import numpy as np
from pydicom.pixel_data_handlers.util import convert_color_space

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mritopng.log"),
        logging.StreamHandler()
    ]
)

def normalize_pixel_array(pixel_array):
    """Normalize pixel array to 0-255 range."""
    pixel_min, pixel_max = pixel_array.min(), pixel_array.max()
    if pixel_max == pixel_min:
        return np.zeros(pixel_array.shape, dtype=np.uint8)
    return ((pixel_array - pixel_min) / (pixel_max - pixel_min) * 255).astype(np.uint8)

def dicom_to_png(dicom_path, png_path):
    """Convert a single DICOM file to a PNG image."""
    try:
        dicom = pydicom.dcmread(dicom_path)
        pixel_array = dicom.pixel_array

        if pixel_array.size == 0:
            logging.warning(f"Empty pixel array in '{dicom_path}'. Skipping.")
            return

        # Handle color images if present
        if dicom.PhotometricInterpretation in ['RGB', 'YBR_FULL']:
            if 'PlanarConfiguration' in dicom:
                pixel_array = convert_color_space(pixel_array, dicom.PhotometricInterpretation, 'RGB')

        pixel_normalized = normalize_pixel_array(pixel_array)

        # Handle different image dimensions
        if pixel_normalized.ndim == 3:
            if pixel_normalized.shape[2] == 3:  # RGB image
                image_data = pixel_normalized.reshape(-1, pixel_normalized.shape[1] * 3)
                greyscale = False
            else:  # Multi-slice image
                logging.info(f"Multi-slice image detected in '{dicom_path}'. Converting first slice.")
                image_data = pixel_normalized[0].tolist()
                greyscale = True
        elif pixel_normalized.ndim == 2:  # Grayscale image
            image_data = pixel_normalized.tolist()
            greyscale = True
        else:
            logging.warning(f"Unsupported image dimensions in '{dicom_path}'. Skipping.")
            return

        with open(png_path, 'wb') as png_file:
            writer = png.Writer(
                width=pixel_normalized.shape[1],
                height=pixel_normalized.shape[0] if pixel_normalized.ndim == 2 else pixel_normalized.shape[1],
                greyscale=greyscale
            )
            writer.write(png_file, image_data)
        
        logging.info(f"Converted '{dicom_path}' to '{png_path}'.")
    except Exception as e:
        logging.error(f"Failed to convert '{dicom_path}' to PNG: {e}")
        raise

def convert_all_dicoms(mri_folder, png_folder):
    """Convert all DICOM files in the specified folder to PNG format."""
    if not os.path.exists(mri_folder):
        logging.error(f"MRI_FOLDER '{mri_folder}' does not exist.")
        return

    os.makedirs(png_folder, exist_ok=True)

    for root, _, files in os.walk(mri_folder):
        rel_path = os.path.relpath(root, mri_folder)
        target_dir = os.path.join(png_folder, rel_path)
        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            if file.lower().endswith('.dcm'):
                dicom_path = os.path.join(root, file)
                png_filename = os.path.splitext(file)[0] + '.png'
                png_path = os.path.join(target_dir, png_filename)
                try:
                    dicom_to_png(dicom_path, png_path)
                except Exception as e:
                    logging.error(f"Error processing '{dicom_path}': {e}")
                    # Continue with the next file

def main():
    parser = argparse.ArgumentParser(description="Convert DICOM files to PNG format.")
    parser.add_argument("mri_folder", help="Path to the folder containing DICOM files")
    parser.add_argument("png_folder", help="Path to the folder where PNG files will be saved")
    args = parser.parse_args()

    convert_all_dicoms(args.mri_folder, args.png_folder)
    logging.info(f"Finished processing DICOM files in '{args.mri_folder}'.")

if __name__ == "__main__":
    main()