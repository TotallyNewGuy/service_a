# Service A
This is the service for polling data from CTA api and publishing to Pub/Sub

## How to run

Service requires Python 3.10(or newer) to run.

1. Create a virtual environmen

```bash
python3 -m venv test_env
```
2. Activate the virtual environment (Linux)
```bash
source test_env/bin/activate
```
3. Install all required packages
```bash
pip install -r requirements.txt
```
4. Set environment variables
```bash
export PORT=<Port Number>
export DEBUG=<FALSE or TRUE>
export TOPIC_ID=<Targeted Topic Name In Pub/Sub>
export PROJECT_ID=<Google Cloud Platform Project ID>
export TRAIN_TRACKER_KEY=<CTA Bus API Key>
export GCP_CRED=<Google Cloud Platform Service Account Json String>
```

5. Start the app
```bash
python3 main.py
```
