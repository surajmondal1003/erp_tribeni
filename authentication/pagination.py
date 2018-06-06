from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination



class ErpLimitOffestpagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10

class ErpPageNumberPagination(PageNumberPagination):
    page_size = 10