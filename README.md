# Información de Krasmoroze
Krasmoroze, es una librería de Python que permite extraer contenido de documentos HTML y transformarlo en una lista, matriz o diccionario. Además, es una biblioteca que proporciona una forma sencilla y eficiente de trabajar con operaciones de E/S asíncronas, como comunicación de red, E/S de archivos y otros tipos de tareas de E/S, permitiendo esperar a que se completen varias operaciones de E/S y luego ejecutar el código apropiado en función de cuál se complete primero. Por otro lado, Requests es una biblioteca cliente HTTP que facilita enormemente el trabajo con peticiones HTTP, siendo una herramienta útil en diversos proyectos.
> El nombre Krasmoroze significa en  español "Belleza gelida" que en verdad es el significado de красивый мороз pero no de la palabra y el como se escrive sino viene del como suena la palabra que seria "krasivyy moroz".

## Adiciones por hacer

#### Comparacion de Remy con requests:

> Puntos Buenos:

1. **Manejo de WebSocket**: El módulo `Remy` tiene la capacidad de manejar conexiones WebSocket, mientras que `requests` no tiene soporte nativo para este protocolo.

2. **Manejo de autenticación Digest**: Aunque `requests` tiene soporte para autenticación básica, el módulo `Remy` también implementa la autenticación Digest, lo cual no está presente en `requests`.

3. **Manejo de compresión de respuestas**: El módulo `Remy` tiene la capacidad de manejar la compresión de las respuestas HTTP, como gzip y deflate, lo cual no está presente de manera explícita en `requests`.

4. **Manejo de redirecciones personalizado**: El módulo `Remy` tiene una función `handle_redirects` que permite personalizar el manejo de las redirecciones HTTP, lo cual no está presente en `requests`.

5. **Manejo de errores personalizado**: Aunque `requests` tiene un manejo de errores más detallado, el módulo `Remy` permite personalizar el manejo de los errores HTTP a través de la función `handle_errors`.

6. **Integración con `urllib3` y `certifi`**: El módulo `Remy` está integrado con las bibliotecas `urllib3` y `certifi`, lo que le permite manejar de manera más explícita las dependencias relacionadas con las solicitudes HTTP.

7. **Soporte para streaming de datos**: El módulo `Remy` tiene la capacidad de descargar respuestas HTTP en modo de streaming, lo cual no está presente de manera nativa en `requests`.

8. **Detección de codificación de caracteres**: El módulo `Remy` utiliza la biblioteca `chardet` para detectar la codificación de caracteres de las respuestas HTTP, lo cual no está presente en `requests`.

9. **Manejo de cookies a través de `http.cookiejar`**: Aunque `requests` tiene un manejo de cookies más avanzado, el módulo `Remy` utiliza la biblioteca `http.cookiejar` para manejar las cookies de manera más explícita.

10. **Interfaz de usuario más personalizable**: Mientras que `requests` tiene una interfaz de usuario más sencilla y abstracta, el módulo `Remy` permite una mayor personalización y control sobre los detalles de las solicitudes HTTP.

> Puntos malos:

1. **Manejo de cookies más avanzado**: `requests` tiene un manejo de cookies más avanzado, con soporte para cookies de sesión y cookies persistentes. El módulo `Remy` tiene un manejo básico de cookies a través de `http.cookiejar`.

2. **Soporte para más tipos de autenticación**: `requests` tiene soporte integrado para varios tipos de autenticación, como autenticación Digest, autenticación de token, etc. El módulo `Remy` solo maneja autenticación básica y Digest.

3. **Manejo de cabeceras más flexible**: `requests` permite un manejo más flexible de las cabeceras HTTP, como la capacidad de agregar, modificar o eliminar cabeceras de manera sencilla. El módulo `Remy` tiene un manejo más básico de las cabeceras.

4. **Manejo de errores más detallado y específico**: `requests` tiene un manejo de errores más detallado, con excepciones específicas para diferentes tipos de errores HTTP (como `RequestException`, `HTTPError`, `ConnectionError`, etc.). El módulo `Remy` solo maneja los errores de manera genérica.

5. **Soporte para más características de HTTP**: `requests` tiene soporte para más características de HTTP, como manejo de cabeceras de rango, streaming de respuestas, etc. El módulo `Remy` solo maneja algunas de estas características.

6. **Integración con otras bibliotecas y ecosistema**: `requests` se integra fácilmente con otras bibliotecas, como `urllib3`, `certifi`, `chardet`, etc. El módulo `Remy` tiene que manejar estas dependencias de manera más explícita.

7. **Soporte para más protocolos y formatos**: `requests` tiene soporte para más protocolos y formatos, como WebSocket, GraphQL, etc. El módulo `Remy` se enfoca principalmente en HTTP.

8. **Funcionalidades adicionales**: `requests` tiene algunas funcionalidades adicionales, como la capacidad de descargar archivos, enviar solicitudes asíncronas, etc. que aún no se han implementado en el módulo `Remy`.

9. **Documentación y comunidad más amplia**: `requests` tiene una documentación más extensa y una comunidad más grande, lo que facilita la resolución de problemas y la obtención de ayuda.
