import json
import gzip # built-in decompression tool

#all_poems = []
author_poem_counts = {}
lines_per_stanza_by_poem_and_author= {}

#with gzip.open('/scratch4/tlippin1/data/chadwyck.jsonl.gz','r') as ifd:
    #for i,line in enumerate(ifd):
        #if i > 10000:
            #break
        #poem = json.loads(line)
        #all_poems.append(poem)
        #author = poem['author']
        #if author not in author_poem_counts:
            #author_poem_counts[author] = 1
        #else:
            #author_poem_counts[author] += 1

with gzip.open('/scratch4/tlippin1/data/chadwyck.jsonl.gz','r') as ifd:
    for line in ifd:
        poem = json.loads(line)
        author = poem['author']
        title = poem['title']
        stanzas = poem['stanzas']

        # first dictionary: author_poem_counts
        if author not in author_poem_counts:
            author_poem_counts[author] = 1
        else:
            author_poem_counts[author] += 1

        # second dictoinary: lines_per_stanza_by_poem_and_author
        # data structure: {author 1:[{poem 1:[{stanza 1:14 lines}]},{poem 2: [{stanza 1: 20 lines},{stanza 2: 20 lines}]}]
        if author not in lines_per_stanza_by_poem_and_author:
            lines_per_stanza_by_poem_and_author[author] = []
        else:
            lines_per_stanza = []
            for i in range(len(stanzas)):
                lines_per_stanza.append({f'stanza {i+1}':f'{len(stanzas[i])} lines'})
            lines_per_stanza_by_poem_and_author[author].append({title:lines_per_stanza})

#print(lines_per_stanza_by_poem_and_author)

with open('author_poem_stanza_lines.json','w') as file:
    json.dump(lines_per_stanza_by_poem_and_author,file)

print('hello')