<div align="right">
  🌍 <strong>Español</strong> | <a href="README_en.md">English</a>
</div>

# 🚕 Automatización Web UI (E2E): Urban Routes

![Project](https://img.shields.io/badge/Project-UI_Automation-blue) ![Language](https://img.shields.io/badge/Language-Python_3-yellow) ![Framework](https://img.shields.io/badge/Framework-Selenium_WebDriver-green) ![Pattern](https://img.shields.io/badge/Pattern-POM-orange)

## 📌 Resumen del Proyecto (Metodología STAR)

*   **Situación:** La aplicación web **Urban Routes** requería garantizar que el flujo crítico del usuario —desde ingresar direcciones hasta la asignación de un conductor— funcionara sin problemas en cada actualización. Las pruebas manuales de este flujo largo y complejo consumían demasiado tiempo.
*   **Tarea:** Desarrollar un framework de automatización UI escalable y robusto desde cero que cubra 9 funcionalidades críticas interactuando con modales dinámicos, pasarelas de pago y validaciones por SMS.
*   **Acción:** 
    *   Implementé un script de pruebas automatizadas en **Python** utilizando **Selenium WebDriver** y el framework de pruebas **Pytest**.
    *   Estructuré el framework bajo el patrón **Page Object Model (POM)**, separando limpiamente los localizadores (XPath, CSS) y los métodos de interacción de la lógica de prueba.
    *   Desarrollé funciones complejas para el manejo del DOM: utilicé **WebDriverWait** (esperas explícitas) para sincronizar modales dinámicos, inyecté JavaScript para forzar el enfoque y desenfoque en campos de tarjetas de crédito, y manipulé contadores dinámicos de UI (ej. selección de cantidad de helados).
    *   Implementé la intercepción de tráfico de red en tiempo real (Performance Logs) para capturar dinámicamente códigos de validación SMS del backend y pasarlos a la UI.
*   **Resultado:** Se automatizó con éxito el 100% del "Happy Path" crítico (E2E). El framework es capaz de solicitar un taxi tarifa Comfort, registrar tarjetas, procesar extras y verificar la cuenta regresiva de asignación del vehículo sin ninguna intervención humana, reduciendo drásticamente el tiempo de regresión de la plataforma.

---

## 🛠️ Stack Tecnológico y Técnicas Aplicadas

*   **Lenguaje & Frameworks:** Python 3.x, Selenium WebDriver, Pytest.
*   **Arquitectura:** Page Object Model (POM).
*   **Estrategias de Localización:** XPath, CSS Selectors, Class Name, ID.
*   **Técnicas Avanzadas:** 
    *   Manejo de tiempos de espera adaptativos (Explicit Waits).
    *   Intercepción de `performance logs` para leer respuestas de red (Captura de SMS).
    *   Interacción con iframes, checkboxes anuidos y botones dinámicos.

---

## 💻 Muestra de Código: Intercepción de Red y Lógica de UI

Uno de los mayores retos en la automatización UI es evitar la dependencia de servicios externos para validaciones como SMS o correos. En este framework, implementé la lectura de los *logs de rendimiento* del navegador para capturar el código SMS directamente desde la respuesta del servidor web:

```python
# Intercepción del Código SMS a través de logs de red
def retrieve_phone_code(driver) -> str:
    import json
    import time
    from selenium.common import WebDriverException
    
    code = None
    for i in range(10):
        try:
            # Filtrado de peticiones de red buscando el endpoint del número
            logs = [log["message"] for log in driver.get_log('performance') 
                    if log.get("message") and 'api/v1/number?number' in log.get("message")]
            
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                    {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if code:
            return code
    raise Exception("No se encontró el código de confirmación del teléfono.")
```

---

## 🚀 Instrucciones de Ejecución

### Prerrequisitos
*   Python 3.8 o superior instalado en el entorno local.
*   Navegador Google Chrome y su respectivo ChromeDriver configurado en el PATH.
*   Instalación de dependencias:
    ```bash
    pip install selenium pytest
    ```

### Estructura de Archivos (POM)
*   `main.py`: Contiene la clase `UrbanRoutesPage` (localizadores y métodos) y la clase `TestUrbanRoutes` (runner de pruebas).
*   `data.py`: Archivo de configuración que contiene datos de prueba (URL del servidor, direcciones, tarjeta de crédito).

### Ejecución de la Suite de Pruebas
Para iniciar la prueba automatizada con salida detallada en terminal, ejecuta:
```bash
python -m pytest main.py -v
```

---

## 🧑‍💻 Perfil Técnico
**María Auxiliadora Vélez Mendoza** - *QA Automation Engineer*
