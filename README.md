# DICOM to PNG Converter

This Python script converts DICOM (Digital Imaging and Communications in Medicine) files to PNG (Portable Network Graphics) format. It's designed to handle various types of DICOM images, including grayscale, RGB, and multi-slice images.
    
It is a modernized (2024), slimmed down fork of @danishm's [mritopng](https://github.com/danishm/mritopng)

## Features

- Converts DICOM files to PNG format
- Handles 2D (grayscale), 3D (RGB), and multi-slice images
- Maintains folder structure when converting multiple files
- Provides detailed logging of the conversion process

## Requirements

- Python 3.6+
- pydicom
- pypng
- numpy

You can install the required packages using pip:

```bash
pip install pydicom pypng numpy
```
    
    
## Usage

1. Clone this repository or download the `mritopng.py` script.

2. Run the script from the command line, providing the input DICOM folder and output PNG folder as arguments:

   ```bash
   python mritopng.py /path/to/dicom/folder /path/to/output/png/folder
   ```

   For example:

   ```bash
   python mritopng.py ~/Downloads/My_MRI ~/Downloads/My_PNG
   ```

3. The script will process all DICOM files in the input folder (including subfolders) and save the converted PNG files in the output folder, maintaining the original folder structure.

4. Check the `mritopng.log` file for detailed information about the conversion process, including any errors or warnings.

## Notes

- For multi-slice images, the script converts only the first slice and logs a message.
- If a DICOM file cannot be converted, the script logs an error and continues with the next file.
- The script normalizes pixel values to the 0-255 range for consistent PNG output.

## Contributing

Contributions to improve the script are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit)