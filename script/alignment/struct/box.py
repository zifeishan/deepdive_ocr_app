_BOX_THRESHOLD = 5

class Box:
  
  def __init__(self):
    self._threshold = _BOX_THRESHOLD
    self._page = 0
    self._box = [0,0,0,0]

  def GetPULRD(self):
    return (self.GetPage(), self.GetUp(), self.GetLeft(), 
      self.GetRight(), self.GetDown())

  # Compare box based on order "up, left, right, down, by commen sense"
  def __lt__(self, other):
     return self.GetPULRD() < other.GetPULRD()

  def GetLeft(self):
    return self._box[0]
  def GetUp(self):
    return self._box[1]
  def GetRight(self):
    return self._box[2]
  def GetDown(self):
    return self._box[3]
  def GetBoxes(self):
    return self._box
  def GetPage(self):
    return self._page
  def GetThreshold(self):
    return self._threshold

  def GetPrinted(self):
    return 'P' + str(self._page)+',' + ' '.join([str(b) for b in self._box])

  # order of "boxes": Left Top Right Bottom
  def SetBoxes(self, boxes):
    for i in range(0,4):
      self._box[i] = int(boxes[i])

  def SetPage(self, page):
    self._page = int(page)

  def SetThreshold(self, threshold):
    self._threshold = threshold

  def IsEmpty(self):
    return self.GetLeft() == self.GetRight() or self.GetUp() == self.GetDown()

  # Test if this box contains another box within a threshold
  def Contain(self, box2):
    return self.GetLeft() <= box2.GetLeft() + self._threshold \
      and self.GetUp() <= box2.GetUp() + self._threshold \
      and self.GetDown() >= box2.GetDown() - self._threshold \
      and self.GetRight() >= box2.GetRight() - self._threshold \
      and self.GetPage() == box2.GetPage()
      # Assume a box only has one page..

  # Test if this box appear above another box, or in an earlier page
  def Above(self, box2):
    return (self.GetDown() < box2.GetUp() + self._threshold and self.GetPage() == box2.GetPage())\
      or self.GetPage() < box2.GetPage()

  # Test if this box appear left to another box, or in an earlier page
  def LeftTo(self, box2):
    return (self.GetRight() < box2.GetLeft() + self._threshold and self.GetPage() == box2.GetPage())\
      or self.GetPage() < box2.GetPage()

  # Test if two boxes are equal (contains each other)
  def Equal(self, box2):
    return self.Contain(box2) and box2.Contain(self)

  # Test if this box appear before another box. Priority: page > Above > Left. 
  # Note that A not before B and B not before A might be true, when they overlap OR WHEN 1 leftdown 2 rightup...
  def Before(self, box2):
    # if self.GetPage() < box2.GetPage():
    #   return True
    # if self.GetPage() > box2.GetPage():
    #   return False
    # if self.GetDown() < box2.GetUp() + self._threshold and\
    #    self.GetRight() < box2.GetLeft() + self._threshold:
    #    return True
    # if box2.GetDown() < self.GetUp() + self._threshold and\
    #    box2.GetRight() < self.GetLeft() + self._threshold:
    #    return False
    # # Else: Not sure whether left or above is top-priority

    if self.GetPage() < box2.GetPage():
      return True
    if self.GetPage() > box2.GetPage():
      return False
    # Same page: TODO now prioritize ABOVE than LEFT
    if self.GetDown() < box2.GetUp() + self._threshold:
      return True
    elif self.GetUp() <= box2.GetUp() + self._threshold \
      and self.GetDown() >= box2.GetDown() - self._threshold:
      if self.GetRight() < box2.GetLeft() + self._threshold:
        return True
    return False


  # Detect if two boxes overlap
  def IsOverlap(self, box2):
    if self.GetPage() != box2.GetPage():
      return False
    return not (box2.GetLeft() > self.GetRight()
        or box2.GetRight() < self.GetLeft()
        or box2.GetUp() > self.GetDown()
        or box2.GetDown() < self.GetUp())
     # return !(r2.left > r1.right
     #        || r2.right < r1.left
     #        || r2.top > r1.bottom
     #        || r2.bottom < r1.top);
      
  # Quickly Detect if two boxes overlap (Given they are in same page!)
  def IsOverlapSamePage(self, box2):
    return not (box2.GetLeft() > self.GetRight()
        or box2.GetRight() < self.GetLeft()
        or box2.GetUp() > self.GetDown()
        or box2.GetDown() < self.GetUp())
     # return !(r2.left > r1.right
     #        || r2.right < r1.left
     #        || r2.top > r1.bottom
     #        || r2.bottom < r1.top);


# Combine two boxes into a box and return it
# TODO: Cannot combine boxes in different pages
def BoxCombine(box1, box2):
  if box1.GetPage() != box2.GetPage:
    return None
  box = Box()
  box.SetLeft(min(box1.GetLeft(), box2.GetLeft()))
  box.SetUp(min(box1.GetUp(), box2.GetUp()))
  box.SetRight(max(box1.GetRight(), box2.GetRight()))
  box.SetDown(max(box1.GetDown(), box2.GetDown()))
  box.SetPage(box1.GetPage())
  box.SetThreshold(box1.GetThreshold())
  return box
