
import io
import vertexai
import os
from google import genai
from google.genai import types
from google.adk.tools.tool_context import ToolContext
from google.genai.types import GenerateContentConfig, Part
from PIL import Image
from io import BytesIO
import base64
from google.cloud import storage
import cairosvg

BUCKET_NAME = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
IMAGEN_MODEL_ID = "imagen-3.0-generate-002"

def get_storage_client():
    # Create a storage client
    return storage.Client()  

def upload_to_gcs(local_file: str, bucket_name: str, blob_name: str) -> str:
    # Upload file to GCS  
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_file)
    return f"gs://{bucket_name}/{blob_name}"

async def generate_image_data(tool_context: ToolContext, fact: str) -> dict:
    """
    Generates an image from 'fact', saves locally, uploads to GCS (BUCKET_NAME),
    and registers the image bytes as an artifact so ADK UI can display it.
    """
    if not BUCKET_NAME:
        return {"status": "error", "error_message": "Environment variable GOOGLE_CLOUD_STORAGE_BUCKET is not set (do not include gs://)."}
    
    print(f"Tool running: Generating image for '{fact}'...")

    try:
        client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
        response = client.models.generate_images(
        model=IMAGEN_MODEL_ID,
        prompt=f"Generate a single image in futuristic style representing the following fact: {fact}",
        config=types.GenerateImagesConfig(
            number_of_images=1,
            include_rai_reason=True,
            output_mime_type='image/png', # Specify the desired image format
            )
        )
        
        # Save the image to a file
        image_object = response.images[0]
        png_path = "image.png"
        with open(png_path, "wb") as f:
            image_object.save(png_path)

        # save image to gcs
        bucket_name = BUCKET_NAME
        png_uri = upload_to_gcs(png_path, bucket_name, "generated/image.png")

        #get image bytes and show image on the UI
        image_bytes = response.generated_images[0].image.image_bytes
        blob_part = Part.from_bytes(data=image_bytes, mime_type="image/png")

        try:
            res = await tool_context.save_artifact(filename="image.png", artifact=blob_part)
            return {
                'status': 'success',
                'result': res,
                'gcs_uri': png_uri
            }
        except Exception as e:
            error_message = f"Failed to save artifact: {e}"
            print(error_message)
            return {"status": "error", "error_message": error_message}
    
    except ValueError as ve:
        print(f"Configuration error: {ve}")
        return {"status": "error", "error_message": str(ve)} 



