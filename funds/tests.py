from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from funds.models import Fund
from django.http import JsonResponse
from funds.services import process_fund_csv
import io
import uuid

class FundViewsTest(TestCase):
    def setUp(self):
        """Set up test data and users."""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_upload_funds_valid_csv(self):
        """Test uploading a valid CSV file."""
        valid_csv = b"Name,Strategy,AUM (USD),Inception Date\nFund A,Strategy 1,1000000,2020-01-01\nFund B,Strategy 2,2000000,2020-02-01"
        file = SimpleUploadedFile("test_funds.csv", valid_csv, content_type="text/csv")
        response = self.client.post(reverse('upload-funds'), {'csv_file': file})
        self.assertRedirects(response, reverse('fund-list'))
        self.assertEqual(Fund.objects.count(), 2) 
        
        fund_a = Fund.objects.get(name="Fund A")
        fund_b = Fund.objects.get(name="Fund B")
        self.assertEqual(fund_a.strategy, "Strategy 1")
        self.assertEqual(fund_a.aum, 1000000)
        self.assertEqual(fund_b.strategy, "Strategy 2")
        self.assertEqual(fund_b.aum, 2000000)


    def test_fund_list_view(self):
        """Test the fund list view."""
        Fund.objects.create(name="Fund A", strategy="Strategy 1", aum=1000000)
        Fund.objects.create(name="Fund B", strategy="Strategy 2", aum=2000000)
        response = self.client.get(reverse('fund-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fund A")
        self.assertContains(response, "Fund B")
        self.assertEqual(len(response.context['funds']), 2) 


    def test_fund_list_with_strategy_filter(self):
        """Test fund list view with a strategy filter."""
        Fund.objects.create(name="Fund A", strategy="Strategy 1", aum=1000000)
        Fund.objects.create(name="Fund B", strategy="Strategy 2", aum=2000000)
        response = self.client.get(reverse('fund-list') + "?strategy=Strategy 1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fund A")
        self.assertNotContains(response, "Fund B")
        self.assertEqual(len(response.context['funds']), 1) 


    def test_delete_fund_view(self):
        """Test deleting a fund."""
        fund = Fund.objects.create(name="Fund A", strategy="Strategy 1", aum=1000000)
        response = self.client.get(reverse('delete-fund', args=[str(fund.id)])) 
        self.assertRedirects(response, reverse('fund-list'))
        self.assertEqual(Fund.objects.count(), 0)



    def test_delete_fund_not_found(self):
        """Test trying to delete a fund that does not exist."""
        response = self.client.get(reverse('delete-fund', args=[uuid.uuid4()])) 
        self.assertEqual(response.status_code, 400)


class FundModelTest(TestCase):
    def test_total_aum(self):
        """Test the total_aum method."""
        fund1 = Fund.objects.create(name="Fund A", strategy="Strategy 1", aum=1000000)
        fund2 = Fund.objects.create(name="Fund B", strategy="Strategy 1", aum=2000000)
        fund3 = Fund.objects.create(name="Fund C", strategy="Strategy 2", aum=None)

        total_aum_strategy_1 = Fund.total_aum("Strategy 1")
        total_aum_all = Fund.total_aum()

        self.assertEqual(total_aum_strategy_1, 3000000) 
        self.assertEqual(total_aum_all, 3000000) 



class FundServiceTest(TestCase):
    def test_process_fund_csv_valid(self):
        """Test that the service correctly processes a valid CSV file."""
        csv_file = io.StringIO("Name,Strategy,AUM (USD),Inception Date\nFund A,Strategy 1,1000000,2020-01-01\nFund B,Strategy 2,2000000,2020-02-01")
        response = process_fund_csv(csv_file, "test_fund_file.csv")
        self.assertIsNone(response)  
        self.assertEqual(Fund.objects.count(), 2) 

        fund_a = Fund.objects.get(name="Fund A")
        self.assertEqual(fund_a.strategy, "Strategy 1")
        self.assertEqual(fund_a.aum, 1000000)

    def test_process_fund_csv_invalid(self):
        """Test that the service returns an error for invalid CSV format."""
        invalid_csv_file = io.StringIO("Name,Strategy,AUM (USD)\nFund A,Strategy 1,1000000\nFund B,Strategy 2,2000000")
        response = process_fund_csv(invalid_csv_file, "invalid_test_fund_file.csv")
        self.assertIsInstance(response, JsonResponse)  
        self.assertIn("Missing columns:", str(response.content))
