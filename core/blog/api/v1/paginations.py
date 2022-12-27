from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BlogPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page-size'
    max_page_size = 100
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total-posts': self.page.paginator.count,
            'total-pages': self.page.paginator.num_pages,
            'results': data
        })