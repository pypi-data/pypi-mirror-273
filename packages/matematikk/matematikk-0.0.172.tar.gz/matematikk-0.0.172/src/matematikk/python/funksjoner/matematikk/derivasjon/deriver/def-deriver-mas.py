from matematikk import diff

def deriver(uttrykk, vari):

	uttrykk_derivert = diff(uttrykk, vari) 

	return uttrykk_derivert

# Alias > 1
derivert                        = diff
momentan_vekst                  = diff
momentan_vekstfart              = diff

# Alias > 2 > ...
