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
    
    # 1. Procesar File Reader o CSV Reader (siempre es el primer nodo)
    source = xtext_json.get("source", {})
    reader = source.get("reader", {})
    reader_type = reader.get("type", "")
    
    # Soportar tanto csv_reader como file_reader
    if reader_type in ["csv_reader", "file_reader"]:
        file_path = reader.get("file_path", {}).get("path", "")
        delimiter = ","
        
        # Comprobar si hay delimiter definido
        if "delimiter" in reader:
            delimiter_obj = reader.get("delimiter", {})
            if isinstance(delimiter_obj, dict):
                delimiter = delimiter_obj.get("value", ",")
            else:
                delimiter = delimiter_obj
        
        # Determinar el nombre y tipo del nodo según el reader_type
        if reader_type == "file_reader":
            node_name = "File Reader"
            node_type = "org.knime.base.node.io.filehandling.csv.reader.FileReaderNodeFactory"
        else:
            node_name = "CSV Reader"
            node_type = "org.knime.base.node.io.filehandling.csv.reader.CSVTableReaderNodeFactory"
        
        reader_node = {
            "id": node_id,
            "node_name": node_name,
            "node_type": node_type,
            "parameters": {
                "file_path": file_path
            }
        }
        
        # Añadir delimiter solo para CSV Reader
        if reader_type == "csv_reader":
            reader_node["parameters"]["column_delimiter"] = delimiter
            
        knime_json["nodes"].append(reader_node)
        
        # Mapear el nombre de la fuente de datos al ID del Reader
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
        
        # Intentar extraer columnas si están presentes
        columns_obj = transformation.get("columns", {})
        columns = columns_obj.get("columns", []) if columns_obj else []
        column_names = [col.get("name", "") for col in columns]
        
        # Si no hay columnas especificadas, usar valores por defecto o vacío
        if column_names:
            in_columns = [{"column_name": col, "column_type": "xstring"} for col in column_names]
            out_columns = [{"column_name": col, "column_type": "xstring"} for col in column_names]
        else:
            # Sin columnas específicas, el nodo aplicará el filtro a todas
            in_columns = []
            out_columns = []
        
        return {
            "id": node_id,
            "node_name": "Row Filter (deprecated)",
            "node_type": "org.knime.base.node.preproc.filter.row.RowFilterNodeFactory",
            "parameters": {
                "filter_type": "Range_RowFilter",  # o "MissingVal_RowFilter" según el caso
                "filter_type_inclusion": "EXCLUDE",
                "in_columns": in_columns,
                "out_columns": out_columns
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
    
    # Mapping (Rule Engine) - puede venir como "mapping" o "value_mapping"
    elif trans_type in ["mapping", "value_mapping"]:
        # Extraer columna del mapeo
        column_obj = transformation.get("column", {})
        column_name = column_obj.get("name", "") if isinstance(column_obj, dict) else str(column_obj)
        
        # Construir las rules en formato KNIME LIKE
        rules_obj = transformation.get("rules", {})
        mappings = transformation.get("mappings", [])
        
        rules = []
        function_types = []
        mapping_parameters = []
        
        # Si hay mappings explícitos, usarlos
        if isinstance(mappings, list) and len(mappings) > 0:
            for mapping in mappings:
                if isinstance(mapping, dict):
                    from_val = mapping.get("from", "")
                    to_val = mapping.get("to", "")
                    rules.append(f"${column_name}$ LIKE \"*{from_val}*\" => \"{to_val}\"")
                    function_types.append("LIKE")
                    mapping_parameters.append({"key": from_val, "value": to_val})
            # Añadir regla por defecto
            rules.append(f"TRUE => ${column_name}$")
        
        in_columns = [{"column_name": column_name, "column_type": "xstring"}] if column_name else []
        out_columns = [{"column_name": "prediction", "column_type": "xstring"}]  # Columna de salida estándar
        
        return {
            "id": node_id,
            "node_name": "Rule Engine",
            "node_type": "org.knime.base.node.rules.engine.RuleEngineNodeFactory",
            "parameters": {
                "rules": rules,
                "function_types": function_types if function_types else ["LIKE"],
                "new_column_name": "prediction",
                "replace_column_name": column_name,
                "append_column": False,
                "in_columns": in_columns,
                "out_columns": out_columns,
                "mapping": {
                    "replace_column_name": column_name,
                    "mapping_parameters": mapping_parameters,
                    "map_operation": "VALUE_MAPPING",
                    "unique_replacement_one_column": False
                }
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
        # Intentar extraer bins de la transformación
        bins_array = transformation.get("bins", [])
        bins = []
        
        if isinstance(bins_array, list) and len(bins_array) > 0:
            # Convertir bins de Xtext a formato KNIME
            for bin_item in bins_array:
                if isinstance(bin_item, dict):
                    bins.append({
                        "binName": bin_item.get("label", "bin"),
                        "closureType": bin_item.get("closure", "openClosed"),
                        "leftMargin": str(bin_item.get("lower_bound", "-Infinity")),
                        "rightMargin": str(bin_item.get("upper_bound", "Infinity"))
                    })
        
        # Si no hay bins, usar bins por defecto
        if not bins:
            bins = [{
                "binName": "default_bin",
                "closureType": "openClosed",
                "leftMargin": "-Infinity",
                "rightMargin": "Infinity"
            }]
        
        # Extraer columnas si existen
        columns_obj = transformation.get("columns", {})
        columns = columns_obj.get("columns", []) if isinstance(columns_obj, dict) else []
        column_names = [col.get("name", "") for col in columns] if columns else []
        
        in_columns = [{"column_name": col, "column_type": "xstring"} for col in column_names]
        out_columns = [{"column_name": f"{col}_binned", "column_type": "xstring"} for col in column_names]
        
        return {
            "id": node_id,
            "node_name": "Numeric Binner",
            "node_type": "org.knime.base.node.preproc.binner.BinnerNodeFactory",
            "parameters": {
                "bins": bins,
                "in_columns": in_columns,
                "out_columns": out_columns
            }
        }
    
    # Imputation
    elif trans_type == "imputation":
        columns_obj = transformation.get("columns", {})
        columns = columns_obj.get("columns", [])
        column_names = [col.get("name", "") for col in columns]
        
        # Obtener el método de imputación si existe, sino usar "other"
        method_obj = transformation.get("method", {})
        method_type = method_obj.get("type", "other")
        
        # Mapear method_type a imputationType (si existe en transformation, usarlo; sino, hardcodear)
        # NOTA: El JSON de Xtext no diferencia bien entre métodos "other"
        # Heurística basada en tipo de columnas y nombre del step:
        step_lower = step_name.lower()
        
        if method_type == "other":
            # Inferir basándose en los nombres de columnas
            is_string_column = any(col in ['sex', 'ETHNICITY', 'IRSCHOOL', 'ACADEMIC_INTEREST'] 
                                  for col in column_names)
            is_numeric_column = any(col in ['satscore', 'avg_income', 'distance'] 
                                  for col in column_names)
            
            if 'sex' in column_names or 'ETHNICITY' in column_names or 'IRSCHOOL' in column_names:
                imputation_type = "MostFrequent"  # Columnas categóricas
            elif 'satscore' in column_names:
                imputation_type = "Interpolation"  # Score usa interpolación
            else:
                imputation_type = "Mean"  # Por defecto para numéricas
        elif method_type == "fixed":
            imputation_type = "Fixed Value"
        elif method_type == "mean":
            imputation_type = "Mean"
        elif method_type == "median":
            imputation_type = "Median"
        elif method_type == "mode":
            imputation_type = "MostFrequent"
        else:
            imputation_type = "Mean"
        
        # Obtener fixStringValues si existe, sino usar array vacío
        fix_string_values = transformation.get("fixStringValues", [])
        
        return {
            "id": node_id,
            "node_name": "Missing Value",
            "node_type": "org.knime.base.node.preproc.pmml.missingval.compute.MissingValueHandlerNodeFactory",
            "parameters": {
                "method": method_type,
                "imputationType": imputation_type,
                "fixStringValues": fix_string_values,
                "in_columns": [
                    {"column_name": col, "column_type": "xstring"} for col in column_names
                ],
                "out_columns": [
                    {"column_name": col, "column_type": "xstring"} for col in column_names
                ]
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
    
    # Tipo desconocido o unknown_transformation
    else:
        print(f"⚠️ Tipo de transformación desconocido: {trans_type} en step '{step_name}'")
        
        # Intentar inferir el tipo de nodo basándonos en el nombre del step
        step_lower = step_name.lower()
        
        if "binner" in step_lower or "bin" in step_lower:
            print(f"   → Inferido como 'Numeric Binner' por el nombre del step")
            # Bins hardcodeados en formato KNIME
            default_bins = [{
                "binName": "default_bin",
                "closureType": "openClosed",
                "leftMargin": "-Infinity",
                "rightMargin": "Infinity"
            }]
            return {
                "id": node_id,
                "node_name": "Numeric Binner",
                "node_type": "org.knime.base.node.preproc.binner.BinnerNodeFactory",
                "parameters": {
                    "bins": default_bins,
                    "in_columns": [],
                    "out_columns": []
                }
            }
        elif "outlier" in step_lower:
            print(f"   → Inferido como 'Numeric Outliers' por el nombre del step")
            return {
                "id": node_id,
                "node_name": "Numeric Outliers",
                "node_type": "org.knime.base.node.stats.outlier.handler.NumericOutliersNodeFactory",
                "parameters": {
                    "in_columns": [],
                    "out_columns": []
                }
            }
        elif "missing" in step_lower or "impute" in step_lower:
            print(f"   → Inferido como 'Missing Value' por el nombre del step")
            return {
                "id": node_id,
                "node_name": "Missing Value",
                "node_type": "org.knime.base.node.preproc.pmml.missingval.compute.MissingValueHandlerNodeFactory",
                "parameters": {
                    "method": "other",
                    "imputationType": "Mean",  # Hardcoded por defecto
                    "fixStringValues": [],  # Hardcoded
                    "in_columns": [],
                    "out_columns": []
                }
            }
        else:
            print(f"   → No se pudo inferir el tipo de nodo")
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
    workflow_name = "Model Data Set"
    
    # Carpeta de entrada donde está el archivo JSON de Xtext
    input_folder = "parsed_json_workflows/Model Data Set"
    
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
