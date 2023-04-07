#!/usr/bin/env python3
import glob, ast, json
output = []
for infofile in glob.glob('./*/src/info'):
    with open(infofile, 'r') as f:
        data = ast.literal_eval(f.read().strip())
        output.append({
            'title': data['title'],
            'description': data['description'],
            'mkp': f"{data['name']}/{data['name']}-{data['version']}.mkp"
        })

with open('mkp_index.json', 'w') as outfile:
    json.dump(output, outfile)
