import os
from xml.etree import ElementTree as ET

def recopilar_archivos(ruta, recursos):
    archivos = []
    archivos_no_utilizados = []
    for root, dirs, files in os.walk(ruta):
        for file in files:
            archivo = os.path.relpath(os.path.join(root, file), ruta)
            archivos.append(archivo)
            # Comprobar si el archivo no está en los recursos definidos
            if archivo not in recursos:
                archivos_no_utilizados.append(archivo)
    return archivos, archivos_no_utilizados

def validar_archivos_necesarios(raiz_proyecto):
    # Lista de archivos necesarios en un proyecto SCORM
    archivos_necesarios = [
        "imsmanifest.xml",
    ]

    for elemento in archivos_necesarios:
        ruta_elemento = os.path.join(raiz_proyecto, elemento)
        if not os.path.exists(ruta_elemento):
            print(f"Error: No se encontró el elemento necesario '{elemento}'")
            return False

    print("La validación de los archivos necesarios se ha completado correctamente.")
    return True

def validar_imsmanifest(ruta_imsmanifest):
    try:
        tree = ET.parse(ruta_imsmanifest)
        root = tree.getroot()

        # Definir el espacio de nombres
        ns = {
            'ims': 'http://www.imsglobal.org/xsd/imscp_v1p1',
            'ns2': 'http://www.adlnet.org/xsd/adlcp_v1p3'
        }

        # Obtener todos los identifiers de los recursos definidos en imsmanifest.xml
        recursos = {resource.attrib['identifier'] for resource in root.findall(".//ims:resource", namespaces=ns)}

        # Obtener los identifierref de los items dentro de organization
        organization_items = root.findall(".//ims:organizations/ims:organization/ims:item", namespaces=ns)
        for item in organization_items:
            identifierref = item.attrib['identifierref']
            if identifierref not in recursos:
                print(f"Error: El identifierref '{identifierref}' no coincide con ningún identifier de recurso en imsmanifest.xml")
                return False

        #print("recursos:", recursos)
        #print("organization_items:", organization_items)
        print("La validación de imsmanifest.xml se ha completado correctamente.")
        return True

    except Exception as e:
        print(f"Error al analizar el archivo imsmanifest.xml: {e}")
        return False


if __name__ == "__main__":
    # Buscar imsmanifest.xml en el directorio actual
    ruta_actual = os.getcwd()
    ruta_imsmanifest = os.path.join(ruta_actual, "imsmanifest.xml")

    if not os.path.exists(ruta_imsmanifest):
        print("Error: No se encontró el archivo imsmanifest.xml en el directorio actual.")
    else:
        # Validar archivos necesarios
        if not validar_archivos_necesarios(ruta_actual):
            print("El proyecto SCORM no está completo o tiene errores.")
        else:
            # Validar imsmanifest.xml
            if not validar_imsmanifest(ruta_imsmanifest):
                print("El proyecto SCORM no está completo o tiene errores.")
            else:
                # Recopilar todos los archivos en el proyecto
                recursos = set()
                tree = ET.parse(ruta_imsmanifest)
                root = tree.getroot()
                for resource in root.findall(".//{http://www.imsglobal.org/xsd/imsmd_rootv1p2p1}resource"):
                    recursos.add(resource.attrib['identifier'])

                archivos, archivos_no_utilizados = recopilar_archivos(ruta_actual, recursos)
                
                print("Archivos encontrados en el proyecto:")
                for archivo in archivos:
                    print(archivo)

                if archivos_no_utilizados:
                    print("\nWarnings:")
                    for archivo_no_utilizado in archivos_no_utilizados:
                        print(f"Warning: El archivo '{archivo_no_utilizado}' no está siendo declarado en el paquete SCORM.")
                        
                print("\nEl proyecto SCORM está listo para ser subido al LMS.")