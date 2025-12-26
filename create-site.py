from Cheetah.Template import Template
from urllib.parse import quote
import json
import os
import sys

if len(sys.argv) < 3:
    print(f"{sys.argv[0]} index.json output_folder")
    exit(1)

index_json = sys.argv[1]
output_path = sys.argv[2]

if not os.path.isfile(index_json):
    print(f'{index_json} does not exist or is not a file')
    exit(2)

if not os.path.isdir(output_path):
    print(f'{output_path} does not exist or is not a directory')
    exit(3)

f = open(index_json, "r")
if not f:
    print(f'Could not open {index_json}')
    exit(4)

repository_data = json.loads(f.read())
f.close()

if not repository_data or not isinstance(repository_data, dict):
    print(f'{index_json} does not define a repository object')
    exit(5)

namespace = {"repository": repository_data, "encoded_repository_url": quote(repository_data['url'], safe='')}
website_path = "Website"
for file_to_convert in ["app.js", "index.html"]:
    website_file_path = os.path.join(website_path, file_to_convert)
    f = open(website_file_path, 'r')
    template_data = f.read()
    f.close()
    output_file_path = os.path.join(output_path, file_to_convert)
    output_file = open(output_file_path, 'w')
    templated = Template(template_data, searchList=[namespace])
    output_file.write(str(templated))

