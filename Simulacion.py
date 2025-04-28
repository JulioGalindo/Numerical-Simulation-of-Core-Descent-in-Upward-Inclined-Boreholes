# Copyright (C) 2025 Julio A. Galindo Q.
# This file is part of Numerical-Simulation-of-Core-Descent-in-Upward-Inclined-Boreholes.
#
# Numerical-Simulation-of-Core-Descent-in-Upward-Inclined-Boreholes is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Numerical-Simulation-of-Core-Descent-in-Upward-Inclined-Boreholes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Numerical-Simulation-of-Core-Descent-in-Upward-Inclined-Boreholes.  If not, see <http://www.gnu.org/licenses/>.


# Copyright (C) 2025 Julio A. Galindo Q.
# Este archivo es parte de Numerical-Simulation-of-Core-Descent-in-Upward-Inclined-Boreholes.
#
# Numerical-Simulation-of-Core-Descent-in-Upward-Inclined-Boreholes es software libre: puedes redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU según lo publicado por
# la Free Software Foundation, ya sea la versión 3 de la licencia o
# (a tu elección) cualquier versión posterior.
#
# Numerical-Simulation-of-Core-Descent-in-Upward-Inclined-Boreholes se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; sin ni siquiera la garantía implícita de
# COMERCIABILIDAD o ADECUACIÓN A UN PROPÓSITO PARTICULAR. Consulta la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con Numerical-Simulation-of-Core-Descent-in-Upward-Inclined-Boreholes.  Si no, consulta <http://www.gnu.org/licenses/>.


import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import textwrap
import argparse
import json
import tkinter as tk

class SimuladorTestigo:
    def __init__(self, config, diametro):
        self.diametros = {
            "NQ": {"d_t": 0.045, "d_b": 0.0476},
            "HQ": {"d_t": 0.0611, "d_b": 0.0635},
            "PQ": {"d_t": 0.083, "d_b": 0.085}
        }
        self.diametro = diametro
        self.d_t = self.diametros[diametro]["d_t"]
        self.d_b = self.diametros[diametro]["d_b"]
        self.L_testigo = config["longitud_testigo_m"]
        self.L_pozo = config["longitud_pozo_m"]
        self.Q = config["caudal_lpm"] / 60000
        self.mu = 1.1 * (config["viscosidad_marsh_seg"] - 25) / 1000
        self.angulo_deg = config["angulo_deg"]
        self.theta_rad = float(np.radians(self.angulo_deg))
        self.rango_viscosidad = config["rango_viscosidad"]
        self.rango_angulo = config.get("rango_angulo", None)
        self.rango_caudal = config.get("rango_caudal", None)

        self.rho_c = config.get("densidad_roca_kgm3", 2200)                            # Densidad de la roca kg/m3
        self.rho_f = config.get("densidad_fluido_kgm3", 1030)                          # Densidad del fluido kg/m3
        self.Cd = 0.8                                                                  # Coeficiente de arrastre frontal del testigo
        self.g = 9.81                                                                  # Gravedad m/s2
        self.Q_min = 25                                                                # Caudal mínimo litros/minuto
        self.max_caudal_bombeo = self.Q_max = config.get("caudal_max_bombeo_lpm", 140) # Caudal máximo de bombeo litros/minuto
        self.max_tiempo_simulacion = config.get("tiempo_max_simulacion_seg", 1000)     # Máximo tiempo de simulación en seg

        self.r1 = self.d_t / 2
        self.r2 = self.d_b / 2
        self.Af = np.pi * self.r1**2
        self.Aa = np.pi * (self.r2**2 - self.r1**2)
        self.Alat = 2 * np.pi * self.r1 * self.L_testigo
        self.V = self.Af * self.L_testigo
        self.m = self.rho_c * self.V

        self.figsize = self._calcular_tamano_figura()

    def v_fluido(self):
        return self.Q / self.Aa

    def aceleracion(self, v):
        vrel = v - self.v_fluido()
        tau = 4.0 * self.mu * abs(vrel) / (self.r1 * (1.0 - (self.r1 / self.r2)**2))
        Fv = -np.sign(vrel) * tau * self.Alat
        Fd = -0.5 * self.rho_f * self.Cd * self.Af * vrel * abs(vrel)
        Fb = self.rho_f * self.V * self.g * np.sin(self.theta_rad)
        Fg = -self.rho_c * self.V * self.g * np.sin(self.theta_rad)
        return (Fb + Fv + Fd + Fg) / self.m

    def simular(self):
        dt = 0.01
        t = 0.0
        x = self.L_pozo
        v = 0.0
        T, X, V, A = [], [], [], []

        while x > 0.0 and t < self.max_tiempo_simulacion:
            a = self.aceleracion(v)
            T.append(t)
            X.append(x)
            V.append(v)
            A.append(a)

            k1v = a
            k1x = v
            k2v = self.aceleracion(v + 0.5 * dt * k1v)
            k2x = v + 0.5 * dt * k1v
            k3v = self.aceleracion(v + 0.5 * dt * k2v)
            k3x = v + 0.5 * dt * k2v
            k4v = self.aceleracion(v + dt * k3v)
            k4x = v + dt * k3v

            dv = (dt / 6.0) * (k1v + 2.0 * k2v + 2.0 * k3v + k4v)
            dx = (dt / 6.0) * (k1x + 2.0 * k2x + 2.0 * k3x + k4x)

            v += dv
            x += dx
            t += dt

            if x > self.L_pozo:
                x = self.L_pozo
                v = 0
            elif x <= 0:
                x = 0
                v = 0
                a = self.aceleracion(v)
                T.append(t)
                X.append(x)
                V.append(v)
                A.append(a)

        return T, X, V, A

    def _calcular_tamano_figura(self):
        root = tk.Tk()
        root.withdraw()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()

        dpi = 100
        max_width_inch = width / dpi
        max_height_inch = height / dpi

        # Ajustes de márgenes más realistas
        ancho = min(16, max_width_inch * 1.00)   # 95% de ancho real disponible
        alto = min(10, max_height_inch * 0.89)   # 89% en vertical

        return (ancho, alto)
    
    def configurar_minor_ticks(self, ax, eje='both'):
        def _set_minor(eje_local):
            if eje_local == 'x':
                majors = ax.get_xticks()
                axis = ax.xaxis
            elif eje_local == 'y':
                majors = ax.get_yticks()
                axis = ax.yaxis
            else:
                raise ValueError("Eje debe ser 'x' o 'y'.")

            if len(majors) >= 2:
                delta = majors[1] - majors[0]
                if delta > 0:
                    minor_locator = plt.MultipleLocator(delta / 2)
                    axis.set_minor_locator(minor_locator)
                    ax.grid(True, which='minor', axis=eje_local, linestyle=':', linewidth=0.3)

        if eje == 'both':
            _set_minor('x')
            _set_minor('y')
        elif eje in ['x', 'y']:
            _set_minor(eje)
        else:
            raise ValueError("Eje debe ser 'x', 'y' o 'both'.")

    def graficar_simulacion(self, axs=None):
        
        crear_figura = False
        if axs is None:
            fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
            crear_figura = True

        T, X, V, A = self.simular()
        
        # Gráfico 1: Posición
        axs[0].plot(T, X, color="blue")
        axs[0].set_ylabel("Posición (m)", color="blue")
        axs[0].tick_params(axis='y', labelcolor="blue")
        axs[0].tick_params(axis='x', labelbottom=True)

        axs[0].grid(True, axis='both', linestyle='--')
        self.configurar_minor_ticks(axs[0], eje='both')

        # Gráfico 2: Velocidad
        axs[1].plot(T, V, color="green")
        axs[1].set_ylabel("Velocidad (m/s)", color="green")
        axs[1].tick_params(axis='y', labelcolor="green")
        axs[1].tick_params(axis='x', labelbottom=True)

        axs[1].grid(True, axis='both', linestyle='--')
        self.configurar_minor_ticks(axs[1], eje='both')

        # Gráfico 3: Aceleración
        axs[2].plot(T, A, color="red")
        axs[2].set_ylabel("Aceleración (m/s²)", color="red")
        axs[2].set_xlabel("Tiempo (s)")
        axs[2].tick_params(axis='y', labelcolor="red")
        axs[2].tick_params(axis='x', labelbottom=True)

        axs[2].grid(True, axis='both', linestyle='--')
        self.configurar_minor_ticks(axs[2], eje='both')

        # Título principal y sub-título
        titulo_principal = f"Simulación de caída – {self.diametro}"
        self.subtitulo_datos = (
            f"Longitud del pozo {self.L_pozo} m, "
            f"Ángulo {self.angulo_deg}\u00B0, "
            f"Longitud del testigo {self.L_testigo} m, "
            f"Caudal {round(self.Q * 60000)} L/min, "
            f"Viscosidad {round(self.mu * 1000 / 1.1 + 25)} seg (Marsh)"
        )

        # Cálculo de resultados
        velocidad_final = V[-2]
        tiempo_final = T[-2]
        fuerza_neta = self.m * A[-2]

        # Peso efectivo (gravedad - flotación)
        fuerza_peso = (self.rho_c - self.rho_f) * self.V * self.g

        # Velocidad del fluido en el anular
        v_fluido = self.Q / self.Aa

        # Fuerza de arrastre por flujo
        fuerza_arrastre = 0.5 * self.rho_f * self.Cd * self.Af * v_fluido * abs(v_fluido)

        # Fuerza de corte viscoso
        if (1 - (self.r1 / self.r2)**2) != 0:
            tau_corte = 4 * self.mu * v_fluido / (self.r1 * (1 - (self.r1 / self.r2)**2))
        else:
            tau_corte = 0.0
        fuerza_corte = tau_corte * self.Alat

        # Fuerza total final
        fuerza_total = (-fuerza_peso + fuerza_arrastre + fuerza_corte) / self.g

        # Subtítulo de resultados
        self.subtitulo_resultados = (f"Velocidad final {velocidad_final:.1f} m/s, "
                                     f"Tiempo total {tiempo_final:.1f} s, "
                                     f"Fuerza total de inpacto del testigo {fuerza_total:.1f} kg")

        if crear_figura:
            fig.suptitle(f"{titulo_principal}", fontsize=13)
            fig.text(0.5, 0.94, self.subtitulo_datos, ha='center', fontsize=10)
            fig.text(0.5, 0.91, self.subtitulo_resultados, ha='center', fontsize=10)

            plt.tight_layout(rect=[0, 0, 1, 0.88])
            plt.show()

    def graficar_viscosidad_limite(self, ax=None):

        def calcular_theta(mu_local, Q_lpm):
            Q_m3s = Q_lpm / 60000
            v_f = Q_m3s / self.Aa
            v_rel = -v_f

            tau = 4 * mu_local * abs(v_rel) / (self.r1 * (1 - (self.r1/self.r2)**2))
            Fv = -np.sign(v_rel) * tau * self.Alat
            Fd = -0.5 * self.rho_f * self.Cd * self.Af * v_rel * abs(v_rel)
            Fg = (self.rho_c - self.rho_f) * self.V * self.g

            sin_theta = (Fv + Fd) / Fg
            sin_theta = np.clip(sin_theta, -1.0, 1.0)
            theta_deg = np.degrees(np.arcsin(sin_theta))
            return max(theta_deg, 0.0)

        created_local_fig = False
        delta_y = -15
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
            created_local_fig = True
            delta_y = 0

        # Determinar viscosidades
        if self.rango_viscosidad:
            viscosidades = list(range(self.rango_viscosidad[0], self.rango_viscosidad[1] + 1, self.rango_viscosidad[2]))
        else:
            viscosidades = [round(self.mu * 1000 / 1.1 + 25, 1)]

        viscosidades = sorted(viscosidades)  # ordenarlas siempre por si acaso

        todas_las_thetas = []
        Qs_dict = {}

        menor_viscosidad = viscosidades[0]
        mu_menor = 1.1 * (menor_viscosidad - 25) / 1000

        Qs_menor = []
        thetas_menor = []
        Q_prev = None
        alcanzado_90 = False
        Q_critico = None
        n_inter = 15

        caudal = self.Q_min
        while caudal <= self.max_caudal_bombeo:
            theta_actual = calcular_theta(mu_menor, caudal)

            if not alcanzado_90:
                if theta_actual >= 90.0 and Q_prev is not None:
                    # Interpolar puntos antes del 90°
                    for i in range(1, n_inter + 1):
                        Q_interp = Q_prev + (caudal - Q_prev) * i / (n_inter + 1)
                        theta_interp = calcular_theta(mu_menor, Q_interp)
                        Qs_menor.append(round(Q_interp, 2))
                        thetas_menor.append(theta_interp)
                    Qs_menor.append(caudal)
                    thetas_menor.append(90.0)
                    alcanzado_90 = True
                    Q_critico = caudal
                else:
                    Qs_menor.append(caudal)
                    thetas_menor.append(theta_actual)
            else:
                Qs_menor.append(caudal)
                thetas_menor.append(90.0)

            Q_prev = caudal
            caudal += 0.5

        # Definir Q_max
        if Q_critico is not None:
            self.Q_max = Q_critico + 20
            self.Q_max = min(self.Q_max, self.max_caudal_bombeo)
        else:
            self.Q_max = self.max_caudal_bombeo

        Qs_dict[menor_viscosidad] = (Qs_menor, thetas_menor)
        todas_las_thetas.append(thetas_menor)

        for marsh in viscosidades[1:]:
            mu_local = 1.1 * (marsh - 25) / 1000
            Qs = []
            thetas = []
            Q_prev = None
            alcanzado_90 = False

            caudal = self.Q_min
            while caudal <= self.Q_max:
                theta_actual = calcular_theta(mu_local, caudal)

                if not alcanzado_90:
                    if theta_actual >= 90.0 and Q_prev is not None:
                        for i in range(1, n_inter + 1):
                            Q_interp = Q_prev + (caudal - Q_prev) * i / (n_inter + 1)
                            theta_interp = calcular_theta(mu_local, Q_interp)
                            Qs.append(round(Q_interp, 2))
                            thetas.append(theta_interp)
                        Qs.append(caudal)
                        thetas.append(90.0)
                        alcanzado_90 = True
                    else:
                        Qs.append(caudal)
                        thetas.append(theta_actual)
                else:
                    Qs.append(caudal)
                    thetas.append(90.0)

                Q_prev = caudal
                caudal += 0.5

            Qs_dict[marsh] = (Qs, thetas)
            todas_las_thetas.append(thetas)

        for marsh in viscosidades:
            Qs, thetas = Qs_dict[marsh]
            ax.plot(Qs, thetas, label=f"{marsh} s Marsh", zorder=2)

            if 90.0 in thetas:
                idx_90 = thetas.index(90.0)
                x_pos = Qs[idx_90]
                y_pos = thetas[idx_90] + delta_y
                ax.annotate(f"{marsh}",
                            (x_pos, y_pos),
                            textcoords="offset points", xytext=(0, 5),
                            ha='center', fontsize=8, fontfamily='monospace', zorder=3,
                            bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.2'))

        for y in range(10, 100, 10):
            ax.axhline(y, color='gray', linestyle='--', linewidth=0.5, zorder=0)
        for x in range(self.Q_min, int(self.Q_max) + 1, 10):
            ax.axvline(x, color='gray', linestyle=':', linewidth=0.4, zorder=0)

        max_theta = max(max(curva) for curva in todas_las_thetas)
        max_theta = min(max_theta * 1.1, 95)

        ax.set_xlim(self.Q_min, self.Q_max)
        ax.set_ylim(0, max_theta)
        ax.set_xlabel("Caudal (L/min)", fontsize=10)
        ax.set_ylabel("Ángulo crítico (°)", fontsize=10)
        ax.set_title(f"Ángulo crítico vs Caudal – {self.diametro}", fontsize=11)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontfamily('monospace')

        ax.legend(
            loc='lower right',
            bbox_to_anchor=(1.0, 0.0),
            ncol=2,
            fontsize=8,
            frameon=True,
            title="Viscosidad:",
            title_fontsize=8
        )
        ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(5))
        ax.grid(which='major', axis='both', linestyle='--')
        ax.grid(which='minor', axis='both', linestyle=':')

        if created_local_fig:
            fig.tight_layout()
            plt.show()

    def graficar_angulo_limite(self, ax=None):

        def calcular_viscosidad(mu_ang_deg, caudal_lpm):
            Q_m3s = caudal_lpm / 60000
            v_f = Q_m3s / self.Aa
            v_rel = -v_f

            Fd = -0.5 * self.rho_f * self.Cd * self.Af * v_rel * abs(v_rel)
            Fg = (self.rho_c - self.rho_f) * self.V * self.g * np.sin(np.radians(mu_ang_deg))

            num = Fg - Fd
            den = (4 * abs(v_rel) / (self.r1 * (1 - (self.r1/self.r2)**2))) * self.Alat

            if den != 0:
                mu_Pa_s = num / den
            else:
                mu_Pa_s = np.nan

            mu_Pa_s = max(mu_Pa_s, 0.0)
            mu_marsh = mu_Pa_s * 1000 / 1.1 + 25
            return mu_marsh  # NO hay truncado a 150

        caudales = np.arange(self.Q_min, self.max_caudal_bombeo+1, 1)

        created_local_fig = False
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
            created_local_fig = True

        # Determinar si se grafican varios ángulos o solo uno
        if self.rango_angulo:
            angulos = np.arange(self.rango_angulo[0], self.rango_angulo[1] + 1, self.rango_angulo[2])
        else:
            angulos = [self.angulo_deg]

        for ang in angulos:
            viscosidades_marsh = []
            for Q_lpm in caudales:
                mu_marsh = calcular_viscosidad(ang, Q_lpm)
                viscosidades_marsh.append(mu_marsh)

            ax.plot(caudales, viscosidades_marsh, label=f"{ang}°", zorder=2)

        ax.grid(True, axis='both', linestyle='--' )
        
        for x in range(self.Q_min, self.max_caudal_bombeo+1, 10):
            ax.axvline(x, color='gray', linestyle=':', linewidth=0.4, zorder=0)

        ax.set_xlim(self.Q_min, self.max_caudal_bombeo)
        ax.set_xlabel("Caudal (L/min)", fontsize=10)
        ax.set_ylabel("Viscosidad crítica (s Marsh)", fontsize=10)
        ax.set_title(f"Viscosidad crítica vs Caudal – {self.diametro}", fontsize=11)
        ax.xaxis.set_major_locator(plt.MultipleLocator(10))
        ax.yaxis.set_major_locator(plt.MultipleLocator(10))
        ax.tick_params(axis='both', labelsize=8)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontfamily('monospace')

        ax.legend(
            loc='upper right',
            bbox_to_anchor=(1.0, 1.0),
            ncol=5,
            fontsize=8,
            frameon=True,
            title="Ángulo:",
            title_fontsize=8
        )
        
        ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(5))
        ax.grid(which='major', axis='both', linestyle='--')
        ax.grid(which='minor', axis='both', linestyle=':')

        if created_local_fig:
            fig.tight_layout()
            plt.show()
    
    def graficar_caudal_limite(self, ax=None):

        created_local_fig = False
        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 6))
            created_local_fig = True

        def calcular_viscosidad_caudal_fijo(Q_m3s, theta_deg):
            v_f = Q_m3s / self.Aa
            v_rel = -v_f

            Fd = -0.5 * self.rho_f * self.Cd * self.Af * v_rel * abs(v_rel)
            Fg = (self.rho_c - self.rho_f) * self.V * self.g * np.sin(np.radians(theta_deg))

            num = Fg - Fd
            den = (4 * abs(v_rel) / (self.r1 * (1 - (self.r1/self.r2)**2))) * self.Alat

            if den != 0:
                mu_Pa_s = num / den
            else:
                mu_Pa_s = np.nan

            mu_Pa_s = max(mu_Pa_s, 0.0)
            mu_marsh = mu_Pa_s * 1000 / 1.1 + 25
            return mu_marsh

        angulos = np.arange(0, 91, 1)

        if self.rango_caudal:
            caudales_lpm = np.arange(self.rango_caudal[0], self.rango_caudal[1] + 1, self.rango_caudal[2])
        else:
            caudales_lpm = [self.Q * 60000]

        todas_las_curvas = []

        for Q_lpm in caudales_lpm:
            Q_m3s = Q_lpm / 60000
            viscosidades_marsh = []
            for theta in angulos:
                mu_marsh = calcular_viscosidad_caudal_fijo(Q_m3s, theta)
                viscosidades_marsh.append(mu_marsh)

            todas_las_curvas.append(viscosidades_marsh)
            ax.plot(angulos, viscosidades_marsh, label=f"{round(Q_lpm,1)} L/min", zorder=2)

        # Ajustar el límite Y de acuerdo al máximo valor real
        mu_max_real = max(max(curva) for curva in todas_las_curvas)
        mu_max_plot = min(mu_max_real * 1.1, 160)

        for y in range(10, int(mu_max_plot)+10, 10):
            ax.axhline(y, color='gray', linestyle='--', linewidth=0.5, zorder=0)
        for x in range(10, 100, 10):
            ax.axvline(x, color='gray', linestyle=':', linewidth=0.4, zorder=0)

        ax.set_xlim(0, 90)
        ax.set_ylim(0, mu_max_plot)
        ax.set_xlabel("Ángulo (°)", fontsize=10)
        ax.set_ylabel("Viscosidad crítica (s Marsh)", fontsize=10)
        ax.set_title(f"Viscosidad crítica vs Ángulo – {self.diametro}", fontsize=11)
        ax.xaxis.set_major_locator(plt.MultipleLocator(10))
        ax.yaxis.set_major_locator(plt.MultipleLocator(10))
        ax.tick_params(axis='both', labelsize=8)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontfamily('monospace')

        ax.legend(
            loc='lower right',
            bbox_to_anchor=(1.0, 0.0),
            ncol=4,
            fontsize=8,
            frameon=True,
            title="Caudal:",
            title_fontsize=8
        )
        
        ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
        ax.grid(which='major', axis='both', linestyle='--')
        ax.grid(which='minor', axis='both', linestyle=':')

        if created_local_fig:
            fig.tight_layout()
            plt.show()

def main():
    parser = argparse.ArgumentParser(description="Simulador de testigo en perforación inclinada con todos los modos de análisis.")
    parser.add_argument("archivo_json", help="Archivo JSON con configuraciones por diámetro.")
    parser.add_argument("--graficar", action="store_true", help="Simulación dinámica con Runge-Kutta.")
    parser.add_argument("--graficar_viscosidad", action="store_true", help="Curvas de ángulo crítico vs caudal para varias viscosidades.")
    parser.add_argument("--graficar_angulo", action="store_true", help="Curvas de viscosidad vs caudal para varios ángulos.")
    parser.add_argument("--graficar_caudal", action="store_true", help="Curvas de viscosidad crítica vs ángulo para varios caudales.")
    args = parser.parse_args()

    with open(args.archivo_json) as f:
        config = json.load(f)

    modo_default = not (args.graficar or args.graficar_viscosidad or args.graficar_angulo or args.graficar_caudal)

    for diam in config:
        sim = SimuladorTestigo(config[diam], diam)

        if modo_default:
            # --- Gráfica integrada de 6 cuadros ---
            fig, axs = plt.subplots(3, 2, figsize=sim.figsize, sharex=False)

            # 1. Simular posición, velocidad, aceleración
            sim.graficar_simulacion(axs=axs[:, 0])

            # 2. Dibujar columna derecha
            sim.graficar_viscosidad_limite(ax=axs[0, 1])
            sim.graficar_angulo_limite(ax=axs[1, 1])
            sim.graficar_caudal_limite(ax=axs[2, 1])

            # 3. Ajuste general de escalas y etiquetas
            for i in range(3):
                axs[i, 0].tick_params(axis='both', labelsize=8)
                axs[i, 0].grid(True)
                axs[i, 0].set_xlabel("Tiempo (s)", fontsize=9)
                
                axs[i, 1].tick_params(axis='both', labelsize=8, labelbottom=True)
                axs[i, 1].grid(True)
                if i in [0, 1]:  # viscosidad vs caudal, ángulo vs caudal
                    axs[i, 1].set_xlabel("Caudal (L/min)", fontsize=9)
                    axs[i, 1].set_xlim(sim.Q_min, sim.Q_max)
                elif i == 2:  # caudal vs ángulo
                    axs[i, 1].set_xlabel("Ángulo (°)", fontsize=9)
                    axs[i, 1].set_xlim(0, 90)

            # 4. Subtítulos de la primera columna
            texto_unificado = sim.subtitulo_datos + "\n" + sim.subtitulo_resultados
            wrapped_text = textwrap.fill(texto_unificado, width=85)

            at = AnchoredText(
                wrapped_text,
                prop=dict(size=9),
                frameon=False,
                loc='upper left',
                bbox_to_anchor=(0.05, 0.93),
                bbox_transform=fig.transFigure,
                borderpad=0.0
            )
            fig.add_artist(at)

            # 5. Título general
            fig.suptitle(f"Simulación Numérica Explícita – {diam}", fontsize=16)

            # 6. Compactar
            plt.tight_layout(rect=[0.02, 0, 0.97, 0.96])
            plt.subplots_adjust(wspace=0.15, hspace=0.4)
            plt.show()

        else:
            # --- Modos separados normales ---
            if args.graficar:
                sim.graficar_simulacion()
            if args.graficar_viscosidad:
                sim.graficar_viscosidad_limite()
            if args.graficar_angulo:
                sim.graficar_angulo_limite()
            if args.graficar_caudal:
                sim.graficar_caudal_limite()

if __name__ == "__main__":
    main()
