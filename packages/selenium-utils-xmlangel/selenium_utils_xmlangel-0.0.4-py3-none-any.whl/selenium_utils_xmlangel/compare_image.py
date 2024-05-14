from skimage.metrics import structural_similarity as compare_ssim
import cv2
import os

def compare_images(image_path1, image_path2):
    """
    Compare two images using structural similarity index (SSIM).

    Args:
        image_path1 (str): Path to the first image file.
        image_path2 (str): Path to the second image file.

    Returns:
        float: Similarity score between the two images.

    Raises:
        ValueError: If image paths are not provided.
        FileNotFoundError: If one or both image files do not exist.
    """
    
    if not image_path1 or not image_path2:
        raise ValueError("Image paths are not provided.")
    
    if not os.path.exists(image_path1) or not os.path.exists(image_path2):
        raise FileNotFoundError("One or both image files do not exist.")

    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)

    # Convert the images to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculate th strutural similrity index (SSIM)
    ssim = compare_ssim(img1_gray, img2_gray)

    return ssim
