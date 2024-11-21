import matplotlib.pyplot as plt
import numpy as np

# Datos estimados
labels = ['Cifrado', 'Descifrado']
time_ascon = [1.5, 1.3]  # en ms
time_elgamal = [8, 7]  # en ms

cpu_usage = [15, 45]  # en porcentaje
memory_sizes = ['256 bytes', '512 bytes', '1024 bytes']
memory_ascon = [5, 7, 10]  # en MB
memory_elgamal = [12, 18, 30]  # en MB

energy_ascon = [20] * 3  # en mW
energy_elgamal = [50] * 3  # en mW

security_categories = ['Fuerza Bruta', 'Criptoanálisis', 'Ataques Laterales']
security_ascon = [10, 9, 8]
security_elgamal = [10, 10, 6]

# Gráfico 1: Tiempo de cifrado y descifrado
x = np.arange(len(labels))
width = 0.35

plt.figure(figsize=(8, 5))
plt.bar(x - width / 2, time_ascon, width, label='ASCON')
plt.bar(x + width / 2, time_elgamal, width, label='ElGamal')
plt.ylabel('Tiempo (ms)')
plt.title('Tiempo de Cifrado y Descifrado')
plt.xticks(x, labels)
plt.legend()
plt.show()

# Gráfico 2: Uso de CPU
plt.figure(figsize=(8, 5))
bars = plt.bar(['ASCON', 'ElGamal'], cpu_usage, color=['blue', 'orange'])
plt.ylabel('Uso de CPU (%)')
plt.title('Uso de CPU en Operaciones Criptográficas')
for bar in bars:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 5, f'{bar.get_height()}%', ha='center', color='white')
plt.show()

# Gráfico 3: Uso de memoria
x = np.arange(len(memory_sizes))
plt.figure(figsize=(8, 5))
plt.plot(x, memory_ascon, marker='o', label='ASCON')
plt.plot(x, memory_elgamal, marker='o', label='ElGamal')
plt.xticks(x, memory_sizes)
plt.ylabel('Uso de Memoria (MB)')
plt.title('Uso de Memoria vs Tamaño de Mensaje')
plt.legend()
plt.show()

# Gráfico 4: Seguridad
x = np.arange(len(security_categories))
plt.figure(figsize=(8, 5))
plt.bar(x - width / 2, security_ascon, width, label='ASCON')
plt.bar(x + width / 2, security_elgamal, width, label='ElGamal')
plt.xticks(x, security_categories)
plt.ylabel('Puntaje de Seguridad')
plt.title('Comparación de Seguridad')
plt.legend()
plt.show()

# Gráfico 5: Consumo Energético
plt.figure(figsize=(8, 5))
x = np.arange(len(memory_sizes))
plt.plot(x, energy_ascon, marker='o', label='ASCON')
plt.plot(x, energy_elgamal, marker='o', label='ElGamal')
plt.xticks(x, memory_sizes)
plt.ylabel('Consumo Energético (mW)')
plt.title('Consumo Energético vs Tamaño de Mensaje')
plt.legend()
plt.show()

