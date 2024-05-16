import os
import numpy as np
import io, re
from skimage import io as skio, filters
from skimage.filters import threshold_local
import pytest

def preprocess_image(image, filename):
    # Perform image processing steps
    black_pixels = np.sum(image < 50 / 255.0)  # Convert threshold to range 0-1
    total_pixels = image.size
    black_percentage = black_pixels / total_pixels * 100

    if black_percentage > 40:
        # Invert the image by subtracting each pixel value from 255
        image = 1.0 - image
        
    block_size = 3
    offset = 0.0000001
    thresh_meth = 'gaussian'
    image = threshold_local(image, block_size, thresh_meth, offset)

    image = filters.unsharp_mask(image, radius=3, amount=3.5)

    new_path = "Dataset/temp/" + filename + "_processed.png"

    # Convert the image back to 8-bit integer before saving
    image = (image * 255).astype(np.uint8)

    skio.imsave(new_path, image) 

    return new_path

def replace_units(text):
    # Replace 'milligram' with 'mg'
    text = re.sub(r'\bmilligram\b', 'mg', text.lower(), flags=re.IGNORECASE)
    # Replace 'microgram' with 'mcg'
    text = re.sub(r'\bmicrogram\b', 'mcg', text.lower(), flags=re.IGNORECASE)
    # Replace 'milligrams' with 'mg'
    text = re.sub(r'\bmilligrams\b', 'mg', text.lower(), flags=re.IGNORECASE)
    # Replace 'micrograms' with 'mcg'
    text = re.sub(r'\bmicrograms\b', 'mcg', text.lower(), flags=re.IGNORECASE)

    text = text.replace(" ", "")
    return text

# Define a mapping function to replace "Smg" with "5mg"
def mapping(dosage_text):
    if "Smg" in dosage_text:
        dosage_text = dosage_text.replace("Smg", "5mg")
    if "S0mg" in dosage_text:
        dosage_text = dosage_text.replace("S0mg", "50mg")
    if "S00mg" in dosage_text:
        dosage_text = dosage_text.replace("S00mg", "500mg")
    if "Smcg" in dosage_text:
        dosage_text = dosage_text.replace("Smcg", "5mcg")
    return dosage_text

# Sample image path (modify as needed)
TEST_IMAGE_PATH = "C:/Users/jieru/Downloads/FIT3164/project/Medication-Dispensing-with-Image-Processing/Dataset_13-5-2024/372.png"


# Test cases for replace_units function
def test_replace_units_milligram():
    assert replace_units("Take 10 Milligrams") == "take10mg"

def test_replace_units_microgram():
    assert replace_units("Take 5 Micrograms") == "take5mcg"

def test_replace_units_mixed_case():
    assert replace_units("Take 20 MILLIGRAMS and 15 micrograms") == "take20mgand15mcg"

def test_replace_units_no_unit():
    assert replace_units("Take 30") == "take30"

def test_replace_units_no_change():
    assert replace_units("Take 25mg and 10mcg") == "take25mgand10mcg"

# Test cases for mapping function
def test_mapping_Smg():
    assert mapping("Take Smg daily") == "Take 5mg daily"

def test_mapping_S0mg():
    assert mapping("Take S0mg twice a day") == "Take 50mg twice a day"

def test_mapping_S00mg():
    assert mapping("Take S00mg three times a day") == "Take 500mg three times a day"

def test_mapping_Smcg():
    assert mapping("Take Smcg as needed") == "Take 5mcg as needed"

def test_mapping_no_change():
    assert mapping("Take 10mg and 20mcg") == "Take 10mg and 20mcg"


def test_preprocess_image_grayscale():
    """Tests if the image is converted to grayscale."""
    image = skio.imread(TEST_IMAGE_PATH, as_gray=True)
    processed_path = preprocess_image(image, "testimage")

    # Assert the processed image exists
    assert os.path.exists(processed_path)

    processed_image = skio.imread(processed_path)

    assert len(processed_image.shape) == 2, "Image should be grayscale (2D)"

def test_preprocess_image_local_thresholding_applied():
    """Tests if local thresholding is likely applied (basic check)."""
    image = skio.imread(TEST_IMAGE_PATH, as_gray=True)
    processed_path = preprocess_image(image, "testimage")

    processed_image = skio.imread(processed_path)

    # Check if there are variations in pixel intensity (suggests local thresholding)
    assert np.std(processed_image) > 10, "Local thresholding may not be applied"

def test_preprocess_image_unsharp_masking_applied():
    """Tests if unsharp masking is likely applied (basic check)."""
    image = skio.imread(TEST_IMAGE_PATH, as_gray=True)
    processed_path = preprocess_image(image, "testimage")

    processed_image = skio.imread(processed_path)

    # Check for high pixel values (suggests sharpening)
    assert np.any(processed_image > 220), "Unsharp masking may not be applied"

# Cleanup function (optional): Remove temporary processed images after tests
@pytest.fixture(autouse=True)
def cleanup_processed_images(scope="session"):
    yield
    processed_files = [f for f in os.listdir("Dataset/temp") if f.endswith("_processed.png")]
    for filename in processed_files:
        os.remove(os.path.join("Dataset/temp", filename))
