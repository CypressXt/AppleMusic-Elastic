#!/usr/bin/env python

### AppleMusic Activity GDPR file to Elasticsearch
# Author:   Clément 'CypressXt' Hampaï
# Github:   https://github.com/CypressXt/AppleMusic-elastic

import argparse, csv, json, requests


# Args management --------------------------------------------------------------
def handle_args():
    parser = argparse.ArgumentParser(description='AppleMusic GDPR export to Elasticsearch')
    parser.add_argument('-i', '--csv-input-file', help='AppleMusic GDPR export file usually "Apple Music Play Activity.csv"',required=True)
    parser.add_argument('-e', '--elastic-index-url', help='Elasticsearch index full url',required=True)
    args = parser.parse_args()
    return args
#-------------------------------------------------------------------------------

# Main -------------------------------------------------------------------------
def main(args):
    input_file = args.csv_input_file
    elastic_index_url = args.elastic_index_url
    try:
        print "Reading CSV file..."
        csv_rows = read_csv_file(input_file)
        print "Generating json bulk datas..."
        json_bulk = generate_json_bulk(csv_rows)
        print "Elasticsearch insertion..."
        post_bulk(elastic_index_url, json_bulk)
     except Exception as e:
        print 'An error occured '+str(e)
#-------------------------------------------------------------------------------

# Read the Apple Music Play Activity csv file ----------------------------------
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
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
    return csv_rows
#-------------------------------------------------------------------------------

# Generate the Elastic Json bulk datas -----------------------------------------
def generate_json_bulk(csv_rows):
    json_bulk = ""
    for data in csv_rows:
        json_bulk+=str('%s\n' % json.dumps({'index': {}}))
        json_bulk+=str('%s\n' % json.dumps(data, indent=0).replace('\n', ''))
    return json_bulk
#-------------------------------------------------------------------------------

# POST the Json bulk to Elasticsearch ------------------------------------------
def post_bulk(elastic_index_url, json_bulk):
    elastic_index_url += "/applemusic/_bulk"
    headers = {'Content-type': 'application/json'}
    bulk = requests.post(elastic_index_url, data=json_bulk, headers=headers)
    print(bulk.status_code, bulk.reason)
    print(bulk.text)
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    args = handle_args()
    main(args)
