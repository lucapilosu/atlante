# Pagine Wikipedia (en, it) e parole chiave per le 31 voci della v0.75 (foto nella v0.76)
import json
M = {
 "event-aids-epidemic": (["HIV/AIDS", "Red ribbon", "NAMES Project AIDS Memorial Quilt", "History of HIV/AIDS"], ["AIDS", "Nastro rosso"], ["ribbon", "quilt", "memorial", "aids", "hiv"]),
 "event-bretton-woods": (["Bretton Woods Conference", "Mount Washington Hotel"], ["Conferenza di Bretton Woods"], ["bretton", "mount washington", "hotel"]),
 "event-1968-protests": (["Protests of 1968", "May 68"], ["Sessantotto", "Maggio francese"], ["1968", "mai 68", "may 68", "sorbonne", "poster", "affiche", "barricade", "atelier populaire"]),
 "event-wto-globalization": (["World Trade Organization", "Centre William Rappard"], ["Organizzazione mondiale del commercio"], ["wto", "omc", "rappard", "marrakesh", "marrakech"]),
 "event-chernobyl": (["Chernobyl disaster", "Chernobyl Nuclear Power Plant", "Pripyat", "Chernobyl New Safe Confinement"], ["Disastro di Černobyl'", "Pryp'jat'"], ["chernobyl", "chornobyl", "pripyat", "prypiat", "reactor", "confinement", "sarcophagus"]),
 "event-solidarnosc": (["Solidarity (Polish trade union)", "Gdańsk Shipyard", "Monument to the Fallen Shipyard Workers 1970", "European Solidarity Centre"], ["Solidarność"], ["solidarno", "solidarity", "stocznia", "shipyard", "gdańsk", "gdansk", "21 postulat"]),
 "event-carnation-revolution": (["Carnation Revolution", "Largo do Carmo", "25 de Abril Bridge"], ["Rivoluzione dei garofani"], ["cravo", "carnation", "25 de abril", "carmo", "chaimite", "revolução", "revolucao"]),
 "event-italo-ethiopian-war": (["Second Italo-Ethiopian War", "Obelisk of Axum"], ["Guerra d'Etiopia"], ["ethiopia", "etiopia", "abyssinia", "abissinia", "axum", "aksum", "adwa", "propaganda"]),
 "event-angola-mozambique-1975": (["Angolan War of Independence", "Mozambican War of Independence", "Agostinho Neto Mausoleum", "Fortaleza de São Miguel"], ["Guerra d'indipendenza angolana"], ["angola", "luanda", "mozambique", "moçambique", "maputo", "neto", "independence", "independência"]),
 "event-congo-wars": (["First Congo War", "Second Congo War", "Goma"], ["Prima guerra del Congo", "Seconda guerra del Congo"], ["congo", "goma", "kivu", "monuc", "kinshasa", "bukavu"]),
 "event-qaddafi-libya": (["Muammar Gaddafi", "Libyan Arab Jamahiriya", "Bab al-Azizia", "Great Man-Made River"], ["Jamahiriya Araba Libica"], ["jamahiriya", "azizia", "man-made river", "tripoli", "libya", "green book", "libia"]),
 "event-armenian-genocide": (["Armenian genocide", "Tsitsernakaberd", "Armenian Genocide Memorial"], ["Genocidio armeno", "Tsitsernakaberd"], ["tsitsernakaberd", "memorial", "genocide", "eternal flame", "forget-me-not"]),
 "event-sykes-picot": (["Sykes–Picot Agreement", "San Remo conference", "Mandate for Mesopotamia"], ["Accordo Sykes-Picot"], ["sykes", "picot", "sanremo", "san remo", "mandate", "devachan"]),
 "event-six-day-war": (["Six-Day War", "Western Wall", "Golan Heights"], ["Guerra dei sei giorni"], ["six-day", "six day", "1967", "golan", "western wall", "sinai", "quneitra"]),
 "event-sri-lanka-civil-war": (["Sri Lankan civil war", "Jaffna Fort", "Jaffna Public Library"], ["Guerra civile in Sri Lanka"], ["sri lanka", "jaffna", "mullaitivu", "kilinochchi", "library", "fort"]),
 "event-bhopal-disaster": (["Bhopal disaster", "Union Carbide India Limited"], ["Disastro di Bhopal"], ["bhopal", "union carbide", "memorial", "factory", "plant"]),
 "event-korea-japanese-rule": (["Korea under Japanese rule", "Japanese General Government Building, Seoul", "Seodaemun Prison", "March 1st Movement"], ["Corea sotto il dominio giapponese"], ["government-general", "general government", "seodaemun", "gyeongbok", "chosen", "keijo", "keijō", "1919"]),
 "event-long-march": (["Long March", "Luding Bridge", "Yan'an"], ["Lunga marcia"], ["long march", "luding", "yan'an", "yanan", "zunyi", "长征", "泸定"]),
 "event-great-leap-forward": (["Great Leap Forward", "People's commune", "Backyard furnace"], ["Grande balzo in avanti"], ["great leap", "furnace", "commune", "大跃进", "poster", "propaganda", "steel"]),
 "event-second-sino-japanese-war": (["Second Sino-Japanese War", "Marco Polo Bridge", "Battle of Shanghai", "Memorial Hall of the Victims in Nanjing Massacre by Japanese Invaders"], ["Seconda guerra sino-giapponese"], ["marco polo", "lugou", "sino-japanese", "shanghai", "memorial hall", "卢沟"]),
 "event-mongolian-revolution": (["Mongolian Revolution of 1921", "Sükhbaatar Square", "Damdin Sükhbaatar"], ["Rivoluzione mongola del 1921"], ["sükhbaatar", "sukhbaatar", "suhbaatar", "1921", "ulaanbaatar", "ulan bator", "square"]),
 "event-kazakh-famine": (["Kazakh famine of 1930–1933", "Asharshylyk"], ["Carestia kazaka del 1930-1933"], ["asharshylyk", "famine", "ашаршылық", "memorial", "monument", "kazakh"]),
 "event-central-asia-independence": (["Dissolution of the Soviet Union", "Independence Monument (Almaty)", "Independence Monument (Tashkent)"], ["Dissoluzione dell'Unione Sovietica"], ["independence", "mustaqillik", "almaty", "tashkent", "monument", "alma-ata", "ashgabat", "bishkek", "dushanbe"]),
 "event-japanese-occupation-southeast-asia": (["Japanese occupation of Malaya", "Japanese occupation of Singapore", "Japanese occupation of the Dutch East Indies", "Greater East Asia Co-Prosperity Sphere"], ["Sfera di co-prosperità della Grande Asia orientale"], ["occupation", "japanese", "banana money", "invasion money", "syonan", "co-prosperity", "kranji", "propaganda"]),
 "event-burma-independence": (["Burma independence", "Independence Monument (Yangon)", "Maha Bandula Park", "Secretariat (Yangon)"], ["Birmania"], ["independence", "maha bandula", "secretariat", "yangon", "rangoon", "monument"]),
 "event-east-timor-independence": (["East Timor independence referendum", "1999 East Timorese crisis", "Dili"], ["Timor Est"], ["timor", "dili", "referendum", "1999", "2002", "independence"]),
 "event-asian-financial-crisis": (["1997 Asian financial crisis", "Sathorn Unique Tower", "Thai baht"], ["Crisi finanziaria asiatica"], ["sathorn", "baht", "ghost tower", "crisis", "1997", "rupiah", "won"]),
 "event-caribbean-independence-1962": (["Jamaica", "Trinidad and Tobago", "West Indies Federation", "Emancipation Park"], ["Giamaica", "Trinidad e Tobago"], ["jamaica", "trinidad", "kingston", "port of spain", "red house", "independence", "1962", "stamp"]),
 "event-chaco-war": (["Chaco War", "Fortín Boquerón"], ["Guerra del Chaco"], ["chaco", "boquerón", "boqueron", "fortín", "fortin", "bolivia", "paraguay", "nanawa"]),
 "event-brazil-military-dictatorship": (["Military dictatorship in Brazil", "Brazilian Truth Commission", "Tortura Nunca Mais"], ["Dittatura militare brasiliana"], ["ditadura", "dictatorship", "1964", "diretas", "brasília", "planalto", "monument"]),
 "event-mabo-decision": (["Mabo v Queensland (No 2)", "Mer Island", "Eddie Mabo"], ["Sentenza Mabo"], ["mabo", "mer island", "murray island", "torres strait", "high court", "native title"]),
}
D = json.load(open('tools/voci/nuove_v075.json'))
N = {r['id']: r['name'] for r in D}
assert set(M) == set(N), set(M) ^ set(N)
out = {k: {'en': en, 'it': it, 'kw': kw, 'n': N[k]} for k, (en, it, kw) in M.items()}
json.dump(out, open('tools/foto/v073/mappa4.json', 'w'), ensure_ascii=False)
print(len(out))
