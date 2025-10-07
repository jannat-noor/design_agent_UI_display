# Design Agent UI Display

Generates high-definition PNG images from user prompts using Vertex AI / Imagen, uploads them to Google Cloud Storage, and displays the image in the ADK UI (via `load_artifacts_tool`).

Sample generated image
- <img width="540" height="416" alt="image2" src="https://github.com/user-attachments/assets/596b0b9f-83ed-4992-a1b9-625d1956ce60" />

## Setup

1. Clone repo:
```bash
git clone https://github.com/jannat-noor/design_agent_UI_display.git
cd design_agent_UI_display
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create .env (see .env.example):
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
IMAGEN_MODEL_ID=imagen-3.0-generate-002
```
4. (Optional) Activate virtualenv:
```bash
python -m venv .venv
source .venv/bin/activate
```
## Usage
Run the agent:
```bash
python agent.py
```
Or run the Docker image:
```bash
docker build -t design-agent-ui .
docker run --env-file .env design-agent-ui
```
## Sample output detail
- image1.png is generated after user prompt: generate a blue sports car with a fall colored tree
- image2.png is generated after user prompt: remove the furistic style, generate the image on a riverbank


##Notes
1. Do not hardcode project/bucket credentials in code — use .env.
2. Ensure GOOGLE_CLOUD_STORAGE_BUCKET is just the bucket name (no gs://).
