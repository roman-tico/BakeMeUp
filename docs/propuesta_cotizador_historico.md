# Propuesta y Especificación Técnica: Sistema Web de Cotización, Histórico, KDS y Proveedores
**Proyecto:** Bake Me Up  
**Líder de Proyecto:** Carlos Ruiz (Woody) / MexaDev  
**Lead Técnico:** Lalo  
**Cliente:** Sofia Gavito Alarcón  
**Versión:** 2.6 - Catálogo de Proveedores, KDS Cocina y Flujo Operativo  

---

## 1. Resumen Ejecutivo
Migración integral del proceso de cotización y gestión de pedidos desde hojas de cálculo de Excel/Exportek hacia la plataforma web de **Bake Me Up**.
* **Problema:** Desajustes de rentabilidad por alza en insumos (ej. huevo), falta de estandarización en precios, descontrol de comandas en papel y dispersión de contactos de proveedores.
* **Solución:** Motor dinámico de costos en cascada, cotizador estandarizado en < 60 segundos, catálogo histórico con búsqueda visual, KDS (Kitchen Display System) en iPad para taller 100% libre de papel y directorio ágil de proveedores con botón a WhatsApp.

---

## 2. Módulos y Arquitectura Técnica

### Módulo A: Matriz Dinámica de Materias Primas e Insumos
* Catálogo de materias primas con unidad de medida y precio de compra vigente.
* Actualización en cascada sobre las fórmulas base.
* **Regla de Costeo Base:** El pan se costea con el insumo de mayor valor para proteger el margen sin importar el sabor elegido por el cliente.

### Módulo B: Motor Web de Cotización Rápida
* Formulario ágil para mostrador / WhatsApp.
* Parámetros: porciones, estilo (*Vintage*, *Domo*, *Clásico*, *Pisos*), sabores y adicionales (flores, impresiones comestibles, papel, MDF).
* Cálculo automático de betún y mano de obra por estilo.

### Módulo C: Histórico y Búsqueda Visual
* Búsqueda por descripción, etiquetas y por fotografía de referencia.
* Comparador: costo histórico original vs. costo recalculado a precios de hoy.

### Módulo D: Flujo de Pedidos y KDS de Cocina (iPad)
* **Vista Admin (Dueñas):** Visibilidad financiera total (costo, anticipo, saldo y estatus). Control de entrega exclusivo para marcar `Entregado`.
* **Vista KDS Cocina (iPad):** Sesión genérica permanente, 100% libre de papel.
* **Seguridad (Data Masking en Backend):** La API de cocina **NO** devuelve campos de dinero (`total_price`, `deposit`, `balance_due`, etc.).
* **3 Estados Operativos:** `Pendiente`, `En vitrina / refri` y `Entregado`.

### Módulo E: Catálogo y Directorio de Proveedores
* **Campos:** Nombre / Negocio, contacto, teléfono, categoría (*Lácteos, Huevo, Harinas, MDF, Flores, etc.*) y notas de entrega/visita.
* **Botón 1-Clic a WhatsApp:** Enlace directo (`https://wa.me/...`) para chat inmediato de pedido.
* **Acceso:** Consulta disponible para todo el equipo (taller, mostrador y admin).
* **Gestión y Soft Delete:** Altas, bajas y edición restringidas a Admin. Borrado lógico (`is_active = false`) para preservar integridad histórica de compras.

---

## 3. Flujo Operativo Paso a Paso (Happy Path)
1. **Paso 1: Solicitud y Captura:** Mostrador carga fecha/hora, personas, estilo y foto de referencia en el cotizador web.
2. **Paso 2: Generación de Precio:** El motor calcula en < 1 segundo betún, horas de trabajo y precio oficial.
3. **Paso 3: Confirmación y Anticipo:** Cliente acepta, dueña cobra anticipo (50%), registra método de pago y el sistema agenda el pedido.
4. **Paso 4: Notificación al Taller:** Aparece en el iPad de cocina en estado `Pendiente` (sin datos de dinero).
5. **Paso 5: Elaboración:** Pastelero hornea, rellena, betuna y decora siguiendo la ficha técnica.
6. **Paso 6: Listo en Frío:** Pastelero cambia tarjeta a `En vitrina / refri`. Se notifica a las dueñas.
7. **Paso 7: Llegada del Cliente:** Cliente llega a mostrador, dueña revisa saldo pendiente y cobra liquidación.
8. **Paso 8: Entrega y Archivo:** Dueña presiona `Entregado`, saliendo de pendientes activos y guardándose en el histórico.

---

## 4. Matriz de Escenarios "What If" (Casos Borde)
* **What If 1 (Cotización vencida):** Vigencia (7-15 días) y recálculo con 1 clic ante alzas de insumos.
* **What If 2 (Cambio de fecha/hora):** Solo Admin edita; se reordena automáticamente en el iPad.
* **What If 3 (Diseño atípico):** Modo "Estilo Personalizado" con mano de obra manual configurable.
* **What If 4 (Cliente sin liquidar saldo):** Bloqueo/advertencia de deuda; no se entrega sin liquidar.
* **What If 5 (Cancelación):** Retiro inmediato de cocina si está `Pendiente`; anticipo no reembolsable si ya está `En vitrina / refri`.
* **What If 6 (Daño accidental en refri):** Regreso a `Pendiente` con marca visual de "Prioridad / Retrabajo".
* **What If 7 (Falla de internet en taller):** Soporte offline en iPad (PWA / caché local).

---

## 5. Criterios de Aceptación para Lalo
- [ ] Modelos de BD relacional para insumos, recetas, estilos, pedidos y proveedores (con soft delete).
- [ ] API backend con data masking estricto para la vista de cocina.
- [ ] Motor algorítmico de cálculo en cascada < 1 segundo.
- [ ] Frontend táctil KDS en iPad con soporte offline y 3 estados.
- [ ] Panel de administración con validación de entrega y control de anticipos.
- [ ] Módulo de proveedores con enlace rápido a WhatsApp accesible globalmente.
