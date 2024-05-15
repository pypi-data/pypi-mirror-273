# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Matematikk AS)
# Oppgave 4 a) Aritmetisk- og geometrisk rekke - Ukentlig beløp de 4 første ukene 

lonn_0      = 100       # Ukelønn første uke
a_n         = lonn_0    # Tilbud 1: Ukelønn første uke
a_d         = 10        # Tilbud 1: Aritmetisk økning (differanse)
g_n         = lonn_0    # Tilbud 2: Ukelønn første uke
g_k         = 1.05      # Tilbud 2: Geometrisk økning (kvotient)
uker        = 4         # Antall uker
desimal     = 2         # Antall desimaler i avrunding

# Print-funksjon
def printing(i, belop): print(f"Tilbud 1 | Uke {i} | Beløp: {round(belop, desimal)}")

# Oppgave a)
print("Oppg a)")

# Aritmetisk rekke
for i in range(1, uker + 1): printing(i, a_n); a_n += a_d

# Geometrisk rekke
print("")
for i in range(1, uker + 1): printing(i, g_n); g_n *= g_k
