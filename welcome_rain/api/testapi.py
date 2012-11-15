from django.test.client import Client
from django.test import TestCase

"""
 c = Client()
>>> response = c.post('/login/', {'username': 'john', 'password': 'smith'})
>>> response.status_code

>>> response = c.get('/customer/details/')
>>> response.content
"""

class APITestCase(TestCase):
    
    def test_GetClusterList(self):
        print ">>> test_GetClusterList"
        response = self.client.post('/api/getClusterList')
        print response.content


