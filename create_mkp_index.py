#!/usr/bin/env python3
import glob, ast, json
output = []
for infofile in glob.glob('./*/src/info'):
    with open(infofile, 'r') as f:
        data = ast.literal_eval(f.read().strip())
        output.append({
            'title': data['title'],
            'name': data['name'],
            'description': data['description'],
            'version': data['version'],
            'version_required': data['version.min_required'],
            'mkp': f"{data['name']}/{data['name']}-{data['version']}.mkp"
        })
        print(f"{data['title']}, {data['version']}")

with open('mkp_index.json', 'w') as outfile:
    json.dump(output, outfile)
