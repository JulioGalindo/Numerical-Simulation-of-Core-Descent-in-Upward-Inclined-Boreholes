
# Simulación de Descenso de Testigo en Pozos Inclinados

Este proyecto simula el comportamiento dinámico de un **testigo de perforación** descendiendo dentro de un **pozo inclinado** lleno de fluido, considerando todas las fuerzas relevantes.

## Modelo Físico

Se consideran las siguientes fuerzas:

- **Fuerza Gravitatoria**  
  <img src="fuerza_gravitatoria.png" alt="Fuerza gravitatoria" width="350"/>

- **Fuerza de Flotación**  
  <img src="fuerza_flotacion.png" alt="Fuerza flotación" width="350"/>

- **Fuerza Viscosa (esfuerzo cortante en régimen anular)**  
  <img src="esfuerzo_cortante.png" alt="Esfuerzo cortante" width="350"/>
  
  <img src="fuerza_viscosa.png" alt="Fuerza viscosa" width="350"/>

- **Fuerza de Arrastre (Drag turbulento)**  
  <img src="fuerza_arrastre.png" alt="Fuerza arrastre" width="350"/>

La ecuación general de movimiento es:

<img src="segunda_ley.png" alt="Segunda Ley de Newton" width="350"/>

o en forma explícita:

<img src="aceleracion_explicita.png" alt="Aceleración explícita" width="350"/>

## Procedimiento Numérico

Sistema resuelto mediante método **Runge-Kutta de 4º orden (RK4)**:

- Actualización de velocidad:  
  <img src="rk4_v.png" alt="RK4 velocidad" width="350"/>

- Actualización de posición:  
  <img src="rk4_x.png" alt="RK4 posición" width="350"/>

Con los incrementos intermedios:

- Primeros incrementos:  
  <img src="rk4_k1.png" alt="RK4 k1" width="350"/>

- Segundos incrementos:  
  <img src="rk4_k2.png" alt="RK4 k2" width="350"/>

- Terceros incrementos:  
  <img src="rk4_k3.png" alt="RK4 k3" width="350"/>

- Cuartos incrementos:  
  <img src="rk4_k4.png" alt="RK4 k4" width="350"/>

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
python Simulacion6.py --config archivo_configuracion.json --tipo HQ
```
