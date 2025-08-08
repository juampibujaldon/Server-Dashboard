# Diseño-de-Sistemas
# 🖥️ Dashboard de Monitoreo de Servidores

## 📌 Descripción
Aplicación cliente-servidor para **monitorear métricas en tiempo real** (carga de CPU, temperatura, uso de disco) de múltiples servidores.

Cada equipo monitoreado tiene un **agente** que envía periódicamente sus métricas al **servidor central**.  
El backend, desarrollado en **Flask**, almacena la información en una **base de datos SQL** y expone una API para que un dashboard muestre gráficas y estadísticas en tiempo real.

---

## 🚀 Tecnologías utilizadas
- **Python 3.13.6**
- **Flask**
- **SQLAlchemy**
- **MongoDB**
- **Docker & Docker Compose**
- **Grafana o D3.js** → Visualización de métricas (opcional).

---
