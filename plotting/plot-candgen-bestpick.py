import sys

# 100 docs
tesspath = "evaluation/ddocr_100_candgen/eval-results-tess.txt"
cunipath = "evaluation/ddocr_100_candgen/eval-results-cuni.txt"
optimalpath = "evaluation/ddocr_100_candgen/bestpick-optimal-fuzzy/opt.0.txt"
fuzzypath = "evaluation/ddocr_100_candgen/bestpick-optimal-fuzzy/"

# opt2path = "evaluation/bestpick-candgen-dict-100.txt"
# opt2path = "evaluation/bestpick-candgen-kb-100.txt"
# opt2path = "evaluation/bestpick-candgen-google-100-dist2.txt"
# opt2path = 'evaluation/bestpick-candgen-domain-100-dist2.txt'
opt2path = 'evaluation/ddocr_100_candgen/bestpick-evalgen.txt'

# fuzzypath = "evaluation/bestpick-optimal-fuzzy-trgm/"
# TODOO!!!
ddpath = 'eval-results.txt'
ddepath = 'eval-results-ensemble.txt'
# DISTRANGE = range(1, 6)
# DISTRANGE = range(1, 4)
DISTRANGE = range(1, 3)
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
opt2 = [l.strip().split('\t') for l in open(opt2path).readlines()]
dd = [l.strip().split('\t') for l in open(ddpath).readlines()]
dde = [l.strip().split('\t') for l in open(ddepath).readlines()]

tess = [ (t[0], float(t[-1].strip('()'))) for t in tess]
cuni = [ (t[0], float(t[-1].strip('()'))) for t in cuni]
dd =   [ (t[0], float(t[-1])) for t in dd]
dde =   [ (t[0], float(t[-1])) for t in dde]
opt = [ (t[0], float(t[-1].strip('()'))) for t in opt]
opt2 = [ (t[0], float(t[-1].strip('()'))) for t in opt2]

data = {'tess':tess, 'opt':opt, 'opt(gen)':opt2, 'dd(gen)':dd, 'dd(ens)':dde} # not added cuni
# data = {'opt':opt, 'dd':dd} # not added cuni / tess

for dist in DISTRANGE:
  # path = fuzzypath + 'opt.%d.txt' % dist
  path = fuzzypath + 'opt.' + str(dist) + '.txt'
  tmp = [l.strip().split('\t') for l in open(path).readlines()]
  tmp = [ (t[0], float(t[-1].strip('()'))) for t in tmp]
  data['opt('+str(dist)+')'] = tmp

docids = [_[0] for _ in sorted(data['tess'], key=lambda x:x[1])]

# plotorder = [i for i in reversed(['tess', 'dd', 'opt'] + ['opt(%d)' % i for i in DISTRANGE] )]
# not added tess
plotorder = [i for i in reversed(['tess', 'dd(ens)', 'opt', 'dd(gen)', 'opt(gen)'] + ['opt(' + str(i) + ')' for i in DISTRANGE] )]
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

# Compute avg on docs where T/C/all has outputs
# Discard documents that does not have T/opt/dd..
complete_data = [] # storing subs
for i in range(len(plotdata['dd(ens)'])):
  if all(plotdata[name][i] for name in ['tess', 'dd(ens)', 'opt', 'dd(gen)', 'opt(1)', 'opt(gen)']):
    complete_data.append(i)
print 'Plotting %d documents' % len(complete_data)

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
colors = [i for i in reversed(['r', 'yellow', 'orange', 'green', 'cyan', 
  '0.5', '0.4'
  # , '0.3'
  # , 'gray', 'black'
  # 'bo--', 'yo--', 'mo--', 'go--', 'ro--'
  # '0.7', '0.6', '0.5', '0.4', '0.3'
  ])]
dname_i = 0
# plt.yscale('linear')
for dname in plotorder:
  # ploty = plotdata[dname]
  ploty = [plotdata[dname][i] for i in complete_data]
  plotx = range(len(complete_data))
  my_xticks = [docids[i][len('JOURNAL_'):] for i in complete_data]
  # [ d[len('JOURNAL_'):] for d in docids]
  plt.xticks(plotx, my_xticks, rotation=45)  # Adding custom sticks
  plt.plot(plotx, ploty, colors[dname_i])
  dname_i += 1
  
maxscore = max( [ max(plotdata[name]) for name in plotdata ])
minscore = min( [ min(plotdata[name]) for name in plotdata ])
# pylab.ylim([0.85, maxscore])
pylab.ylim([0.88, 1])
# pylab.ylim([minscore, 1])
plt.legend(tuple([name for name in plotorder]), loc='lower right')
plt.savefig('pick-result.eps')
plt.clf()

print 'Plot saved to: ', 'pick-result.eps'

def MacroErrRed(new, base):
  counter = 0
  sumred = 0.0
  # for i in range(len(base)):
  for i in complete_data:
    if new[i] and base[i]:  # have data for both (Tess has Nones)
      counter += 1
      # print '%.4f %.4f: ErrRed =' % (new[i], base[i]), (new[i] - base[i]) / float(1 - base[i])
      sumred += (new[i] - base[i]) / float(1 - base[i])

  return sumred / counter

  # return sum([(new[i] - base[i]) / float(base[i]) for i in range(len(base)) if new[i] and base[i]]) / len(base)

def MacroAvg(data):
  counter = 0
  sumdata = 0.0
  # for i in range(len(data)):
  for i in complete_data:
    if data[i]:  # have data for both (Tess has Nones)
      counter += 1
      sumdata += data[i]
    else:  # None
      counter += 1
  return sumdata / counter

print 'tess avg    : %.5f' % MacroAvg(plotdata['tess'])
print 'dd(ens) avg : %.5f' % MacroAvg(plotdata['dd(ens)'])
print 'opt avg     : %.5f' % MacroAvg(plotdata['opt'])
print 'dd(gen) avg : %.5f' % MacroAvg(plotdata['dd(gen)'])
print 'opt(gen) avg: %.5f' % MacroAvg(plotdata['opt(gen)'])
print 'opt(1) avg  : %.5f' % MacroAvg(plotdata['opt(1)'])
print 'opt(2) avg  : %.5f' % MacroAvg(plotdata['opt(2)'])
print 'ErrRed tess -> dd(ens) : %.5f' % MacroErrRed(plotdata['dd(ens)'], plotdata['tess'])
print 'ErrRed tess -> dd(gen) : %.5f' % MacroErrRed(plotdata['dd(gen)'], plotdata['tess'])
print 'ErrRed opt -> opt(gen) : %.5f' % MacroErrRed(plotdata['opt(gen)'], plotdata['opt'])
print 'ErrRed tess -> opt(gen): %.5f' % MacroErrRed(plotdata['opt(gen)'], plotdata['tess'])

fout = open('result-errred.txt', 'w')
print >>fout, 'tess avg    :\t%.5f' % MacroAvg(plotdata['tess'])
print >>fout, 'dd(ens) avg :\t%.5f' % MacroAvg(plotdata['dd(ens)'])
print >>fout, 'opt avg     :\t%.5f' % MacroAvg(plotdata['opt'])
print >>fout, 'dd(gen) avg :\t%.5f' % MacroAvg(plotdata['dd(gen)'])
print >>fout, 'opt(gen) avg:\t%.5f' % MacroAvg(plotdata['opt(gen)'])
print >>fout, 'opt(1) avg  :\t%.5f' % MacroAvg(plotdata['opt(1)'])
print >>fout, 'opt(2) avg  :\t%.5f' % MacroAvg(plotdata['opt(2)'])
print >>fout, 'ErrRed tess -> dd(ens) :\t%.5f' % MacroErrRed(plotdata['dd(ens)'], plotdata['tess'])
print >>fout, 'ErrRed tess -> dd(gen) :\t%.5f' % MacroErrRed(plotdata['dd(gen)'], plotdata['tess'])
print >>fout, 'ErrRed opt -> opt(gen) :\t%.5f' % MacroErrRed(plotdata['opt(gen)'], plotdata['opt'])
print >>fout, 'ErrRed tess -> opt(gen):\t%.5f' % MacroErrRed(plotdata['opt(gen)'], plotdata['tess'])
fout.close()
