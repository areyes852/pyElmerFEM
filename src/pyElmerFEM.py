# -*- coding: utf-8 -*-

import vtk
import struct


def leer_elements():
    # Código
    print()


def leer_boundary():
    # Código
    print()


def leer_header():
    # Código
    print()


def leer_nodes():
    # Código
    print()


def abrir_vtu(archivo):
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(archivo)
    reader.Update()  # Needed because of GetScalarRange
    return reader.GetOutput().GetPointData()


def lista_vtu_props(output):
    props = []
    p = []
    propiedad = ''
    bol = 0
    # Só hai iguales nas liñas que inclúen o nome da propiedade.
    # Se atopo un = añado os carácteres á propiedade ata atopar un salto de liña

    for c in str(output):
        if c == '\n' and bol == 1:
            bol = 0
            propiedad = ''.join(p).strip()
            props.append(propiedad)
            p = []
        if bol == 1:
            p.append(c)
        if c == '=':
            bol = 1
    return props


def obter_raw_vtu(archivo):
    # NON SEI SE ESTO FUNCONA SEMPRE!
    # O ficheiro vtu ten unha cabeceira en xml e a continuación un bloque en binario
    # As únicas líneas que parece que varía entre archivos son as de propiedades.
    # Polo tanto, as líneas de cabeceira deben ser LINEAS_FIXAS + NUM_PROPIEDADES
    # A maiores hai 3 líneas de texto (xml) ó final.
    # LÍÑAS FIXAS = 20
    liñas_fixas = 20
    num_props = len(lista_vtu_props(abrir_vtu(archivo)))
    liñas_texto = liñas_fixas + num_props

    with open(archivo, 'rb') as f:
        for line in range(liñas_texto):
            f.readline()
        raw = f.read()
    # Non necesito chegar ata a final do archivo (creo), así que as líneas finais non
    # estorban
    return raw


def bin_offset_prop(output,propiedades):
    offset_anterior = 0
    offsets = [0]
    for propiedade in propiedades:
        tamaño = output.GetArray(propiedade).GetSize() # Tamaño xa ten en conta o número de compoñentes que hai en cada propiedade
        tipo = output.GetArray(propiedade).GetDataType()
        # ncomp = output.GetArray(propiedade).GetNumberOfComponents()
        if tipo == 11:
            offset = offset_anterior +tamaño*8 + 4 # Hai catro bits que sobran entre cada propiedade
            offset_anterior = offset
            offsets.append(offset)
        else:
            offset = 0
    return offsets


def obter_valores(raw,offsets,ncomp):
    n = len(offsets)
    vals = []
    for i in range(n-1):
        nc = ncomp[i]
        offset = offsets[i]+4+1 # Nin idea de onde sae ese +1
        fin = offsets[i+1]
        dat_raw=[]
        while offset < fin:
            a=struct.unpack_from("<dd",raw,offset=offset) # 2 valores por lectura
            dat_raw.append(a[0])
            dat_raw.append(a[1])
            offset = offset + 8
        dat_raw.pop() # Hai un último dato que non sei que é, pero non é un valor válido
        dat_subdiv=[]
        if nc > 1:
            for j in range(0,len(dat_raw),nc):
                dat_subdiv.append(dat_raw[j:j+nc])
        else:
            dat_subdiv=dat_raw
        vals.append(dat_subdiv)
    return vals

def obter_ncomp(output,propiedades):
    ncomps = []
    for i in range(len(propiedades)): ncomps.append(output.GetArray(propiedades[i]).GetNumberOfComponents())
    return ncomps


if __name__ == "__main__":
    archivo = "../muestras/case0001.vtu"
    obter_raw_vtu(archivo)
    output = abrir_vtu(archivo)
    lista_props = lista_vtu_props(output)
    offsets = bin_offset_prop(output,lista_props)
    raw = obter_raw_vtu(archivo)
    ncomp = obter_ncomp(output,lista_props)
    print(obter_valores(raw,offsets,ncomp))
