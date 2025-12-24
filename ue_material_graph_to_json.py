"""Export Unreal Engine 5.4 material graphs to JSON.

Usage (from UE Python):
    import ue_material_graph_to_json as exporter
    exporter.export_material_graph('/Game/Materials/M_MyMaterial', 'C:/Temp/M_MyMaterial.json')

Usage (command line in UE):
    UnrealEditor.exe <Project> -ExecutePythonScript=ue_material_graph_to_json.py -- \
        --material /Game/Materials/M_MyMaterial --output C:/Temp/M_MyMaterial.json
"""

import argparse
import json
import sys
from typing import Any, Dict, List

import unreal


MATERIAL_OUTPUT_NODE_ID = "MaterialOutput"


def _get_editor_property(expression: unreal.Object, name: str, default: Any = None) -> Any:
    try:
        return expression.get_editor_property(name)
    except Exception:
        return default


def _get_expression_input_names(expression: unreal.MaterialExpression) -> List[str]:
    try:
        return unreal.MaterialEditingLibrary.get_material_expression_input_names(expression)
    except Exception:
        return []


def _get_expression_input_source(
    expression: unreal.MaterialExpression,
    input_name: str,
) -> Dict[str, Any]:
    try:
        source_node = unreal.MaterialEditingLibrary.get_material_expression_input_node(
            expression, input_name
        )
        if not source_node:
            return {}
        output_index = unreal.MaterialEditingLibrary.get_material_expression_input_output_index(
            expression, input_name
        )
        return {
            "source_node": source_node,
            "output_index": output_index,
        }
    except Exception:
        return {}


def _serialize_expression(expression: unreal.MaterialExpression) -> Dict[str, Any]:
    return {
        "id": str(_get_editor_property(expression, "material_expression_guid", expression.get_name())),
        "name": expression.get_name(),
        "class": expression.get_class().get_name(),
        "desc": _get_editor_property(expression, "desc", ""),
        "position": {
            "x": _get_editor_property(expression, "material_expression_editor_x", 0),
            "y": _get_editor_property(expression, "material_expression_editor_y", 0),
        },
    }


def _material_property_list() -> List[unreal.MaterialProperty]:
    try:
        return list(unreal.MaterialProperty)
    except Exception:
        return []


def export_material_graph(material_path: str, output_path: str) -> Dict[str, Any]:
    material = unreal.load_asset(material_path)
    if not material:
        raise RuntimeError(f"Material not found: {material_path}")

    expressions = unreal.MaterialEditingLibrary.get_material_expressions(material)
    node_map = {}
    nodes = []
    edges = []

    for expression in expressions:
        node_data = _serialize_expression(expression)
        nodes.append(node_data)
        node_map[expression] = node_data["id"]

    for expression in expressions:
        input_names = _get_expression_input_names(expression)
        for input_name in input_names:
            source_info = _get_expression_input_source(expression, input_name)
            if not source_info:
                continue
            source_node = source_info["source_node"]
            if source_node not in node_map:
                continue
            edges.append(
                {
                    "from": node_map[source_node],
                    "to": node_map[expression],
                    "input": input_name,
                    "output_index": source_info.get("output_index", 0),
                }
            )

    material_node = {
        "id": MATERIAL_OUTPUT_NODE_ID,
        "name": material.get_name(),
        "class": material.get_class().get_name(),
    }
    nodes.append(material_node)

    for material_property in _material_property_list():
        try:
            source_node = unreal.MaterialEditingLibrary.get_material_property_input_node(
                material, material_property
            )
        except Exception:
            continue
        if not source_node:
            continue
        output_index = 0
        try:
            output_index = unreal.MaterialEditingLibrary.get_material_property_input_output_index(
                material, material_property
            )
        except Exception:
            pass
        edges.append(
            {
                "from": node_map.get(source_node, source_node.get_name()),
                "to": MATERIAL_OUTPUT_NODE_ID,
                "input": material_property.name,
                "output_index": output_index,
            }
        )

    payload = {
        "material": {
            "path": material_path,
            "name": material.get_name(),
        },
        "nodes": nodes,
        "edges": edges,
    }

    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    unreal.log(f"Exported material graph to {output_path}")
    return payload


def _parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export a UE material graph to JSON.")
    parser.add_argument("--material", required=True, help="Material asset path, e.g. /Game/Materials/M_MyMaterial")
    parser.add_argument("--output", required=True, help="Output JSON path")
    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    args = _parse_args(argv)
    export_material_graph(args.material, args.output)


if __name__ == "__main__":
    main(sys.argv[1:])
