from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from customers.models import Customer


class CustomerViewSetTest(APITestCase):
    def setUp(self):
        self.customer_data = {
            "name": "Jack Jones",
            "contact_number": "123456789",
            "email": "jackjones@example.com",
        }
        self.customer = Customer.objects.create(**self.customer_data)

    def test_list_customers(self):
        response = self.client.get("/api/customers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_customer(self):
        new_customer_data = {
            "name": "Jane Doe",
            "contact_number": "987654321",
            "email": "jane.doe@example.com",
        }
        response = self.client.post("/api/customers/", data=new_customer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)

    def test_update_customer_patch(self):
        updated_data_1 = {
            "id": self.customer.id,
            "name": "Updated Name",
        }
        updated_data_2 = {
            "id": self.customer.id,
            "name": "Updated Name",
            "contact_number": "987654321",
            "email": "update1234@example.com",
        }
        response = self.client.patch(f"/api/customers/", data=updated_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.patch(f"/api/customers/", data=updated_data_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, "Updated Name")

    def test_update_customer_put(self):
        updated_data = {
            "id": self.customer.id,
            "name": "Updated Name 2",
            "contact_number": "987600321",
        }
        response = self.client.put(f"/api/customers/", data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, "Updated Name 2")
        self.assertEqual(self.customer.contact_number, "987600321")

    def test_delete_customer(self):
        delete_data = {"id": self.customer.id}
        response = self.client.delete("/api/customers/", data=delete_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)
