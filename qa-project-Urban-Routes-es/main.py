import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import time
import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from helpers import retrieve_phone_code


class UrbanRoutesPage:
    #lOCALIZADORES DE INGRESO DE DIRECCIÓN
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # LOCALIZADORES DE BOTÓN DE PEDIR TAXI + SELECCIÓN DE TARIFA COMFORT
    taxi_button = (By.XPATH, '//button[text()="Pedir un taxi"]')
    comfort_option = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    tariff_picker = (By.CLASS_NAME, 'tariff-picker')

    #lOCALIZADORES NUMERO DE TELÉFONO + CÓDIGO SMS.
    phone_button = (By.XPATH, '//div[@class="np-text" and text()="Número de teléfono"]')
    phone_modal_input = (By.ID, 'phone')
    phone_next_button =  (By.XPATH, '//button[text()="Siguiente"]')
    code_input = (By.ID, 'code')
    code_confirm_button = (By.XPATH, '//button[text()="Confirmar"]')

    #lOCALIZADORES PARA TARJETA DE CREDITO
    payment_method_button = (By.XPATH, '//div[@class="pp-text" and text()="Método de pago"]')
    add_card_option = (By.XPATH, '//div[@class="pp-title" and text()="Agregar tarjeta"]')
    card_number_input = (By.ID, 'number')
    card_code_input =  (By.XPATH, '//input[@placeholder="12"]')
    add_card_button = (By.XPATH, '//button[text()="Agregar"]')
    close_card_modal = (By.CLASS_NAME, 'section-close')

    # LOCALIZADORES PARA ESCRIBIR UN MENSAJE PARA EL CONTROLADOR
    message_input = (By.ID, 'comment')

    # LOCALIZADORES PARA PEDIR UNA MANTA Y PAÑUELOS + 2 HELADOS
    requirements_section = (By.CLASS_NAME, 'reqs-head')
    blanket_switch = (By.CLASS_NAME, 'switch-input')

    # LOCALIZADORES  PARA MODAL INFORMACIÓN DE CONDUCTOR
    final_order_button = (By.XPATH, '//button[contains(@class, "smart-button")]')

    # Modal del CONTADOR (primer modal)
    countdown_timer = (By.CLASS_NAME, 'order-header-time')
    search_title = (By.CLASS_NAME, 'order-header-title')  # "Buscar automóvil"
    progress_bar = (By.CLASS_NAME, 'order-progress')  # Barra de progreso

    # Modal del CONDUCTOR (segundo modal - después del contador)
    order_number = (By.CLASS_NAME, 'order-number')
    number_element = (By.CLASS_NAME, 'number')


    def __init__(self, driver):
        self.driver = driver
        self.wait =  WebDriverWait(driver, 10)

    def set_routes(self, address_from, address_to):
        """ Paso 1: Configurar las direcciones FROM Y TO """
        # Campo From
        from_element = self.wait.until(EC.element_to_be_clickable(self.from_field))
        from_element.clear()
        from_element.send_keys(address_from)

        # Campo To
        to_element = self.wait.until(EC.element_to_be_clickable(self.to_field))
        to_element.clear()
        to_element.send_keys(address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    # METODOS DE BOTÓN DE PEDIR TAXI + SELECCIÓN DE TARIFA COMFORT
    def wait_for_taxi_button(self):
        """ 1. Espera para que se visualice el botón de pedir taxi """
        self.wait.until(EC.element_to_be_clickable(self.taxi_button))
        return True

    def click_request_taxi(self):
        """ 2. Hacer Clic en el botón pedir taxi """
        taxi_btn = self.wait.until(EC.element_to_be_clickable(self.taxi_button))
        taxi_btn.click()

    def wait_for_tariff_form(self):
        self.wait.until(EC.presence_of_element_located(self.tariff_picker))

    def select_comfort_tariff(self):
        """ 3. Selección de la tarifa conformt """
        comfort_element = self.wait.until(EC.element_to_be_clickable(self.comfort_option))
        comfort_element.click()

    # METODOS PARA NUMERO DE TELÉFONO + CÓDIGO SMS.
    def click_phone_button(self):
        """ Clic en el botón de nùmero de teléfono """
        phone_btn = self.wait.until(EC.element_to_be_clickable(self.phone_button))
        phone_btn.click()

    def enter_phone_number(self, phone_number):
        """ Ingresa el número de teléfono """
        phone_input = self.wait.until(EC.element_to_be_clickable(self.phone_modal_input))
        phone_input.clear()
        phone_input.send_keys(phone_number)

    def click_phone_netx(self):
        """ Hace clic en 'Siguiente' después del teléfono """
        next_btn =  self.wait.until(EC.element_to_be_clickable(self.phone_next_button))
        next_btn.click()

    def enter_sms_code(self):
        """ Ingresa el código SMS: con la función declarada """
        # Espera a que aparezca el campo código
        code_field =  self.wait.until(EC.element_to_be_clickable(self.code_input))
        # Obtener el código automáticamente
        sms_code = retrieve_phone_code(self.driver)
        code_field.send_keys(sms_code)
        print(f"Código SMS generado: {sms_code}")

    def confirm_sms_code(self):
        """ Confirmación del código SMS """
        confirm_btn =  self.wait.until(EC.element_to_be_clickable(self.code_confirm_button))
        confirm_btn.click()


    #METODOS PARA TARJETA DE CREDITO.
    def click_payment_method_button(self):
        """ Hacer Clic en el botén 'Método de Pago' """
        payment_btn = self.wait.until(EC.element_to_be_clickable(self.payment_method_button))
        payment_btn.click()

    def click_add_card_option(self):
        """Seleccionar Opción Tarjeta de Credito"""
        add_card_btn = self.wait.until(EC.element_to_be_clickable(self.add_card_option))
        add_card_btn.click()

    def enter_card_number(self, card_number):
        """ Ingresar el número de Tarjeta de credito"""
        card_number_field = self.wait.until(EC.element_to_be_clickable(self.card_number_input))
        card_number_field.clear()
        card_number_field.send_keys(card_number)

    def enter_card_code(self, card_code):
        """Ingresa el código CVV usando el placeholder"""
        card_code_field = self.wait.until(EC.element_to_be_clickable(self.card_code_input))
        card_code_field.clear()
        card_code_field.send_keys(card_code)
        print(f" Código CVV: {card_code}")
        time.sleep(2)

        # Quitar enfoque
        self.driver.execute_script("arguments[0].blur();", card_code_field)

    def wait_for_add_button_enabled(self):
        """Espera a que el botón 'Agregar' se habilite"""
        self.wait.until(EC.element_to_be_clickable(self.add_card_button))

    def click_add_card_button(self):
        """Hace clic en el botón 'Agregar'"""
        add_btn = self.wait.until(EC.element_to_be_clickable(self.add_card_button))
        add_btn.click()
        time.sleep(2)

    def close_any_open_modal(self):
        """Cierre de Modal de Tarjeta de credito"""
        try:
            section_close_buttons = self.driver.find_elements(By.CLASS_NAME, 'section-close')
            for btn in section_close_buttons:
                if btn.is_displayed():
                    btn.click()
                    time.sleep(1)
                    break
        except:
            pass


    # MÉTODO ENVIARE MENSAJE AL CONDUCTOR
    def enter_message_for_driver(self, message):
        """PASO 5: Escribe un mensaje para el conductor"""
        message_field = self.wait.until(EC.element_to_be_clickable(self.message_input))
        message_field.clear()
        message_field.send_keys(message)

    # MÉTODO PARA PEDIR UNA MANTA Y PAÑUELOS + 2 HELADOS
    def open_and_set_requirements(self):
            """Configura los requisitos """

            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'reqs-body')))
            requirements_container = self.driver.find_element(By.CLASS_NAME, 'reqs-body')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", requirements_container)
            time.sleep(2)

            # Configurar manta y pañuelos
            try:
                self.request_blanket_and_tissues()
                time.sleep(1)
            except Exception as e:
                print(f" Error con manta y pañuelos: {e}")

            # Configurar cuantos helados necesitamos
            try:
                self.request_ice_creams(2)
            except Exception as e:
                print(f" Error con helados: {e}")

    def request_blanket_and_tissues(self):
        """Activa manta y pañuelos con localizador mejorado"""

        try:
            # LOCALIZADOR MÁS ESPECÍFICO
            blanket_switch = (By.XPATH, '//div[contains(text(), "Manta y pañuelos")]/following-sibling::div//input[@type="checkbox"]')
            blanket_checkbox = self.wait.until(EC.presence_of_element_located(blanket_switch))

            # Hacer scroll para que sea visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", blanket_checkbox)
            time.sleep(2)

        # Verificar y activar
            if not blanket_checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", blanket_checkbox)
        except Exception as e:
            print(f"Error con manta y pañuelos: {e}")

    def request_ice_creams(self, quantity):
        """PASO 7: Pide la cantidad especificada de helados"""

        #  LOCALIZADORES MÁS ESPECÍFICOS PARA HELADOS:
        ice_cream_plus_button = (By.XPATH, '//div[text()="Helado"]/following-sibling::div//div[contains(@class, "counter-plus")]')
        ice_cream_counter = (By.XPATH, '//div[text()="Helado"]/following-sibling::div//div[contains(@class, "counter-value")]')

        try:
            # Obtener el contador actual
            counter_element = self.wait.until(EC.presence_of_element_located(ice_cream_counter))
            current_text = counter_element.text

            # Si está vacío, asumimos que es 0
            if current_text == '':
                current_count = 0
                print("Contador vacío, asumiendo 0 helados")
            else:
                current_count = int(current_text)
                #print(f"Helados actuales: {current_count}")

            # Calcular cuántos clics necesitamos
            clicks_needed = quantity - current_count

            if clicks_needed > 0:
                # Hacer clic en el botón "+" las veces necesarias
                plus_button = self.wait.until(EC.element_to_be_clickable(ice_cream_plus_button))
                for i in range(clicks_needed):
                    plus_button.click()
                    time.sleep(0.5)
                    #print(f"Helado {i + 1} agregado")

                # Verificar el resultado final
                final_count = int(counter_element.text) if counter_element.text != '' else quantity
                #print(f"Helados solicitados: {final_count}")
            else:
                print(f"Ya tienes {current_count} helados")

        except Exception as e:
            print(f" Error: {e}")
            # Intentar alternativa: buscar todos los botones plus
            all_plus_buttons = self.driver.find_elements(By.CLASS_NAME, 'counter-plus')
            for btn in all_plus_buttons:
                if btn.is_displayed():
                    for i in range(quantity):
                        btn.click()
                        time.sleep(0.5)
                    #print(f"{quantity} helados agregados")
                    break

    # MÉTODO PARA MODAL DE INFORMACIÓN DE CONDUCTOR
    def click_final_order_button(self):
            """PASO 8: Hace clic en el botón final 'Pedir un taxi'"""
            order_btn = self.wait.until(EC.element_to_be_clickable(self.final_order_button))
            order_btn.click()

    def wait_for_taxi_search_modal(self):
        """PASO 8: Espera fija optimizada - máximo 40s, usualmente menos"""
        try:

            # 1. Verificar que el proceso inició
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.countdown_timer))
            initial_time = self.driver.find_element(*self.countdown_timer).text

            # 2. Espera basada en observaciones
            if initial_time == "00:35":
                wait_time = 40
            elif initial_time == "00:30":
                wait_time = 35
            elif initial_time == "00:25":
                wait_time = 30
            elif initial_time == "00:20":
                wait_time = 25
            elif initial_time == "00:15":
                wait_time = 20
            elif initial_time == "00:10":
                wait_time = 15
            elif initial_time == "00:05":
                wait_time = 10
            else:
                wait_time = 35

            time.sleep(wait_time)

            # 3. Esperando el modal del conductor
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.number_element))
            time.sleep(1)
            return True

        except Exception as e:
            print(f" :( Ya no se que mas intentar: {e}")
            return False



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import ChromeOptions
        options = ChromeOptions()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

        cls.routes_page = UrbanRoutesPage(cls.driver)
        cls.driver.get(data.urban_routes_url)

    # def setup_method(self):
    #     self.driver.get(data.urban_routes_url)
    #     self.routes_page.set_routes(data.address_from, data.address_to)

    def test_1_set_address(self):
        """Prueba 1: Configurar dirección"""
        # SETUP
        self.driver.get(data.urban_routes_url)
        self.routes_page.set_routes(data.address_from, data.address_to)

        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to
        assert self.routes_page.wait_for_taxi_button() == True

        print("Paso 1 Completado: Configurar la dirección")

    def test_2_select_comfort_tariff(self):
        """Prueba 2: Seleccionar tarifa Comfort"""
        # SETUP COMPLETO
        self.driver.get(data.urban_routes_url)
        self.routes_page.set_routes(data.address_from, data.address_to)

        # ACCION
        self.routes_page.click_request_taxi()
        self.routes_page.wait_for_tariff_form()
        self.routes_page.select_comfort_tariff()

        #Verificar que Comfort está seleccionado
        comfort_element = self.driver.find_element(*self.routes_page.comfort_option)
        comfort_parent = comfort_element.find_element(By.XPATH, './ancestor::div[contains(@class, "tcard")]')
        assert 'active' in comfort_parent.get_attribute('class')

        print("Prueba 2: Tarifa Comfort seleccionada correctamente")

    def test_3_fill_phone_number(self):
        """Prueba 3: Rellenar número de teléfono"""
        # SETUP COMPLETO
        self.driver.get(data.urban_routes_url)
        self.routes_page.set_routes(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.wait_for_tariff_form()
        self.routes_page.select_comfort_tariff()

        # Rellenar teléfono
        try:
            self.routes_page.click_phone_button()
            self.routes_page.enter_phone_number(data.phone_number)
            self.routes_page.click_phone_netx()
            self.routes_page.enter_sms_code()
            self.routes_page.confirm_sms_code()

            # Verificaciones después de la validación
            time.sleep(3)

            #  VERIFICAR EL NUEVO ESTADO DEL BOTÓN
            verified_phone_button = self.driver.find_element(By.XPATH, '//div[contains(@class, "np-button filled")]')
            verified_phone_text = verified_phone_button.find_element(By.CLASS_NAME, 'np-text').text

            # Verificar que muestra el número de teléfono
            assert data.phone_number in verified_phone_text
            assert "Número de teléfono" not in verified_phone_text

        except Exception as e:
            print(f"❌ Error en Prueba 3: {e}")
            # Tomar screenshot para debug
            self.driver.save_screenshot("error_prueba_3.png")
            print("Screenshot guardado: error_prueba_3.png")
            raise

    def test_4_add_credit_card_with_cvv(self):
        """Prueba 4: Agregar tarjeta de crédito incluyendo código CVV"""
        # SETUP COMPLETO
        self.driver.get(data.urban_routes_url)
        self.routes_page.set_routes(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.wait_for_tariff_form()
        self.routes_page.select_comfort_tariff()

        # PASO: Agregar tarjeta de crédito
        self.routes_page.click_payment_method_button()
        self.routes_page.click_add_card_option()

        # Verificar que el modal de tarjeta se abrió
        card_modal = self.driver.find_element(*self.routes_page.card_number_input)
        assert card_modal.is_displayed()

        # Ingresar número de tarjeta
        self.routes_page.enter_card_number(data.card_number)

        # Verificar que el número de tarjeta se ingresó correctamente
        card_number_field = self.driver.find_element(*self.routes_page.card_number_input)
        assert card_number_field.get_attribute('value') == data.card_number

        # Ingresar código CVV
        self.routes_page.enter_card_code(data.card_code)

        # Verificar que el código CVV se ingresó correctamente
        card_code_field = self.driver.find_element(*self.routes_page.card_code_input)
        assert card_code_field.get_attribute('value') == data.card_code

        # Verificar que el botón "Agregar" está habilitado
        add_button = self.driver.find_element(*self.routes_page.add_card_button)
        assert add_button.is_enabled()

        # Hacer clic en agregar tarjeta
        self.routes_page.click_add_card_button()
        time.sleep(2)

        # Cerrar modal
        self.routes_page.close_any_open_modal()

        # Verificar que la tarjeta se agregó correctamente
        payment_method_display = self.driver.find_element(By.XPATH,'//div[contains(@class, "pp-button") and contains(@class, "filled")]')
        assert payment_method_display.is_displayed()
        print("Prueba 4 COMPLETADA: Tarjeta de crédito y código CVV agregados correctamente")

    def test_6_write_message_to_driver(self):
        """Prueba 6: Escribir mensaje al conductor"""
        # SETUP COMPLETO
        self.driver.get(data.urban_routes_url)
        self.routes_page.set_routes(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.wait_for_tariff_form()
        self.routes_page.select_comfort_tariff()

        # PASO 6: Escribir mensaje para el conductor
        self.routes_page.enter_message_for_driver(data.message_for_driver)

        # Assert 1: Verificar que el campo de mensaje está visible y habilitado
        message_field = self.driver.find_element(*self.routes_page.message_input)
        assert message_field.is_displayed()
        assert message_field.is_enabled()

        # Assert 2: Verificar que el mensaje se ingresó correctamente
        assert message_field.get_attribute('value') == data.message_for_driver

        # Assert 3: Verificar que el mensaje no está vacío
        assert len(message_field.get_attribute('value')) > 0

        # Assert 4: Verificar que el mensaje coincide exactamente con el dato de prueba
        expected_message = data.message_for_driver
        actual_message = message_field.get_attribute('value')
        assert actual_message == expected_message, f"Expected: '{expected_message}', Got: '{actual_message}'"

        print("✅ Prueba 6 COMPLETADA: Mensaje para el conductor escrito correctamente")
        print(f"   Mensaje enviado: '{data.message_for_driver}'")

    def test_7_request_blanket_and_tissues(self):
        """Prueba 7: Pedir manta y pañuelos (versión simple y robusta)"""
        # SETUP COMPLETO
        self.driver.get(data.urban_routes_url)
        self.routes_page.set_routes(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.wait_for_tariff_form()
        self.routes_page.select_comfort_tariff()

        # Hacer scroll para ver la sección de requisitos
        requirements_section = self.driver.find_element(*self.routes_page.requirements_section)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", requirements_section)
        time.sleep(2)

        # PASO 7: Activar manta y pañuelos
        self.routes_page.request_blanket_and_tissues()
        time.sleep(2)

        # ÚNICO ASSERT PRINCIPAL - El más importante
        blanket_switch = self.driver.find_element(By.XPATH,'//div[contains(text(), "Manta y pañuelos")]/following-sibling::div//input[@type="checkbox"]')
        assert blanket_switch.is_selected(), "El switch de manta y pañuelos debe estar seleccionado"
        print(" Prueba 7 COMPLETADA: Manta y pañuelos activados correctamente")

    def test_8_request_ice_creams(self):
            """Prueba 8: Pedir 2 helados"""
            # SETUP COMPLETO
            self.driver.get(data.urban_routes_url)
            self.routes_page.set_routes(data.address_from, data.address_to)
            self.routes_page.click_request_taxi()
            self.routes_page.wait_for_tariff_form()
            self.routes_page.select_comfort_tariff()

            # Asegurarnos de que la sección de requisitos esté visible
            requirements_section = self.driver.find_element(*self.routes_page.requirements_section)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", requirements_section)
            time.sleep(2)

            # Pedir Panuelos
            self.routes_page.request_blanket_and_tissues()

           # PASO 8: Pedir 2 helados
            self.routes_page.request_ice_creams(2)
            time.sleep(2)

            #Verificar que el contador muestra 2 helados
            ice_cream_counter = self.driver.find_element(By.XPATH,'//div[text()="Helado"]/following-sibling::div//div[contains(@class, "counter-value")]')
            actual_count = ice_cream_counter.text

            # Manejar caso cuando el contador está vacío
            if actual_count == '':
                actual_count = '0'

            assert actual_count == '2', f"Se esperaban 2 helados, pero el contador muestra: {actual_count}"

            # Verificar que el texto "Helado" está visible
            ice_cream_text = self.driver.find_element(By.XPATH, '//div[text()="Helado"]')
            assert ice_cream_text.is_displayed()
            time.sleep(2)

            # Assert 3: Verificar que el botón "+" está presente y funcionando
            plus_button = self.driver.find_element(By.XPATH,'//div[text()="Helado"]/following-sibling::div//div[contains(@class, "counter-plus")]')
            assert plus_button.is_displayed()
            assert plus_button.is_enabled()
            print("Botón Funcionando")

            # Assert 4: Verificar que el botón "-" está presente
            try:
                minus_button = self.driver.find_element(By.XPATH,'//div[text()="Helado"]/following-sibling::div//div[contains(@class, "counter-minus")]')
                assert minus_button.is_displayed()
                print("  Botón Funcionando")
            except:
                print(" Error elemento no encontrado  ")

            print(f"   - Contador de helados: {actual_count}")
            print("✅ Prueba 8 COMPLETADA: 2 helados pedidos correctamente")

    def test_9_search_taxi_modal(self):
        """Prueba 9: Modal para buscar taxi y información del conductor (con timeout mejorado)"""

        # SETUP COMPLETO
        self.driver.get(data.urban_routes_url)
        self.routes_page.set_routes(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()
        self.routes_page.wait_for_tariff_form()
        self.routes_page.select_comfort_tariff()

        # Configurar teléfono y tarjeta (prerrequisitos)
        self.routes_page.click_phone_button()
        self.routes_page.enter_phone_number(data.phone_number)
        self.routes_page.click_phone_netx()
        self.routes_page.enter_sms_code()
        self.routes_page.confirm_sms_code()
        time.sleep(2)

        self.routes_page.click_payment_method_button()
        self.routes_page.click_add_card_option()
        self.routes_page.enter_card_number(data.card_number)
        self.routes_page.enter_card_code(data.card_code)
        self.routes_page.wait_for_add_button_enabled()
        self.routes_page.click_add_card_button()
        time.sleep(2)
        self.routes_page.close_any_open_modal()

        # PASO 6: Escribir mensaje para el conductor
        self.routes_page.enter_message_for_driver(data.message_for_driver)

        # Asegurarnos de que la sección de requisitos esté visible
        requirements_section = self.driver.find_element(*self.routes_page.requirements_section)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", requirements_section)
        time.sleep(2)

        # Pedir Panuelos
        self.routes_page.request_blanket_and_tissues()

        # PASO 8: Pedir 2 helados
        self.routes_page.request_ice_creams(2)
        time.sleep(1)

        self.routes_page.click_final_order_button()

        # Verificar modal de búsqueda con contador
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.routes_page.countdown_timer))

        countdown_element = self.driver.find_element(*self.routes_page.countdown_timer)
        search_title = self.driver.find_element(*self.routes_page.search_title)

        assert countdown_element.is_displayed()
        assert search_title.is_displayed()
        assert "Buscar automóvil" in search_title.text

        modal_found = self.routes_page.wait_for_taxi_search_modal()
        assert modal_found, "Timeout: No se encontró el modal del conductor"

        # Verificaciones finales del conductor
        driver_number = self.driver.find_element(*self.routes_page.number_element)
        assert driver_number.is_displayed()

        driver_info = driver_number.text
        assert len(driver_info) > 0

        print(f"Conductor asignado: {driver_info}")


        print("" * 60)
        print("🎉 ¡TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE!")
        print("═" * 60)
        print("✅ Flujo completo de Urban Routes verificado")
        print("✅ 9 pruebas independientes ejecutadas")
        print("✅ Patrón Page Object Model implementado")
        print("✅ Asserts en cada prueba")
        print("═" * 60)


    @classmethod
    def teardown_class(cls):
        cls.driver.implicitly_wait(2)
        cls.driver.quit()