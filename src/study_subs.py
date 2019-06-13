#!/usr/bin/env python3
# study_subs.py

"""
Accepts a table of study attributes in TSV format, parses them to a
PROJECT_SET XML, validates the XML and then submits it to ENA.
Options exist to just generate the XML and validate it, without submitting.

Usage: python3 study_subs.py -u [Username] -p [Password] -i [File] ...

-u  Webin Username: Webin-XXXXX
-p  Webin password
-i  Path to input TSV
-s  Submit studies to ENA production, default=FALSE
-v  Validate TSV and quit, default=FALSE
-g  Make XML and quit, default=FALSE
-h  Print help and quit

TODO:
  - Validate content of TSV file
  - Merge various functions for readability, maintainability, etc.
"""

import argparse
import csv
import os
import re
import sys
import subprocess
import xml.etree.ElementTree as ET
from lxml import etree


def parse_opts():
    """Define and parse options"""
    parser = argparse.ArgumentParser(description="Register studies with ENA")
    parser.add_argument("-u", "--username", type=str,
                        help="Webin Username: Webin-XXXXX")
    parser.add_argument("-p", "--password", type=str,
                        help="Webin password")
    parser.add_argument("-s", "--submit", action="store_true",
                        help="Submit studies to ENA production, default=FALSE")
    parser.add_argument("-i", "--input_tsv", type=str,
                        help="Path to input TSV")
    parser.add_argument("-v", "--validate", action="store_true",
                        help="Validate TSV and quit, default=FALSE")
    parser.add_argument("-g", "--generate_xml", action="store_true",
                        help="Make XML and quit, default=FALSE")

    if len(sys.argv) == 1:
        parser.print_help()
        print("\n")
        quit()

    args = parser.parse_args()
    return args


def validate_credentials(username, password, submit):
    """Validate credentials


    Keyword arguments:
    username -- a Webin username
    password -- password associated with username
    submit -- flag to indicate whether submission is production or test

    Returns:
    bool -- indicates whether credentials were successfully validated
    """
    # Build curl command:
    curl = "curl"
    u_flag = "-u"

    # Concatenation will fail if one value cannot be coerced to string
    try:
        credentials = (username + ":" + password)
    except (NameError, TypeError):
        print("Username or password is null, cannot validate submission")
        return False

    submission = "-F SUBMISSION=@VALIDATE.xml"

    if submit:
        url = "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    else:
        url = "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"

    # Submission command with validation XML to check credential validity
    print("Validating Webin credentials:")
    credential_check = subprocess.check_output([curl, u_flag, credentials,
                                                submission, url],
                                               universal_newlines=True)

    # Handle result of check
    if re.search("Access Denied", credential_check):
        print("Invalid username/password")
        return False
    else:
        print("Credentials validated")
        return True


def get_rows(input_tsv):
    """Parse input CSV into list of rows

    Keyword arguments:
    input_tsv -- input TSV containing study metadata

    Returns
    _csv.reader -- content of input file
    """
    tsv_rows = csv.reader(open(input_tsv, 'r'), delimiter='\t')
    return tsv_rows
    # see tsv2xml.py



def validate_csv_row(row):
    """Validate input spreadsheet content

    Keyword arguments:
    row -- a list of study metadata describing a single study
    """
    #TODO: include validation
    # write and call subfunctions to validate each element
    return True


def csv_to_xml(row):
    """Convert row from input TSV to study set XML

    Keyword arguments:
    row -- a list of study metadata descrbing a single study

    Returns:
    ElementTree -- content of input row in PROJECT XML format
    """

    project = etree.Element('PROJECT', alias=row[0])
    project_xml = etree.ElementTree(project)

    name_elt = etree.SubElement(project, 'NAME')
    name_elt.text = row[1]

    title_elt = etree.SubElement(project, 'TITLE')
    title_elt.text = row[2]

    description_elt = etree.SubElement(project, 'DESCRIPTION')
    description_elt.text = row[3]

    submission_project_elt = etree.SubElement(project, 'SUBMISSION_PROJECT')

    sequencing_project_elt = etree.SubElement(submission_project_elt,
                                              'SEQUENCING_PROJECT')

    if len(row) == 5:
        locus_tag_prefix_elt = etree.SubElement(sequencing_project_elt,
                                                'LOCUS_TAG_PREFIX')
        locus_tag_prefix_elt.text = row[4]

    return project_xml


def generate_study_xml(input_tsv, generate_xml):
    """Generate Project Set XML

    Keyword arguments:
    input_tsv -- input TSV containing study metadata
    generate_xml -- boolean, if true then generate XML and quit
    """
    csv_rows = csv.reader(open(input_tsv, 'r'), delimiter='\t')
    next(csv_rows)  # Skips header row

    project_set_xml_file = open('project_set.xml', 'wb')

    project_set = etree.Element('PROJECT_SET')
    project_set_xml = etree.ElementTree(project_set)

    row_number = 0

    for row in csv_rows:
        validate_csv_row(row)  # Revisit line once function does something
        project_xml = csv_to_xml(row)

        child_project = project_xml.getroot()
        project_set.insert(row_number, child_project)

        row_number += 1

    project_set_xml.write(project_set_xml_file, pretty_print=True,
                          xml_declaration=True, encoding='UTF-8')

    project_set_xml_file.close()

    if generate_xml:
        quit()


def generate_submission_xml(instruction):
    """Generates submission xml containing instruction for database

    Keyword arguments:
    instruction -- either 'ADD' or 'VALIDATE', to be inserted into XML
    """
    submission_xml_file = (instruction + '.xml')
    submission_xml_file = open(submission_xml_file, 'wb')

    submission = etree.Element('SUBMISSION')
    submission_xml = etree.ElementTree(submission)
    actions_elt = etree.SubElement(submission, 'ACTIONS')
    action_elt = etree.SubElement(actions_elt, 'ACTION')
    instruction_elt = etree.SubElement(action_elt, instruction)

    submission_xml.write(submission_xml_file, pretty_print=True,
                         xml_declaration=True, encoding='UTF-8')
    submission_xml_file.close()


def curl_validate(username, password, submit, validate):
    """Run submission with validation XML, use to decide whether to proceed

    Keyword arguments:
    username -- a Webin username
    password -- password associated with username
    submit -- flag to indicate whether submission is production or test
    validate -- boolean, if true then validate XML and quit
    """
    # Build curl command:
    curl = "curl"
    u_flag = "-u"

    # Concatenation will fail if one value cannot be coerced to string
    try:
        credentials = (username + ":" + password)
    except (NameError, TypeError):
        print("Username or password is null, cannot validate submission")
        return False

    submission = "-F SUBMISSION=@VALIDATE.xml"
    xml = "-F PROJECT=@project_set.xml"

    if submit:
        url = "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    else:
        url = "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"

    # Submission command with validation XML to check credential validity
    print("Validating project set submission:")
    validate_study_xml = subprocess.check_output([curl, u_flag, credentials,
                                                  submission, xml, url],
                                                 universal_newlines=True)
    print(validate_study_xml)

    # Handle result of check
    if re.search("Access Denied", validate_study_xml):
        print("Access to ENA submission server denied")
        return False
    elif re.search("success=\"false\"", validate_study_xml):
        print("Invalid submission, please check input TSV")
        return False
    elif re.search("success=\"true\"", validate_study_xml) and validate:
        print("Study set validated, exiting")
        return False
    elif re.search("success=\"true\"", validate_study_xml):
        print("Study set validated, proceeding")
        return True
    else:
        print("Study set could not be processed, exiting")
        return False

    return False


def curl_submit(username, password, submit):
    """Submit to ENA, return output of submission

    Keyword arguments:
    username -- a Webin username
    password -- password associated with username
    submit -- flag to indicate whether submission is production or test

    Returns:
    bool -- indicates whether submission was successful or not
    """
    # Build curl command:
    curl = "curl"
    u_flag = "-u"

    # Concatenation will fail if one value cannot be coerced to string:
    try:
        credentials = (username + ":" + password)
    except (NameError, TypeError):
        print("Username or password is null, cannot validate submission")
        return False

    submission = "-F SUBMISSION=@ADD.xml"
    xml = "-F PROJECT=@project_set.xml"

    if submit:
        url = "https://www.ebi.ac.uk/ena/submit/drop-box/submit/"
    else:
        url = "https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/"

    # Submission command with validation XML to check credential validity
    print("Submitting project set:")
    submit_study_xml = subprocess.check_output([curl, u_flag, credentials,
                                                submission, xml, url],
                                               universal_newlines=True)

    # Handle result of check
    if re.search("Access Denied", submit_study_xml):
        print("Access to ENA submission server denied")
        return False, submit_study_xml
    elif re.search("success=\"false\"", submit_study_xml):
        print("Invalid submission, please check input TSV")
        return False, submit_study_xml
    elif re.search("success=\"true\"", submit_study_xml) and submit:
        print("Study set submission completed")
        return True, submit_study_xml
    elif re.search("success=\"true\"", submit_study_xml):
        print("Study set TEST submission completed")
        return True, submit_study_xml
    else:
        print("Study set could not be processed, exiting")
        return False, submit_study_xml

    return False, submit_study_xml


def report_accessions(submission_result):
    """Report Accessions

    Keyword arguments:
    submission_result -- captured output of curl submission, XML receipt object
    """
    tree = ET.fromstring(submission_result)
    #root = tree.getroot()

    print("Assigned accessions follow:\n")
    print("Alias\tPrimary_ID\tSecondary_ID")

    for project in tree.findall("PROJECT"):
        alias = project.get("alias")
        prj = project.get("accession")
        erp = project.find("EXT_ID").attrib.get("accession")
        print("%s\t%s\t%s" % (alias, prj, erp))

    for messages in tree.findall('MESSAGES'):
        infos = messages.findall('INFO')
        for info in infos:
            if re.match("This submission is a TEST", info.text):
                print("\nNOTICE: this was a TEST submission, you have not "
                      "yet submitted any ENA studies. If you are happy "
                      "with this submission, rerun with the `-s` flag")


def __main__():

    user_args = parse_opts()

    # Check an input CSV has been given:
    if user_args.input_tsv:
        infile_exists = os.path.isfile(user_args.input_tsv)

    if user_args.input_tsv and infile_exists:
        pass
    else:
        print("Input file path invalid or no path given, exiting")
        quit()

    # Generate validation XML
    generate_submission_xml("VALIDATE")

    # Validate credentials if we will be running curl commands:
    if user_args.generate_xml:
        pass  # Credential validation is irrelevant in this case
    else:
        if validate_credentials(user_args.username, user_args.password,
                                user_args.submit):
            pass
        else:
            print("Credential validation failed, exiting")
            quit()

    # Produce project set XML
    generate_study_xml(user_args.input_tsv, user_args.generate_xml)

    # Generate submission XML
    generate_submission_xml("ADD")

    file_validity = curl_validate(user_args.username, user_args.password,
                                  user_args.submit, user_args.validate)

    if file_validity:
        pass
    else:
        quit()

    submission_result = curl_submit(user_args.username, user_args.password,
                                    user_args.submit)

    if submission_result[0]:
        report_accessions(submission_result[1])
    else:
        quit()


if __name__ == "__main__":
    __main__()
