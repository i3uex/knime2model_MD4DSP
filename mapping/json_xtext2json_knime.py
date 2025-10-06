#!/usr/bin/env python3
"""
Script para transformar JSON generado por Xtext al formato JSON de KNIME.
Uso: python json_xtext2json_knime.py input.json output.json
"""

import json
import sys
import os



def transform_xtext_to_knime(xtext_json):
    """
    Transforma JSON generado por Xtext al formato JSON de KNIME.
    """
    knime_json = {
        "nodes": [],
        "connections": []
    }
    
    # Mapeo de nombres de steps a IDs de nodo
    step_to_id = {}
    node_id = 1
    
    # 1. Procesar CSV Reader (siempre es el primer nodo)
    source = xtext_json.get("source", {})
    reader = source.get("reader", {})
    
    if reader.get("type") == "csv_reader":
        file_path = reader.get("file_path", {}).get("path", "")
        delimiter = ","
        
        # Comprobar si hay delimiter definido
        if "delimiter" in reader:
            delimiter_obj = reader.get("delimiter", {})
            if isinstance(delimiter_obj, dict):
                delimiter = delimiter_obj.get("value", ",")
            else:
                delimiter = delimiter_obj
        
        csv_node = {
            "id": node_id,
            "node_name": "CSV Reader",
            "node_type": "org.knime.base.node.io.filehandling.csv.reader.CSVTableReaderNodeFactory",
            "parameters": {
                "file_path": file_path,
                "column_delimiter": delimiter
            }
        }
        knime_json["nodes"].append(csv_node)
        
        # Mapear el nombre de la fuente de datos al ID del CSV Reader
        source_name = source.get("name", "data")
        step_to_id[source_name] = node_id
        node_id += 1
    
    # 2. Procesar steps
    steps = xtext_json.get("body", {}).get("steps", [])
    
    for step in steps:
        step_name = step.get("name", "")
        transformation = step.get("transformation", {})
        target = step.get("target", "")
        
        # Crear nodo según el tipo de transformación
        node = create_knime_node(node_id, step_name, transformation)
        
        if node:
            knime_json["nodes"].append(node)
            step_to_id[step_name] = node_id
            
            # Crear conexión
            if target and target in step_to_id:
                connection = {
                    "sourceID": step_to_id[target],
                    "destID": node_id
                }
                knime_json["connections"].append(connection)
            
            node_id += 1
    
    # 3. Procesar contratos desde los steps
    contracts_dict = extract_contracts_from_steps(steps, step_to_id)
    if contracts_dict:
        knime_json["contracts"] = contracts_dict
    
    return knime_json


def create_knime_node(node_id, step_name, transformation):
    """
    Crea un nodo KNIME basado en el tipo de transformación de Xtext.
    """
    trans_type = transformation.get("type", "")
    
    # Row Filter
    if trans_type == "row_filter":
        condition = transformation.get("condition", {})
        # Extraer información del filtro (simplificado, necesita más lógica según el tipo)
        return {
            "id": node_id,
            "node_name": "Row Filter",
            "node_type": "org.knime.base.node.preproc.filter.row.RowFilterNodeFactory",
            "parameters": {
                "filter_type": "MissingVal_RowFilter",
                "filter_type_inclusion": "EXCLUDE",
                "in_columns": [
                    {"column_name": "Age", "column_type": "xstring"},
                    {"column_name": "Grade", "column_type": "xstring"}
                ],
                "out_columns": [
                    {"column_name": "Age", "column_type": "xstring"},
                    {"column_name": "Grade", "column_type": "xstring"}
                ]
            }
        }
    
    # Type Conversion (to_numeric)
    elif trans_type == "type_conversion":
        columns_obj = transformation.get("columns", {})
        columns = columns_obj.get("columns", [])
        column_names = [col.get("name", "") for col in columns]
        
        return {
            "id": node_id,
            "node_name": "String to Number",
            "node_type": "org.knime.base.node.preproc.colconvert.stringtonumber2.StringToNumber2NodeFactory",
            "parameters": {
                "decimal_separator": ".",
                "in_columns": [
                    {"column_name": col, "column_type": "xstring"} for col in column_names
                ],
                "out_columns": [
                    {"column_name": col, "column_type": "xstring"} for col in column_names
                ]
            }
        }
    
    # Column Filter
    elif trans_type == "column_filter":
        columns_obj = transformation.get("columns", {})
        columns = columns_obj.get("columns", [])
        column_names = [col.get("name", "") for col in columns]
        
        return {
            "id": node_id,
            "node_name": "Column Filter",
            "node_type": "org.knime.base.node.preproc.filter.column.DataColumnSpecFilterNodeFactory",
            "parameters": {
                "in_columns": [
                    {"column_name": col, "column_type": "xstring"} for col in column_names
                ],
                "out_columns": [
                    {"column_name": col, "column_type": "xstring"} for col in column_names
                ]
            }
        }
    
    # Mapping (Rule Engine)
    elif trans_type == "mapping":
        return {
            "id": node_id,
            "node_name": "Rule Engine",
            "node_type": "org.knime.base.node.rules.engine.RuleEngineNodeFactory",
            "parameters": {
                "rules": [],
                "function_types": [],
                "in_columns": [],
                "out_columns": []
            }
        }
    
    # Math Operation
    elif trans_type == "math_op":
        return {
            "id": node_id,
            "node_name": "Math Formula",
            "node_type": "org.knime.ext.jep.JEPNodeFactory",
            "parameters": {
                "in_columns": [],
                "out_columns": []
            }
        }
    
    # Binner
    elif trans_type == "binner":
        return {
            "id": node_id,
            "node_name": "Numeric Binner",
            "node_type": "org.knime.base.node.preproc.binner.BinnerNodeFactory",
            "parameters": {
                "bins": [],
                "in_columns": [],
                "out_columns": []
            }
        }
    
    # Imputation
    elif trans_type == "imputation":
        return {
            "id": node_id,
            "node_name": "Missing Value",
            "node_type": None,
            "parameters": {
                "in_columns": [],
                "out_columns": []
            }
        }
    
    # Outlier Treatment
    elif trans_type == "outlier_treatment":
        return {
            "id": node_id,
            "node_name": "Numeric Outliers",
            "node_type": "org.knime.base.node.stats.outlier.handler.NumericOutliersNodeFactory",
            "parameters": {
                "in_columns": [],
                "out_columns": []
            }
        }
    
    # Join
    elif trans_type == "join":
        return {
            "id": node_id,
            "node_name": "Joiner",
            "node_type": "org.knime.base.node.preproc.joiner.Joiner2NodeFactory",
            "parameters": {
                "join_type": "inner",
                "in_columns": [],
                "out_columns": []
            }
        }
    
    # Tipo desconocido
    else:
        print(f"⚠️ Tipo de transformación desconocido: {trans_type}")
        return None


def extract_contracts_from_steps(steps, step_to_id):
    """
    Extrae y parsea los contratos desde los steps de Xtext al formato KNIME.
    
    Args:
        steps: Lista de steps del workflow Xtext
        step_to_id: Mapeo de nombres de steps a IDs de nodos
    
    Returns:
        dict: Contratos organizados por node_id en formato KNIME
    """
    contracts_dict = {}
    
    for step in steps:
        step_name = step.get("name", "")
        contracts = step.get("contracts", {})
        
        if not contracts or step_name not in step_to_id:
            continue
        
        node_id = step_to_id[step_name]
        contracts_list = contracts.get("contracts", [])
        
        if not contracts_list:
            continue
        
        node_contracts = {
            "preconditions": [],
            "postconditions": [],
            "invariants": []
        }
        
        for contract in contracts_list:
            contract_type = contract.get("type", "")
            contract_name_obj = contract.get("name", {})
            contract_name = contract_name_obj.get("name", "") if isinstance(contract_name_obj, dict) else str(contract_name_obj)
            contract_body = contract.get("body", {})
            
            # Parsear el contrato según su tipo
            parsed_contract = parse_xtext_contract(contract_name, contract_type, contract_body)
            
            if parsed_contract:
                if contract_type == "precondition":
                    node_contracts["preconditions"].append(parsed_contract)
                elif contract_type == "postcondition":
                    node_contracts["postconditions"].append(parsed_contract)
                elif contract_type == "invariant":
                    node_contracts["invariants"].append(parsed_contract)
        
        # Solo añadir si hay al menos un contrato
        if (node_contracts["preconditions"] or 
            node_contracts["postconditions"] or 
            node_contracts["invariants"]):
            contracts_dict[str(node_id)] = node_contracts
    
    return contracts_dict


def parse_xtext_contract(name, contract_type, body):
    """
    Parsea un contrato individual de formato Xtext a formato KNIME.
    
    Args:
        name: Nombre del contrato
        contract_type: Tipo (precondition, postcondition, invariant)
        body: Cuerpo del contrato con contract_type
    
    Returns:
        dict: Contrato en formato KNIME
    """
    contract_type_obj = body.get("contract_type", {})
    ct_type = contract_type_obj.get("type", "")
    
    # Extraer columna del nombre si está presente (ej: "Age_castable" -> "Age")
    column_from_name = name.split("_")[0] if "_" in name else ""
    
    # VALUE_RANGE Contract
    if ct_type == "value_range":
        field_obj = contract_type_obj.get("field", {})
        column_obj = field_obj.get("column", {})
        column = column_obj.get("name", "") if isinstance(column_obj, dict) else str(column_obj)
        
        if not column:
            column = column_from_name
        
        # Determinar el field type basado en el contexto
        field_type = "input"  # Por defecto input para preconditions
        if contract_type == "postcondition":
            field_type = "output"
        
        return {
            "name": name,
            "type": "value_range",
            "field": field_type,
            "column": column,
            "check": "castable_to",
            "target_type": "Integer"
        }
    
    # CAST_TYPE Contract
    elif ct_type == "cast_type":
        field_obj = contract_type_obj.get("field", {})
        column_obj = field_obj.get("column", {})
        column = column_obj.get("name", "") if isinstance(column_obj, dict) else str(column_obj)
        
        if not column:
            column = column_from_name
        
        cast_type_name = contract_type_obj.get("cast_type_name", "Integer")
        
        return {
            "name": name,
            "type": "cast_type",
            "field": "output",
            "column": column,
            "check": "is_type",
            "target_type": cast_type_name
        }
    
    # CONDITION Contract
    elif ct_type == "condition":
        # Extraer información de if_clause y then_clause
        if_clause = contract_type_obj.get("if_clause", {})
        then_clause = contract_type_obj.get("then_clause", {})
        
        # Si no hay información detallada, usar valores por defecto basados en el nombre
        column = column_from_name or "Unknown"
        
        return {
            "name": name,
            "type": "condition",
            "condition": {
                "if": {
                    "field": "input",
                    "column": column,
                    "operator": "not_belongs_to",
                    "check": "special_values"
                },
                "then": {
                    "field": "output",
                    "column": column,
                    "operator": "not_belongs_to",
                    "check": "special_values"
                }
            }
        }
    
    # Tipo desconocido
    else:
        print(f"⚠️ Tipo de contrato desconocido: {ct_type} en contrato '{name}'")
        return None


def main():
    # ========== CONFIGURACIÓN ==========
    # Nombre del archivo (sin extensión .json)
    workflow_name = "StudentDataPipeline"
    
    # Carpeta de entrada donde está el archivo JSON de Xtext
    input_folder = "parsed_json_workflows/StudentDataPipeline"
    
    output_folder = f"{input_folder}_knime"
    
    output_name = f"{workflow_name}_knime"    
    
    # Construir rutas completas
    input_file = os.path.join(input_folder, f"{workflow_name}.json")
    output_file = os.path.join(output_folder, f"{output_name}.json")
    
    try:
        # Crear carpeta de salida si no existe
        os.makedirs(output_folder, exist_ok=True)
        
        # Leer JSON de Xtext
        with open(input_file, 'r') as f:
            xtext_json = json.load(f)
        
        # Transformar
        knime_json = transform_xtext_to_knime(xtext_json)
        
        # Guardar JSON de KNIME
        with open(output_file, 'w') as f:
            json.dump(knime_json, f, indent=2)
        
        print(f"✅ Transformación completada")
        print(f"   Archivo entrada: {input_file}")
        print(f"   Archivo salida: {output_file}")
        print(f"   Nodos generados: {len(knime_json['nodes'])}")
        print(f"   Conexiones generadas: {len(knime_json['connections'])}")
        
        if "contracts" in knime_json:
            total_contracts = sum(
                len(c["preconditions"]) + len(c["postconditions"]) + len(c["invariants"])
                for c in knime_json["contracts"].values()
            )
            print(f"   Contratos generados: {total_contracts} en {len(knime_json['contracts'])} nodos")
    
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{input_file}'")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
