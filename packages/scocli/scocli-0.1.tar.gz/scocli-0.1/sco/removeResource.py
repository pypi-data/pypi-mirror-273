import os
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom

def prettify_xml(elem):
    """Retorna una versión con formato legible del elemento XML"""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    lines = []
    for node in reparsed.childNodes:
        if node.nodeType == node.COMMENT_NODE:
            lines.append("<!--{}-->".format(node.data))
        else:
            lines.append(node.toxml())
    return "\n".join(lines)

def remove_resource_from_imsmanifest(resource_id):
    # Buscar el archivo imsmanifest.xml en el directorio actual
    current_directory = os.getcwd()
    xml_file = os.path.join(current_directory, "imsmanifest.xml")

    # Verificar si el archivo XML existe
    if not os.path.exists(xml_file):
        print("El archivo imsmanifest.xml no se encuentra en el directorio actual.")
        sys.exit(1)

    # Parsear el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Encontrar el elemento de recursos
    resources = root.find("./{http://www.imsglobal.org/xsd/imscp_v1p1}resources")
    if resources is None:
        print("No se encontraron recursos en el archivo imsmanifest.xml.")
        sys.exit(1)

    # Buscar el recurso específico por su identificador y eliminarlo
    resource_to_remove = resources.find(f"./{{http://www.imsglobal.org/xsd/imscp_v1p1}}resource[@identifier='{resource_id}']")
    if resource_to_remove is None:
        print(f"No se encontró el recurso con el identificador '{resource_id}' en el archivo imsmanifest.xml.")
        sys.exit(1)

    resources.remove(resource_to_remove)

    # Escribir el árbol XML en el archivo imsmanifest.xml con formato legible
    with open(xml_file, "wb") as f:
        f.write(prettify_xml(root).encode('utf-8'))

    print(f"Recurso con identificador '{resource_id}' eliminado del archivo imsmanifest.xml.")

def main():
    # Verificar que se pasó el argumento correctamente
    if len(sys.argv) != 2:
        print("Uso: python script.py <identificador_recurso>")
        sys.exit(1)

    resource_id = sys.argv[1]

    # Eliminar el recurso del imsmanifest.xml
    remove_resource_from_imsmanifest(resource_id)

if __name__ == "__main__":
    main()
