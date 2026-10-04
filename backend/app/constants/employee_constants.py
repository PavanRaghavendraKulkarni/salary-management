from decimal import Decimal
from enum import StrEnum

FULL_NAME_MIN_LENGTH = 2
FULL_NAME_MAX_LENGTH = 100
EMAIL_MAX_LENGTH = 254
CATEGORY_MAX_LENGTH = 50
CURRENCY_CODE_LENGTH = 3

SALARY_PRECISION = 12
SALARY_SCALE = 2
SALARY_QUANTUM = Decimal("0.01")
MIN_ANNUAL_SALARY_EXCLUSIVE = Decimal("0")
MAX_ANNUAL_SALARY = Decimal("9999999999.99")


class Currency(StrEnum):
    USD = "USD"
    GBP = "GBP"
    EUR = "EUR"
    INR = "INR"
    CAD = "CAD"
    AUD = "AUD"
    SGD = "SGD"
    JPY = "JPY"


class Country(StrEnum):
    UNITED_STATES = "United States"
    UNITED_KINGDOM = "United Kingdom"
    GERMANY = "Germany"
    FRANCE = "France"
    INDIA = "India"
    CANADA = "Canada"
    AUSTRALIA = "Australia"
    SINGAPORE = "Singapore"
    JAPAN = "Japan"


COUNTRY_CURRENCY: dict[Country, Currency] = {
    Country.UNITED_STATES: Currency.USD,
    Country.UNITED_KINGDOM: Currency.GBP,
    Country.GERMANY: Currency.EUR,
    Country.FRANCE: Currency.EUR,
    Country.INDIA: Currency.INR,
    Country.CANADA: Currency.CAD,
    Country.AUSTRALIA: Currency.AUD,
    Country.SINGAPORE: Currency.SGD,
    Country.JAPAN: Currency.JPY,
}


class Department(StrEnum):
    ENGINEERING = "Engineering"
    PRODUCT = "Product"
    DESIGN = "Design"
    SALES = "Sales"
    MARKETING = "Marketing"
    FINANCE = "Finance"
    HUMAN_RESOURCES = "Human Resources"
    OPERATIONS = "Operations"
    CUSTOMER_SUPPORT = "Customer Support"


class JobTitle(StrEnum):
    SOFTWARE_ENGINEER = "Software Engineer"
    SENIOR_SOFTWARE_ENGINEER = "Senior Software Engineer"
    ENGINEERING_MANAGER = "Engineering Manager"
    PRODUCT_MANAGER = "Product Manager"
    DESIGNER = "Designer"
    DATA_ANALYST = "Data Analyst"
    SALES_REPRESENTATIVE = "Sales Representative"
    MARKETING_SPECIALIST = "Marketing Specialist"
    ACCOUNTANT = "Accountant"
    HR_SPECIALIST = "HR Specialist"
    OPERATIONS_MANAGER = "Operations Manager"
    SUPPORT_SPECIALIST = "Support Specialist"


class EmployeeSortField(StrEnum):
    FULL_NAME = "full_name"
    EMAIL = "email"
    JOB_TITLE = "job_title"
    DEPARTMENT = "department"
    COUNTRY = "country"
    ANNUAL_SALARY = "annual_salary"
    HIRE_DATE = "hire_date"


DEFAULT_EMPLOYEE_SORT_FIELD = EmployeeSortField.FULL_NAME
SEARCH_MAX_LENGTH = 100
