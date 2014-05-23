import fileinput
import re
 
for line in fileinput.input(inplace=1):
    line = re.sub(r'http\:\/\/virtuallyhyper.com\/wp-content\/uploads/(.*)', r'https://github.com/elatov/uploads/raw/master/\1', line.rstrip())
    print(line)
