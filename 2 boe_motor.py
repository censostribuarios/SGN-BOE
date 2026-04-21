"""
Motor de búsqueda BOE - Gestoría SGN
Consulta el Tablón Edictal Único y el Tablón Edictal Judicial del BOE
por matrícula y/o NIF y devuelve si hay o no incidencias.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# URLs de búsqueda
URL_TEU  = "https://www.boe.es/notificaciones/notificaciones.php"   # Tablón Edictal Único
URL_TEJU = "https://www.boe.es/buscar/edictos_judiciales.php"       # Tablón Edictal Judicial

# Frase que aparece cuando no hay resultados
SIN_RESULTADOS = "No se han encontrado documentos que satisfagan sus criterios de búsqueda"


def _crear_driver():
    """Crea y devuelve un driver de Chrome en modo headless (sin ventana)."""
    opciones = Options()
    opciones.add_argument("--headless")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    opciones.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opciones
    )
    return driver


def _buscar_en_url(driver, url, termino):
    """
    Abre la URL, introduce el término de búsqueda y devuelve:
    - True  si se encontró algún resultado
    - False si no hay resultados
    """
    wait = WebDriverWait(driver, 20)
    try:
        driver.get(url)
        # Buscar el campo de texto principal (dato o texto según la página)
        campo = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name='dato'], input[name='texto'], input[type='text']")
        ))
        campo.clear()
        campo.send_keys(termino)
        campo.send_keys(Keys.ENTER)
        time.sleep(4)  # Dar tiempo a que cargue la respuesta

        cuerpo = driver.find_element(By.TAG_NAME, "body").text
        hay_resultados = SIN_RESULTADOS.lower() not in cuerpo.lower()
        return hay_resultados

    except Exception as e:
        print(f"[ERROR] Al buscar en {url}: {e}")
        return False  # En caso de error, asumimos sin resultados (conservador)


def consultar(matricula: str, nif: str = "") -> dict:
    """
    Función principal. Recibe matrícula y NIF opcionales.
    Devuelve un diccionario con:
      - incidencia (bool): True si se encontró algo
      - fuentes (list): lista de fuentes donde apareció
    """
    driver = _crear_driver()
    incidencias = []

    try:
        # Construir término de búsqueda combinado si hay NIF
        if nif:
            termino = f"{matricula} .O {nif}"
        else:
            termino = matricula

        # Búsqueda 1: Tablón Edictal Único (administrativo)
        if _buscar_en_url(driver, URL_TEU, termino):
            incidencias.append("Tablón Edictal Único (BOE)")

        # Búsqueda 2: Tablón Edictal Judicial
        if _buscar_en_url(driver, URL_TEJU, termino):
            incidencias.append("Tablón Edictal Judicial (BOE)")

    finally:
        driver.quit()

    return {
        "incidencia": len(incidencias) > 0,
        "fuentes": incidencias,
        "matricula": matricula.upper(),
        "nif": nif.upper() if nif else ""
    }


# --- Uso directo desde línea de comandos (para pruebas) ---
if __name__ == "__main__":
    import sys
    mat = sys.argv[1] if len(sys.argv) > 1 else "1234ABC"
    nif = sys.argv[2] if len(sys.argv) > 2 else ""
    print(f"\nConsultando matrícula: {mat}" + (f" / NIF: {nif}" if nif else ""))
    resultado = consultar(mat, nif)
    if resultado["incidencia"]:
        print(f"⚠️  INCIDENCIA ENCONTRADA en: {', '.join(resultado['fuentes'])}")
    else:
        print("✅  Sin incidencias encontradas")
