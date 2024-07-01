# Tarea 1 Modulo 10 Reversing en sistemas operativos (Windows)	
# Mario German Gavira Gonzalez
# Script para ocultar un proceso usando DKOM

import pykd
import re

# Pedir como entrada el PID del proceso que se quiere ocultar
pid = input("Introducir el PID del proceso que se desea ocultar: ")

print("\nBuscando proceso con PID: " + pid + "\n")

# Obtener info del proceso
process_info = pykd.dbgCommand("!process " + str(hex(int(pid)))[2:] + " 0")

# Extraer la direccion de eprocess y el nombre del proceso
process_match = re.search(r"PROCESS (\w+)", process_info)
image_match = re.search(r"Image: (\w+\.\w+)", process_info)

# Mostrar informacion del proceso encontrado
if process_match and image_match:
    eprocess = process_match.group(1)
    process_name = image_match.group(1)
    print("Se ha encontrado el proceso: " + process_name + " con direccion eprocess: " + eprocess)
else:
    print("No se ha encontrado el proceso")

# Obtener direcciones de ActiveProcessLinks de los procesos anterior y posterior
ActiveProcessLinks = pykd.dbgCommand("dq " + eprocess + "+448 L2")
flink_ActiveProcessLinks = ActiveProcessLinks.split('  ')[1].split(' ')[0]
blink_ActiveProcessLinks = ActiveProcessLinks.split('  ')[1].split(' ')[1]

# Obtener los nombres de los procesos anterior y posterior y los PIDs
# FLINK
flink = pykd.dbgCommand("da " + flink_ActiveProcessLinks + "-448+5a8")
flink_pid = pykd.dbgCommand("dd " + flink_ActiveProcessLinks + "-448+440 L1")
print("\nEl nombre del proceso posterior es: " + flink.split('"')[1] + " con PID: " + flink_pid.split('  ')[1].lstrip('0'))
# BLINK
blink = pykd.dbgCommand("da " + blink_ActiveProcessLinks + "-448+5a8")
blink_pid = pykd.dbgCommand("dd " + blink_ActiveProcessLinks + "-448+440 L1")
print("El nombre del proceso anterior es: " + blink.split('"')[1] + " con PID: " + blink_pid.split('  ')[1].lstrip('0'))

# Modificar los valores de FLINK y BLINK para ocultar el proceso
print("\nOcultando el proceso: " + process_name)
pykd.dbgCommand("eq " + blink_ActiveProcessLinks + " " + flink_ActiveProcessLinks)
pykd.dbgCommand("eq " + flink_ActiveProcessLinks + "+8 " + blink_ActiveProcessLinks)
print("\nProceso ocultado con exito!")