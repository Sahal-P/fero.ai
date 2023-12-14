from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from products.models import Product
from customers.models import Customer
from orders.models import Order, OrderItem

class OrderAPITestCase(APITestCase):
    def setUp(self):
        
        self.customer_data_1 = {
            "name": "person_1",
            "contact_number": "123456789",
            "email": "person_1@example.com",
        }
        self.customer_data_2 = {
            "name": "person_2",
            "contact_number": "123456788",
            "email": "person_2@example.com",
        }
        self.customers = Customer.objects.bulk_create(
            [Customer(**self.customer_data_1), Customer(**self.customer_data_2)]
        )
        self.product_data_1 = {
            "name": "test product_1",
            "weight": "10",
        }
        self.product_data_2 = {
            "name": "test product_2",
            "weight": "20",
        }
        self.product_data_3 = {
            "name": "test product_3",
            "weight": "15",
        }

        self.products = Product.objects.bulk_create(
            [
                Product(**self.product_data_1),
                Product(**self.product_data_2),
                Product(**self.product_data_3),
            ]
        )
        self.order = Order.objects.create(customer=self.customers[1], address="Test Address")
        OrderItem.objects.create(order=self.order, product=self.products[2], quantity=2)
        
        

    def test_post_order(self):
        url = reverse("orders")
        data = {
            "customer_id": str(
                self.customers[0].id
            ), 
            "address": "Test Address",
            "order_items": [
                {"product_id": str(self.products[0].id), "quantity": 2},
                {"product_id": str(self.products[1].id), "quantity": 1},
                {"product_id": str(self.products[2].id), "quantity": 1},
            ],
        }
        data_weight_more_than_cumulative = {
            "customer_id": str(
                self.customers[1].id
            ),  
            "address": "Test Address",
            "order_items": [
                {"product_id": str(self.products[0].id), "quantity": 4},
                {"product_id": str(self.products[1].id), "quantity": 6},
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_bad = self.client.post(url, data_weight_more_than_cumulative, format="json")
        self.assertEqual(response_bad.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_orders(self):
        url = reverse("orders")  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_by_customer(self):
        customer_name = "person_1"
        url = reverse("orders") + f"?customer={customer_name}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_by_products(self):
        product_names = (
            "test product_1,test product_2,test product_3" 
        )
        url = reverse("orders") + f"?products={product_names}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_order(self):
        order_id = self.order.id
        url = reverse('orders') + f"?id={order_id}"  
        data = {
            "customer_id": str(self.customers[1].id),
            "address": "Updated Address",
            "order_items": [{"product_id": str(self.products[0].id), "quantity": 14}]
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        data_weight_more_than_cumulative = {
            "customer_id": str(self.customers[1].id),
            "address": "Updated Address",
            "order_items": [{"product_id": str(self.products[0].id), "quantity": 16}]
        }

        response = self.client.put(url, data_weight_more_than_cumulative, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
