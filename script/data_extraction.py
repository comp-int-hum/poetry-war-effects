import json
import gzip # built-in decompression tool


with gzip.open('/scratch4/tlippin1/data/chadwyck_new.jsonl.gz','r') as ifd, gzip.open('/home/jzhan299/poetry_project/work/prewar_poetry.jsonl.gz','w') as ofd_pre, gzip.open('/home/jzhan299/poetry_project/work/postwar_poetry.jsonl.gz','w') as ofd_post:
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
                if int(author_dob) <= 1864 or int(author_dob) >= 1904: # author is born at least 50 years before WWI (prewar), or author is never drafted into WWI (postwar)
                    year_written = int(author_dob) + 35
                else:
                    year_written = 0
            
            # check year_written conditions
            # write into jsonlines file
            # count number of poems in each category
            if year_written >= 1893 and year_written <= 1913:
                count_pre_war += 1
                ofd_pre.write(line)
            elif year_written >= 1919 and year_written <= 1939:
                count_post_war += 1
                ofd_post.write(line)

print(count_pre_war) # 13950
print(count_post_war) # 11382