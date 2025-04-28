# Simulación de Descenso de Testigo en Pozos Ascendentes Inclinados

Este proyecto simula el comportamiento dinámico de un **testigo de perforación** descendiendo dentro de **las barras** de un **pozo inclinado ascendente (positivo)** lleno de fluido, considerando todas las fuerzas relevantes, para demostrar que es posible perforar pozos ascendentes **sin tubo interior** y con bajas viscosidades, lo que implica un ahorro importante de tiempo y costo.

## Modelo Físico

Se consideran las siguientes fuerzas:

- **Fuerza Gravitatoria**  
  <img src="fuerza_gravitatoria.png" alt="Fuerza gravitatoria" width="450"/>

- **Fuerza de Flotación**  
  <img src="fuerza_flotacion.png" alt="Fuerza flotación" width="450"/>

- **Fuerza Viscosa (esfuerzo cortante en régimen anular)**  
  <img src="esfuerzo_cortante.png" alt="Esfuerzo cortante" width="450"/>
  
  <img src="fuerza_viscosa.png" alt="Fuerza viscosa" width="450"/>

- **Fuerza de Arrastre (Drag turbulento)**  
  <img src="fuerza_arrastre.png" alt="Fuerza arrastre" width="450"/>

La ecuación general de movimiento es:

<img src="segunda_ley.png" alt="Segunda Ley de Newton" width="450"/>

o en forma explícita:

<img src="aceleracion_explicita.png" alt="Aceleración explícita" width="450"/>

## Procedimiento Numérico

Sistema resuelto mediante método **Runge-Kutta de 4º orden (RK4)**:

- Actualización de velocidad:  
  <img src="rk4_v.png" alt="RK4 velocidad" width="450"/>

- Actualización de posición:  
  <img src="rk4_x.png" alt="RK4 posición" width="450"/>

Con los incrementos intermedios:

- Primeros incrementos:  
  <img src="rk4_k1.png" alt="RK4 k1" width="450"/>

- Segundos incrementos:  
  <img src="rk4_k2.png" alt="RK4 k2" width="450"/>

- Terceros incrementos:  
  <img src="rk4_k3.png" alt="RK4 k3" width="450"/>

- Cuartos incrementos:  
  <img src="rk4_k4.png" alt="RK4 k4" width="450"/>

## Parámetros Principales

- `tipo`: NQ, HQ o PQ (define diámetros).
- `longitud_testigo`: Longitud del testigo (m).
- `longitud_pozo`: Longitud del pozo (m).
- `caudal_lpm`: Caudal (lpm).
- `viscosidad_marsh`: Viscosidad medida (s Marsh).
- `angulo_deg`: Ángulo del pozo (°).

## Resultados

Se generan gráficos de velocidad, posición y aceleración en función del tiempo.

## Requisitos

- Python 3.7+
- numpy
- matplotlib
- argparse
- json

## Ejecución

```bash
python Simulacion.py --help
python Simulacion.py input.json
```
-------
# Numerical Simulation of Core Descent in Upward-Inclined Boreholes

This project develops a full numerical model of the dynamic behavior of a core sample descending inside an upward-inclined borehole.  
It rigorously considers the combined effects of gravity, buoyancy, drilling fluid drag, viscous shear, and simulates the core's movement using a **Runge–Kutta explicit integration scheme**.  
Additionally, it computes critical operational limits based on the drilling parameters.

---

## Geometrical and Physical Parameters

| Symbol | Meaning | Unit |
|:------|:--------|:----|
| $d_t$ | Core diameter | m |
| $d_b$ | Borehole internal diameter | m |
| $r_1 = \frac{d_t}{2}$ | Core radius | m |
| $r_2 = \frac{d_b}{2}$ | Borehole radius | m |
| $A_f = \pi r_1^2$ | Frontal area of the core | m² |
| $A_a = \pi (r_2^2 - r_1^2)$ | Annular flow area | m² |
| $A_{\text{lateral}} = 2 \pi r_1 L$ | Lateral surface of the core | m² |
| $V = A_f L$ | Core volume | m³ |
| $m = \rho_c V$ | Core mass | kg |

---

## Reference Axis and Sign Convention

- **Reference axis**: aligned with the borehole.
- **Positive direction**: upwards, following the borehole inclination.

| Force | Direction | Sign |
|:------|:----------|:----|
| Gravitational force $F_g$ | Downward | Negative |
| Buoyant force $F_b$ | Upward | Positive |
| Viscous force $F_v$ | Opposite to relative velocity | Depends on $v_{rel}$ |
| Drag force $F_d$ | Opposite to relative velocity | Depends on $v_{rel}$ |
| Core downward motion | Negative velocity | |
| Core upward motion | Positive velocity | |

---

## Governing Equations

The core's motion is governed by Newton's Second Law along the borehole axis:

$m \ \frac{dV}{dt} = F_g + F_b + F_d + F_v$

where:

- $m$ = mass of the core kg
- $V$ = instantaneous velocity along the borehole m/s
- $F_g$ = gravitational force
- $F_b$ = buoyancy force
- $F_d$ = drag force due to relative motion against fluid
- $F_v$ = viscous wall shear force

---

## Forces Definitions

- **Gravitational Force**:

  $F_g = -m\ g\ \sin(\theta)$

- **Buoyant Force**:

  $F_b = \rho_f \ V \ g \ \sin(\theta)$
- **Drag Force**:

  $F_d = -\frac{1}{2} \ C_d \ \rho_f \ A_f \ v_{rel} \ |v_{rel}|$
- **Viscous Force**:

  $F_v = -\tau \ A_{\text{lateral}}$
  
Where:

- $\theta$ = borehole inclination angle $[^\circ]$
- $g$ = gravitational acceleration $[9.81 \ m/s^2]$
- $\rho_f$ = fluid density $[kg/m^3]$
- $C_d$ = drag coefficient (dimensionless)
- $v_{rel} = V - V_{fluid}$ = core velocity relative to the fluid

---

## Wall Shear Stress (Bingham Model)

The shear stress due to the fluid on the core wall is:

  $\tau = \dfrac{4 \ \mu \ V_{fluid}}{r_1 \ (1 - (r_1/r_2)^2)}$
  
Where:

- $\mu$ = apparent dynamic viscosity $[Pa \cdot s]$
- $V_{fluid}$ = fluid velocity through the annular area $[m/s]$

---

## Numerical Integration: Explicit Runge-Kutta Scheme

The integration is based on a **second-order Runge–Kutta** method:

$V_{n+1} = V_n + \Delta t \left( \frac{dV}{dt} \right)_n$

$X_{n+1} = X_n + \Delta t V_{n+1}$

Where:

- $\Delta t$ = time step (adapted for numerical stability)
- $X$ = core position along borehole

Velocity stabilization is detected when acceleration becomes smaller than a defined threshold.

---

## Critical Limit Calculations

The simulation computes critical conditions where the core may stop descending:

- **Critical viscosity vs flowrate** (fixed inclination)
- **Critical viscosity vs inclination** (fixed flowrate)
- **Critical inclination vs flowrate** (fixed viscosity)

These charts are essential for **drilling fluid design** and **borehole planning**.

---

## Requirements

- Python 3.8+
- NumPy
- Matplotlib

Install with:

```
pip install -r requirements.txt
```

---

## Example Plots

- Core position, velocity, acceleration vs time
- Critical Marsh viscosity curves
- Stability operational maps

---

## Marsh Funnel Conversion (Approximate Model)

The drilling fluid viscosity in field operations is typically measured in **Marsh seconds**, defined as the time required for a known volume to flow through a standard Marsh funnel.

The approximate conversion between Marsh seconds and dynamic viscosity (Pa·s) used in this project is:

$\mu = \dfrac{1.1 \times (\text{Marsh Seconds} - 25)}{1000}$

Where:

- 25 seconds is the baseline drainage time of pure water at 25°C.
- 1.1 is a correction coefficient to approximate dynamic viscosity from empirical Marsh seconds.

Thus:

- A fluid with $35$ seconds Marsh time has an estimated viscosity of:

  $\mu \approx \dfrac{1.1 \times (35 - 25)}{1000} = 0.011 \, \ \ Pa \cdot s$

**Note:** This conversion is an engineering approximation and assumes Newtonian behavior for low-range Marsh readings, which may not be strictly valid for non-Newtonian drilling fluids.

---

## Detailed Sign Convention

| Force | Direction | Sign |
|:------|:----------|:----|
| $F_g$ | Downward along borehole | Negative |
| $F_b$ | Upward (buoyancy) | Positive |
| $F_d$ | Opposes relative motion | Depends on $v_{rel}$ |
| $F_v$ | Opposes relative motion | Depends on $v_{rel}$ |
| Core descending motion | Downward along borehole | Negative velocity |
| Core ascending motion | Upward along borehole | Positive velocity |

---

## Borehole Inclination Definition

- $\theta > 0^\circ$: Borehole is **ascending** (upward inclined).
- $\theta = 0^\circ$: Borehole is **horizontal**.
- $\theta < 0^\circ$: Borehole is **descending** (natural fall by gravity).

The positive axis follows the borehole upwards.

---

## Special Cases Handled in the Code

- Fluid flow may push the core **upwards** if the annular flow velocity is sufficiently high.
- Reverse movement of the core (upward motion) is automatically detected.
- Dynamic forces (drag and viscous shear) switch signs based on the relative velocity $v_{rel}$.

The model thus supports:

- Normal descent (gravity-dominated)
- Decelerated descent (fluid resistance)
- Static equilibrium (core arrested)
- Reverse ascent (core uplift)

---

## Shear Stress Between Two Concentric Cylinders

The model uses the analytical solution for laminar viscous flow between two cylinders:

**Shear stress at core surface**:

$\tau = \dfrac{4 \mu V_{fluid}}{r_1 (1 - (r_1/r_2)^2)}$

derived from the Navier-Stokes equations under steady, incompressible, axisymmetric conditions.

---

## Units Used Throughout

| Quantity | Symbol | Unit |
|:---------|:-------|:-----|
| Mass | $m$ | kg |
| Position | $X$ | m |
| Velocity | $V$ | m/s |
| Acceleration | $a$ | m/s² |
| Force | $F$ | N |
| Viscosity | $\mu$ | Pa·s |
| Fluid Density | $\rho_f$ | kg/m³ |
| Core Density | $\rho_c$ | kg/m³ |
| Gravitational Acceleration | $g$ | 9.81 m/s² |
| Marsh Viscosity | – | seconds (Marsh funnel) |
| Flow Rate | $Q$ | L/min |

---

# Final Notes

- The simulation was specifically designed for the analysis of **core retrieval** during **upward-inclined borehole drilling**.
- The code structure is optimized for **scientific exploration** and **operational analysis** in drilling engineering.
