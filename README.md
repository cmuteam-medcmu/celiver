# CEliver model 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18297357.svg)](https://doi.org/10.5281/zenodo.18297357)

This model is early liver cancer detection model, developed based on automated capillary electrophoresis data of cell-free DNA.

### Classes definition
- 0 = Non-cancer
- 1 = Liver cancer


# Installation
## Docker 
Docker >= 28.5.1 with docker compose plugin
[Docker installation](https://docs.docker.com/desktop/setup/install/linux/debian/)
```
git clone https://github.com/cmuteam-medcmu/celiver.git
cd celiver
docker compose run --rm celiver
```

### Test with demo dataset
```
bash celiver-run.sh
```

### Run through python argument
```
#!/bin/bash

compose_path="docker-compose.yaml" 
output_dir="test"

docker compose -f $compose_path \
    -v $output_dir:/output \
    run --rm \
    celiver \
    --input dataset/test_dataset.csv \
    --prefic celiver \
    --fromraw True \
    --validate dataset/true_label.csv \
    --outdir /output
```

### Run through configuration file
```
#!/bin/bash

compose_path="docker-compose.yaml" 
output_dir="test"

docker compose -f $compose_path \
    -v $output_dir:/output \
    run --rm \
    celiver \
    -c test/config.yaml
```

## Singularity
[Singularity installation](https://docs.sylabs.io/guides/3.0/user-guide/installation.html)
```
singularity pull celiver-v1.0.0.sif docker://moonipur148/celiver:latest
git clone https://github.com/cmuteam-medcmu/celiver.git
cd celiver
```

### Run through singularity with configulation file
```
#!/bin/bash

celiver_root="$PWD" # Change to your full path

singularity run --cleanenv \
    --pwd /work \
    -B "test":/output \
    -B $celiver_root:/work \
    celiver.sif \
    -c /work/test/config.yaml 
```

# Citation


# License
**CEliver © 2025** by _Cancer Research Unit_, _CMUTEAM_, _Faculty of Medicine_, _Chiang Mai University_ is licensed under <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a> <img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" width="20" height="20"> <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" width="20" height="20"> <img src="https://mirrors.creativecommons.org/presskit/icons/nc.svg" width="20" height="20"> 
