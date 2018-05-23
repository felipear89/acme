# xerpa
## Requirements
Docker or python 3.6.0 (used in development)

## How to run?
There are two input parameters to run
#### --config
The path of the config file
#### --timeclock
The path of the timeclock file

### Using docker
Run the command:
`docker run -it --rm --name acme-timesheet -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.6.5-alpine3.7 python main.py --config input_files/config.json --timeclock input_files/timeclock_entries.json`
### Your bash
Run the command:
`python main.py --config input_files/config.json --timeclock input_files/timeclock_entries.json`

## Notice
Only days with two or four entries is valid

## Tests
Just install and run *pytest*

`pip install pytest`

or using docker

`docker build -t xerpa .`

`docker run -it --rm --name just-testing xerpa`