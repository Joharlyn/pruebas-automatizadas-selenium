import pytest
from datetime import datetime
import os

# Configuración del reporte HTML
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Crear directorio para reportes si no existe
    report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(report_dir, exist_ok=True)
    
    # Nombre del reporte con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(report_dir, f"report_{timestamp}.html")
    
    # Configurar la opción de reporte HTML
    config.option.htmlpath = report_path
    config.option.self_contained_html = True

# Función para añadir capturas de pantalla a los reportes de error
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Si la prueba falló, intentar adjuntar una captura de pantalla al reporte
    if report.when == "call" and report.failed:
        try:
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
                # Crear directorio para capturas de error si no existe
                screenshot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "error_screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                
                # Tomar captura de pantalla
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(screenshot_dir, f"error_{item.name}_{timestamp}.png")
                driver.save_screenshot(screenshot_path)
                
                # Adjuntar al reporte
                if hasattr(report, "extras"):
                    report.extras.append(pytest.html.extras.image(screenshot_path))
                else:
                    report.extras = [pytest.html.extras.image(screenshot_path)]
        except:
            pass