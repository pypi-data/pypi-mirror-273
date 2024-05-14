import xml.etree.ElementTree as ET

def print_manifest_tree(manifest_path, indent=0):
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    print_element(root, indent)

def print_element(element, indent):
    tag = element.tag.split("}")[1] if "}" in element.tag else element.tag
    value = element.text.strip() if element.text else None
    if tag == "resource":
        identifier = element.attrib.get("identifier", "")
        print(" " * indent + f"{tag} {identifier}")
    elif tag == "file":
        file_name = element.attrib.get("href", "")
        file_name = file_name.split("/")[-1]  # Solo el nombre del archivo
        print(" " * (indent + 2) + f"file: {file_name}")
    else:
        print(" " * indent + tag + (f": {value}" if value else ""))
    for child in element:
        print_element(child, indent + 2)

def main():
    manifest_path = "imsmanifest.xml"  # Cambia esto al path de tu archivo imsmanifest.xml
    print_manifest_tree(manifest_path)

if __name__ == "__main__":
    main()
    