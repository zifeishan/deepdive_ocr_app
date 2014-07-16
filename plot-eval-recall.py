import sys

# 100 docs
tesspath = "evaluation/bestpick-tess-eval-100.txt"
cunipath = 'evaluation/bestpick-cuni-eval-100.txt'
# optimalpath = "evaluation/bestpick-optimal-eval-100.txt"
optimalpath = "evaluation/bestpick-optimal-fuzzy/opt.0.txt"
fuzzypath = "evaluation/bestpick-optimal-fuzzy/"
# fuzzypath = "evaluation/bestpick-optimal-fuzzy-trgm/"
ddpath = 'eval-results.txt'
# DISTRANGE = range(1, 6)
DISTRANGE = range(1, 4)
# DISTRANGE = [0.1, 0.3, 0.5, 0.7, 0.9]

# # 30 docs
# tesspath = "evaluation/bestpick-tess-eval-30-sample.txt"
# cunipath = 'evaluation/bestpick-cuni-eval-30-sample.txt'
# optimalpath = "evaluation/bestpick-optimal-fuzzy/opt.0.txt"
# fuzzypath = "evaluation/bestpick-optimal-fuzzy/"
# ddpath = 'eval-results.txt'


# if len(sys.argv) == 3:
#   path = sys.argv[1]
#   num = int(sys.argv[2])
# else:
#   print 'Usage:',sys.argv[0],'<ocrbase>'
#   print 'e.g. ',sys.argv[0],'evaluation/100doc-ocrexp-backup/'
    


if len(sys.argv) == 5:
  tesspath, cunipath, optimalpath, ddpath = sys.argv[1:]
else:
  print 'Usage:',sys.argv[0],'tesspath cunipath optimalpath ddpath. Used default.'
  

tess = [l.strip().split('\t') for l in open(tesspath).readlines()]
cuni = [l.strip().split('\t') for l in open(cunipath).readlines()]
opt = [l.strip().split('\t') for l in open(optimalpath).readlines()]
dd = [l.strip().split('\t') for l in open(ddpath).readlines()]

tess = [ (t[0], float(t[-1].strip('()'))) for t in tess]
cuni = [ (t[0], float(t[-1].strip('()'))) for t in cuni]
dd =   [ (t[0], float(t[-1])) for t in dd]
opt = [ (t[0], float(t[-1].strip('()'))) for t in opt]

data = {'tess':tess, 'opt':opt, 'dd':dd} # not added cuni
# data = {'opt':opt, 'dd':dd} # not added cuni / tess

for dist in DISTRANGE:
  # path = fuzzypath + 'opt.%d.txt' % dist
  path = fuzzypath + 'opt.' + str(dist) + '.txt'
  tmp = [l.strip().split('\t') for l in open(path).readlines()]
  tmp = [ (t[0], float(t[-1].strip('()'))) for t in tmp]
  data['opt('+str(dist)+')'] = tmp

docids = [_[0] for _ in sorted(data['opt'], key=lambda x:x[1])]

# plotorder = [i for i in reversed(['tess', 'dd', 'opt'] + ['opt(%d)' % i for i in DISTRANGE] )]
# not added tess
plotorder = [i for i in reversed(['tess', 'dd', 'opt'] + ['opt(' + str(i) + ')' for i in DISTRANGE] )]
plotdata = {}
for key in data:
  oldlist = data[key]
  olddict = {}
  for pair in oldlist:
    olddict[pair[0]] = pair[1]

  newlist = []
  for docid in docids:
    if docid not in olddict:
      newlist.append(None)
    else:
      newlist.append(olddict[docid])

  plotdata[key] = newlist


import numpy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab

# Called by function below
def PlotPrep(xlabel, ylabel, loglog=False):
  grid_width = 50
  pylab.grid(True)
  # possible formatting:
  # plt.plot(line_x, line_y, 'r-')
  # plt.plot(pdf_x, pdf_y, 'y.')
  # plt.plot(epdf_x, epdf_y, 'b.')
  pylab.xlabel(xlabel)
  pylab.ylabel(ylabel)
  if loglog: 
    plt.loglog()
  # if legends != None:
  #   plt.legend(legends)

PlotPrep(xlabel='Document ID', ylabel='Word Recall')
colors = [i for i in reversed(['r', 'g', 'orange', 
  'blue', 'yellow', 'purple'
  # , 'gray', 'black'
  # 'bo--', 'yo--', 'mo--', 'go--', 'ro--'
  # '0.7', '0.6', '0.5', '0.4', '0.3'
  ])]
i = 0
# plt.yscale('linear')
for dname in plotorder:
  ploty = plotdata[dname]
  plotx = range(len(docids))
  my_xticks = [ d[len('JOURNAL_'):] for d in  docids]
  plt.xticks(plotx, my_xticks, rotation=45)  # Adding custom sticks
  plt.plot(plotx, ploty, colors[i])
  i += 1
  
maxscore = max( [ max(plotdata[name]) for name in plotdata ])
minscore = min( [ min(plotdata[name]) for name in plotdata ])
# pylab.ylim([0.85, maxscore])
pylab.ylim([0.85, 1])
# pylab.ylim([minscore, 1])
plt.legend(tuple([name for name in plotorder]), loc='lower right')
plt.savefig('pick-result.eps')
plt.clf()

print 'Plot saved to: ', 'pick-result.eps'

def MacroErrRed(new, base):
  counter = 0
  sumred = 0.0
  for i in range(len(base)):
    if new[i] and base[i]:  # have data for both (Tess has Nones)
      counter += 1
      # print '%.4f %.4f: ErrRed =' % (new[i], base[i]), (new[i] - base[i]) / float(1 - base[i])
      sumred += (new[i] - base[i]) / float(1 - base[i])

  return sumred / counter

  # return sum([(new[i] - base[i]) / float(base[i]) for i in range(len(base)) if new[i] and base[i]]) / len(base)

tessred = MacroErrRed(plotdata['dd'], plotdata['tess'])
optred = MacroErrRed(plotdata['dd'], plotdata['opt'])
print 'Avg Error reduction from Tesseract:', tessred
print 'Avg Error reduction from Optimal:', optred
fout = open('result-errred.txt', 'w')
print >>fout, tessred
print >>fout, optred
fout.close()
