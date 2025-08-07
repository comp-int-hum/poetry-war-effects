import json
import gzip
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dataset',dest = 'dataset',default ='/scratch4/tlippin1/data/chadwyck_new.jsonl.gz',help = 'dataset tp examine')
parser.add_argument('--latest_year_prewar',dest = 'latest_year_prewar',type = int, default = 1864,help = 'the latest year authors are born, so that their works are considered prewar')
parser.add_argument('--earliest_year_postwar',dest = 'earliest_year_postwar',type = int, default = 1904,help = 'the earliest year authors are born, so that their works are considered postwar')
parser.add_argument('--prewar_from',dest = 'prewar_from',type = int, default = 1893,help = 'from what year the poems are considered prewar')
parser.add_argument('--prewar_to',dest = 'prewar_to',type = int, default = 1913,help = 'to what year the poems are considered prewar')
parser.add_argument('--postwar_from',dest = 'postwar_from',type = int, default = 1919,help = 'from what year the poems are considered postwar')
parser.add_argument('--postwar_to',dest = 'postwar_to',type = int, default = 1939,help = 'to what year the poems are considered postwar')
parser.add_argument('--output_prewar',dest = 'output_prewar',default = 'work/prewar_poetry.jsonl.gz',help = 'jsonlines file of prewar poetry')
parser.add_argument('--output_postwar',dest = 'output_postwar',default = 'work/postwar_poetry.jsonl.gz',help = 'jsonlines file of postwar poetry')
args = parser.parse_args()

with gzip.open(args.dataset,'r') as ifd, gzip.open(args.output_prewar,'w') as ofd_pre, gzip.open(args.output_postwar,'w') as ofd_post:
    count_pre_war = 0
    count_post_war = 0

    for line in ifd:
        poem = json.loads(line)
        author_dob = poem['original_metadata']['author_dob']

        if author_dob == 'None':
            continue
        else:
            # extract the year in which the poem is written
            if poem['original_metadata']['year'] != '0':
                year_written = int(poem['original_metadata']['year'])
            else:
                if int(author_dob) <= args.latest_year_prewar or int(author_dob) >= args.earliest_year_postwar: # author is born at least 50 years before WWI (prewar), or author is never drafted into WWI (postwar)
                    year_written = int(author_dob) + 35
                else:
                    year_written = 0
            
            # check year_written conditions
            # write into jsonlines file
            # count number of poems in each category
            if year_written >= args.prewar_from and year_written <= args.prewar_to:
                count_pre_war += 1
                ofd_pre.write(line)
            elif year_written >= args.postwar_from and year_written <= args.postwar_to:
                count_post_war += 1
                ofd_post.write(line)

print(count_pre_war) # 13950
print(count_post_war) # 11382
