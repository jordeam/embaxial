"""Script to eval emf in one coil."""

import math

# Constants
HP: float = 745  # one horse power in watts
rho_al: float = 0.0282e-6  # aluminum resistivity in Ohm.m
rho_copper: float = 0.0172e-6  # copper resitivity in Ohm.m

# Parameters
rho_cond: float = rho_al  # electric resistivity of used conductor material
x_insul: float = 0.2e-3  # dielectric insulation thickness of conductor
P_shaft: float = 65 * HP  # Power available in shaft, after fiction losses
c_fric: float = 0.05  # relative estimated friction losses in
r_int: float = 0.9  # internal radius im m
w_tooth: float = 36.0e-3  # tooth tickness
w_tip: float = 3e-3  # tooth tip entrance
x_tooth: float = 4e-3  # interval between teeth or sloth openning
rpm: float = 1600.0  # angular speed in rpm
B_mag: float = 0.9  # magnet flux density in T
N_slots: int = 48  # number of slots
N_par: int = 1  # number of circuits in parallel
N_serie: int = 8  # number of circuits in series
N_turns: int = 2  # number of turns per tooth
N_circ: int = 8  # number of total circuits
N_poles: int = 40  # number of magnet poles
d_curr: float = 30e6  # current density in A/m2

# directly evaluated parameters
P_mec: float = P_shaft / (1.0 - c_fric)  # total shaft mechanical power
omega: float = rpm * math.pi / 30  # rotor angular speed in rad/s
r_ext: float = r_int + w_tooth  # external radius
r_avg: float = (r_int + r_ext) / 2  # average radius
d_slots: float = 2 * math.pi * r_avg / N_slots  # distance between slots
l_total = 2 * math.pi * r_avg  # total average circunference length
l_tooth: float = d_slots - x_tooth  # average tooth length
speed: float = omega * r_avg  # tangential or linear speed
f_op: float = omega / (2 * math.pi) * N_poles / 2  # steel magnetic operational frequency Hz
A_tooth: float = w_tooth * l_tooth  # tooth airgap area
flux_1c: float = A_tooth * B_mag  # flux per turn, suposing all tooth area covered by magnet

e_1c: float = 2 * speed * flux_1c / d_slots  # voltage per coil turn

e_T: float = N_serie * N_turns * e_1c  # total voltage, considering number of circuits and number of coil turns

I_m: float = P_mec / (2 * e_T * N_par)  # six-step current amplitude per phase
I_R: float = math.sqrt(2.0 / 3) * I_m  # RMS phase current
I_coil: float = I_m / N_par  # current in one coil wire
A_wire: float = I_coil / d_curr  # cross sectional area of coil wire
r_wire: float = math.sqrt(A_wire / math.pi)  # wire radius
l_wire: float = N_turns * (2 * (l_tooth + w_tooth - 4 * w_tip) + 2 * math.pi * (r_wire + x_insul))  # total conductor length per coil
R_coil: float = N_turns * rho_cond * l_wire / A_wire  # resistence of one coil
R_phase: float = N_serie * R_coil / N_par  # Phase resistence
P_loss1: float = (I_R ** 2) * R_phase  # Joule power loss in one phase
P_loss: float = 3 * P_loss1  # Total Joule power loss
effic: float = P_mec / (P_mec + P_loss)  # power efficiency without frictional losses

if N_par * N_serie != N_circ:
    print(f'Error: number of circuits in parallel({N_par}) and series ({N_serie}) must match number of circuits({N_circ}).')


print(f'Magnetic density flux = {B_mag} T')
print(f'Tooth area = {A_tooth*1e4} cm2')
print(f'Total average circunference length = {2*math.pi*r_avg} m')
print(f'Distance between consecutive slots = {d_slots} m')
print(f'Circuit linear length = {l_total/N_circ}')
print(f'Tooth length = {l_tooth} m')
print(f'Number of circuits in series = {N_serie}')
print(f'Number of circuits in arallel = {N_par}')
print(f'Number of circuits of total circuits = {N_circ}')
print(f'Number of turns = {N_turns}')
print(f'Average radius {r_avg} m')
print(f'Angular speed = {omega} rad/s')
print(f'Steel magnetic operational frequency = {f_op} Hz')
print(f'Tangential speed = {speed} m/s')
print(f'Estimated turn BMEF amplitude = {e_1c} V')
print(f'Estimated phase BEMF amplitude = {e_T} V')
print(f'Current amplitude in one phase = {I_m} A')
print(f'Current RMS in one phase = {I_R} A')
print(f'Wire area = {A_wire * 1*6} mm2')
print(f'Wire diameter = {r_wire * 2e3} mm')
print(f'Coil resistence = {R_coil} Ohm')
print(f'Coil wire length = {l_wire*1e3} mm')
print(f'Resistive power loss in all phases = {P_loss} W')
print(f'Overall power efficiency = {effic*100} % without frictional losses')
