# MetaomeKB
Meta-ome KnowledgeBase

An AI-powered protein homology classifier that is built to assist researchers in collecting 
and analysing relevant metadata across multi-omics databases to conduct their experiments.

![MetaomeKB](./assets/image/MetaomeKB.png)

Setting up environment and installing libraries locally:
```
# Setting up a virtual environment
python -m venv env

# Activating the virtual environment
# Mac OS / Linux
source env/bin/activate

# Windows
.\env\Scripts\activate

# Installing packages using Pip
pip install -r requirements.txt
```

For local hosting, use the following docker command to build and run the image:
```
# Build image
docker build -f Dockerfile -t metaomekb:latest .

# Run image
docker run -p 80:8080 -e PORT=8080 metaomekb:latest
```

Pulling from DockerHub and running the image:
```
docker pull astralbloke/metaome-streamlit

docker run -p 80:8080 -e PORT=8080 astralbloke/metaome-streamlit
```
