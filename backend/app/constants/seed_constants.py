from decimal import Decimal

from app.constants.employee_constants import Country, Department, JobTitle

SEED_EMPLOYEE_COUNT = 10_000
SEED_RANDOM_SEED = 42
SEED_BATCH_SIZE = 1_000
SEED_EMAIL_DOMAIN = "acme.com"
SEED_EMAIL_FALLBACK_NAME = "employee"
SEED_MAX_TENURE_DAYS = 15 * 365
SEED_SALARY_ROUNDING = Decimal("100")

# Annual gross base salary band for a mid-level Software Engineer, in each country's local currency.
COUNTRY_BASE_SALARY_BAND: dict[Country, tuple[Decimal, Decimal]] = {
    Country.UNITED_STATES: (Decimal("95000"), Decimal("140000")),
    Country.UNITED_KINGDOM: (Decimal("50000"), Decimal("80000")),
    Country.GERMANY: (Decimal("55000"), Decimal("80000")),
    Country.FRANCE: (Decimal("45000"), Decimal("65000")),
    Country.INDIA: (Decimal("900000"), Decimal("2000000")),
    Country.CANADA: (Decimal("80000"), Decimal("115000")),
    Country.AUSTRALIA: (Decimal("95000"), Decimal("135000")),
    Country.SINGAPORE: (Decimal("70000"), Decimal("110000")),
    Country.JAPAN: (Decimal("5500000"), Decimal("8500000")),
}

# How each role is paid relative to the Software Engineer band in the same country.
JOB_TITLE_SALARY_MULTIPLIER: dict[JobTitle, Decimal] = {
    JobTitle.SOFTWARE_ENGINEER: Decimal("1.00"),
    JobTitle.SENIOR_SOFTWARE_ENGINEER: Decimal("1.35"),
    JobTitle.ENGINEERING_MANAGER: Decimal("1.70"),
    JobTitle.PRODUCT_MANAGER: Decimal("1.40"),
    JobTitle.DESIGNER: Decimal("0.95"),
    JobTitle.DATA_ANALYST: Decimal("0.85"),
    JobTitle.SALES_REPRESENTATIVE: Decimal("0.80"),
    JobTitle.MARKETING_SPECIALIST: Decimal("0.80"),
    JobTitle.ACCOUNTANT: Decimal("0.85"),
    JobTitle.HR_SPECIALIST: Decimal("0.75"),
    JobTitle.OPERATIONS_MANAGER: Decimal("1.10"),
    JobTitle.SUPPORT_SPECIALIST: Decimal("0.55"),
}

JOB_TITLE_DEPARTMENT: dict[JobTitle, Department] = {
    JobTitle.SOFTWARE_ENGINEER: Department.ENGINEERING,
    JobTitle.SENIOR_SOFTWARE_ENGINEER: Department.ENGINEERING,
    JobTitle.ENGINEERING_MANAGER: Department.ENGINEERING,
    JobTitle.PRODUCT_MANAGER: Department.PRODUCT,
    JobTitle.DESIGNER: Department.DESIGN,
    JobTitle.DATA_ANALYST: Department.PRODUCT,
    JobTitle.SALES_REPRESENTATIVE: Department.SALES,
    JobTitle.MARKETING_SPECIALIST: Department.MARKETING,
    JobTitle.ACCOUNTANT: Department.FINANCE,
    JobTitle.HR_SPECIALIST: Department.HUMAN_RESOURCES,
    JobTitle.OPERATIONS_MANAGER: Department.OPERATIONS,
    JobTitle.SUPPORT_SPECIALIST: Department.CUSTOMER_SUPPORT,
}

# Relative headcount per country and per role, so the seed resembles a real organisation.
COUNTRY_HEADCOUNT_WEIGHT: dict[Country, int] = {
    Country.UNITED_STATES: 30,
    Country.INDIA: 25,
    Country.UNITED_KINGDOM: 10,
    Country.GERMANY: 8,
    Country.CANADA: 7,
    Country.FRANCE: 6,
    Country.AUSTRALIA: 5,
    Country.SINGAPORE: 5,
    Country.JAPAN: 4,
}

JOB_TITLE_HEADCOUNT_WEIGHT: dict[JobTitle, int] = {
    JobTitle.SOFTWARE_ENGINEER: 25,
    JobTitle.SENIOR_SOFTWARE_ENGINEER: 12,
    JobTitle.ENGINEERING_MANAGER: 4,
    JobTitle.PRODUCT_MANAGER: 6,
    JobTitle.DESIGNER: 5,
    JobTitle.DATA_ANALYST: 6,
    JobTitle.SALES_REPRESENTATIVE: 12,
    JobTitle.MARKETING_SPECIALIST: 7,
    JobTitle.ACCOUNTANT: 5,
    JobTitle.HR_SPECIALIST: 4,
    JobTitle.OPERATIONS_MANAGER: 4,
    JobTitle.SUPPORT_SPECIALIST: 10,
}

COUNTRY_NAME_LOCALE: dict[Country, str] = {
    Country.UNITED_STATES: "en_US",
    Country.UNITED_KINGDOM: "en_GB",
    Country.GERMANY: "de_DE",
    Country.FRANCE: "fr_FR",
    Country.INDIA: "en_IN",
    Country.CANADA: "en_CA",
    Country.AUSTRALIA: "en_AU",
    Country.SINGAPORE: "en_US",
    Country.JAPAN: "ja_JP",
}
