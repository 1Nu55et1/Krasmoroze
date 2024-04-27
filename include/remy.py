# path: include/remy.py
import urllib3
import certifi
import chardet
import idna
import http.cookiejar
import os
import sys
import time
import datetime
import asyncio
import json
import hashlib
import hmac
import base64
from typing import Union, Dict, Any, Tuple, Callable
import aiohttp

class Remy:
    def __init__(self):
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        self.cookie_jar = aiohttp.CookieJar(unsafe=True)  # Usar la clase CookieJar de aiohttp
        self.session = None

    async def request(self, method: str, url: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """
        Realiza una solicitud HTTP asíncrona.

        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE, etc.).
            url (str): URL de la solicitud.
            **kwargs: Argumentos adicionales para la solicitud (headers, data, json, etc.).

        Returns:
            aiohttp.ClientResponse: Objeto de respuesta HTTP.
        """
        async with aiohttp.ClientSession(cookie_jar=self.cookie_jar) as session:
            async with session.request(method, url, **kwargs) as response:
                return response


    def request_sync(self, method: str, url: str, **kwargs: Any) -> urllib3.response.HTTPResponse:
        """
        Realiza una solicitud HTTP síncrona.

        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE, etc.).
            url (str): URL de la solicitud.
            **kwargs: Argumentos adicionales para la solicitud (headers, data, json, etc.).

        Returns:
            urllib3.response.HTTPResponse: Objeto de respuesta HTTP.
        """
        return self.http.request(method, url, **kwargs)

    def upload_file(self, url: str, file_path: str, field_name: str = 'file') -> urllib3.response.HTTPResponse:
        """
        Carga un archivo a través de una solicitud HTTP.

        Args:
            url (str): URL de la solicitud.
            file_path (str): Ruta del archivo a cargar.
            field_name (str, optional): Nombre del campo del formulario. Predeterminado es 'file'.

        Returns:
            urllib3.response.HTTPResponse: Objeto de respuesta HTTP.
        """
        with open(file_path, 'rb') as file:
            fields = {
                field_name: (os.path.basename(file_path), file, 'application/octet-stream')
            }
            return self.http.request_encode_multipart('POST', url, fields)

    async def stream_response(self, url: str, chunk_size: int = 1024) -> bytes:
        """
        Descarga una respuesta HTTP en modo de streaming.

        Args:
            url (str): URL de la solicitud.
            chunk_size (int, optional): Tamaño del bloque de datos a descargar. Predeterminado es 1024 bytes.

        Yields:
            bytes: Bloques de datos de la respuesta.
        """
        async with aiohttp.ClientSession(cookie_jar=self.cookie_jar) as session:
            async with session.get(url) as response:
                async for chunk in response.content.iter_chunked(chunk_size):
                    yield chunk

    def get_encoding(self, response: urllib3.response.HTTPResponse) -> str:
        """
        Detecta la codificación de caracteres de la respuesta HTTP.

        Args:
            response (urllib3.response.HTTPResponse): Objeto de respuesta HTTP.

        Returns:
            str: Codificación de caracteres detectada.
        """
        encoding = chardet.detect(response.data)['encoding']
        return encoding or 'utf-8'

    def handle_redirects(self, response: urllib3.response.HTTPResponse, max_redirects: int = 5) -> urllib3.response.HTTPResponse:
        """
        Maneja las redirecciones de la respuesta HTTP.

        Args:
            response (urllib3.response.HTTPResponse): Objeto de respuesta HTTP.
            max_redirects (int, optional): Número máximo de redirecciones a seguir. Predeterminado es 5.

        Returns:
            urllib3.response.HTTPResponse: Objeto de respuesta HTTP final.
        """
        redirect_count = 0
        while response.status in [301, 302, 303, 307, 308] and redirect_count < max_redirects:
            location = response.headers.get('Location')
            if not location:
                break
            response = self.http.request('GET', location)
            redirect_count += 1
        return response

    def handle_auth(self, response: urllib3.response.HTTPResponse, username: str, password: str) -> urllib3.response.HTTPResponse:
        """
        Maneja la autenticación básica o de formularios de la respuesta HTTP.

        Args:
            response (urllib3.response.HTTPResponse): Objeto de respuesta HTTP.
            username (str): Nombre de usuario.
            password (str): Contraseña.

        Returns:
            urllib3.response.HTTPResponse: Objeto de respuesta HTTP con autenticación.
        """
        if response.status == 401:  # Autenticación básica
            auth_header = f'Basic {idna.encode(username).decode()}:{idna.encode(password).decode()}'
            return self.http.request('GET', response.geturl(), headers={'Authorization': auth_header})
        elif response.status == 403:  # Autenticación de formularios
            # Implementar lógica de autenticación de formularios
            pass
        return response

    def handle_compression(self, response: urllib3.response.HTTPResponse) -> urllib3.response.HTTPResponse:
        """
        Maneja la compresión de la respuesta HTTP.

        Args:
            response (urllib3.response.HTTPResponse): Objeto de respuesta HTTP.

        Returns:
            urllib3.response.HTTPResponse: Objeto de respuesta HTTP descomprimido.
        """
        encoding = response.headers.get('Content-Encoding')
        if encoding == 'gzip':
            return self.http.request('GET', response.geturl(), headers={'Accept-Encoding': 'gzip'})
        elif encoding == 'deflate':
            return self.http.request('GET', response.geturl(), headers={'Accept-Encoding': 'deflate'})
        return response

    def handle_cookies(self, response: urllib3.response.HTTPResponse) -> urllib3.response.HTTPResponse:
        """
        Maneja las cookies de la respuesta HTTP.

        Args:
            response (urllib3.response.HTTPResponse): Objeto de respuesta HTTP.

        Returns:
            urllib3.response.HTTPResponse: Objeto de respuesta HTTP con cookies.
        """
        self.cookie_jar.extract_cookies(response, response.request)
        return response

    def handle_errors(self, response: urllib3.response.HTTPResponse) -> urllib3.response.HTTPResponse:
        """
        Maneja los errores de la respuesta HTTP.

        Args:
            response (urllib3.response.HTTPResponse): Objeto de respuesta HTTP.

        Raises:
            Exception: Excepción correspondiente al error HTTP.
        """
        if response.status >= 400:
            raise Exception(f'HTTP Error {response.status}: {response.reason}')
        return response

    def get(self, url: str, **kwargs: Any) -> Union[aiohttp.ClientResponse, urllib3.response.HTTPResponse]:
        """
        Realiza una solicitud HTTP GET.

        Args:
            url (str): URL de la solicitud.
            **kwargs: Argumentos adicionales para la solicitud (headers, params, etc.).

        Returns:
            Union[aiohttp.ClientResponse, urllib3.response.HTTPResponse]: Objeto de respuesta HTTP.
        """
        return self.request('GET', url, **kwargs)

    def post(self, url: str, data: Union[Dict[str, Any], bytes, str] = None, json: Any = None, **kwargs: Any) -> Union[aiohttp.ClientResponse, urllib3.response.HTTPResponse]:
        """
        Realiza una solicitud HTTP POST.

        Args:
            url (str): URL de la solicitud.
            data (Union[Dict[str, Any], bytes, str], optional): Datos de la solicitud.
            json (Any, optional): Datos JSON de la solicitud.
            **kwargs: Argumentos adicionales para la solicitud (headers, etc.).

        Returns:
            Union[aiohttp.ClientResponse, urllib3.response.HTTPResponse]: Objeto de respuesta HTTP.
        """
        if json is not None:
            kwargs['json'] = json
        elif data is not None:
            kwargs['data'] = data
        return self.request('POST', url, **kwargs)

    def put(self, url: str, data: Union[Dict[str, Any], bytes, str] = None, **kwargs: Any) -> Union[aiohttp.ClientResponse, urllib3.response.HTTPResponse]:
        """
        Realiza una solicitud HTTP PUT.

        Args:
            url (str): URL de la solicitud.
            data (Union[Dict[str, Any], bytes, str], optional): Datos de la solicitud.
            **kwargs: Argumentos adicionales para la solicitud (headers, etc.).

        Returns:
            Union[aiohttp.ClientResponse, urllib3.response.HTTPResponse]: Objeto de respuesta HTTP.
        """
        kwargs['data'] = data
        return self.request('PUT', url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> Union[aiohttp.ClientResponse, urllib3.response.HTTPResponse]:
        """
        Realiza una solicitud HTTP DELETE.

        Args:
            url (str): URL de la solicitud.
            **kwargs: Argumentos adicionales para la solicitud (headers, etc.).

        Returns:
            Union[aiohttp.ClientResponse, urllib3.response.HTTPResponse]: Objeto de respuesta HTTP.
        """
        return self.request('DELETE', url, **kwargs)

    def add_header(self, key: str, value: str) -> None:
        """
        Agrega una cabecera HTTP a la solicitud.

        Args:
            key (str): Nombre de la cabecera.
            value (str): Valor de la cabecera.
        """
        self.http.headers[key] = value

    def remove_header(self, key: str) -> None:
        """
        Elimina una cabecera HTTP de la solicitud.

        Args:
            key (str): Nombre de la cabecera a eliminar.
        """
        if key in self.http.headers:
            del self.http.headers[key]

    def set_auth(self, auth_type: str, username: str, password: str) -> None:
        """
        Establece la autenticación para las solicitudes.

        Args:
            auth_type (str): Tipo de autenticación ('basic' o 'digest').
            username (str): Nombre de usuario.
            password (str): Contraseña.
        """
        if auth_type == 'basic':
            auth_header = f'Basic {idna.encode(username).decode()}:{idna.encode(password).decode()}'
            self.add_header('Authorization', auth_header)
        elif auth_type == 'digest':
            # Implementar lógica de autenticación Digest
            pass

    def set_cookies(self, cookies: Dict[str, str]) -> None:
        """
        Establece las cookies para las solicitudes.

        Args:
            cookies (Dict[str, str]): Diccionario de cookies.
        """
        for key, value in cookies.items():
            self.cookie_jar.set_cookie(http.cookiejar.Cookie(
                version=0, name=key, value=value, port=None,
                port_specified=False, domain='', domain_specified=False,
                domain_initial_dot=False, path='/', path_specified=True,
                expires=None, discard=True, comment=None, comment_url=None,
                rest={'HttpOnly': None}, rfc2109=False
            ))

    def get_cookies(self) -> Dict[str, str]:
        """
        Obtiene las cookies actuales.

        Returns:
            Dict[str, str]: Diccionario de cookies.
        """
        cookies = {}
        for cookie in self.cookie_jar:
            cookies[cookie.name] = cookie.value
        return cookies

    def handle_websocket(self, url: str, on_message: Callable[[str], None]) -> None:
        """
        Maneja una conexión WebSocket.

        Args:
            url (str): URL de la conexión WebSocket.
            on_message (Callable[[str], None]): Función de devolución de llamada para manejar los mensajes recibidos.
        """
        async def websocket_handler():
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(url) as ws:
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            on_message(msg.data)
                        elif msg.type == aiohttp.WSMsgType.CLOSED:
                            break
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            break

        asyncio.create_task(websocket_handler())
