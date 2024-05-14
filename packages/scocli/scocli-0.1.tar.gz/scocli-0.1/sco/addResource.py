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

def find_or_create_element(root, xpath, element_tag):
    """Encuentra o crea un elemento en el árbol XML"""
    element = root.find(xpath)
    if element is None:
        element = ET.SubElement(root, element_tag)
    return element

def add_files_to_resource(resource, files):
    """Agrega archivos a un recurso"""
    for file_path in files:
        if not os.path.exists(file_path):
            print("El archivo " + file_path + " no existe")
            sys.exit(1)
        file_name = os.path.basename(file_path)
        existing_file = resource.find(f"./{{http://www.imsglobal.org/xsd/imscp_v1p1}}file[@href='{file_name}']")
        if existing_file is None:
            file_element = ET.SubElement(resource, "{http://www.imsglobal.org/xsd/imscp_v1p1}file")
            file_element.set("href", file_name)
            file_element.tail = '\n'  # Agregar salto de línea después de la etiqueta <file>

def add_resource_to_imsmanifest(files):
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

    # Encontrar o crear el elemento de recursos
    resources = find_or_create_element(root, "./{http://www.imsglobal.org/xsd/imscp_v1p1}resources", "{http://www.imsglobal.org/xsd/imscp_v1p1}resources")

    # Encontrar o crear el elemento de organización
    organization = find_or_create_element(root, "./{http://www.imsglobal.org/xsd/imscp_v1p1}organizations/{http://www.imsglobal.org/xsd/imscp_v1p1}organization", "{http://www.imsglobal.org/xsd/imscp_v1p1}organization")

    # Verificar si el resource ya existe
    identifier = os.path.splitext(os.path.basename(files[0]))[0] if len(files) > 1 else input("Ingrese el identificador del recurso (o presione Enter para usar el nombre del archivo principal sin extensión): ")
    existing_resource = resources.find(f"./{{http://www.imsglobal.org/xsd/imscp_v1p1}}resource[@identifier='{identifier}']")
    if existing_resource is not None:
        # El resource ya existe, agregar solo los archivos que faltan
        add_files_to_resource(existing_resource, files)
        existing_resource.tail = '\n'  # Agregar salto de línea después de la etiqueta <resource>
    else:
        # El resource no existe, crear uno nuevo y agregar archivos
        new_resource = ET.SubElement(resources, "{http://www.imsglobal.org/xsd/imscp_v1p1}resource")
        new_resource.set("identifier", identifier)
        new_resource.set("type", "webcontent")
        new_resource.set("{http://www.adlnet.org/xsd/adlcp_v1p3}scormType", "sco")
        new_resource.set("href", files[0])
        add_files_to_resource(new_resource, files)

        # Crear un ítem de recurso en la sección de organización
        item = ET.SubElement(organization, "{http://www.imsglobal.org/xsd/imscp_v1p1}item")
        item.set("identifier", "item_" + identifier)
        item.set("identifierref", identifier)
        title = input(f"Ingrese el título del recurso '{identifier}' (o presione Enter para omitir): ")
        if title:
            title_element = ET.SubElement(item, "{http://www.imsglobal.org/xsd/imscp_v1p1}title")
            title_element.text = title

        new_resource.tail = '\n'  # Agregar salto de línea después de la etiqueta <resource>
        # Write the XML tree to the imsmanifest.xml file with readable formatting
        ET.register_namespace("", "http://www.imsglobal.org/xsd/imscp_v1p1")
        ET.indent(tree, '  ')   # Indentar el árbol XML

    # Escribir el árbol XML en el archivo imsmanifest.xml con formato legible
    with open(xml_file, "wb") as f:
        f.write(prettify_xml(root).encode('utf-8'))

    print(f"Archivos {', '.join(files)} añadidos al archivo imsmanifest.xml.")

def main():
    # Verificar que se pasó al menos un argumento
    if len(sys.argv) < 2:
        print("Uso: python script.py <archivo1> <archivo2> ...")
        sys.exit(1)

    files = sys.argv[1:]

    # Verificar si los archivos existen
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"El archivo {file_path} no existe.")
            sys.exit(1)

    # Agregar los archivos al imsmanifest.xml
    add_resource_to_imsmanifest(files)

if __name__ == "__main__":
    main()
