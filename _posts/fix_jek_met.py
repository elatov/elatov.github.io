#!/usr/bin/env python
import yaml, sys, re, os

# define patterns to match the categories and tags in the yaml metadata
cat_pat = re.compile(r'^categories:$(.*?)^tags:$', re.DOTALL+re.M)
tag_pat = re.compile(r'^tags:$(.*?)^---$', re.DOTALL+re.M)

# set the first arguement as the file we are going to modify
file = sys.argv[1]

# open the file as read only
fh = open(file,'r')

# get the tags and categories from the yaml metadata
docs = yaml.load_all(fh)
for doc in docs:
#    print doc
    if doc['author']:
        t = doc['tags']
        c = doc['categories']
    break

# convert each string in list to lowercase
t_to_lower = [el.lower() for el in t]
c_to_lower = [el.lower() for el in c]

# Replace each space with understore in each string in the list
t_rm_space = [el.replace(' ','_') for el in t_to_lower]
c_rm_space = [el.replace(' ','_') for el in c_to_lower]

# since the file was already read once, we need to reset the pointer
fh.seek(0)

# read the file the second time
data = fh.read()
changed_cat = False
changed_tag = False

# check if we matched the pattern, if match then do the changes
if cat_pat.findall(data):
    replace_cat_data = cat_pat.sub('categories: '+ str(c_rm_space) +'\ntags:', data,count=1)
    changed_cat = True

# check if categories were found, if not search on the original data
if changed_cat:
    # check if tag pattern is found
    if tag_pat.findall(replace_cat_data):
        replace_tag_data = tag_pat.sub('tags: '+ str(t_rm_space) +'\n---\n', replace_cat_data,count=1)
        changed_tag = True
elif tag_pat.findall(data):
        replace_tag_data = tag_pat.sub('tags: '+ str(t_rm_space) +'\n---\n', replace_cat_data,count=1)
        change_tag = True

# close the original read-only file handle
fh.close()

# write out the same file with new data
if changed_tag or changed_cat:
    nf = open(file, 'w')
    nf.write(replace_tag_data)
    nf.close()
    print "File: " + file + " converted"
else:
    print "File: " + file + " was NOT converted"
