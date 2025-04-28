# Simulación numérica del descenso del testigo en pozos inclinados hacia arriba

Este proyecto desarrolla un modelo numérico completo del comportamiento dinámico de una muestra de testigo descendiendo dentro de un pozo inclinado hacia arriba.  
Considera rigurosamente los efectos combinados de la gravedad, la flotabilidad, la resistencia del fluido de perforación, el esfuerzo viscoso, y simula el movimiento del testigo utilizando un **esquema de integración explícita Runge–Kutta**.  
Además, calcula los límites operacionales críticos basados en los parámetros de perforación.

---

## Parámetros geométricos y físicos

| Símbolo | Significado | Unidad |
|:------|:--------|:----|
| $d_t$ | Diámetro del testigo | m |
| $d_b$ | Diámetro interno del pozo | m |
| $r_1 = \frac{d_t}{2}$ | Radio del testigo | m |
| $r_2 = \frac{d_b}{2}$ | Radio del pozo | m |
| $A_f = \pi r_1^2$ | Área frontal del testigo | m² |
| $A_a = \pi (r_2^2 - r_1^2)$ | Área de flujo anular | m² |
| $A_{\text{lateral}} = 2 \pi r_1 L$ | Superficie lateral del testigo | m² |
| $V = A_f L$ | Volumen del testigo | m³ |
| $m = \rho_c V$ | Masa del testigo | kg |

---

## Eje de referencia y convención de signos

- **Eje de referencia**: alineado con el pozo.
- **Dirección positiva**: hacia arriba, siguiendo la inclinación del pozo.

| Fuerza | Dirección | Signo |
|:------|:----------|:----|
| Fuerza gravitacional $F_g$ | Hacia abajo | Negativo |
| Fuerza de flotabilidad $F_b$ | Hacia arriba | Positivo |
| Fuerza viscosa $F_v$ | Opuesta a la velocidad relativa | Depende de $v_{rel}$ |
| Fuerza de arrastre $F_d$ | Opuesta a la velocidad relativa | Depende de $v_{rel}$ |
| Movimiento hacia abajo del testigo | Velocidad negativa | |
| Movimiento hacia arriba del testigo | Velocidad positiva | |

---

## Ecuaciones gobernantes

El movimiento del testigo está gobernado por la segunda ley de Newton a lo largo del eje del pozo:

  $m \ \frac{dV}{dt} = F_g + F_b + F_d + F_v$

donde:

- $m$ = masa del testigo [kg]
- $V$ = velocidad instantánea a lo largo del pozo [m/s]
- $F_g$ = fuerza gravitacional
- $F_b$ = fuerza de flotabilidad
- $F_d$ = fuerza de arrastre debido al movimiento relativo contra el fluido
- $F_v$ = fuerza de cizallamiento viscoso en la pared

---

## Definiciones de fuerzas

- **Fuerza gravitacional**:

  $F_g = -m\ g\ \sin(\theta)$

- **Fuerza de flotabilidad**:

  $F_b = \rho_f \ V \ g \ \sin(\theta)$
- **Fuerza de arrastre**:

  $F_d = -\frac{1}{2} \ C_d \ \rho_f \ A_f \ v_{rel} \ |v_{rel}|$
- **Fuerza viscosa**:

  $F_v = -\tau \ A_{\text{lateral}}$
  
Donde:

- $\theta$ = ángulo de inclinación del pozo $[^\circ]$
- $g$ = aceleración gravitacional $[9.81 \ m/s^2]$
- $\rho_f$ = densidad del fluido $[kg/m^3]$
- $C_d$ = coeficiente de arrastre (adimensional)
- $v_{rel} = V - V_{fluid}$ = velocidad del testigo relativa al fluido

---

## Esfuerzo de cizallamiento en la pared (modelo de Bingham)

El esfuerzo de cizallamiento debido al fluido en la pared del testigo es:

  $\tau = \dfrac{4 \ \mu \ V_{fluid}}{r_1 \ (1 - (r_1/r_2)^2)}$
  
Donde:

- $\mu$ = viscosidad dinámica aparente $[Pa \cdot s]$
- $V_{fluid}$ = velocidad del fluido a través del área anular $[m/s]$

---

## Integración numérica: Esquema explícito de Runge-Kutta

La integración se basa en el método **Runge–Kutta de cuarto orden**:

  $V_{n+1} = V_n + \Delta t \left( \frac{dV}{dt} \right)_n$

  $X_{n+1} = X_n + \Delta t V_{n+1}$

#### Actualización de la velocidad y la posición:

La velocidad se actualiza como:

$dv = \dfrac{dt}{6} \left( k_1v + 2k_2v + 2k_3v + k_4v \right)$

Y la posición se actualiza como:

$dx = \dfrac{dt}{6} \left( k_1x + 2k_2x + 2k_3x + k_4x \right)$

Donde:

- $\Delta t$ = paso de tiempo (adaptado para estabilidad numérica)
- $k_1$, $k_2$, $k_3$, y $k_4$ representan las aproximaciones de la aceleración y la posición a diferentes pasos intermedios.

La estabilización de la velocidad se detecta cuando la aceleración se vuelve más pequeña que un umbral definido.

---

## Cálculos de límites críticos

La simulación calcula las condiciones críticas donde el testigo puede dejar de descender:

- **Viscosidad crítica vs caudal** (inclinación fija)
- **Viscosidad crítica vs inclinación** (caudal fijo)
- **Inclinación crítica vs caudal** (viscosidad fija)

Estos gráficos son esenciales para el **diseño del fluido de perforación** y la **planificación del pozo**.

---

## Requisitos

- Python 3.8+
- NumPy
- Matplotlib

Instalar con:

```
pip install -r requirements.txt
```

---

## Ejemplos de gráficos

- Posición del testigo, velocidad, aceleración vs tiempo
- Curvas críticas de viscosidad Marsh
- Mapas operacionales de estabilidad

---

## Conversión del embudo Marsh (modelo aproximado)

La viscosidad del fluido de perforación en las operaciones de campo se mide típicamente en **segundos Marsh**, definidos como el tiempo necesario para que un volumen conocido fluya a través de un embudo Marsh estándar.

La conversión aproximada entre los segundos Marsh y la viscosidad dinámica (Pa·s) utilizada en este proyecto es:

  $\mu = \dfrac{1.1 \times (\text{Marsh Seconds} - 25)}{1000}$

Donde:

- 25 segundos es el tiempo base de drenaje del agua pura a 25°C.
- 1.1 es un coeficiente de corrección para aproximar la viscosidad dinámica a partir de los segundos Marsh.

Así:

- Un fluido con $35$ segundos Marsh tiene una viscosidad estimada de:

  $\mu \approx \dfrac{1.1 \times (35 - 25)}{1000} = 0.011 \, \ \ Pa \cdot s$

**Nota:** Esta conversión es una aproximación ingenieril y asume un comportamiento newtoniano para lecturas bajas de Marsh, lo que puede no ser estrictamente válido para fluidos de perforación no newtonianos.

---

## Convención detallada de signos

| Fuerza | Dirección | Signo |
|:------|:----------|:----|
| $F_g$ | Hacia abajo a lo largo del pozo | Negativo |
| $F_b$ | Hacia arriba (flotabilidad) | Positivo |
| $F_d$ | Opuesta al movimiento relativo | Depende de $v_{rel}$ |
| $F_v$ | Opuesta al movimiento relativo | Depende de $v_{rel}$ |
| Movimiento hacia abajo del testigo | Hacia abajo a lo largo del pozo | Velocidad negativa |
| Movimiento hacia arriba del testigo | Hacia arriba a lo largo del pozo | Velocidad positiva |

---

## Definición de la inclinación del pozo

- $\theta > 0^\circ$: El pozo es **ascendente** (inclinación hacia arriba).
- $\theta = 0^\circ$: El pozo es **horizontal**.
- $\theta < 0^\circ$: El pozo es **descendente** (caída natural por gravedad).

El eje positivo sigue el pozo hacia arriba.

---

## Casos especiales manejados en el código

- El flujo del fluido puede empujar el testigo **hacia arriba** si la velocidad del flujo anular es suficientemente alta.
- El movimiento inverso del testigo (movimiento hacia arriba) se detecta automáticamente.
- Las fuerzas dinámicas (arrastre y cizallamiento viscoso) cambian de signo en función de la velocidad relativa $v_{rel}$.

El modelo, por lo tanto, soporta:

- Descenso normal (dominado por la gravedad)
- Descenso desacelerado (resistencia del fluido)
- Equilibrio estático (testigo detenido)
- Ascenso inverso (testigo ascendente)

---

## Esfuerzo de cizallamiento entre dos cilindros concéntricos

El modelo utiliza la solución analítica para el flujo laminar viscoso entre dos cilindros:

**Esfuerzo de cizallamiento en la superficie del testigo**:

  $\tau = \dfrac{4 \mu V_{fluid}}{r_1 (1 - (r_1/r_2)^2)}$

derivado de las ecuaciones de Navier-Stokes bajo condiciones estáticas, incomprensibles y axiales.

---

## Unidades utilizadas en todo el documento

| Cantidad | Símbolo | Unidad |
|:---------|:-------|:-----|
| Masa | $m$ | kg |
| Posición | $X$ | m |
| Velocidad | $V$ | m/s |
| Aceleración | $a$ | m/s² |
| Fuerza | $F$ | N |
| Viscosidad | $\mu$ | Pa·s |
| Densidad del fluido | $\rho_f$ | kg/m³ |
| Densidad del testigo | $\rho_c$ | kg/m³ |
| Aceleración gravitacional | $g$ | 9.81 m/s² |
| Viscosidad Marsh | – | segundos (embudo Marsh) |
| Caudal | $Q$ | L/min |

---

# Notas finales

- La simulación fue diseñada específicamente para el análisis de **recuperación del testigo** durante la perforación en pozos inclinados hacia arriba.
- La estructura del código está optimizada para la **exploración científica** y el **análisis operativo** en ingeniería de perforación.





---

- Actualización de la velocidad \( V \) y la posición \( X \) usando el método Runge-Kutta:

$V_{n+1} = V_n + \Delta t \left( \frac{dV}{dt} \right)_n$

$X_{n+1} = X_n + \Delta t V_{n+1}$

#### 5. Actualización de la velocidad y la posición:

La velocidad se actualiza como:

\[
dv = \frac{dt}{6} \left( k_1v + 2k_2v + 2k_3v + k_4v \right)
\]

Y la posición se actualiza como:

\[
dx = \frac{dt}{6} \left( k_1x + 2k_2x + 2k_3x + k_4x \right)
\]

#### 6. Parámetros de la simulación:

- **$k_1$, $k_2$, $k_3$, y $k_4$** representan las aproximaciones de la aceleración y la posición a diferentes pasos intermedios.

---

Este es el conjunto de **ecuaciones en LaTeX** que representan el método numérico **Runge-Kutta de cuarto orden** junto con las ecuaciones de movimiento y las fuerzas involucradas en el sistema.

Puedes copiar y pegar estas ecuaciones directamente en tu archivo `.tex` para generar el documento completo. Si necesitas más explicaciones o ajustes, estaré disponible para ayudarte.
