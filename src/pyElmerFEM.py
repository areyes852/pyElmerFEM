# -*- coding: utf-8 -*-

import vtk

def leer_vtu(archivo):
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(archivo)
    reader.Update()  # Needed because of GetScalarRange
    output = reader.GetOutput().GetPointData()
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

    for i in props:
        a = output.GetScalars(i)
        print(a)
    print(props)

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

if __name__ == "__main__":
    archivo = "../muestras/case0001.vtu"
    leer_vtu(archivo)
