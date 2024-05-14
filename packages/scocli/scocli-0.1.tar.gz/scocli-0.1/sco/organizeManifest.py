import sys
import os
from xml.etree import ElementTree as ET

def reorganize_organization(manifest_xml, item_identifier, new_position):
    # Define namespaces
    namespaces = {
        "": "http://www.imsglobal.org/xsd/imscp_v1p1"
    }
    
    # Register the namespace
    ET.register_namespace("", namespaces[""])
    
    # Parse the XML
    root = ET.fromstring(manifest_xml)
    
    # Find the organization element
    organization = root.find(".//organization", namespaces)
    
    # Find the item to be reorganized
    item_to_move = organization.find(".//item[@identifier='" + item_identifier + "']", namespaces)
    
    # Raise an error if the item is not found
    if item_to_move is None:
        raise ValueError("Item with identifier '{}' not found in the organization.".format(item_identifier))
    
    # Remove the item from its current position
    organization.remove(item_to_move)
    
    # Insert the item at the new position
    organization.insert(new_position, item_to_move)
    
    # Serialize the modified XML back to string
    new_manifest_xml = ET.tostring(root, encoding='unicode')
    
    return new_manifest_xml

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python reorganize_manifest.py <item_identifier> <new_position>")
        sys.exit(1)

    item_identifier = sys.argv[1]
    new_position = int(sys.argv[2])

    # Check if imsmanifest.xml exists in the current directory
    manifest_path = "imsmanifest.xml"
    if not os.path.exists(manifest_path):
        print("Error: imsmanifest.xml not found in the current directory.")
        sys.exit(1)

    # Read the contents of imsmanifest.xml
    with open(manifest_path, 'r') as file:
        manifest_xml = file.read()

    try:
        # Perform reorganization
        new_manifest_xml = reorganize_organization(manifest_xml, item_identifier, new_position)

        # Write the modified XML back to imsmanifest.xml
        with open(manifest_path, 'w') as file:
            file.write(new_manifest_xml)

        print("Organization reorganized successfully.")

    except ValueError as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()