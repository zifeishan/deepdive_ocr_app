def CntSubstr(word, substr):
  return word.lower().count(substr.lower())

# Get 1st and 2nd level only 
# Return: [features] [feature values]
def CntAllSubstr(word):
  subs = []
  values = []

  chars = [chr(x) for x in range(ord('a'), ord('z') + 1)]
  chars += '-,.?![]"'
  chars += "'"
  for x in chars:
      sub = x
      subs.append(sub)
      values.append(CntSubstr(word, sub))

  for x in chars:
    for y in chars:
      sub = x + y
      subs.append(sub)
      values.append(CntSubstr(word, sub))

  return subs, values

# print CntAllSubstr('AAAaabb fififlflflfl')

# Get 1st and 2nd level only 
# Return: [features] [feature values]
def CntReducedSubStr(word, char1gram = None, char2gram = None):
  subs = []
  values = []

  if char1gram == None:
    chars = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    chars += '-,.?![]"'
    chars += "'"
  else:
    chars = char1gram

  for x in chars:
    sub = x
    subs.append(sub)
    values.append(CntSubstr(word, sub))

  if char2gram != None: 
    reduced = char2gram
  else: 
    reduced = ['fi','fl','rn', 'rm','nn']

  for sub in reduced:
    subs.append(sub)
    values.append(CntSubstr(word, sub))

  return subs, values

# print CntAllSubstr('AAAaabb fififlflflfl')