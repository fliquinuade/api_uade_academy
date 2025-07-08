from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    #Cantidad de elementos dentro de cada pagina
    page_size = 3
    page_size_query_param = 'page_size'
    #Limite de elementos que el cliente puede solicitar
    #  por medio del parametro 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):

        return Response({
            'total_items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'data': data
        })