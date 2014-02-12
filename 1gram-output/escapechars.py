import os,sys
if __name__ == "__main__": 
  if len(sys.argv) == 2:
    path = sys.argv[1]
  else:
    print 'Usage:',sys.argv[0],'<path>'
    sys.exit(1)

  fin = open(path)
  while True:
    line = fin.readline().strip()
    if line == '': break
    if '\\' in line: continue
    print line.replace('\\', '')
