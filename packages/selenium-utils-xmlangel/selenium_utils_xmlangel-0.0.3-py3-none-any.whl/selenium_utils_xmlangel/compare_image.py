from skimage.metrics import structural_similarity as compare_ssim
import cv2

def compare_images(image_path1, image_path2):
        img1 = cv2.imread(image_path1)
        img2 = cv2.imread(image_path2)

        # Convert the images to grayscale
        img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Calculate th strutural similrity index (SSIM)
        ssim = compare_ssim(img1_gray, img2_gray)

        return ssim

image1_path = 'test1.png'
image2_path = 'test2.png'
similarity = compare_images(image1_path, image2_path)
print(f"similarity: {similarity}")

