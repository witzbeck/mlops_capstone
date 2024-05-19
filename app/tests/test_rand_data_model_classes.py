from collections.abc import Iterable, Mapping
from datetime import date
import datetime
from typing import Union
from unittest import TestCase, main


from app.data_model import (
    OutputModelBase,
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
        data = OutputModelBase()
        self.assertIsInstance(data, OutputModelBase)
        self.assertEqual(data.__class__.__name__, "OutputModelBase")
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
        self.assertIsInstance(data.fax_number, Union[str, int, None])

    def test_rand_Address(self) -> None:
        data = Address.rand()
        self.assertIsInstance(data, Address)
        self.assertIsInstance(data.line1, str)
        self.assertIsInstance(data.line2, Union[str, None])
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
        self.assertIsInstance(data.fein_or_ssn, Union[int, str, None])

    def test_rand_PolicyInfo(self) -> None:
        data = PolicyInfo.rand()
        self.assertIsInstance(data, PolicyInfo)
        self.assertIsInstance(data.proposed_eff_date, (str, date, datetime))
        self.assertIsInstance(data.proposed_exp_date, (str, date, datetime))
        self.assertIsInstance(data.lines_of_business, (str, list, tuple, Iterable))
        self.assertIsInstance(data.premium_details, (Mapping, dict))

    def test_rand_BusinessInfo(self) -> None:
        data = BusinessInfo.rand()
        self.assertIsInstance(data, BusinessInfo)
        self.assertIsInstance(data.entity_type, str)
        self.assertIsInstance(data.description_of_operations, str)

    def test_rand_Coverage(self) -> None:
        data = Coverage.rand()
        self.assertIsInstance(data, Coverage)
        self.assertIsInstance(data.coverage_code, (str, int))
        self.assertIsInstance(data.premium, (int, float))
        self.assertIsInstance(data.line_of_business, str)

    def test_rand_Application(self) -> None:
        data = Application.rand()
        self.assertIsInstance(data, Application)
        self.assertIsInstance(data.agency, Agency)
        self.assertIsInstance(data.first_named_insured, InsuredInfo)
        self.assertIsInstance(data.additional_insureds, (list, tuple, Iterable))
        self.assertIsInstance(data.policy_info, PolicyInfo)
        self.assertIsInstance(data.business_info, BusinessInfo)
        self.assertIsInstance(data.coverages, (Coverage, list, tuple, Iterable))


if __name__ == "__main__":
    main()
