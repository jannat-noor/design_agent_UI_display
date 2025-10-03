from google import adk
from google import genai
from google.adk.agents import Agent
from google.adk.tools.load_artifacts_tool import load_artifacts_tool
# Import the tools
from .tools import generate_image_data, upload_to_gcs

import os
# Add credentials here or in the .env 
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "default-project")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
BUCKET_NAME = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
IMAGEN_MODEL_ID = "imagen-3.0-generate-002"

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# Create the ADK agent
root_agent = adk.Agent(
    model="gemini-2.0-flash",
    name="design_agent",
    description="Greeting design agent",
    instruction="""
    You are a design assistant or image generation assistant. Introduce yourself as Design Assistant.
    Ask user to describe a design they want as detail as possible. Use the 'ImageGen' tool to create images from user prompts. 
    Display the image_artifact in the response using the load_artifacts_tool. 
    """, # Generate all images with black backgroud 
    tools=[generate_image_data, load_artifacts_tool],
)