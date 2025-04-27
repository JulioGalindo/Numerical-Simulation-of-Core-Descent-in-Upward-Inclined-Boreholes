
# Simulación de Descenso de Testigo en Pozos Inclinados

Este proyecto simula el comportamiento dinámico de un **testigo de perforación** descendiendo dentro de un **pozo inclinado** lleno de fluido, considerando todas las fuerzas relevantes.

## Modelo Físico

Se consideran las siguientes fuerzas:

- **Fuerza Gravitatoria**  
  ![Fuerza gravitatoria](fuerza_gravitatoria.png)

- **Fuerza de Flotación**  
  ![Fuerza flotación](fuerza_flotacion.png)

- **Fuerza Viscosa (esfuerzo cortante en régimen anular)**  
  ![Esfuerzo cortante](esfuerzo_cortante.png)
  ![Fuerza viscosa](fuerza_viscosa.png)

- **Fuerza de Arrastre (Drag turbulento)**  
  ![Fuerza arrastre](fuerza_arrastre.png)

La ecuación general de movimiento es:

![Segunda Ley de Newton](segunda_ley.png)

o en forma explícita:

![Aceleración explícita](aceleracion_explicita.png)

## Procedimiento Numérico

Sistema resuelto mediante método **Runge-Kutta de 4º orden (RK4)**:

- Actualización de velocidad:  
  ![RK4 velocidad](rk4_v.png)

- Actualización de posición:  
  ![RK4 posición](rk4_x.png)

Con los incrementos intermedios:

- Primeros incrementos:  
  ![RK4 k1](rk4_k1.png)

- Segundos incrementos:  
  ![RK4 k2](rk4_k2.png)

- Terceros incrementos:  
  ![RK4 k3](rk4_k3.png)

- Cuartos incrementos:  
  ![RK4 k4](rk4_k4.png)

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
