import json
import gzip

with gzip.open('work/data_examination.jsonl.gz','r') as ifd:
    for line in ifd:
        print(line)