import os
import sys
import json
from string import Template

# Add parent directory to path to import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.json_parser_functions import get_transformation_dp_values
from utils.library_functions import get_library_transformation_name, get_library_transformation_names
from jinja2 import Template as JinjaTemplate
from utils.logger import print_and_log



def _parse_single_contract(contract, contract_type, column_name):
    """
    Parsea un único contrato y lo convierte al formato esperado.
    
    Args:
        contract (dict): El contrato a parsear
        contract_type (str): PRECONDITION, POSTCONDITION, INVARIANT
        column_name (str): Nombre de la columna
    
    Returns:
        dict: Contrato parseado
    """
    # Detectar si el contrato tiene "type" directamente o "contract_type"
    contract_kind = contract.get("type", contract.get("contract_type", "value_range"))
    name = contract.get("name", "")
    
    # Crear estructura base del contrato
    parsed_contract = {
        "type": contract_kind,
        "name": name,
        "column": column_name,
    }
    
    # Parsear detalles según el tipo de contrato
    # Si hay un objeto "details", usar ese; si no, usar el contrato directamente
    details = contract.get("details", contract)
    
    if contract_kind == "value_range":
        parsed_contract.update({
            "check": details.get("check", ""),
            "target_type": details.get("target_type", ""),
            "belong_op": details.get("belong_op", ""),
            "field": "input" if contract_type == "PRECONDITION" else "output"
        })
    
    elif contract_kind == "condition":
        if_clause = details.get("if", {})
        then_clause = details.get("then", {})
        parsed_contract.update({
            "if": {
                "condition_type": if_clause.get("condition_type", "special_value"),
                "belong_op": if_clause.get("belong_op", "NOTBELONG"),
                "target_type": if_clause.get("target_type", "")
            },
            "then": {
                "result_type": then_clause.get("result_type", "special_value"),
                "belong_op": then_clause.get("belong_op", "NOTBELONG"),
                "target_type": then_clause.get("target_type", "")
            }
        })
    
    elif contract_kind == "field_range":
        parsed_contract.update({
            "belong_op": details.get("belong_op", "BELONG"),
            "fields": details.get("fields", [])
        })
    
    return parsed_contract


def parse_contracts_from_json(node, node_id):
    """
    Parsea los contratos desde el JSON del nodo y los convierte al formato esperado por los templates XMI.
    
    Formato JSON esperado (opción 1 - por columnas):
    {
      "contracts": {
        "node_id": {
          "columns": {
            "column_name": {
              "preconditions": [...],
              "postconditions": [...],
              "invariants": [...]
            }
          }
        }
      }
    }
    
    Formato JSON esperado (opción 2 - lista):
    {
      "contracts": {
        "node_id": [
          {
            "column": "column_name",
            "type": "PRECONDITION" | "POSTCONDITION" | "INVARIANT",
            "contract_type": "value_range" | "condition" | "field_range",
            "name": "nombre_contrato",
            "details": {...}
          }
        ]
      }
    }
    
    Args:
        node (dict): El nodo del JSON que contiene los contratos
        node_id (int): El ID del nodo
    
    Returns:
        dict: Contratos organizados por tipo y columna
    """
    contracts = node.get("contracts", {})
    
    if not contracts:
        return None
    
    parsed_contracts = {
        "preconditions": [],
        "postconditions": [],
        "invariants": [],
        "by_column": {}  # Contratos organizados por columna
    }
    
    # Obtener contratos del nodo específico
    node_contracts = contracts.get(str(node_id), {})
    
    if not node_contracts:
        return None
    
    # Detectar formato: si es dict con "columns", usar formato 1; si es lista, usar formato 2
    if isinstance(node_contracts, dict) and "columns" in node_contracts:
        # FORMATO 1: Por columnas
        columns_contracts = node_contracts.get("columns", {})
        
        for column_name, column_data in columns_contracts.items():
            if column_name not in parsed_contracts["by_column"]:
                parsed_contracts["by_column"][column_name] = {
                    "column_name": column_name,
                    "preconditions": [],
                    "postconditions": [],
                    "invariants": []
                }
            
            # Procesar preconditions
            for contract in column_data.get("preconditions", []):
                parsed_contract = _parse_single_contract(contract, "PRECONDITION", column_name)
                parsed_contracts["preconditions"].append(parsed_contract)
                parsed_contracts["by_column"][column_name]["preconditions"].append(parsed_contract)
            
            # Procesar postconditions
            for contract in column_data.get("postconditions", []):
                parsed_contract = _parse_single_contract(contract, "POSTCONDITION", column_name)
                parsed_contracts["postconditions"].append(parsed_contract)
                parsed_contracts["by_column"][column_name]["postconditions"].append(parsed_contract)
            
            # Procesar invariants
            for contract in column_data.get("invariants", []):
                parsed_contract = _parse_single_contract(contract, "INVARIANT", column_name)
                parsed_contracts["invariants"].append(parsed_contract)
                parsed_contracts["by_column"][column_name]["invariants"].append(parsed_contract)
    
    elif isinstance(node_contracts, list):
        # FORMATO 2: Lista de contratos
        for contract in node_contracts:
            # El tipo puede venir en "type" (formato nuevo) o inferirse del contexto
            contract_type = contract.get("type", "")  # PRECONDITION, POSTCONDITION, INVARIANT
            column = contract.get("column", "")  # Nombre de la columna (opcional)
            
            # Si el contrato tiene "details", extraer el tipo de contrato de ahí
            if "contract_type" in contract:
                # Formato: {type: "PRECONDITION", contract_type: "value_range", details: {...}}
                parsed_contract = _parse_single_contract(
                    {"type": contract["contract_type"], "name": contract.get("name", ""), 
                     "details": contract.get("details", {})}, 
                    contract_type, 
                    column
                )
            else:
                # Formato antiguo: el contrato directamente tiene los campos
                parsed_contract = _parse_single_contract(contract, contract_type, column)
            
            # Agregar a la lista correspondiente
            if contract_type == "PRECONDITION":
                parsed_contracts["preconditions"].append(parsed_contract)
            elif contract_type == "POSTCONDITION":
                parsed_contracts["postconditions"].append(parsed_contract)
            elif contract_type == "INVARIANT":
                parsed_contracts["invariants"].append(parsed_contract)
            
            # También organizarlo por columna si se especificó
            if column:
                if column not in parsed_contracts["by_column"]:
                    parsed_contracts["by_column"][column] = {
                        "column_name": column,
                        "preconditions": [],
                        "postconditions": [],
                        "invariants": []
                    }
                
                if contract_type == "PRECONDITION":
                    parsed_contracts["by_column"][column]["preconditions"].append(parsed_contract)
                elif contract_type == "POSTCONDITION":
                    parsed_contracts["by_column"][column]["postconditions"].append(parsed_contract)
                elif contract_type == "INVARIANT":
                    parsed_contracts["by_column"][column]["invariants"].append(parsed_contract)
    
    # Si no hay contratos, retornar None
    if (not parsed_contracts["preconditions"] and 
        not parsed_contracts["postconditions"] and 
        not parsed_contracts["invariants"]):
        return None
    
    return parsed_contracts


def process_nodes_with_json_contracts(nodes: list, json_contracts: dict, include_contracts: bool, 
                                      node_flow_mapping: dict) -> tuple[str, int, int, dict]:
    """
    Procesa los nodos desde los datos JSON e incluye contratos leídos del JSON.

    Args:
        nodes: (list) Lista de nodos del JSON
        json_contracts: (dict) Contratos del JSON organizados por node_id
        include_contracts: (bool) Flag para incluir contratos
        node_flow_mapping: (dict) Mapeo de nodos y sus conexiones

    Returns:
        dataset_processing_filled_content: (str) Contenido lleno de los nodos
        nodes_cont (int): Número de nodos en el workflow
        mapped_nodes (int): Número de nodos mapeados
        mapped_nodes_info (dict): Información de mapeo
    """
    dataset_processing_filled_content = ""
    library_transformation_names = get_library_transformation_names('library_hashing/library_transformation_names.json')
    mapped_nodes = 0
    nodes_cont = 0
    mapped_nodes_info = {}

    for index, node in enumerate(nodes):
        node_id = node.get("id", index)
        node_name = node.get("node_name", f"Node_{index}")

        # Get library transformation name
        library_transformation_name = get_library_transformation_name(node=node, index=index)

        print(f"Node: {node_name} -> Library transformation: {library_transformation_name}")

        # Get the data processing values for the node type
        # NOTA: Se genera SIN contratos automáticos (False), ya que los leeremos del JSON
        dataprocessing_values = get_transformation_dp_values(node, node_id, node_name, False,
                                                             library_transformation_name)

        # Si include_contracts es True, parsear contratos del JSON
        if include_contracts and json_contracts:
            node_contracts = parse_contracts_from_json({"contracts": json_contracts}, node_id)
            if node_contracts:
                print(f"   ✅ Contratos encontrados para {node_name}: "
                      f"{len(node_contracts['preconditions'])} PRE, "
                      f"{len(node_contracts['postconditions'])} POST, "
                      f"{len(node_contracts['invariants'])} INV")
                # Agregar contratos y activar el flag para que el template los renderice
                dataprocessing_values["contracts"] = node_contracts
                dataprocessing_values["include_contracts"] = True
            else:
                print(f"   ℹ️  Sin contratos para {node_name}")

        # If the node is not a reader/writer/connector node, increment the nodes_cont counter
        if dataprocessing_values["input_filepath"] == "":
            nodes_cont += 1
            # Get the input file path from the previous node
            previous_node_id = node_flow_mapping[node_id]["previous_node_id"]
            if previous_node_id is not None:
                dataprocessing_values["input_filepath"] = (
                    f"output/{node_flow_mapping[previous_node_id]['node_name'].replace(' ', '_')}"
                    "_output_dataDictionary.csv"
                )
        dataprocessing_values["output_filepath"] = f"output/{node_name.replace(' ', '_')}_output_dataDictionary.csv"

        # Check if the library transformation name exists and the template file exists. If so, use the template file.
        # Otherwise, use the unknownDataProcessing template.
        dp_templates_path = "templates/data_processing"
        dp_template_filepath = f"{dp_templates_path}/{library_transformation_name}_template.xmi"
        if library_transformation_name in library_transformation_names and os.path.exists(dp_template_filepath):

            mapped_nodes += 1
            print_and_log(f"KNIME node: {node_name} -> mapped to library transformation: {library_transformation_name}")

            # Read the workflow template file
            with open(dp_template_filepath, "r") as file:
                data_processing_jinja_template = JinjaTemplate(file.read())

            # Update the mapped_nodes_info dict with the node_name and the number of times it has been mapped
            if node_name in mapped_nodes_info:
                mapped_nodes_info[node_name]["mapped_count"] = mapped_nodes_info[node_name].get("mapped_count", 0) + 1
            else:
                mapped_nodes_info[node_name] = {"mapped_count": 1, "not_mapped_count": 0}

        else:
            print_and_log(f"No mapped node: {node_name}")
            # Read the workflow template file
            with open(f"{dp_templates_path}/unknownDataProcessing.xmi", "r") as file:
                data_processing_jinja_template = JinjaTemplate(file.read())
            print_and_log(f"KNIME node: {node_name} -> unknown library transformation: {library_transformation_name}")

            # Update the mapped_nodes_info dict with the node_name and the number of times it has not been mapped
            if node_name in mapped_nodes_info:
                mapped_nodes_info[node_name]["not_mapped_count"] = mapped_nodes_info[node_name].get("not_mapped_count",
                                                                                                    0) + 1
            elif all(substring not in node_name for substring in ["Reader", "Table", "Connector", "Writer"]):
                mapped_nodes_info[node_name] = {"mapped_count": 0, "not_mapped_count": 1}

        # Fill the template with jinja2
        dataset_processing_filled_content += data_processing_jinja_template.render(
            dataprocessing=dataprocessing_values) + "\n"

    return dataset_processing_filled_content, nodes_cont, mapped_nodes, mapped_nodes_info


def process_links(data: dict, nodes: list) -> tuple[str, dict]:
    """
    Processes the links between nodes from the JSON data and appends the corresponding XML elements to the root element.
    It also returns a dict in which we have the node_name, the previous node_id and the next node_id.
    The dict is ordered so the connections between next_node_id and previous_node_id are consecutive.

    Args:
        data (dict): The JSON data containing the workflow information.
        nodes (list): The list of nodes from the JSON data.

    Returns:
        links_filled_content: (str) The filled content of the links.
        node_flow_mapping: (dict) an ordered dict with the node_name, the previous node_id and the next node_id.
    """

    node_mapping = {}
    # The node_flow_mapping is a list of dictionaries with the node_name, the previous node_id and the next node_id.
    node_flow_mapping = {}

    for index, node in enumerate(nodes):
        node_id = node.get("id", index)
        node_name = node.get("node_name", f"Node_{index}")
        node_mapping[node_id] = {"index": index, "name": node_name}
        node_flow_mapping[node_id] = {"node_name": node_name, "previous_node_id": None, "next_node_id": None}

    links = data.get("connections", [])
    links_filled_content = ""
    link_index = 0
    for conn in links:
        source_id = conn.get("sourceID")
        dest_id = conn.get("destID")

        # Connection between two "normal" nodes
        if source_id in node_mapping and dest_id in node_mapping:
            # Read the workflow template file
            with open("templates/link.xmi", "r") as file:
                link_template = Template(file.read())

            source_transformation_name = node_mapping[source_id]["name"]
            target_transformation_name = node_mapping[dest_id]["name"]

            link_values = {
                "source": source_id,
                "target": dest_id,
                "transformation_name_source": source_transformation_name,
                "transformation_name_target": target_transformation_name
            }

            # Update the node flow link mapping
            node_flow_mapping[source_id]["next_node_id"] = dest_id
            node_flow_mapping[dest_id]["previous_node_id"] = source_id

            # Fill the template
            links_filled_content += link_template.safe_substitute(
                link_values
            ) + "\n"
            link_index += 1

    # Order the node_flow_mapping so the connections between next_node_id and previous_node_id are consecutive.
    ordered_mapping = {}
    current_node_id = next(
        node_id for node_id, details in node_flow_mapping.items() if details['previous_node_id'] is None)

    while current_node_id is not None:
        ordered_mapping[current_node_id] = node_flow_mapping[current_node_id]
        next_node_id = node_flow_mapping[current_node_id]['next_node_id']
        current_node_id = next_node_id if next_node_id in node_flow_mapping else None

    return links_filled_content, node_flow_mapping


def preprocess_nodes_connections(nodes, connections):
    """
    Convert nodes id and its associated links with its sourceID and destID to numbers between 0 and n-1.
    Además, si un nodo tiene el atributo 'original_node_id' en parameters, este también se mapea
    al nuevo rango de IDs.

    Args:
        nodes (list): List of nodes from the JSON data.
        connections (list): List of connections from the JSON data.

    Returns:
        tuple: Updated nodes and connections with IDs (y original_node_id) mapeados a un nuevo rango.
    """
    # Creamos un diccionario para mapear cada ID original al nuevo índice 0..n-1
    id_mapping = {node["id"]: idx for idx, node in enumerate(nodes)}

    # Actualizamos el 'id' de cada nodo, y si existe 'original_node_id', lo mapeamos también
    for node in nodes:
        old_id = node["id"]
        node["id"] = id_mapping[old_id]

        params = node.get("parameters", {})
        if "original_node_id" in params:
            orig_old = params["original_node_id"]
            if orig_old in id_mapping:
                params["original_node_id"] = id_mapping[orig_old]
            else:
                # Si el original_node_id no está en el mapeo, lo eliminamos
                params.pop("original_node_id", None)

    # Recorremos las conexiones, filtrando aquellas cuyas IDs ya no existan,
    # y mapeamos sourceID y destID al nuevo rango
    updated_connections = []
    for conn in connections:
        src_old = conn["sourceID"]
        dst_old = conn["destID"]
        if src_old not in id_mapping or dst_old not in id_mapping:
            # Descartamos conexiones inválidas
            connections.remove(conn)
            continue
        conn['sourceID'] = id_mapping[conn['sourceID']]
        conn['destID'] = id_mapping[conn['destID']]

    return nodes, updated_connections


def preprocess_contracts(contracts, id_mapping):
    """
    Actualiza las claves del diccionario de contratos para que coincidan
    con el nuevo mapeo de IDs de nodos.
    
    Args:
        contracts (dict): Contratos organizados por node_id (como strings)
        id_mapping (dict): Mapeo de IDs antiguos a nuevos
    
    Returns:
        dict: Contratos con claves actualizadas al nuevo rango de IDs
    """
    if not contracts:
        return {}
    
    new_contracts = {}
    for old_id_str, contract_data in contracts.items():
        old_id = int(old_id_str)
        if old_id in id_mapping:
            new_id = id_mapping[old_id]
            new_contracts[str(new_id)] = contract_data
    
    return new_contracts


def json_to_xmi_workflow_with_templates(json_input_folder: str, workflow_filename: str, xmi_output_folder: str,
                                        include_contracts=True) -> tuple[int, int, dict]:
    """
    Convierte un archivo JSON de workflow a XMI usando templates, 
    PARSEANDO LOS CONTRATOS DESDE EL JSON en lugar de generarlos automáticamente.

    Args:
        json_input_folder (str): Ruta a la carpeta con los archivos JSON
        workflow_filename (str): Nombre del archivo JSON (sin extensión)
        xmi_output_folder (str): Ruta donde se guardará el XMI
        include_contracts (bool): Flag para incluir contratos (leídos del JSON)

    Returns:
        mapped_nodes: (int) Nodos mapeados a transformaciones
        nodes_cont: (int) Número de nodos en el workflow
        mapped_nodes_info: (dict) Información de mapeo
    """
    # Load JSON data
    with (open(os.path.join(json_input_folder, workflow_filename, workflow_filename + ".json"),
               "r", encoding="utf-8") as f):
        data = json.load(f)

        # Read the workflow template file
        with open("templates/workflow_template.xmi", "r") as file:
            workflow_template_content = Template(file.read())

        nodes = data.get("nodes", [])
        connections = data.get("connections", [])
        
        # Extraer contratos ANTES de preprocesar los IDs
        json_contracts_original = data.get("contracts", {})

        # Preprocess nodes and connections to map IDs to a new range (0 to n-1)
        # Guardamos el mapeo para actualizar los contratos
        id_mapping = {node["id"]: idx for idx, node in enumerate(nodes)}
        nodes, connections = preprocess_nodes_connections(nodes, connections)
        
        # Actualizar las claves de contratos según el nuevo mapeo de IDs
        json_contracts = preprocess_contracts(json_contracts_original, id_mapping)
        
        if json_contracts:
            print(f"📋 Contratos encontrados en JSON para {len(json_contracts)} nodos")

        # Process links
        links_filled_content, node_flow_mapping = process_links(data, nodes)

        # Process nodes with JSON contracts
        data_processing_filled_content, nodes_cont, mapped_nodes, mapped_nodes_info = process_nodes_with_json_contracts(
            nodes, json_contracts, include_contracts, node_flow_mapping
        )

        # ------------------------------

        # Read the workflow template file
        with open(f"templates/workflow_template.xmi", "r") as file:
            workflow_jinja_template = JinjaTemplate(file.read())

        # Define the replacement values to the workflow template
        workflow_values = {
            "workflow_name": workflow_filename,
            "data_processing_list": data_processing_filled_content,
            "link_list": links_filled_content,
            "nodes_count": nodes
        }

        # Fill the template with jinja2
        workflow_filled_content = workflow_jinja_template.render(
            workflow=workflow_values)

        # ------------------------------

        output_xmi_filepath = os.path.join(xmi_output_folder, workflow_filename + ".xmi")
        os.makedirs(os.path.dirname(output_xmi_filepath), exist_ok=True)
        with open(output_xmi_filepath, "w", encoding="utf-8") as file:
            file.write(workflow_filled_content)

    return mapped_nodes, nodes_cont, mapped_nodes_info


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Command line mode: python script.py <input_json> <output_xmi>
        json_filepath = sys.argv[1]
        xmi_output_filepath = sys.argv[2]
        
        print("="*60)
        print("JSON2WORKFLOW WITH CONTRACTS FROM JSON")
        print("="*60)
        print(f"Input JSON: {json_filepath}")
        print(f"Output XMI: {xmi_output_filepath}")
        print("="*60)
        
        # Extract filename without extension
        workflow_filename = os.path.splitext(os.path.basename(json_filepath))[0]
        json_input_folder = os.path.dirname(json_filepath)
        xmi_output_folder = os.path.dirname(xmi_output_filepath)
        
        mapped_nodes, nodes_cont, mapped_nodes_info = json_to_xmi_workflow_with_templates(
            json_input_folder, workflow_filename, xmi_output_folder, include_contracts=True)
        
        print("\n" + "="*60)
        print(f"✅ Mapped nodes: {mapped_nodes}/{nodes_cont}")
        print("Mapping details:", mapped_nodes_info)
        print(f"✅ XMI generated: {xmi_output_filepath}")
        print("="*60)
    else:
        # Example usage
        # Parameter to change for the json workflow to convert
        workflow_filename = "Model data set with metanode_with_contracts"

        json_input_folder = "parsed_json_workflows"
        xmi_output_folder = f"parsed_xmi_workflows/{workflow_filename}"

        print("="*60)
        print("JSON2WORKFLOW WITH CONTRACTS FROM JSON")
        print("="*60)
        
        mapped_nodes, nodes_cont, mapped_nodes_info = json_to_xmi_workflow_with_templates(
            json_input_folder, workflow_filename, xmi_output_folder, include_contracts=True)

        print("\n" + "="*60)
        print(f"✅ Mapped nodes: {mapped_nodes}/{nodes_cont}")
        print("Mapping details:", mapped_nodes_info)
        print("="*60)
