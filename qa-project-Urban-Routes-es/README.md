# 🚕 Automatización de Pruebas Web UI (E2E): Urban Routes

![Project](https://img.shields.io/badge/Project-UI_Automation-blue) ![Language](https://img.shields.io/badge/Language-Python_3-yellow) ![Framework](https://img.shields.io/badge/Framework-Selenium_WebDriver-green) ![Framework](https://img.shields.io/badge/Framework-Pytest-lightgray) ![Pattern](https://img.shields.io/badge/Pattern-POM-orange)

## 📌 Descripción del Proyecto

Este proyecto contiene un framework de automatización End-to-End (E2E) para la aplicación web **Urban Routes**. Su objetivo es validar de forma automatizada el flujo completo ("Happy Path") de solicitud de un taxi con tarifa Comfort. 

El script asegura que la interfaz de usuario responda correctamente desde la inserción de direcciones hasta la asignación de un conductor, interactuando con modales dinámicos, pasarelas de pago complejas y sistemas de validación por SMS.

---

## 🛠️ Tecnologías y Patrones de Diseño

El framework está construido bajo el patrón **Page Object Model (POM)**, garantizando que el código sea escalable, mantenible y tolerante a cambios estructurales en la interfaz gráfica.

*   **Python 3:** Lenguaje principal.
*   **Selenium WebDriver:** Herramienta core de automatización de navegadores e interacción con el DOM.
*   **Pytest:** Motor de ejecución de pruebas y orquestación de aserciones.
*   **Técnicas Avanzadas Aplicadas:** 
    *   Esperas Explícitas (`WebDriverWait`).
    *   Inyección de JavaScript para forzar eventos del navegador (ej. `blur`).
    *   Lectura de *Performance Logs* para intercepción de tráfico de red.

### 📂 Estructura de Archivos (Arquitectura POM)

La separación de responsabilidades es clave en este framework para no mezclar configuraciones con la lógica de pruebas:
*   `data.py`: Centraliza los datos de prueba estáticos (URLs del servidor, direcciones de origen/destino, números telefónicos y datos de tarjetas de crédito).
*   `main.py`: Contiene la clase principal de la página (`UrbanRoutesPage`), donde se encapsulan todos los localizadores web (XPath, CSS, ID) y los métodos de interacción (ej. `set_route()`, `click_comfort_tariff()`).
*   `test_urban_routes.py`: Archivo *runner* que contiene la lógica de validación, orquestando los métodos de forma secuencial para ejecutar el flujo E2E.

---

## 🚀 Flujo Automatizado y Cobertura (Happy Path)

El script automatiza secuencialmente las siguientes 9 acciones críticas sin ninguna intervención humana:

| # | Acción Automatizada en la Interfaz (UI) | Estado de Ejecución |
| :--- | :--- | :--- |
| **1** | Configurar las direcciones "Desde" y "Hasta". | ✅ PASSED |
| **2** | Seleccionar la tarifa "Comfort". | ✅ PASSED |
| **3** | Rellenar número de teléfono y confirmar mediante código SMS. | ✅ PASSED |
| **4** | Agregar y validar una tarjeta de crédito (forzando evento con JS). | ✅ PASSED |
| **5** | Escribir un mensaje personalizado para el conductor. | ✅ PASSED |
| **6** | Agregar extras al pedido: Solicitar "Manta y pañuelos" (usando Auto-scroll). | ✅ PASSED |
| **7** | Agregar extras al pedido: Pedir exactamente "2 helados" (cálculo dinámico). | ✅ PASSED |
| **8** | Desplegar el modal de búsqueda de taxi y verificar la cuenta regresiva. | ✅ PASSED |
| **9** | Confirmar la asignación exitosa del conductor en la interfaz. | ✅ PASSED |

> 💡 **Nota Técnica sobre el SMS (Paso 3):** La confirmación telefónica no utiliza esperas manuales ni dispositivos reales. El framework está programado para interceptar los registros de rendimiento del navegador (`performance logs`), extrayendo el código de confirmación directamente desde la respuesta del backend en la red.

---

## ⚙️ Instrucciones de Ejecución

### Precondiciones
1. Instalar Python 3.8+ y tener Google Chrome instalado junto con su respectivo `ChromeDriver`.
2. Instalar las dependencias requeridas del proyecto ejecutando:
   ```bash
   pip install selenium pytest
   ```
3. Iniciar el servidor de Urban Routes y actualizar la variable de URL en el archivo `data.py`.

### Ejecución de la Suite
Para correr la prueba completa mostrando la salida detallada por consola:
```bash
pytest test_urban_routes.py -v
```

---

## 🧑‍💻 Perfil Técnico
**María Auxiliadora Vélez Mendoza** - *QA Automation Engineer*

