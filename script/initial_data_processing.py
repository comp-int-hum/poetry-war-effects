import json
import gzip

with gzip.open('prewar_poetry.jsonl.gz','r') as ifd_pre,gzip.open('postwar_poetry.jsonl.gz','r') as ifd_post:
    for i,line in enumerate(ifd_pre):
        if i > 1000:
            break
        poem = json.loads(line)
        print(poem)