import json
import gzip

with gzip.open('work/prewar_poetry.jsonl.gz','r') as ifd_pre,gzip.open('work/postwar_poetry.jsonl.gz','r') as ifd_post:
    for i,line in enumerate(ifd_pre):
        if i > 15:
            break
        poem = json.loads(line)
        content = poem['content']['stanzas']
        for item in content:
            print(item)