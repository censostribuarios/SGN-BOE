# 🚀 Guía de puesta en marcha - Gestoría SGN
## Motor de búsqueda BOE

---

## ¿Qué hace este sistema?

Cuando un cliente introduce su matrícula en el formulario web,
este motor busca automáticamente en:

- **Tablón Edictal Único** (notificaciones administrativas, multas DGT, Hacienda...)
- **Tablón Edictal Judicial** (procedimientos judiciales)

Y devuelve en segundos uno de los dos mensajes acordados.

---

## Paso 1 — Crear cuenta en GitHub (gratis)

1. Ir a https://github.com
2. Registrarse con el email de la gestoría
3. Crear un repositorio nuevo llamado `sgn-boe`
4. Subir los archivos: `boe_motor.py`, `api.py`, `requirements.txt`

---

## Paso 2 — Desplegar en Render (gratis)

Render.com permite alojar la API sin coste para uso bajo.

1. Ir a https://render.com y crear cuenta
2. Nuevo servicio → "Web Service"
3. Conectar con el repositorio de GitHub
4. Configurar:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python api.py`
5. Render da una URL pública del tipo: `https://sgn-boe.onrender.com`

---

## Paso 3 — Conectar el formulario web con la API

En el formulario HTML, cambiar la URL de la API:

```javascript
const API_URL = "https://sgn-boe.onrender.com/consultar";
```

---

## Paso 4 — Probar

Abrir el formulario, introducir una matrícula y comprobar que:
- Si no hay resultados → mensaje verde
- Si hay resultados → mensaje rojo con aviso de contacto

---

## Coste total

| Concepto | Coste |
|---|---|
| GitHub | Gratis |
| Render (plan gratuito) | Gratis |
| Dominio (opcional) | ~10€/año |
| **Total para arrancar** | **0€** |

---

## Nota importante

El plan gratuito de Render "duerme" el servidor si no recibe
peticiones durante 15 minutos. La primera consulta del día
puede tardar 30-60 segundos en responder mientras "despierta".
Para evitarlo, el plan de pago de Render cuesta ~7€/mes.

---

## Soporte

Cualquier duda o error, consultar con Claude en claude.ai
describiendo el mensaje de error exacto.
