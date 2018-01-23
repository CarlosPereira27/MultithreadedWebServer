path_file = "dist/resources_request.txt"

file = open(path_file, 'r')

for line in file:
    if line[-1] == '\n':
        line = line[:-1]
    line = "/" + line
    print ("    - get:")
    print ("        url: \"%s\"" % (line))