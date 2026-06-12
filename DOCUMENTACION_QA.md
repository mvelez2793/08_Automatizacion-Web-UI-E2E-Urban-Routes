# 📂 Documentación Técnica: Automatización UI E2E (Urban Routes)

Este documento expone la arquitectura del framework de automatización, los retos técnicos superados en la manipulación del DOM y la estrategia de intercepción de red implementada para validar el flujo End-to-End (E2E) de la aplicación web Urban Routes.

## 🧠 Arquitectura del Framework: Page Object Model (POM)

Para garantizar la mantenibilidad y escalabilidad del código, la suite fue diseñada estrictamente bajo el patrón **Page Object Model (POM)**. 
*   **Encapsulamiento:** Separación total entre los localizadores web (XPath, ID, ClassName), los métodos de interacción (`click`, `send_keys`) y la lógica de aserción en el runner de pruebas (Pytest).
*   **Sincronización:** Implementación exclusiva de **Esperas Explícitas (`WebDriverWait`)** para manejar la carga asíncrona de modales y la aparición de elementos dinámicos, eliminando las frágiles esperas implícitas (`time.sleep` estáticos para la lógica core).

---

## 🛠️ Retos Técnicos y Soluciones Implementadas

Durante el desarrollo del script, superé varios obstáculos comunes en la automatización de interfaces modernas (Single Page Applications). A continuación, detallo las soluciones técnicas aplicadas:

### 1. Intercepción de Tráfico de Red (Bypass de validación SMS)
*   **El Reto:** El flujo de registro exigía validar un número telefónico mediante un código SMS dinámico devuelto por el backend.
*   **La Solución:** En lugar de depender de servicios de terceros, habilité la captura de logs de rendimiento (`performance logs`) en las capacidades de ChromeDriver. Implementé una función para leer el tráfico de red, buscar el endpoint `/api/v1/number?number` y extraer el código SMS directamente de la respuesta JSON del servidor.

```python
# Extracto de la lógica de intercepción de red
logs = [log["message"] for log in driver.get_log('performance') 
        if log.get("message") and 'api/v1/number?number' in log.get("message")]
# Extracción del cuerpo de la respuesta para obtener los dígitos numéricos
```

### 2. Manipulación del DOM mediante Inyección JavaScript (Eventos Focus/Blur)
*   **El Reto:** Al ingresar la tarjeta de crédito, el botón "Agregar" (link) permanecía inactivo (disabled) hasta que el campo del código de seguridad (CVV) perdiera el enfoque (evento blur o pulsación de tecla TAB).
*   **La Solución:** Para evitar inconsistencias al simular teclas de teclado, utilicé la interfaz `execute_script` de Selenium para inyectar JavaScript puro, forzando la pérdida de enfoque sobre el elemento web y disparando la validación del formulario.

```python
# Ingreso del código CVV
card_code_field.send_keys(card_code)

# Forzar pérdida de enfoque (Blur) mediante JavaScript para habilitar el botón
self.driver.execute_script("arguments[0].blur();", card_code_field)
```

### 3. Manejo de Contadores Dinámicos en la UI (Lógica Matemática)
*   **El Reto:** El requerimiento exigía agregar exactamente "2 helados" al pedido. El contador podía iniciar en 0 o vacío, requiriendo clics dinámicos en el botón +.
*   **La Solución:** Programé una lógica condicional que extrae el texto actual del contador, lo parsea a entero (asumiendo 0 si está vacío) y calcula matemáticamente cuántas iteraciones de `click()` son necesarias en el botón "Más" para alcanzar el objetivo, haciendo el código tolerante a estados previos.

```python
# Lógica de cálculo de clics para elementos incrementales
current_text = counter_element.text
current_count = 0 if current_text == '' else int(current_text)
clicks_needed = quantity - current_count

if clicks_needed > 0:
    for i in range(clicks_needed):
        plus_button.click()
```

### 4. Visibilidad de Elementos Ocultos (Scrolling)
*   **El Reto:** Algunos checkboxes, como el requerimiento de "Manta y pañuelos", se encontraban fuera del área visible del navegador (Viewport), causando excepciones de tipo `ElementNotInteractableException` al intentar hacer clic.
*   **La Solución:** Implementé la función `scrollIntoView(true)` de JavaScript para forzar al navegador a desplazar la pantalla hasta el elemento antes de interactuar con él, garantizando la estabilidad de la prueba sin importar la resolución del monitor.

```javascript
// Desplazamiento del scroll hasta el elemento objetivo
arguments[0].scrollIntoView(true);
```

---

Documentación técnica estructurada por **María Auxiliadora Vélez Mendoza** - *QA Automation Engineer*.
