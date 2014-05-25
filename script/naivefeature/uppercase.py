
def UpperPunish(word):
  if len(word[1:]) == 0:
    return 0
  uppercase = 0
  lowercase = 0
  for char in word[1:]:
    if char.islower():
      lowercase += 1
    if char.isupper():
      uppercase += 1

  # y = -4x(x-1)
  if uppercase + lowercase == 0: 
    return 0
  x = uppercase / float(uppercase + lowercase)
  y = 4 * x * (1 - x)
  return y

# low to high changes
def ChangeTime(word):
  if len(word) == 0:
    return 0
  casechange = 0
  last = word[0]
  for char in word:
    if last.islower() and char.isupper():
      casechange += 1
    last = char
  # print casechange
  return casechange

