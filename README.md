# Portfolio Rebalancer – Django REST Demo

## 📌 Descripción general

Este proyecto es un **ejemplo mínimo pero realista** de un módulo de gestión de portafolios para una aplicación de inversiones personales.

El objetivo principal es exponer un **endpoint REST** que, dado un portafolio con:

* acciones actuales (holdings)
* precios de mercado
* una asignación objetivo (target allocation)

calcula **qué acciones comprar y cuáles vender** para rebalancear el portafolio.

El proyecto fue construido usando:

* **Python 3**
* **Django**
* **Django REST Framework**
* **SQLite**
* Servidor de desarrollo estándar de Django

---

## 🧠 Decisiones de diseño clave

### 1. Acciones como enteros positivos

* No se permiten fracciones de acciones
* Todas las operaciones de compra/venta trabajan con **enteros positivos**
* Esto refleja mercados reales donde no siempre existen fractional shares

### 2. Precisión financiera

* Todo el dinero se maneja con `Decimal`
* Se evita completamente el uso de `float` para cálculos monetarios

### 3. Cash remainder explícito

Debido a que las acciones son enteras:

* No siempre es posible alcanzar exactamente la asignación objetivo
* El dinero que no se puede asignar se retorna como `cash_remainder`

Esto es **correcto y esperado**, no un error.

### 4. Separación de responsabilidades

* **models.py** → persistencia
* **services.py** → lógica de negocio (rebalanceo)
* **views.py** → capa HTTP

---

## 🧮 Algoritmo de rebalanceo (resumen)

1. Calcular el valor total actual del portafolio
2. Calcular el valor objetivo por acción según el porcentaje
3. Comparar valor actual vs valor objetivo
4. Convertir la diferencia en **acciones enteras**
5. Acumular el dinero no asignable como `cash_remainder`

### Invariante importante

```text
Dinero gastado ≤ Valor total del portafolio
```

Nunca se gasta más dinero del disponible.

---

## 🔌 Endpoint disponible

### Rebalancear portafolio

**POST**

```
/api/portfolio/<portfolio_id>/rebalance/
```

### Ejemplo de respuesta

```json
{
  "total_value": "4000.00",
  "cash_remainder": "100.00",
  "actions": [
    {
      "stock": "META",
      "action": "SELL",
      "shares": 4
    },
    {
      "stock": "AAPL",
      "action": "BUY",
      "shares": 7
    }
  ]
}
```

---

## 🧪 Datos iniciales

El proyecto incluye una **migración con datos de prueba** que crea:

* Stocks: `META`, `AAPL`
* Un portafolio de prueba
* Holdings desbalanceados
* Target allocation 40% / 60%

Esto permite probar el endpoint inmediatamente tras ejecutar:

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🧑‍💻 Uso de LLM (ChatGPT)

### Declaración explícita

Este proyecto **sí utilizó un LLM (ChatGPT)** para asistir en:

* Diseño del algoritmo de rebalanceo
* Decisiones de precisión financiera
* Estructura del proyecto Django
* Documentación

Esto está permitido explícitamente por el enunciado del ejercicio.

---

## 📜 Historial de consultas realizadas al LLM

Las siguientes consultas fueron realizadas durante el desarrollo, todas dentro de **una única conversación**:

1. *"Create a minimal django project with django-rest framework, sqllite and default django lightweight web server that has one endpoint to rebalance the stocks"*
2. *"change PortfolioRebalancer classso it will have decimal base precision, and it will consider one return value for the money it couldn't assign correctly"*
3. *"generate migration with initial data to test endpoint"*
4. *"generar migracion con datos iniciales para probar endpoint"*
5. *"considerar que la cantidad de acciones es entero positivo"*
6. *"crear readme con documentacion, y con las consultas que se hicieron al LLM"*

No se usaron prompts externos, herramientas adicionales ni conversaciones separadas.
