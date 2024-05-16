# 🚀 programmering.no | 🤓 matematikk.as
# S2 - Eksamen - 2023 Vår (Matematikk AS)
# Oppgave 3 a) Coca-Cola vs. Pepsi-Cola - 10 glass 

from scipy.stats import binom

n                   = 10      # Forsøk
p                   = 0.5     # Sannsynlighet
x_liste             = []      # Liste med verdiene til x
fordeling_liste     = []      # Liste med sannsynlighetsfordelingen til x
riktig              = 6       # Antall riktige
desimal             = 3       # Antall desimaler i avrunding

# Legger alle mulige x-verdier i listen: 0 -> 10
for i in range(n + 1):
    x_liste.append(i)

# Lager en liste med sannsynlighetsfordelingen
fordeling_liste = binom.pmf(x_liste, n, p)

# Lager en liste med sannsynlighetsfordelingen
fordeling_liste[riktig] = round(fordeling_liste[riktig], desimal)

# Print svaret
print(f"Sannsynlighet for å gjette 6 riktige: {fordeling_liste[riktig]}")
