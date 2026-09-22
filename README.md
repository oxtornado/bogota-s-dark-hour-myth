# El Mito de la Hora Oscura: Patrones Espacio-Temporales del Hurto a Personas en Bogotá D.C.

Este repositorio contiene la investigación exploratoria y la aplicación web estática interactiva desarrollada para la exposición académica en el semillero de investigación. El estudio utiliza registros de microdatos oficiales para contrastar la percepción ciudadana sobre la criminalidad nocturna frente a la evidencia estadística real en Bogotá, D.C.

## 📌 Tabla de Contenidos

* [1. Resumen del Proyecto](#1-resumen-del-proyecto)dos 

* [2. Fuentes de Datos Consultadas](#2-fuentes-de-datos-consultadas)

* [3. Matriz de Premisas Refutadas y Corolarios](#3-matriz-de-premisas-refutadas-y-corolarios)

* [4. Desglose Metodológico (Guión de Exposición)](#4-desglose-metodológico-guión-de-exposición)

* [5. Concepto Clave: Población Flotante y Heterogeneidad Territorial](#5-concepto-clave-población-flotante-y-heterogeneidad-territorial)

* [6. Instrucciones para la Exposición y Uso del Tablero](#6-instrucciones-para-la-exposición-y-uso-del-tablero)

## 1. Resumen del Proyecto

* **Tema:** Análisis estadístico espacio-temporal del delito de hurto a personas en Bogotá D.C.

* **Tesis Central:** Existe un sesgo de disponibilidad popular que atribuye la mayor probabilidad de victimización a la madrugada y fines de semana. La evidencia muestra que la criminalidad responde a la *Teoría de las Actividades Rutinarias* (Cohen & Felson), concentrando su volumen en franjas laborales diurnas y de retorno (06:00 - 10:00 y 17:00 - 20:00).

* **Alcance:** Descriptivo, inferencial ($\chi^2$) e interactivo en formato web monocapa (`index.html`).

## 2. Fuentes de Datos Consultadas

El análisis se alimenta de las fuentes públicas e institucionales oficiales de la República de Colombia y la Alcaldía Mayor de Bogotá:

1. **Datos Abiertos Colombia – Ministerio de Defensa / Policía Nacional (SIEDCO):**

   * *Descripción:* Registro microdato de incidentes procesados por el Sistema de Información Estadístico, Delincuencial, Contravencional y Operativo.

   * *Enlace directo:* [Dataset Oficial de Hurto a Personas - Datos.gov.co](https://www.datos.gov.co/Seguridad-y-Defensa/HURTO-PERSONAS/4rxi-8m8d?utm_source=gemini)

2. **Secretaría Distrital de Seguridad, Convivencia y Justicia (SDSCJ):**

   * *Descripción:* Portal oficial de datos abiertos sobre indicadores de seguridad ciudadana y convivencia en Bogotá D.C.

   * *Enlace directo:* [Sección Datos Abiertos SCJ Bogotá](https://scj.gov.co/transparencia/datos-abiertos/seccion-datos-abiertos?utm_source=gemini)

3. **Infraestructura de Datos Espaciales de Bogotá (IDECA):**

   * *Descripción:* Cartografía vectorial, límites político-administrativos por localidad y mapas de referencia espacial.

   * *Enlace directo:* [Catálogo IDECA Bogotá](https://www.ideca.gov.co/?utm_source=gemini)

## 3. Matriz de Premisas Refutadas y Corolarios

### Premisas Populares Refutadas por los Datos

| Premisa Popular Falsa | Evidencia Estadística Contraria | 
 | ----- | ----- | 
| **1. "La madrugada (00:00 - 05:59) es la franja con más hurtos."** | La madrugada concentra solo entre el **10% y 12%** del volumen diario. Las franjas de la mañana (06:00-11:59) y noche (18:00-23:59) abarcan más del **65%** acumulado. | 
| **2. "El fin de semana supera drásticamente en volumen a los días hábiles."** | La distribución semanal es uniforme. Días laborales como **miércoles y viernes** registran picos iguales o superiores al fin de semana debido al tránsito masivo. | 
| **3. "El hurto se comete mayoritariamente con armas de fuego."** | Cerca del **50% al 55%** de los eventos corresponden a **Factor Oportunidad** (descuido) y **Cosquilleo** en transporte o zonas comerciales. | 
| **4. "El riesgo de hurto es homogéneo en toda la ciudad."** | Existe una fuerte variación micro-territorial: localidades de borde (Suba/Engativá) registran picos matutinos, mientras que localidades centrales (Chapinero/Santa Fe) registran picos vespertinos. | 

### Corolarios Derivados

* **Corolario 1 (Hipótesis del Flujo Humano):** El criminal opera bajo un criterio de eficiencia de oportunidad: busca la mayor densidad de víctimas potenciales en momentos de tránsito obligatorio (ej. portales y estaciones de Transmilenio en horas pico).

* **Corolario 2 (Gravedad Severa vs. Frecuencia):** Aunque el volumen *absoluto* de hurtos es menor en la madrugada, la *proporción de violencia física/armas* empleada en esa franja es mayor que en el día.

* **Corolario 3 (Efecto Pendular de Movilidad):** La curva temporal del delito en sectores residenciales es inversa a la de sectores comerciales y universitarios.

## 4. Desglose Metodológico (Guión de Exposición)

A continuación se detalla el flujo de trabajo computacional para sustentarlo durante la presentación del semillero:

```
[Datos Crudos SIEDCO] ➔ [Filtrado DIVIPOLA 11001] ➔ [Normalización Temporal (Bloques 6h)] 
                                                             │
[Tablero Interactivo]  [Matriz Localidad × Hora × Tipología]  [Limpieza e Imputación Nulos]

```

1. **Extracción y Filtrado Geográfico (ETL):**

   * Se descargó la base nacional y se aplicó un filtro estricto por el código municipal `11001` correspondiente a Bogotá, D.C.

2. **Normalización de Variables Temporales:**

   * La hora del reporte (`HH:MM:SS`) fue convertida a variable discreta y agrupada en tramos operativos para eliminar el sesgo de redondeo ciudadano en las denuncias.

3. **Depuración y Tratamiento de inconsistencias:**

   * Eliminación de registros atípicos (coordenadas fuera del perímetro distrital) e imputación mediante centroides geográficos para eventos catalogados solo a nivel de localidad.

4. **Agregación Multidimensional:**

   * Creación de matrices de frecuencia cruzadas ($Localidad \times Franja Horaria \times Modalidad$) para permitir el cálculo dinámico de porcentajes en tiempo real (*Client-Side Rendering*).

## 5. Concepto Clave: Población Flotante y Heterogeneidad Territorial

Durante la exposición es crucial responder por qué ciertas localidades centrales muestran un volumen elevado de hurtos:

> **Población Flotante:** Es el conjunto de personas que frecuentan y transitan un espacio geográfico durante el día por motivos de trabajo, estudio, comercio o recreación, pero cuyo lugar de residencia fijo (pernocta) está en otra localidad o municipio.

* **Implicación en el cálculo de tasas:** Las fórmulas tradicionales dividen los delitos entre la *Población Residente (DANE)*. En localidades como **Chapinero**, **Santa Fe** o **La Candelaria**, esto distorsiona la tasa (falso denominador), ya que la oportunidad delictiva no depende de cuántas personas viven allí, sino de las cientos de miles que transitan diariamente.

## 6. Instrucciones para la Exposición y Uso del Tablero

1. Abre el archivo `index.html` en cualquier navegador web moderno.

2. Durante la ponencia, utiliza los selectores superiores de **Localidad** y **Franja Horaria**.

3. Señala a los evaluadores cómo el bloque de **Modalidad de Hurto** recalcula dinámicamente sus barras y porcentajes, demostrando que al seleccionar *Suba* en la *Mañana*, el "Factor Oportunidad" domina, mientras que al seleccionar *Santa Fe* en la *Madrugada*, la proporción de armas de fuego se incrementa.

*Desarrollado para el Semillero de Analítica de Datos Urbanos • Bogotá, Colombia.*