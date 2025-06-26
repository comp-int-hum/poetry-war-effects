import json

with open('author_poem_stanza_lines.json','r') as ifd:
    author_poem_stanza_lines = json.load(ifd)

for author in author_poem_stanza_lines.keys():
    if 'Owen, Wilfred' in author:
        print(author_poem_stanza_lines[author])

#with open('all_poems.json','r') as ifd2:
    #all_poems = json.load(ifd2)
#print(all_poems[5])
