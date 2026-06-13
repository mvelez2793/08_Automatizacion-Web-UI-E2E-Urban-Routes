<div align="right">
  🌍 <a href="README.md">Español</a> | <strong>English</strong>
</div>

# 🚕 Web UI Automation (E2E): Urban Routes

#### 📌 Project Summary (STAR Methodology)
*   **Situation:** The **Urban Routes** web application required guaranteeing that the critical user flow —from entering addresses to driver assignment— worked flawlessly on every update. Manual testing of this long and complex flow consumed too much time.
*   **Task:** Develop a scalable and robust UI automation framework from scratch covering 9 critical functionalities by interacting with dynamic modals, payment gateways, and SMS validations
*   **Action:**
    *   Implemented an automated test script in **Python** using **Selenium WebDriver** and the **Pytest** testing framework.
    *   Structured the framework under the **Page Object Model (POM)** pattern, cleanly separating locators (XPath, CSS) and interaction methods from the test logic.
    *   Developed complex functions for DOM handling: used **WebDriverWait** (explicit waits) to synchronize dynamic modals, injected JavaScript to force focus and blur on credit card fields, and manipulated dynamic UI counters (e.g., selecting the amount of ice creams).
    *   Implemented real-time network traffic interception (Performance Logs) to dynamically capture SMS validation codes from the backend and pass them to the UI.
*   **Result:** Successfully automated 100% of the critical "Happy Path" (E2E). The framework is capable of requesting a Comfort fare taxi, registering cards, processing extras, and verifying the vehicle assignment countdown without any human intervention, drastically reducing the platform's regression time.

---

#### 🛠️ Tech Stack and Applied Techniques
*   **Language & Frameworks:** Python 3.x, Selenium WebDriver, Pytest.
*   **Architecture:** Page Object Model (POM).
*   **Locator Strategies:** XPath, CSS Selectors, Class Name, ID.
*   **Advanced Techniques:**
    *   Adaptive wait time management (Explicit Waits).
    *   Interception of performance logs to read network responses (SMS Capture).
    *   Interaction with iframes, nested checkboxes, and dynamic buttons.

---
#### 💻 Code Sample: Network Interception and UI Logic
One of the biggest challenges in UI automation is avoiding reliance on external services for validations like SMS or emails. In this framework, I implemented reading the browser's *performance logs* to capture the SMS code directly from the web server's response:


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

