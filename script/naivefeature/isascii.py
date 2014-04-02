def IsASCII(s):
  return all(ord(c) < 128 for c in s)