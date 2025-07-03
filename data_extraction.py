import json
import gzip # built-in decompression tool


with gzip.open('/scratch4/tlippin1/data/chadwyck_new.jsonl.gz','r') as ifd:
    count_pre_war = 0
    count_post_war = 0

    for line in ifd:
        poem = json.loads(line)

        # eliminate poems where author dob is unknown
        # question about this code block: modern poets?
        if poem['original_metadata']['author_dob'] == 'None':
            continue
        else:
            # extract the year in which the poem is written
            if poem['original_metadata']['year'] != '0':
                year_written = int(poem['original_metadata']['year'])
            else:
                if poem['original_metadata']['author_dod'] != 'None':
                    year_written = int(poem['original_metadata']['author_dob']) + 40
                else:
                    year_written = int(int((poem['original_metadata']['author_dob']) + int(poem['original_metadata']['author_dod'])) / 2)
            
            # check year_written conditions
            # write into jsonlines file
            # I don't know how to do that
            # so first I will count how many entries are in each category
            if year_written >= 1893 and year_written <= 1913:
                count_pre_war += 1
            elif year_written >= 1919 and year_written <= 1939:
                count_post_war += 1

print(count_pre_war) # 13950
print(count_post_war) # 11382