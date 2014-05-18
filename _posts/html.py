import fileinput
import re
 
for line in fileinput.input(inplace=1):
    line = re.sub(r'<a href="(.*)">(.*)</a>', r'[\2](\1)', line.rstrip())
    print(line)
