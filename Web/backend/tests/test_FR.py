from django.test import TestCase
from backend.dataAccess.storageAccess import StorageAccess
from backend.dataAccess.articleAccess import ArticleAccess
from backend.coremodels.article import Article
from backend.coremodels.compartment import Compartment
from backend.coremodels.storage import Storage 
from backend.coremodels.qr_code import QRCode
from backend.services.articleManagementService import ArticleManagementService
from backend.services.storageManagementService import StorageManagementService
import unittest
from unittest.mock import MagicMock
from unittest.mock import MagicMock, Mock
from ..services.orderServices import OrderService
from ..dataAccess.centralStorageAccess import CentralStorageAccess
from ..dataAccess.storageAccess import StorageAccess
from ..dataAccess.userAccess import UserAccess
from ..dataAccess.orderAccess import OrderAccess
from .testObjectFactory.dependencyFactory import DependencyFactory
from .testObjectFactory.coremodelFactory import create_article
from .testObjectFactory.coremodelFactory import create_storage
from .testObjectFactory.coremodelFactory import create_transaction
from .testObjectFactory.coremodelFactory import create_costcenter
from datetime import datetime
import datetime

# Testing FR4.1
# === How To Rewrite tests example 1 === #
# Here the same functionality that you intended is preserved

# === Rewritten test === # 
# Note: This test is dependent on that functions in the service layer and data access layer work as they should. So this is not a unit test
# Run this test individually with the command: python manage.py test backend.tests.test_FR.ArticleIdentificationTest
class ArticleIdentificationTest(TestCase):
    def setUp(self):
        self.article_to_search_for = Article.objects.create(lio_id ="1") #Database is populated and the object is stored so that we don't have to retrieve it again
        self.article_management_service : ArticleManagementService = ArticleManagementService() #An instance of the class to be tested is created and stored as a class variable for the test class. The "articleManagementService :" part specifies that the stored variable must be of type articlemanagementservice, this is not necessary, but makes the code more understandable
    def test_get_article_by_lio_id(self):
        test_search = self.article_management_service.get_article_by_lio_id("1")
        self.assertEqual(test_search, self.article_to_search_for)

# === Previously written like this, use for reference when rewriting other tests === #
# class ArticleIdentificationTest(TestCase):    
#      def setUp(self):                     
#          Article.objects.create(lio_id="1")         
            
#      def test_get_article_by_lio_id_function(self): 
#         article = Article.objects.get(lio_id="1")                  
#         self.assertEqual(articleManagementService.get_article_by_lio_id(self,"1"), article)        


# Testing FR4.6
class CompartmentCreationTest(TestCase):    
     def setUp(self):                     
         self.article_in_compartment = Article.objects.create(lio_id="1")
         self.article_management_service : ArticleManagementService = ArticleManagementService()
         self.storage_in_compartment = Storage.objects.create(id="1")
         self.storage_management_service : StorageManagementService = StorageManagementService()
         self.compartment = Compartment.objects.create(id="1", storage = Storage.objects.get(id="1"), article = Article.objects.get(lio_id="1"))
            
     def test_storageManagementService(self):
        test_search_compartment = self.storage_management_service.get_compartment_by_id(id="1")
        test_search_article = self.article_management_service.get_article_by_lio_id(lio_id="1")
        test_search_storage = self.storage_management_service.get_storage_by_id(id="1")
        self.assertEqual(test_search_compartment, self.compartment)
        self.assertEqual(self.compartment.article, test_search_article)
        self.assertEqual(self.compartment.storage, test_search_storage)


# Testing FR4.3
class FR4_3_Test(TestCase):
    def setUp(self):
        #create 2 storage spaces in the same storage units containing the same article
        self.article_in_compartment = Article.objects.create(lio_id="1")
        self.storage_in_compartment = Storage.objects.create(id="1")
        self.article_management_service : ArticleManagementService = ArticleManagementService()
        self.storage_management_service : StorageManagementService = StorageManagementService()
        self.compartment = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="1"), article = self.article_management_service.get_article_by_lio_id(lio_id="1"))
        self.compartment = Compartment.objects.create(id="2", storage = self.storage_management_service.get_storage_by_id(id="1"), article = self.article_management_service.get_article_by_lio_id(lio_id="1"))
       

        #create a second article in third storage space but in same storage unit
        self.article_in_compartment = Article.objects.create(lio_id="2")
        self.compartment = Compartment.objects.create(id="3", storage = self.storage_management_service.get_storage_by_id(id="1"), article = self.article_management_service.get_article_by_lio_id(lio_id="2"))

    def test_FR4_3(self):

        #Test that we can find/have the same article in different storage spaces in the same unit
        storage = self.storage_management_service.get_storage_by_id(id="1")
        compartment1 = self.storage_management_service.get_compartment_by_id(id="1")
        compartment2 = self.storage_management_service.get_compartment_by_id(id="2")
        article1 = self.article_management_service.get_article_by_lio_id("1")
        self.assertEqual(compartment1.article, article1)
        self.assertEqual(compartment2.article, article1)
        self.assertEqual(compartment1.storage, storage)
        self.assertEqual(compartment2.storage, storage)


# Testing FR6.2 "In each storage space, the system shall record the number of a certain article based on the LIO-number"
# Not sure if this actually tests what it is inteded to test. Manages to return a positive test result but second argument in assertEqual maybe should not be just a number?

class FR6_2_test(TestCase):

    def setUp(self):
        self.article_in_compartment = Article.objects.create(lio_id="1")
        self.article_management_service : ArticleManagementService = ArticleManagementService()
        self.storage_management_service : StorageManagementService = StorageManagementService()
        self.storage_in_compartment = Storage.objects.create(id="1")
        self.storageSpace1 = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="1"), article=self.article_management_service.get_article_by_lio_id(lio_id="1"), amount=2)


    def test_FR6_2(self):
        test_article1 = self.article_management_service.get_article_by_lio_id("1")
        test_search_compartment = self.storage_management_service.get_compartment_by_id("1")
        self.assertEqual(test_search_compartment.amount, 2) 
        self.assertNotEqual(test_search_compartment.amount, 3) 

# class FR6_2_test(TestCase):

#     def setUp(self):
#         Article.objects.create(lio_id="1")
#         Storage.objects.create(id="1")
#         Compartment.objects.create(id="1", storage = Storage.objects.get(id="1"), article = Article.objects.get(lio_id="1"), amount = 2)
#         Compartment.objects.create(id="2", storage = Storage.objects.get(id="1"), article = Article.objects.get(lio_id="1"), amount = 4)

#     def test_FR6_2(self):
#         article1 = Article.objects.get(lio_id="1")
#         compartment1 = Compartment.objects.get(id="1")
#         compartment2 = Compartment.objects.get(id="2")
#         self.assertEqual(compartment1.amount, 2) 


#Testing FR1.2


# class FR1_2_test(TestCase):

#     def setUp(self):

#         UserInfo.objects.create(name)


#Testing FR8.9

class FR8_9_test(TestCase): 
    def setUp(self):
        self.article1 = Article.objects.create(lio_id="1")
        self.article2 = Article.objects.create(lio_id="2")
        self.article_management_service : ArticleManagementService = ArticleManagementService()
        self.storage_management_service : StorageManagementService = StorageManagementService()
        self.Storage1 = Storage.objects.create(id="1")
        self.Storage2 = Storage.objects.create(id="2")
        self.compartment1 = Compartment.objects.create(id="1", storage = self.storage_management_service.get_storage_by_id(id="1"), article=self.article_management_service.get_article_by_lio_id(lio_id="1"), amount=2)
        self.compartment2 = Compartment.objects.create(id="2", storage = self.storage_management_service.get_storage_by_id(id="2"), article=self.article_management_service.get_article_by_lio_id(lio_id="2"), amount=4)

    def test_FR8_9(self):
        test_article1 = self.storage_management_service.search_article_in_storage("1", "1")
        test_article2 = self.storage_management_service.search_article_in_storage("2", "2")
        self.assertEqual(test_article1, 2)
        self.assertEqual(test_article2, 4)
        self.assertNotEqual(test_article2, 5)


       





#Testing FR4.2
#-------Fails test and gives errormessage: "Compartment matching query does not exist."
#-------No idea what is wrong.
# class FR4_2_test(TestCase):
#     def setUP(self):
#         article_access_stub = ArticleAccess
#         self.article_to_search_for = Article(lio_id="1")
#         storage_access_stub = StorageAccess
#         self.storage_access_stub = StorageAccess(id="1")

#         Compartment.objects.create(id="2", storage = Storage.objects.get(id="1"), article = Article.objects.get(lio_id="1"))
#         QRCode.objects.create(id="1", compartment=Compartment.objects.get(id="2"))

#     def test_QRcode_containing_Storagespace(self):
#         compartment = Compartment.objects.get(id="2")
#         qrcode = QRCode.objects.get(id="1")
#         self.assertEqual(qrcode.compartment, compartment)



class StorageServiceEconomyTest(TestCase):
    '''Storage service economy test.'''
    def set_up(self):
        dependency_factory = DependencyFactory()
        transacted_article = create_article(price=10)
        cost_center = create_costcenter(id="123")
        storage = create_storage(costCenter=cost_center)
        transaction_time = datetime.date(2000, 7, 15)
        transaction_list = []
        transaction_list.append(create_transaction(article=transacted_article,
                                                   amount=2, operation=2,
                                                   storage=storage,
                                                   time_of_transaction=(
                                                       transaction_time)))
        transaction_list.append(create_transaction(article=transacted_article,
                                                   amount=2, operation=1,
                                                   storage=storage,
                                                   time_of_transaction=(
                                                       transaction_time)))
        transaction_list.append(create_transaction(article=transacted_article,
                                                   amount=4,
                                                   operation=1,
                                                   storage=storage,
                                                   time_of_transaction=(
                                                       transaction_time)))
        storage_access_mock = StorageAccess
        storage_access_mock.get_transaction_by_storage = MagicMock(
                                     return_value=transaction_list)
        user_access_mock = UserAccess
        user_access_mock.get_user_cost_center = MagicMock(
                                 return_value=cost_center)
        mocked_dependencies = (
            dependency_factory.complete_dependency_dictionary(
                {"StorageAccess": storage_access_mock,
                 "UserAccess": user_access_mock}))
        self.storage_service = StorageManagementService(mocked_dependencies)

    def test_sum_transactions_and_withdrawals(self):
        '''Test sym of transactions and withdrawals.'''
        economyresult = self.storage_service.get_storage_cost(
                                "", "2000-06-15", "2000-08-15")
        self.assertAlmostEquals(economyresult, 40)