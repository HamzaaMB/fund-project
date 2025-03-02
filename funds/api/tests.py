from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from funds.models import Fund
from django.urls import reverse
import uuid

class FundAPITests(TestCase):
    
    def setUp(self):
        """Set up test data for the tests."""
        self.client = APIClient()
        self.fund_1 = Fund.objects.create(
            name="Fund 1", strategy="Equity", aum=1000000, inception_date="2010-01-01"
        )
        self.fund_2 = Fund.objects.create(
            name="Fund 2", strategy="Bond", aum=500000, inception_date="2015-05-01"
        )
        self.fund_3 = Fund.objects.create(
            name="Fund 3", strategy="Equity", aum=2000000, inception_date="2012-06-10"
        )

        self.url_fund_list = reverse('fund-list-api')  
        self.url_fund_detail = reverse('fund-detail-api', kwargs={'pk': self.fund_1.id})

    def test_fund_list_api_success(self):
        """Test that the fund list API returns all funds successfully."""
        response = self.client.get(self.url_fund_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], self.fund_1.name)  

    def test_fund_list_api_filter_by_strategy(self):
        """Test filtering the fund list by strategy."""
        response = self.client.get(self.url_fund_list, {'strategy': 'Equity'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  
        self.assertEqual(response.data[0]['strategy'], 'Equity')

    def test_fund_detail_api_success(self):
        """Test that the fund detail API returns the correct fund details."""
        response = self.client.get(self.url_fund_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.fund_1.name)
        self.assertEqual(response.data['strategy'], self.fund_1.strategy)
        self.assertEqual(str(response.data['aum']), str(self.fund_1.aum)) 


    def test_fund_detail_api_not_found(self):
        """Test that the API returns a 404 when the fund does not exist."""
        response = self.client.get(reverse('fund-detail-api', kwargs={'pk': uuid.uuid4()}))  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Fund not found.')

    def test_fund_detail_api_unexpected_error(self):
        """Test that unexpected errors are handled gracefully."""
        response = self.client.get(self.url_fund_detail)
        self.assertNotEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
