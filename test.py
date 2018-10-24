import unittest
from script1 import diffMonth
from script1 import nextMonth
from script1 import previousMonth
from datetime import datetime

class Test(unittest.TestCase):

  def test_diffMonth(self):
    self.assertEqual( diffMonth(datetime.strptime("07/2018", '%m/%Y'), datetime.strptime("01/2018", '%m/%Y')), 7 )
    self.assertEqual( diffMonth(datetime.strptime("04/2018", '%m/%Y'), datetime.strptime("05/2018", '%m/%Y')), 2 )
    self.assertEqual( diffMonth(datetime.strptime("05/2017", '%m/%Y'), datetime.strptime("04/2018", '%m/%Y')), 12 )
    self.assertEqual( diffMonth(datetime.strptime("04/2018", '%m/%Y'), datetime.strptime("05/2017", '%m/%Y')), 12 )
    self.assertEqual( diffMonth(datetime.strptime("04/2017", '%m/%Y'), datetime.strptime("04/2018", '%m/%Y')), 13 )

  def test_nextMonth(self):
      self.assertEqual( nextMonth(datetime.strptime("07/2018", '%m/%Y')), datetime.strptime("08/2018", '%m/%Y') )
      self.assertEqual( nextMonth(datetime.strptime("12/2018", '%m/%Y')), datetime.strptime("01/2019", '%m/%Y') )

  def test_previousMonth(self):
      self.assertEqual( previousMonth(datetime.strptime("07/2018", '%m/%Y')), datetime.strptime("06/2018", '%m/%Y') )
      self.assertEqual( previousMonth(datetime.strptime("12/2018", '%m/%Y')), datetime.strptime("11/2018", '%m/%Y') )
      self.assertEqual( previousMonth(datetime.strptime("01/2018", '%m/%Y')), datetime.strptime("12/2017", '%m/%Y') )

if __name__ == '__main__':
    unittest.main()