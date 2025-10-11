# CHAI Bias

## Setup
Config.json :
```bash 
{
    "txt_path": ".....mapaie/data/txts",
  }
  
```
# visualisation
```bash
docker pull jheinecke/metamorphosed:latest

docker run --name metamorphosed -p 4567:4567 \
  --volume /home/ambroise012/CHAI-bias/data:/data \
  --env AMRFILE=bias-small.amr \
  jheinecke/metamorphosed:latest
```