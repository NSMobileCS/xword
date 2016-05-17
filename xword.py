import os
from random import (choice as Ch, randrange as rr)

os.chdir('/sdcard')
#the above line is only needed on my android setup to 
#switch to the directory w/ the words list
#make sure satlist1.txt is in the same directory as this
#file, & run it from here & you should be fine

d = dict()
with open('satlist1.txt', 'r') as f:
  l = []
  for line in f:
    l.append(line.strip('\n'))
    if len(l) == 2:
      d[l[0]] = l[1]
      l = []



class M:
  def __init__(self, d, m=16, n=16):
    self._m = [['*' for _ in range(n)] for _ in range(m)]
    self.d = d
    self.words = None
    
  def __str__(self):
    l = ['.'.join(li) for li in self._m]
    return '_\n'.join(l)
  
  def rmword(self, word, idxm, idxn, across):
    slice = ['*' for _ in range(len(word))]
    if across:
      self._m[idxm][idxn:idxn+len(word)+1] = slice
    else:
      for n, ch in enumerate(slice):
        self._m[idxm+n][idxn] = '*'
        
    for word, idxm, idxn, across in self.words:
      errorsum = 0
      if across:
        errorsum += self.addwordacross(word, idxm, idxn)
      else:  
        errorsum += self.addworddown(word, idxm, idxn)
    assert errorsum == 0
    
    
  def addwordacross(self, word, idxm, idxn):
    try:
      slice = self._m[idxm][idxn:idxn+len(word)+1]
      for n, ch in enumerate(word):
        if slice[n] == ch:
          continue  
        elif slice[n] == '*':
          slice[n] = ch
        else:
          return False
    except IndexError:
      return False  
    self._m[idxm][idxn:idxn+len(word)+1] = slice
    return True
      
  def addworddown(self, word, idxm, idxn):
    try:
      slice = list([row[idxn] for row in self._m[idxm:]])   
      for n, ch in enumerate(word):
        if slice[n] == ch:
          continue  
        elif slice[n] == '*':
          slice[n] = ch
        else:
          return False
    except IndexError:
      return False
    for n, ch in enumerate(slice):
      self._m[idxm+n][idxn] = ch
    return True
    
  def mkxword(self):
    l = [k for k in self.d]
    counter = 0
    if self.words is None:
      self.words = []
    across = 0
    while True:
      counter += 1
      w = Ch(l)
      m, n = rr(16), rr(16)
      if len(self.words) == 24:
        print('correct exit point, hardwired n of 24', len(self.words))
        return
      
      elif across:
        if self.addwordacross(w, m, n) is True:
          l.pop(l.index(w))
          self.words.append((w, m, n, across)) 
          #tuple format (0 word, 1 m, 2 n, 3 across<bool> )
          across ^= 1
          
      elif across == 0:    
        if self.addworddown(w, m, n) is True:
          l.pop(l.index(w))
          self.words.append((w, m, n, across))
          across ^= 1
         
      elif counter > 55:
        print('self.words', self.words)
        print('len(self.words)', len(self.words), 'type', type(self.words))
        print('counter', counter)
        ridx = rr(len(self.words))
        word, idxm, idxn, across = self.words.pop(ridx)
        self.rmword(word, idxm, idxn, across)
        print('counter reset. removed word', word)
        counter = 0
        continue
    
def test1():
  m = M(d)
  a=m.addworddown('phallic', 3, 1)
  b=m.addwordacross('gallant', 5, 0)
  assert a is True
  print('passed assert a is True')
  assert b is True
  print('passed assert b is True')
  print(m)
  print('test1 success' + '\n'+'- _'*9+'\n')

def test2():
  m = M(d)
  words = m.mkxword()
  print(m)
  print(m.words)
  print('test2 success' + '\n'+'- _'*9+'\n')



if __name__ == '__main__':
  test1()
  test2()