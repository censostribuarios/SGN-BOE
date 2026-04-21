import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
SIN_RESULTADOS = "No se han encontrado documentos"

def _buscar_teu(termino):
    try:
        fecha = (datetime.now() - timedelta(days=90)).strftime("%d/%m/%Y")
        params = {"dato": termino, "fecha_desde": fecha, "fecha_hasta": "", "page_hits": "10", "origen": "N", "lang": "es", "searchType": "anuncio_notif"}
        url = "https://www.boe.es/notificaciones/notificaciones.php?" + urlencode(params)
        resp = requests.get(url, headers=HEADERS, timeout=15)
        return SIN_RESULTADOS.lower() not in resp.text.lower() and len(resp.text) > 500
    except:
        return False

def _buscar_teju(termino):
    try:
        fecha = (datetime.now() - timedelta(days=120)).strftime("%d/%m/%Y")
        params = {"texto": termino, "fecha_desde": fecha, "fecha_hasta": "", "page_hits": "10", "origen": "N", "lang": "es", "searchType": "edicto_judicial"}
        url = "https://www.boe.es/buscar/edictos_judiciales.php?" + urlencode(params)
        resp = requests.get(url, headers=HEADERS, timeout=15)
        return SIN_RESULTADOS.lower() not in resp.text.lower() and len(resp.text) > 500
    except:
        return False

def consultar(matricula: str, nif: str = "") -> dict:
    incidencias = []
    if _buscar_teu(matricula.upper()):
        incidencias.append("Tablón Edictal Único (BOE)")
    if nif and "Tablón Edictal Único (BOE)" not in incidencias:
        if _buscar_teu(nif.upper()):
            incidencias.append("Tablón Edictal Único (BOE)")
    if _buscar_teju(matricula.upper()):
        incidencias.append("Tablón Edictal Judicial (BOE)")
    if nif and "Tablón Edictal Judicial (BOE)" not in incidencias:
        if _buscar_teju(nif.upper()):
            incidencias.append("Tablón Edictal Judicial (BOE)")
    return {"incidencia": len(incidencias) > 0, "fuentes": incidencias, "matricula": matricula.upper(), "nif": nif.upper() if nif else ""}
