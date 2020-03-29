#!/usr/bin/env python

# AppleMusic Activity GDPR file to Elasticsearch
# Author: Clement 'CypressXt' Hampai
# Github: https://github.com/CypressXt/AppleMusic-Elastic

import argparse
import csv
import json
import datetime
import getpass
import requests


# Args management -------------------------------------------------------------
def handle_args():
    parser = argparse.ArgumentParser(
        description='AppleMusic GDPR export to Elasticsearch'
    )
    commands = parser.add_subparsers(title='sub-commands')
    setup_parser = commands.add_parser('setup')
    setup_parser.set_defaults(func=setup)
    setup_parser.add_argument(
        '-e',
        '--elastic-url',
        help='Elasticsearch server url',
        required=True
    )
    setup_parser.add_argument(
        '-k',
        '--kibana-url',
        help='Kibana server url',
        required=True
    )
    setup_parser.add_argument(
        '-x',
        '--basic-auth-username',
        help='HTTP basic auth username',
        required=False
    )
    inflate_parser = commands.add_parser('inflate')
    inflate_parser.set_defaults(func=inflate)
    inflate_parser.add_argument(
        '-i',
        '--csv-input-file',
        help='AppleMusic export file usually \
            "Apple Music Play Activity.csv"',
        required=True
    )
    inflate_parser.add_argument(
        '-e',
        '--elastic-url',
        help='Elasticsearch server url',
        required=True
    )
    inflate_parser.add_argument(
        '-x',
        '--basic-auth-username',
        help='HTTP basic auth username',
        required=False
    )
    return parser
# ------------------------------------------------------------------------------


# Setup -----------------------------------------------------------------------
def setup(args):
    elastic_url = args.elastic_url
    kibana_url = args.kibana_url
    auth_username = args.basic_auth_username
    auth = ""
    if auth_username:
        auth_passwd = getpass.getpass("HTTP basic auth password: ")
        auth = (auth_username, auth_passwd)
    try:
        print("Elasticsearch & kibana Setup...")
        print(" Elasticsearch "+str(elastic_url))
        print(" Kibana "+str(kibana_url))
        template = get_template()
        template_result = set_template(elastic_url, template, auth)
        if not template_result:
            raise Exception('Error while setting es template')
        visualizations = get_visualizations()
        push_visualizations(kibana_url, visualizations, auth)
    except Exception as excep:
        print(str(excep))
# ------------------------------------------------------------------------------


# Get Elasticsearch mapping from Github ---------------------------------------
def get_template():
    template_url = \
        "https://raw.githubusercontent.com/CypressXt/\
AppleMusic-Elastic/master/template_applemusic.json"
    call = requests.get(template_url)
    template = ''
    if call.status_code == 200:
        template = call.json()
    else:
        raise Exception('Failed to get the template for Github')
    print("     template downloaded from Github")
    return template
# ------------------------------------------------------------------------------


# Set Elasticsearch template --------------------------------------------------
def set_template(elastic_url, template, auth):
    template_url = elastic_url+"/_template/applemusic"
    headers = {'Content-type': 'application/json'}
    call = ""
    if auth:
        call = requests.put(
            template_url,
            data=json.dumps(template),
            headers=headers,
            auth=auth
        )
    else:
        call = requests.put(
            template_url,
            data=json.dumps(template),
            headers=headers
        )
    result = False
    if call.status_code == 200 and call.text == '{"acknowledged":true}':
        result = True
    else:
        raise Exception(
            'Failed to set the Elasticsearch template ' +
            str(template_url)+"\n" +
            str(call.text)
        )
    print("         template applied")
    return result
# ------------------------------------------------------------------------------


# Get Elasticsearch mapping from Github ---------------------------------------
def get_visualizations():
    visualizations = "https://raw.githubusercontent.com/CypressXt/\
AppleMusic-Elastic/master/kibana_dashboard_visualization.json"
    call = requests.get(visualizations)
    visualizations = ''
    if call.status_code == 200:
        visualizations = call.json()
    else:
        raise Exception('Failed to get visualizations for Github')
    print("     visualizations downloaded from Github")
    return visualizations
# ------------------------------------------------------------------------------


# Creating Elasticsearch visualizations and dashboards ------------------------
def push_visualizations(kibana_url, visualizations, auth):
    for visualization in visualizations:
        visualization_url = kibana_url + \
            "/api/saved_objects/" + \
            visualization["_type"] + "/" + visualization["_id"] + \
            "?overwrite=true"
        headers = {'Content-type': 'application/json', 'kbn-xsrf': 'true'}
        visualization_object = dict()
        visualization_object["attributes"] = visualization["_source"]
        call = ""
        if auth:
            call = requests.post(
                visualization_url,
                data=json.dumps(visualization_object),
                headers=headers,
                auth=auth
            )
        else:
            call = requests.post(
                visualization_url,
                data=json.dumps(visualization_object),
                headers=headers
            )
        if call.status_code == 200:
            print(
                "         pushing " + str(visualization["_type"]) +
                " " + visualization["_source"]["title"]
            )
        else:
            raise Exception(
                'Failed to push the Elasticsearch visualization \n  ' +
                str(visualization_url) +
                " " +
                str(visualization["_source"]["title"]) + "\n "
                + call.text
            )
# ------------------------------------------------------------------------------


# Inflate ---------------------------------------------------------------------
def inflate(args):
    input_file = args.csv_input_file
    elastic_url = args.elastic_url
    auth_username = args.basic_auth_username
    auth = ""
    if auth_username:
        auth_passwd = getpass.getpass("HTTP basic auth password: ")
        auth = (auth_username, auth_passwd)
    try:
        print("Reading CSV file...")
        csv_rows = read_csv_file(input_file)
        print("Generating json bulk datas...")
        json_bulk = generate_json_bulk(csv_rows)
        print("Elasticsearch insertion...")
        post_bulk(elastic_url, json_bulk, auth)
    except Exception as excep:
        print('An error occured '+str(excep))
# ------------------------------------------------------------------------------


# Read the Apple Music Play Activity csv file ---------------------------------
def read_csv_file(file):
    csv_rows = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        # Optimization needed here, working on it...
        for row in reader:
            for i in range(len(title)):
                if row[title[i]] == "":
                    row[title[i]] = None
            csv_rows.extend(
                [
                    {
                        title[i].lower().replace(' ', '_'):row[title[i]]
                        for i in range(len(title))
                    }
                ]
            )
    return csv_rows
# ------------------------------------------------------------------------------


# Generate the Elastic Json bulk datas ----------------------------------------
def generate_json_bulk(csv_rows):
    json_bulk = ""
    for data in csv_rows:
        json_bulk += str('%s\n' % json.dumps({'index': {}}))
        json_bulk += str('%s\n' % json.dumps(data, indent=0).replace('\n', ''))
    return json_bulk
# ------------------------------------------------------------------------------


# POST the Json bulk to Elasticsearch -----------------------------------------
def post_bulk(elastic_url, json_bulk, auth):
    index_date = datetime.datetime.now().strftime("%Y.%m.%d")
    elastic_index_url = elastic_url + \
        "/applemusic-" + str(index_date)+"/applemusic/_bulk"
    headers = {'Content-type': 'application/json'}
    chuck_size = 5000
    bulk_lines = json_bulk.split('\n')
    index = 0
    bulked = 0
    bulk = ''
    docs = len(bulk_lines)/2
    for bulk_line in bulk_lines:
        bulk += bulk_line+"\n"
        if bulk_line != '{"index": {}}':
            index += 1
        if index == chuck_size:
            bulked += chuck_size
            print(
                "\t\tinsertion " +
                str(bulked) + "/" +
                str(docs) + " events..."
            )
            bulk_exec(elastic_index_url, bulk, headers, auth)
            bulk = ''
            index = 0
    if index < chuck_size and index > 0:
        bulked += index
        print("\t\tinsertion " + str(bulked) + "/" + str(docs) + " events...")
        bulk_exec(elastic_index_url, bulk, headers, auth)
# ------------------------------------------------------------------------------


# Elasticsearch bulk exec -----------------------------------------------------
def bulk_exec(elastic_index_url, bulk, headers, auth):
    bulk_query = ""
    if auth:
        bulk_query = requests.post(
            elastic_index_url,
            data=bulk,
            headers=headers,
            auth=auth
        )
    else:
        bulk_query = requests.post(
            elastic_index_url,
            data=bulk,
            headers=headers
        )
    if bulk_query.status_code != 200:
        print(bulk_query.status_code, bulk_query.reason)
        print(bulk)
        print(bulk_query.text)
# ------------------------------------------------------------------------------


# Main ------------------------------------------------------------------------
if __name__ == "__main__":
    PARSER = handle_args()
    ARGS = PARSER.parse_args()
    try:
        ARGS.func(ARGS)
    except AttributeError:
        PARSER.print_help()
