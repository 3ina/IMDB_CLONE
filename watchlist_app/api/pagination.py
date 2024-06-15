from rest_framework.pagination import CursorPagination


class WatchListPagination(CursorPagination):
    page_size = 5
    ordering = 'created'
    cursor_query_param = 'record'
