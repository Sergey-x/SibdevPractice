from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework import status

from .base import BaseTestClass
from .factories.category_factory import CategoryFactory
from .factories.transaction_factory import TransactionFactory


class BaseTransactionTests(BaseTestClass):
    """
    Base class for testing transaction functionalities.
    """

    @staticmethod
    def create_transaction(owner):
        return TransactionFactory(
            owner=owner,
            category=CategoryFactory(owner=owner),
        )


class CreateTransactionTests(BaseTransactionTests):
    """
    Class provides testing creating transaction.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.url = reverse("api:summary:transaction-list")

        new_transaction = TransactionFactory.build()
        new_transaction.category = CategoryFactory(owner=cls.user)
        cls.new_transaction = model_to_dict(
            new_transaction,
            fields=('sum', 'category'),
        )

    def test_right_auth_header(self):
        """
        Test that request has right http header authorization.
        Response must have 201 status code.
        """
        response = self.client.post(path=self.url, data=self.new_transaction)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_auth_header(self):
        """
        Test that request with `bad` http header authorization don't work.
        Response must have 401 status code.
        """
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(path=self.url, data=self.new_transaction)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListTransactionTests(BaseTransactionTests):
    """
    Class provides testing getting list of transactions.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.url = reverse("api:summary:transaction-list")
        # create own transaction
        cls.create_transaction(cls.user)
        # create someone else's transaction
        cls.create_transaction(cls.another_user)

    def test_get_only_personal_transactions(self):
        """
        Check that user will get only personal transactions.
        Test assumes that exist transactions owned by different users.
        """
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for transaction in response.data['results']:
            self.assertEqual(transaction['owner'], self.user.id)


class UpdateTransactionTests(BaseTransactionTests):
    """
    Class provides testing updating and partial updating transaction.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # create own transaction
        cls.own_transaction = cls.create_transaction(cls.user)
        # create someone else's transaction
        cls.another_transaction = cls.create_transaction(cls.another_user)

        # create updating dict
        update_transaction = TransactionFactory.build()
        update_transaction.category = CategoryFactory(owner=cls.user)
        cls.update_transaction = model_to_dict(
            update_transaction,
            exclude=('id', 'owner'),
        )

    def test_partial_update_personal_transaction(self):
        """
        Test that user can partially update own transaction.
        """
        transaction_url = reverse(
            "api:summary:transaction-detail", args=[self.own_transaction.id]
        )
        response = self.client.patch(
            path=transaction_url,
            data=self.update_transaction,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_another_transaction(self):
        """
        Test that user can't partially update someone else's transaction.
        """
        transaction_url = reverse(
            "api:summary:transaction-detail", args=[self.another_transaction.id]
        )
        response = self.client.patch(
            path=transaction_url,
            data=self.update_transaction,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_transaction(self):
        """
        Test that user can update own transaction.
        """
        url = reverse(
            "api:summary:transaction-detail", args=[self.own_transaction.id]
        )
        response = self.client.patch(path=url, data=self.update_transaction)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_another_transaction(self):
        """
        Test that user can't update someone else's transaction.
        """
        url = reverse(
            "api:summary:transaction-detail", args=[self.another_transaction.id]
        )
        response = self.client.patch(path=url, data=self.update_transaction)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteTransactionTests(BaseTransactionTests):
    """
    Class provides testing deleting transaction.
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # create own transaction
        cls.own_transaction = cls.create_transaction(cls.user)
        # create someone else's transaction
        cls.another_transaction = cls.create_transaction(cls.another_user)

    def test_delete_own_transaction(self):
        """
        Test that user can delete own transaction.
        """
        url = reverse(
            "api:summary:transaction-detail", args=[self.own_transaction.id]
        )
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_transaction(self):
        """
        Test that user can't delete someone else's transaction.
        """
        url = reverse(
            "api:summary:transaction-detail", args=[self.another_transaction.id]
        )
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
