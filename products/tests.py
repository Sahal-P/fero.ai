from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product


class ProductAPIView(APITestCase):
    def setUp(self):
        self.product_data = {
            "name": "test product",
            "weight": "15",
        }
        self.product = Product.objects.create(**self.product_data)

    def test_list_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        new_product_data = {
            "name": "product 2",
            "weight": "20",
        }
        response = self.client.post("/api/products/", data=new_product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product_patch(self):
        updated_data_1 = {
            "id": self.product.id,
            "name": "Updated Name",
            "weight": "26",
        }
        updated_data_2 = {
            "id": self.product.id,
            "name": "Updated Name",
            "weight": "25",
        }
        response = self.client.patch(f"/api/products/", data=updated_data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response = self.client.patch(f"/api/products/", data=updated_data_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Name")

    def test_update_product_put(self):
        updated_data = {
            "id": self.product.id,
            "weight": "5",
        }
        response = self.client.put(f"/api/products/", data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.weight, 5.00)

    def test_delete_product(self):
        delete_data = {"id": self.product.id}
        response = self.client.delete("/api/products/", data=delete_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
