from unittest import TestCase, main


from app.data_model import (
    DataModelBase,
    ContactInfo,
    Address,
    Agency,
    InsuredInfo,
    PolicyInfo,
    BusinessInfo,
    Coverage,
    Application,
)


class TestDataModelClasses(TestCase):
    def test_DataModelBase(self):
        data = DataModelBase()
        self.assertIsInstance(data, DataModelBase)
        self.assertEqual(data.__class__.__name__, "DataModelBase")
        self.assertEqual(data.__class__.__module__, "app.data_model")
        self.assertEqual(data.__class__.__bases__[0].__name__, "object")

    def test_rand_ContactInfo(self) -> None:
        data = ContactInfo.rand()
        self.assertIsInstance(data, ContactInfo)
        self.assertIsInstance(data.first_name, str)
        self.assertIsInstance(data.last_name, str)
        self.assertIsInstance(data.email, str)
        self.assertIsInstance(data.phone_number, str)
        self.assertIsInstance(data.phone_type, str)
        self.assertIsInstance(data.fax_number, str)

    def test_rand_Address(self) -> None:
        data = Address.rand()
        self.assertIsInstance(data, Address)
        self.assertIsInstance(data.line1, str)
        self.assertIsInstance(data.line2, (str, None))
        self.assertIsInstance(data.city, str)
        self.assertIsInstance(data.state, str)
        self.assertIsInstance(data.zip_code, str)

    def test_rand_Agency(self) -> None:
        data = Agency.rand()
        self.assertIsInstance(data, Agency)
        self.assertIsInstance(data.agency_name, str)
        self.assertIsInstance(data.address, Address)
        self.assertIsInstance(data.contact_info, ContactInfo)

    def test_rand_InsuredInfo(self) -> None:
        data = InsuredInfo.rand()
        self.assertIsInstance(data, InsuredInfo)
        self.assertIsInstance(data.name, str)
        self.assertIsInstance(data.mailing_address, Address)
        self.assertIsInstance(data.fein_or_ssn, ContactInfo)

    def test_rand_PolicyInfo(self) -> None:
        data = PolicyInfo.rand()
        self.assertIsInstance(data, PolicyInfo)
        self.assertIsInstance(data.proposed_eff_date, str)
        self.assertIsInstance(data.proposed_exp_date, str)
        self.assertIsInstance(data.lines_of_business, str)
        self.assertIsInstance(data.premium_details, str)

    def test_rand_BusinessInfo(self) -> None:
        data = BusinessInfo.rand()
        self.assertIsInstance(data, BusinessInfo)
        self.assertIsInstance(data.entity_type, str)
        self.assertIsInstance(data.description_of_operations, str)

    def test_rand_Coverage(self) -> None:
        data = Coverage.rand()
        self.assertIsInstance(data, Coverage)
        self.assertIsInstance(data.coverage_code, str)
        self.assertIsInstance(data.premium, str)
        self.assertIsInstance(data.line_of_business, str)

    def test_rand_Application(self) -> None:
        data = Application.rand()
        self.assertIsInstance(data, Application)
        self.assertIsInstance(data.agency, Agency)
        self.assertIsInstance(data.policy_info, InsuredInfo)
        self.assertIsInstance(data.policy_info, PolicyInfo)
        self.assertIsInstance(data.business_info, BusinessInfo)
        self.assertIsInstance(data.coverages, Coverage)


if __name__ == "__main__":
    main()
