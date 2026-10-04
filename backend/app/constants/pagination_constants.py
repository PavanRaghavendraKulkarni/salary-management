from enum import StrEnum

DEFAULT_PAGE = 1
MIN_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 100


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


DEFAULT_SORT_ORDER = SortOrder.ASC
