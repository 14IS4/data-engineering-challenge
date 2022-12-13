## Data Engineering Challenge Submission - Kendrick Horeftis



## Submission Items

1. [Python scripts](https://gitlab.com/khoreftis/data-engineering/-/tree/Development/atlas) written to solve the problem.
2. A [requirements.txt](https://gitlab.com/khoreftis/data-engineering/-/blob/Development/requirements.txt) file that contains the list of packages required to run my script.
3. An [output.txt](https://gitlab.com/khoreftis/data-engineering/-/blob/Development/output.txt) file containing the output from my script matching the expect output.
4. An [instructions.txt](https://gitlab.com/khoreftis/data-engineering/-/blob/Development/instructions.txt) file containing instructions on how to run my submission.

---

### Quick Start

- First thing that needs to be done is to set the `MYSQL_USER` and `MYSQL_PASS` environment variables in `env.sh`
- After that you can choose whether you want to run in the development or production environment by setting the `RUN_TYPE` environment variable to either `DEV` or `PROD`. It is defaulted to `DEV` and will load the final records into MySQL at the end of the run.
- Finally run the `setup.sh` script in order to set your environment variables and kick off the job with the default arguments.

---

### Usage

This project utilizes [Typer](https://typer.tiangolo.com/) to take in command line arguments. All of the arguments are configured with defaults but can be overridden with the CLI arugments or by setting the environment variables. 

*Please Note: the command line arguments will take precedence over any set environment variables*

```
python3 main.py --help
Usage: main.py [OPTIONS] [RUN_DATE]:[%Y-%m-%d] [DOX_BATCH_PERCENTAGE]
               [API_BATCH_PERCENTAGE] [VENDOR_BASE_URL] [API_VERSION]

Arguments:
  [RUN_DATE]:[%Y-%m-%d]   Please pass through a run_date if you would like to
                          override the default.  [default: 2017-02-02]
  [DOX_BATCH_PERCENTAGE]  Please enter a batch percentage for Doximity MySQL
                          between 1 and 100 if you would like to override the
                          default.  [env var: DOX_BATCH_PERCENTAGE;default:
                          10]
  [API_BATCH_PERCENTAGE]  Please enter a batch percentage for the Vendor API
                          between 1 and 100 if you would like to override the
                          default.  [env var: API_BATCH_PERCENTAGE;default:
                          10]
  [VENDOR_BASE_URL]       Please enter the base url for the Vendor API if you
                          would like to override the default, example:
                          https://example.com/api - don't enter the API
                          Version Number here.  [env var:
                          VENDOR_BASE_URL;default: https://de-tech-challenge-
                          api.herokuapp.com/api]
  [API_VERSION]           Please enter a valid API version for the Vendor API
                          if you would like to override the default. Not
                          implemented yet as there is only one version of the
                          API.  [env var: API_VERSION;default: 1]

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

---



### Project Structure

``` bash
├── GUIDELINES.md
├── README.md
├── atlas
│   ├── Dockerfile
│   ├── atlas
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dox.py
│   │   ├── main.py
│   │   ├── match.py
│   │   ├── setup.py
│   │   └── utils.py
│   ├── docs
│   ├── setup.cfg
│   ├── setup.py
│   ├── setup.sh
│   └── tests
├── instructions.txt
├── output.txt
└── requirements.txt
```
