import json
from odoo import http
from odoo.http import request

class HomeApiController(http.Controller):

    def _fix_url(self, url, base_url):
        """
        Convierte rutas relativas (/web/image...) en absolutas públicas
        usando la configuración de Odoo (web.base.url).
        """
        if not url:
            return ""
        
        # Si ya es absoluta (http), la dejamos tal cual
        if url.startswith("http"):
            return url
            
        # Limpiamos slashes y concatenamos
        clean_base = base_url.rstrip('/')
        clean_path = url.lstrip('/')
        return f"{clean_base}/{clean_path}"

    def _traverse_and_fix_images(self, data, base_url):
        """
        Recorre recursivamente el JSON para arreglar las URLs,
        igual que lo hacías en tu CMSService.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if key in ['src', 'image'] and isinstance(value, str):
                    data[key] = self._fix_url(value, base_url)
                elif key == 'image' and isinstance(value, dict):
                    self._traverse_and_fix_images(value, base_url)
                else:
                    self._traverse_and_fix_images(value, base_url)
        elif isinstance(data, list):
            for item in data:
                self._traverse_and_fix_images(item, base_url)
        return data

    @http.route('/api/v1/home', type='http', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_home(self, **kw):
        """
        Endpoint público que reemplaza a tu Flask API.
        """
        try:
            # 1. Buscar el registro (usamos sudo() porque es acceso público)
            home_record = request.env['jasper.home'].sudo().search([], limit=1)
            
            if not home_record:
                return request.make_response(
                    json.dumps({"error": "No Home Page configuration found."}),
                    headers=[('Content-Type', 'application/json')],
                    status=404
                )

            # 2. Obtener la data cruda desde el modelo
            raw_data = home_record.get_home_data()

            # 3. Obtener la URL base del sistema (System Parameters)
            # Esto reemplaza a tu variable de entorno Odoo_PUBLIC_URL
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')

            # 4. Hidratar URLs (Convertir relativas a absolutas)
            final_data = self._traverse_and_fix_images(raw_data, base_url)

            # 5. Construir respuesta idéntica a Flask
            response_data = {"data": final_data}
            
            # 6. Retornar JSON puro con headers CORS
            headers = [
                ('Content-Type', 'application/json'),
                ('Access-Control-Allow-Origin', '*'), # Importante si tu front está en otro dominio
                ('Access-Control-Allow-Methods', 'GET, OPTIONS'),
                ('Cache-Control', 'no-store')
            ]
            
            return request.make_response(
                json.dumps(response_data),
                headers=headers
            )

        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500
            )