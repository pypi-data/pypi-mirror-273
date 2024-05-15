import logging
import boto3
from PIL import Image
from typing import Tuple
from espy_pdfier.util import CONSTANTS
import os
import io

def is_greater_than_allowed_size(image_path):
    return os.path.getsize(image_path) > CONSTANTS.IMAGE_SIZE_MB * 1024 * 1024

def is_image_size_valid(file):
    max_size_mb = CONSTANTS.IMAGE_SIZE_MB * 1024 * 1024
    file_size_mb = file.file.seek(0, 2) / (1024 * 1024)  # Get file size in MB
    file.file.seek(0)  # Reset file pointer to the beginning
    return file_size_mb <= max_size_mb
    
def resize_image(image, size):
    resized_image = image.copy()
    resized_image.thumbnail(size)
    return resized_image

def store_image_in_s3(image_buffer, bucket_name, key):
    """Can be called directly to store image in S3.
    args:
    image_buffer: file.file from FastAPI file upload.
    """
    try:
        s3 = boto3.client('s3', aws_access_key_id=CONSTANTS.ACCESS_KEY, aws_secret_access_key=CONSTANTS.SECRET_KEY)
        s3.upload_fileobj(image_buffer,bucket_name, key)
    except Exception as e:
        logging.error(f"An error occured uploadig to s3: {str(e)}")
        raise Exception(f"An error occured: {str(e)}.")

def resize_and_store_images(image, 
                            bucket_name: str, 
                            thumbnail_size: Tuple[int, int] = (100, 100), 
                            display_size: Tuple[int, int] = (512, 512)):
    try:
        if not is_image_size_valid(image):
            raise ValueError("Image size exceeds the allowed limit.")
        
        store_image_in_s3(image.file, bucket_name, f"raw_{image.filename}")
        
        thumbnail_image = resize_image(image, thumbnail_size)
        display_image = resize_image(image, display_size)

        # Generate unique keys for each image size
        thumbnail_key = f"thumbnail_{image.filename}"
        display_key = f"display_{image.filename}"

        # Upload the resized images to S3
        thumbnail_buffer = io.BytesIO()
        thumbnail_image.save(thumbnail_buffer, format='WEBP')
        thumbnail_buffer.seek(0)
        store_image_in_s3(thumbnail_buffer, bucket_name, thumbnail_key)

        display_buffer = io.BytesIO()
        display_image.save(display_buffer, format='WEBP')
        display_buffer.seek(0)
        store_image_in_s3(display_buffer, bucket_name, display_key)
    except Exception as e:
        logging.error(f"An error occurred resizing and storing: {str(e)}")
        raise Exception(f"An error occurred: {str(e)}.")
