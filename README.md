# CEliver model
This model is early liver cancer detection model, developed based on automated capillary electrophoresis data of cell-free DNA.

# Installation
## Docker-based
```
git clone https://github.com/cmuteam-medcmu/celiver.git
cd celiver
docker compose run --rm celiver
```

## Test with demo dataset
```
bash celiver-run.sh
```

## Run through python argument
```
#!/bin/bash

compose_path="docker-compose.yaml" 
output_dir="test"

docker compose -f $compose_path \
    -v $output_dir:/output \
    run --rm \
    celiver \
    --input dataset/true_label.csv \
    --prefic celiver \
    --fromraw True \
    --validate dataset/true_label.csv \
    --outdir /output
```

## Run through config file
```
#!/bin/bash

compose_path="docker-compose.yaml" 
output_dir="test"

docker compose -f $compose_path \
    -v $output_dir:/output \
    run --rm \
    celiver \
    -c test/config.yaml \
    -o /output
```

## Classes definition
- 0 = Non-cancer
- 1 = Liver cancer

# License
**CEliver © 2025** by _Cancer Research Unit_, _CMUTEAM_, _Faculty of Medicine_, _Chiang Mai University_ is licensed under <a href="https://creativecommons.org/licenses/by-nc/4.0/">CC BY-NC 4.0</a> <img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" width="20" height="20"> <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" width="20" height="20"> <img src="https://mirrors.creativecommons.org/presskit/icons/nc.svg" width="20" height="20"> 
