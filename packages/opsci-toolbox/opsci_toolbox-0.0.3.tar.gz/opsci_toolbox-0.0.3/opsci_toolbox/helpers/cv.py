import os
from PIL import Image
import supervision as sv
import cv2
import numpy as np

def open_image(image_path):
    """
    Open and return an image.

    Parameters:
    - image_path (str): The path to the image file.

    Returns:
    - Image object: The opened image.
    """
    try:
        # Open the image file
        img = Image.open(image_path)
        return img
    except Exception as e:
        print(f"Error opening image: {e}")
        return None
    
def save_image(image, output_path, name):
    """
    Save an image to the local disk.

    Parameters:
    - image (Image object): The image to be saved.
    - output_path (str): The path to save the image.

    Returns:
    - bool: True if saving is successful, False otherwise.
    """
    try:
        # Save the image to the specified path
        file_path=os.path.join(output_path, name)
        image.save(file_path)
        return file_path
    except Exception as e:
        print(f"Error saving image: {e}")
        return False
    
def convert_image_format(input_path, output_path, output_filename, output_format="JPEG"):
    """
    Convert an image to another image format (ex from PNG to JPEG)
    """
    try:
        file_path=os.path.join(output_path, output_filename+"."+output_format)
        # Open the input image
        with Image.open(input_path) as img:
            # Convert and save the image to the desired format
            img.convert("RGB").save(file_path, format=output_format)
            print(f"Image converted successfully: {file_path}")
    except Exception as e:
        print(f"Error converting image: {e}")

    return file_path
    
def resize_image(image, new_width, new_height):
    """
    Resize an image to the specified width and height.

    Parameters:
    - image : PIL image
    - new_width (int): The desired width of the resized image.
    - new_height (int): The desired height of the resized image.

    Returns:
    - Image object: The resized image.
    """
    try:
        # Open the image file
        
        resized_img = image.resize((new_width, new_height))

        return resized_img
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None
    
def crop_image(image, x, y, width, height):
    """
    Crop an image based on the specified coordinates and dimensions.

    Parameters:
    - image : PIL image
    - x (int): The x-coordinate of the top-left corner of the cropping region.
    - y (int): The y-coordinate of the top-left corner of the cropping region.
    - width (int): The width of the cropping region.
    - height (int): The height of the cropping region.

    Returns:
    - Image object: The cropped image.
    """
    try:
        # Crop the image
        cropped_img = image.crop((x, y, x + width, y + height))

        return cropped_img
    except Exception as e:
        print(f"Error cropping image: {e}")
        return None
    
def flip_image(image, direction='horizontal'):
    """
    Flip an image horizontally or vertically.

    Parameters:
    - image : PIL image
    - direction (str): The direction of the flip ('horizontal' or 'vertical').

    Returns:
    - Image object: The flipped image.
    """
    try:
       
        # Flip the image
        if direction == 'horizontal':
            flipped_img = image.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            flipped_img = image.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            print("Invalid flip direction. Please use 'horizontal' or 'vertical'.")
            return None

        return flipped_img
    except Exception as e:
        print(f"Error flipping image: {e}")
        return None


def rotate_image(image, angle):
    """
    Rotate an image by the given angle (in degrees).

    Parameters:
    - image : PIL image
    - angle (float): The angle by which to rotate the image (in degrees).

    Returns:
    - Image object: The rotated image.
    """
    try:

        # Rotate the image
        rotated_img = image.rotate(angle)

        return rotated_img
    except Exception as e:
        print(f"Error rotating image: {e}")
        return None

def convert_to_grayscale(image):
    """
    Convert a color image to grayscale.

    Parameters:
    - image : PIL image

    Returns:
    - Image object: The grayscale image.
    """
    try:
        
        # Convert the image to grayscale
        grayscale_img = image.convert("L")

        return grayscale_img
    except Exception as e:
        print(f"Error converting image to grayscale: {e}")
        return None
    
def PIL_get_image_size(image):
    """
    Get PILLOW image size
    """
    width, height = image.size
    return  width, height

def cv_get_image_size(image):
    """
    Get cv2 image size
    """
    height, width, _ = image.shape
    return width, height

def convert_PIL_to_cv(image):
    """
    Convert an image from Pillow to CV2
    """
    numpy_array = np.array(image)
    cv2_image = cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)
    return cv2_image

def convert_cv2_to_pil(cv2_image):
    """
    Convert an image from CV2 to Pillow
    """
    # Convert the cv2 image to RGB format
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    
    # Create a PIL Image from the RGB image
    pil_image = Image.fromarray(rgb_image)
    
    return pil_image

def compress_image(image, output_path, name, quality):
    """
    Compress an image with a specified quality level.

    Parameters:
    - image object
    - output_path (str): The path to save the compressed image.
    - name of the file
    - quality (int): The quality level for compression (0 to 100, higher is better).

    Returns:
    - file_path
    """
    try:
        # Open the image file
        file_path=os.path.join(output_path, name)
        image.save(file_path, quality=quality)

        return file_path
    except Exception as e:
        print(f"Error compressing image: {e}")
        return False
    

def cv2_read_image(path):
    """
    Read an image file
    """
    image = cv2.imread(path)
    return image

def cv2_write_image(image, path, name):
    """
    Write an image file
    """
    file_path=os.path.join(path, name)
    cv2.imwrite(file_path, image)
    return file_path

def cv2_crop_image(image, xmin, ymin, xmax, ymax):
    """
    Crop image by coordinates
    """
    cropped_img=image[ymin:ymax, xmin:xmax]
    return cropped_img

def cv2_flip(image, direction='horizontal'):
    """
    Flip an image using CV2
    """
    if direction=='horizontal':
        flipped_image = cv2.flip(image, 1)
    elif direction=='vertical':
        flipped_image = cv2.flip(image, 0)
    else:
        print("error - direction should be horizontal or vertical")
    return flipped_image

def cv2_rotate_image(image, angle):
    """
    Rotate an image using CV2
    """

    # Get the height and width of the image
    height, width = image.shape[:2]

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)

    # Apply the rotation to the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    return rotated_image

def cv2_convert_to_grayscale(image):
    """
    Convert an image to grayscale using CV2
    """

    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return grayscale_image
    
def draw_circle(image, x, y, size=5, color=(255, 0, 0)):
    """
    Draw a circle on a CV2 image
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_with_circle=cv2.circle(image_rgb, (x,y), size, color, -1)
    return image_with_circle


def apply_mask(image, mask, color_mask=[255, 255, 255], reverse=True, transparency=1.0):
    """
    Apply a transparent color mask on an image
    """
    # Validate transparency value
    transparency = max(0.0, min(1.0, transparency))

    # Create a copy of the image
    masked_image = np.copy(image)

    # Calculate alpha value based on transparency
    alpha = int(255 * (1 - transparency))

    # Set the alpha channel of the color_mask
    color_mask_with_alpha = color_mask + [alpha]

    # Create a mask for the region where the color_mask will be applied
    region_mask = np.stack([mask] * 3, axis=-1)

    if reverse:
        # Set the color_mask with alpha where the mask is False
        masked_image[~region_mask] = color_mask_with_alpha
    else:
        # Set the color_mask with alpha where the mask is True
        masked_image[region_mask] = color_mask_with_alpha

    return masked_image


def transform_coordinates_CV_to_YOLO(left, top, width, height):
    """
    Transform MS Custom Vision annotation format to YOLO
    """
    
    center_x = left + (width/2)
    center_y = top + (height/2)
    return (center_x, center_y, width, height)


def transform_coordinates_PascalVOC_to_YOLO(xmin, ymin, xmax, ymax, width, height):
    """
    Transform PascalVOC coordinates to YOLO
    """
    x_center = ((xmax + xmin) / 2) / width
    y_center = ((ymax + ymin) / 2) / height
    box_width = (xmax - xmin) / width
    box_height = (ymax - ymin) / height
    return (x_center, y_center, box_width, box_height)


def transform_coordinates_YOLO_to_PascalVOC(center_x, center_y, width, height, image_width, image_height):
    """
    Convert YOLO coordinates to Pascal VOC format.

    Parameters:
    - YOLO format coordinates center_x, center_y, width, height
    - image_width (int): Width of the image
    - image_height (int): Height of the image

    Returns:
    - tuple: Pascal VOC coordinates (xmin, ymin, xmax, ymax)
    """

    # Convert YOLO coordinates to absolute coordinates
    abs_x = int(center_x * image_width)
    abs_y = int(center_y * image_height)
    abs_width = int(width * image_width)
    abs_height = int(height * image_height)

    # Calculate Pascal VOC coordinates
    xmin = max(0, int(abs_x - abs_width / 2))
    ymin = max(0, int(abs_y - abs_height / 2))
    xmax = min(image_width, int(abs_x + abs_width / 2))
    ymax = min(image_height, int(abs_y + abs_height / 2))

    return xmin, ymin, xmax, ymax



def sv_detections_ultralytics(results):
    """
    Loads detections from results
    """
    detections = sv.Detections.from_ultralytics(results)
    return detections

def sv_convert_mask_to_box(masks):
    """
    Convert mask coordinates to boxes
    """
    detections = sv.Detections(
      xyxy=sv.mask_to_xyxy(masks=masks),
      mask=masks
    )
    return detections


def sv_annotate_image_bbox(image, detections):
    """
    Draw a bounding box
    """
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
    return annotated_image


def sv_annotate_image_mask(image, detections):
    """
    Draw a mask area on an image
    """
    mask_annotator = sv.MaskAnnotator()
    annotated_image = mask_annotator.annotate(scene=image, detections=detections)
    return annotated_image

def sv_annotate_image_label(image, detections, model, color=sv.Color.ROBOFLOW, text_color=sv.Color.WHITE, text_position=sv.Position.TOP_CENTER):
    """
    Draw a label rectangle on detections
    """
    # possible values for colors : https://supervision.roboflow.com/latest/draw/color/#supervision.draw.color.Color
    # Possible positions for text relative to the detection = "CENTER" / "CENTER_LEFT" / "CENTER_RIGHT" / "TOP_CENTER"
    # "TOP_LEFT" / "TOP_RIGHT" / "BOTTOM_LEFT" / "BOTTOM_CENTER" / "BOTTOM_RIGHT" / "CENTER_OF_MASS"

    label_annotator = sv.LabelAnnotator(color=color, text_color=text_color, text_position=text_position)

    labels = [
        model.model.names[class_id]
        for class_id
        in detections.class_id
    ]

    annotated_image = label_annotator.annotate(scene=image, detections=detections, labels=labels)

    return annotated_image



    

    




