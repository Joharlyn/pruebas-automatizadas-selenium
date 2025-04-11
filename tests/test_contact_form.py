import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains

# Directorio para guardar capturas de pantalla
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Función para tomar capturas de pantalla
def take_screenshot(driver, name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    driver.save_screenshot(filepath)
    return filepath

# Configuración inicial
@pytest.fixture
def driver():
    # Forzamos el path correcto al ejecutable .exe
    driver_path = ChromeDriverManager().install()
    if not driver_path.endswith("chromedriver.exe"):
        driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")

    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Descomenta si no quieres ver el navegador
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


# Ruta al archivo HTML local
def get_html_path():
    return "file://" + os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "index.html"))

# Tests
def test_required_fields_validation(driver):
    """Test que valida que los campos obligatorios sean validados correctamente"""
    driver.get(get_html_path())
    take_screenshot(driver, "initial_form")
    
    # Intentar enviar el formulario sin completar campos
    submit_button = driver.find_element(By.TAG_NAME, "button")
    submit_button.click()
    time.sleep(1)
    take_screenshot(driver, "validation_errors")
    
    # Verificar mensajes de error para campos obligatorios
    name_error = driver.find_element(By.ID, "name-error").text
    email_error = driver.find_element(By.ID, "email-error").text
    subject_error = driver.find_element(By.ID, "subject-error").text
    message_error = driver.find_element(By.ID, "message-error").text
    terms_error = driver.find_element(By.ID, "terms-error").text
    
    assert name_error == "El nombre es obligatorio"
    assert email_error == "El correo electrónico es obligatorio"
    assert subject_error == "Por favor, selecciona un asunto"
    assert message_error == "El mensaje es obligatorio"
    assert terms_error == "Debes aceptar los términos y condiciones"

def test_email_format_validation(driver):
    """Test que valida el formato de correo electrónico"""
    driver.get(get_html_path())
    
    # Completar email con formato incorrecto
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("correo_invalido")
    
    # Simular que el usuario sale del campo con ActionChains
    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element(By.ID, "name")).click().perform()
    time.sleep(1)
    take_screenshot(driver, "email_invalid_format")
    
    # Verificar mensaje de error
    email_error = driver.find_element(By.ID, "email-error").text
    assert "Por favor, introduce un correo electrónico válido" in email_error
    
    # Corregir el formato del email
    email_input.clear()
    email_input.send_keys("correo_valido@dominio.com")
    driver.find_element(By.ID, "name").click()
    time.sleep(1)
    take_screenshot(driver, "email_valid_format")
    
    # Verificar que el mensaje de error desaparece
    email_error = driver.find_element(By.ID, "email-error").text
    assert email_error == ""

def test_minimum_length_validation(driver):
    """Test que valida la longitud mínima en campos de texto"""
    driver.get(get_html_path())
    
    # Probar nombre corto
    name_input = driver.find_element(By.ID, "name")
    name_input.send_keys("AB")
    
    # Hacer clic en otro campo para activar la validación
    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element(By.ID, "email")).click().perform()
    time.sleep(1)
    take_screenshot(driver, "name_too_short")
    
    # Verificar mensaje de error
    name_error = driver.find_element(By.ID, "name-error").text
    assert "El nombre debe tener al menos 3 caracteres" in name_error
    
    # Probar mensaje corto
    message_input = driver.find_element(By.ID, "message")
    message_input.send_keys("Corto")
    
    # Hacer clic en otro campo para activar la validación
    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element(By.ID, "email")).click().perform()
    time.sleep(1)
    take_screenshot(driver, "message_too_short")
    
    # Verificar mensaje de error
    message_error = driver.find_element(By.ID, "message-error").text
    assert "El mensaje debe tener al menos 10 caracteres" in message_error

def test_successful_form_submission(driver):
    """Test que valida el envío exitoso del formulario"""
    driver.get(get_html_path())
    
    # Completar todos los campos correctamente
    driver.find_element(By.ID, "name").send_keys("Juan Pérez")
    driver.find_element(By.ID, "email").send_keys("juan@ejemplo.com")
    driver.find_element(By.ID, "phone").send_keys("123456789")
    
    # Seleccionar asunto
    subject_select = driver.find_element(By.ID, "subject")
    subject_select.click()
    driver.find_element(By.CSS_SELECTOR, "option[value='consulta']").click()
    
    # Completar mensaje
    driver.find_element(By.ID, "message").send_keys("Este es un mensaje de prueba para validar el funcionamiento del formulario.")
    
    # Aceptar términos
    driver.find_element(By.ID, "terms").click()
    
    time.sleep(1)
    take_screenshot(driver, "form_filled")
    
    # Enviar formulario
    submit_button = driver.find_element(By.TAG_NAME, "button")
    submit_button.click()
    time.sleep(1)
    take_screenshot(driver, "form_submitted")
    
    # Verificar mensaje de éxito
    success_message = driver.find_element(By.ID, "success-message")
    assert success_message.is_displayed()
    assert "¡Mensaje enviado correctamente!" in success_message.text
    
    # Probar botón para enviar nuevo mensaje
    new_message_button = driver.find_element(By.ID, "new-message")
    new_message_button.click()
    time.sleep(1)
    take_screenshot(driver, "form_reset")
    
    # Verificar que el formulario está visible y vacío
    form = driver.find_element(By.ID, "contact-form")
    assert form.is_displayed()
    assert driver.find_element(By.ID, "name").get_attribute("value") == ""

def test_phone_format_validation(driver):
    """Test que valida el formato del número telefónico"""
    driver.get(get_html_path())
    
    # Probar teléfono con formato incorrecto (letras)
    phone_input = driver.find_element(By.ID, "phone")
    phone_input.send_keys("123abc456")
    
    # Hacer clic en otro campo para activar la validación
    actions = ActionChains(driver)
    actions.move_to_element(driver.find_element(By.ID, "name")).click().perform()
    time.sleep(1)
    take_screenshot(driver, "phone_invalid_format")
    
    # Verificar mensaje de error
    phone_error = driver.find_element(By.ID, "phone-error").text
    assert "Introduce un número de teléfono válido" in phone_error
    
    # Probar teléfono con pocos dígitos
    phone_input.clear()
    phone_input.send_keys("12345")
    driver.find_element(By.ID, "name").click()  # Hacer clic en otro campo
    time.sleep(1)
    take_screenshot(driver, "phone_too_short")
    
    # Verificar mensaje de error
    phone_error = driver.find_element(By.ID, "phone-error").text
    assert "Introduce un número de teléfono válido" in phone_error
    
    # Probar con teléfono válido
    phone_input.clear()
    phone_input.send_keys("123456789")
    driver.find_element(By.ID, "name").click()  # Hacer clic en otro campo
    time.sleep(1)
    take_screenshot(driver, "phone_valid")
    
    # Verificar que no hay mensaje de error
    phone_error = driver.find_element(By.ID, "phone-error").text
    assert phone_error == ""
    
    # Probar envío con campo teléfono vacío (opcional)
    phone_input.clear()
    
    # Completar los demás campos obligatorios
    driver.find_element(By.ID, "name").send_keys("Juan Pérez")
    driver.find_element(By.ID, "email").send_keys("juan@ejemplo.com")
    
    # Seleccionar asunto
    subject_select = driver.find_element(By.ID, "subject")
    subject_select.click()
    driver.find_element(By.CSS_SELECTOR, "option[value='consulta']").click()
    
    # Completar mensaje
    driver.find_element(By.ID, "message").send_keys("Este es un mensaje de prueba para validar el funcionamiento del formulario.")
    
    # Aceptar términos
    driver.find_element(By.ID, "terms").click()
    
    time.sleep(1)
    take_screenshot(driver, "form_without_phone")
    
    # Enviar formulario
    submit_button = driver.find_element(By.TAG_NAME, "button")
    submit_button.click()
    time.sleep(1)
    take_screenshot(driver, "form_without_phone_submitted")
    
    # Verificar mensaje de éxito (el formulario debería enviarse sin teléfono)
    success_message = driver.find_element(By.ID, "success-message")
    assert success_message.is_displayed()