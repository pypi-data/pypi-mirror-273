# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Matematikk AS)
# Oppgave 4 b) Aritmetisk- og geometrisk rekke - Uker før tilbud 2 gir mer ukelønn enn tilbud 1 

lonn_0      = 100       # Ukelønn første uke
a_n         = lonn_0    # Tilbud 1: Ukelønn første uke
a_d         = 10        # Tilbud 1: Aritmetisk økning (differanse)
g_n         = lonn_0    # Tilbud 2: Ukelønn første uke
g_k         = 1.05      # Tilbud 2: Geometrisk økning (kvotient)
uker        = 1         # Antall uker
desimal     = 2         # Antall desimaler i avrunding

# Print-funksjon
def printing_rader(i, tilbud, belop): print(f"Uke {i} | Tilbud {tilbud} | Beløp: {round(belop, desimal)}")

# Oppgave b)
print("Oppg b)")

# Kjøres så lenge geometrisk ukelønn er lavere enn aritmetisk
while g_n <= a_n:
    printing_rader(uker, "1 (A)", a_n); a_n += a_d  # Aritmetisk formel
    printing_rader(uker, "2 (G)", g_n); g_n *= g_k  # Geometrisk formel
    print("")                                       # Blank linje
    uker += 1                                       # Uker øker med 1

# Print svar
print(f"Etter {uker} uker er geometrisk ukelønn størst ({round(g_n, desimal)} > {a_n})")
