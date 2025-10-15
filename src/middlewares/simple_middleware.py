from django.utils.deprecation import MiddlewareMixin

class SimpleLoggingMiddleware(MiddlewareMixin):

    #Se agregran contadores temporales para cada ruta
    contadores = {}

    """
    Se ejecuta antes que la vista procese la petición
    """
    def process_request(self, request):
        metodo = request.method
        ruta = request.path
        ip = request.META.get('REMOTE_ADDR','IP desconocida')

        if ruta in self.contadores:
            #Incrementar el contador de visitas por ruta
            self.contadores[ruta] +=1
        else:
            #Se inicializa contador de visita para una ruta
            self.contadores[ruta] = 1

        print(f"Petición interceptada: [{metodo}] - {ruta} - IP: {ip}")
        print(f"{ruta} - Vistada {self.contadores[ruta]} veces")
        
        return None

    """
        Se ejecuta despues de que la vista procese la petición
    """
    def process_response(self, request, response):
        status_code = response.status_code
        
        #Registro información de la respuesta
        print(f"Respuesta capturada: {status_code}")

        #Podria agregar información a la cabeceras de las respuesta
        response['X-API-Name'] = 'UADE Academy API'
        response['X-API-Version'] = '1.0'

        return response
