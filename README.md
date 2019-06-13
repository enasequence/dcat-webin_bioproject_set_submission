# ENA BioProject Registration

This script has been produced to streamline the process of registering many
BioProjects with ENA in a single step. This is already supporting through
the existence of the PROJECT_SET XML object. The main contribution of this
script is to automate the production of this object from an input TSV, and
to then submit this to ENA.

It is possible to run the script without submission, in which case the XML
will be produced and the program will end.

A Webin account is required to use this script. You can register this here:
https://www.ebi.ac.uk/ena/submit/sra/

By default, the script will submit to the ENA test service. All
submissions to this service are removed after 24 hours. You should submit
first to test and review the results of this at:
https://wwwdev.ebi.ac.uk/ena/submit/sra/

Use the test server to convince yourself the TSV has been prepared
correctly,
then submit to the real server.

For assistance with the use of this script, please contact the ENA
helpdesk, currently at datasubs@ebi.ac.uk

## Installation
### Python version support
3
### Pip package using Conda

```bash
$ conda create -q -n yourenvname python=3.7.3

$ source activate yourenvname

$ pip install -U git+git://github.com/enasequence/dcat-webin-bioproject-set-submission.git

```

## Usage

```
study_subs [-h] [-u USERNAME] [-p PASSWORD] [-s] [-i INPUT_TSV] [-v] [-g]
```


## Options

```
-h, --help            show this help message and exit
-u USERNAME, --username USERNAME
                      Webin Username: Webin-XXXXX
-p PASSWORD, --password PASSWORD
                      Webin password
-s, --submit          Submit studies to ENA production, default=FALSE
-i INPUT_TSV, --input_tsv INPUT_TSV
                      Path to input TSV
-v, --validate        Validate TSV and quit, default=FALSE
-g, --generate_xml    Make XML and quit, default=FALSE
```
