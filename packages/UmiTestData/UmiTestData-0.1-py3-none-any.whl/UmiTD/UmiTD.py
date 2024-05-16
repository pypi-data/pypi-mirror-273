import random
import time
import json
import string
from datetime import datetime, timedelta

class UmiTD:
    def __init__(self):
        pass

    def RanStr(self, lenth, punct=False, digit=False, upper=False, lower=True):
        letters = ''
        if punct:
            letters += string.punctuation
        if digit:
            letters += string.digits
        if upper:
            letters += string.ascii_uppercase
        if lower:
            letters += string.ascii_lowercase

        return ''.join(random.choice(letters) for i in range(lenth))
    
    def RanInt(self, lenth):
        if lenth < 1:
            raise ValueError('Length must be a positive integer')
        min = 10 ** (lenth - 1)
        max = 10 ** lenth - 1
        return random.randint(min, max)
    
    def RanFloat(self, lenth, decimal=2):
        if lenth < 1:
            raise ValueError('Length must be a positive integer')
        if decimal < 1:
            raise ValueError('Decimal must be a positive integer')
        min = 10 ** (lenth - 1)
        max = 10 ** lenth - 1
        return round(random.uniform(min, max), decimal)
    
    def RanBool(self):
        return random.choice([True, False])
    
    def RanList(self, lenth=5, num=False, str=True, bool=False):
        if lenth < 1:
            raise ValueError('Length must be a positive integer')
        
        if not any([num, str, bool]):
            raise ValueError('At least one of the three parameters must be True')
        
        list = []
        for _ in range(lenth):
            type_choice = random.choice([(num, self.RanInt), (str, lambda: self.RanStr(lenth)), (bool, self.RanBool)])
            while not type_choice[0]:
                type_choice = random.choice([(num, self.RanInt), (str, lambda: self.RanStr(lenth)), (bool, self.RanBool)])
            list.append(type_choice[1]())
        
        return list
    
    def RanTuple(self, lenth=5, num=False, str=True, bool=False):
        if lenth < 1:
            raise ValueError('Length must be a positive integer')
        
        if not any([num, str, bool]):
            raise ValueError('At least one of the three parameters must be True')
        
        list = []
        for _ in range(lenth):
            type_choice = random.choice([(num, self.RanInt), (str, lambda: self.RanStr(lenth)), (bool, self.RanBool)])
            while not type_choice[0]:
                type_choice = random.choice([(num, self.RanInt), (str, lambda: self.RanStr(lenth)), (bool, self.RanBool)])
            list.append(type_choice[1]())
        
        return tuple(list)
    
    def RanDict(self, lenth=5, num=False, str=True, bool=False):
        if lenth < 1:
            raise ValueError('Length must be a positive integer')
        
        if not any([num, str, bool]):
            raise ValueError('At least one of the three parameters must be True')
        
        dict = {}
        for _ in range(lenth):
            key = self.RanStr(5)
            type_choice = random.choice([(num, self.RanInt), (str, lambda: self.RanStr(lenth)), (bool, self.RanBool)])
            while not type_choice[0]:
                type_choice = random.choice([(num, self.RanInt), (str, lambda: self.RanStr(lenth)), (bool, self.RanBool)])
            dict[key] = type_choice[1]()
        
        return dict
    
    def RanJson(self, lenth=5, num=False, str=True, bool=False):
        if lenth < 1:
            raise ValueError('Length must be a positive integer')
        
        if not any([num, str, bool]):
            raise ValueError('At least one of the three parameters must be True')
        
        dict = {}
        for _ in range(lenth):
            key = self.RanStr(5)
            type_choice = random.choice([(num, self.RanInt), (str, lambda: self.RanStr(lenth)), (bool, self.RanBool)])
            while not type_choice[0]:
                type_choice = random.choice([(num, self.RanInt), (str, lambda: self.RanStr(lenth)), (bool, self.RanBool)])
            dict[key] = type_choice[1]()
        
        return json.dumps(dict)
    
    def RanImgUrl(self, amount=1):
        if amount < 1:
            raise ValueError('Amount must be a positive integer')
        
        if amount == 1:
            return f"https://picsum.photos/{random.randint(100, 1000)}"
        else:
            return [f"https://picsum.photos/{random.randint(100, 1000)}" for _ in range(amount)]
    
    def RanDate(self, start='2000-01-01', end=datetime.now().strftime('%Y-%m-%d')):
        start = time.mktime(time.strptime(start, '%Y-%m-%d'))
        end = time.mktime(time.strptime(end, '%Y-%m-%d'))
        return time.strftime('%Y-%m-%d', time.localtime(random.randint(start, end)))

    def RanTime(self, start='00:00:00', end='23:59:59'):
        start = datetime.strptime(start, '%H:%M:%S')
        end = datetime.strptime(end, '%H:%M:%S')

        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)

        return (start + timedelta(seconds=random_second)).strftime('%H:%M:%S')

    def RanDay(self, start=0, end=365):
        return random.randint(start, end)
    
    def RanMonth(self, start=1, end=12):
        return random.randint(start, end)
    
    def RanYear(self, start=2000, end=datetime.now().year):
        return random.randint(start, end)
    
    def RanWeek(self, start=0, end=52):
        return random.randint(start, end)