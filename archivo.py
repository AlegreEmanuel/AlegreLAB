import requests

r = requests.get('https://www.frcon.utn.edu.ar/galileo/downld02.txt')

#print(r.headers)
#print(r.status_code)
#print(r.encoding)
#print(r.content)
#print(r.text)

#texto = str(r.content)
#textoLista = texto.split("\\r\\n")
#print(texto.split("\\r\\n"))

#print(len(textoLista))

texto = r.text.split("\r\n")
tamaño = len(texto)


array = texto[(tamaño-2)]
print("El dia "+array[0:8])
print("A la hora "+array[10:16])
print("La temperatura es "+array[18:23])


"""
for x in reversed(range(tamaño)):
    if(array[x]=="/"):
        if(array[x-3]=="/"):
            print("El dia "+array[x-5:x+3])
            print("A la hora "+array[x+5:x+10])
            print("La temperatura es "+array[x+13:x+17])

            break
"""