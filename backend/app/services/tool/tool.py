import asyncio
from typing import Dict, List

from fastapi import APIRouter

from app.config import CONFIG
from app.models import BundleInstance, Tool, ToolInput, ToolOutput, ToolRef, ToolType
from app.operators import action_ops, bundle_instance_ops
from app.services.tool.plugin.cache import get_bundle, i18n_text
from tkhelper.error import raise_request_validation_error

from .action import run_action
from .plugin import get_plugin, run_plugin

router = APIRouter()


async def verify_tools(tools: List[ToolRef]):
    """
    Verify tools, raise error if any tool is invalid
    :param tools: the tools
    :return: None
    """

    for tool in tools:
        if tool.type == "action":
            await action_ops.get(action_id=tool.id)

        elif tool.type == "plugin":
            if "/" not in tool.id:
                raise_request_validation_error(f"Invalid plugin tool ID: {tool.id}")
            bundle_instance_id, plugin_id = tool.id.split("/")
            bundle: BundleInstance = await bundle_instance_ops.get(bundle_instance_id=bundle_instance_id)
            get_plugin(bundle_id=bundle.bundle_id, plugin_id=plugin_id)

        else:
            raise_request_validation_error(f"Invalid tool type: {tool.type}")


async def fetch_tools(tool_refs: List[ToolRef]) -> List[Tool]:
    """
    Fetch tools
    :param tool_refs: the tool references
    :return: the tools
    """

    tools: List[Tool] = []
    tool_ids = []
    name_number_dict = {}
    # todo: handle duplicate tool name

    for tool_ref in tool_refs:
        if tool_ref.type == ToolType.ACTION:
            action = await action_ops.get(action_id=tool_ref.id)
            if action:
                tool_ids.append(tool_ref.id)
                tools.append(
                    Tool(
                        tool_id=tool_ref.id,
                        type=ToolType.ACTION,
                        function_def=action.function_def.model_dump(),
                    )
                )

        elif tool_ref.type == ToolType.PLUGIN:
            if "/" not in tool_ref.id:
                raise_request_validation_error(f"Invalid plugin tool ID: {tool_ref.id}")
            bundle_instance_id, plugin_id = tool_ref.id.split("/")
            bundle: BundleInstance = await bundle_instance_ops.get(bundle_instance_id=bundle_instance_id)
            plugin = get_plugin(bundle_id=bundle.bundle_id, plugin_id=plugin_id)
            tools.append(
                Tool(
                    tool_id=tool_ref.id,
                    type=ToolType.PLUGIN,
                    function_def=plugin.function_def.model_dump(),
                )
            )

        else:
            raise_request_validation_error(f"Invalid tool type: {tool_ref.type}")

    return tools


async def run_tools(tool_inputs: List[ToolInput]) -> List[ToolOutput]:
    """
    Run tools
    :param tool_inputs: the tool inputs
    :return: the tool outputs
    """

    tasks = []
    for tool_input in tool_inputs:
        if tool_input.type == ToolType.ACTION:
            tasks.append(
                run_action(
                    action_id=tool_input.tool_id,
                    parameters=tool_input.arguments,
                )
            )

        elif tool_input.type == ToolType.PLUGIN:
            if "/" not in tool_input.tool_id:
                raise_request_validation_error(f"Invalid plugin tool ID: {tool_input.id}")
            bundle_instance_id, plugin_id = tool_input.tool_id.split("/")
            tasks.append(
                run_plugin(
                    bundle_instance_id=bundle_instance_id,
                    plugin_id=plugin_id,
                    parameters=tool_input.arguments,
                )
            )
        else:
            raise_request_validation_error(f"Invalid tool type: {tool_input.type}")

    results = await asyncio.gather(*tasks)

    tool_outputs: List[ToolOutput] = []
    for i, tool in enumerate(tool_inputs):
        if tool.type == ToolType.ACTION or tool.type == ToolType.PLUGIN:
            tool_outputs.append(
                ToolOutput(
                    type=tool.type,
                    tool_id=tool.tool_id,
                    tool_call_id=tool.tool_call_id,
                    status=results[i].get("status"),
                    data=results[i].get("data"),
                )
            )

    return tool_outputs


async def ui_fetch_tools(tools: List[Dict]) -> List[Dict]:
    lang = CONFIG.DEFAULT_LANG
    for tool in tools:
        if tool["type"] == ToolType.ACTION:
            action = await action_ops.get(action_id=tool["id"])
            if action:
                tool["name"] = action.name

        elif tool["type"] == ToolType.PLUGIN:
            if "/" not in tool["id"]:
                raise_request_validation_error(f"Invalid plugin tool ID: {tool['id']}")
            bundle_instance_id, plugin_id = tool["id"].split("/")
            bundle_instance: BundleInstance = await bundle_instance_ops.get(bundle_instance_id=bundle_instance_id)
            bundle = get_bundle(bundle_id=bundle_instance.bundle_id)
            real_bundle_name = i18n_text(bundle.bundle_id, bundle.name, lang)
            plugin = get_plugin(bundle_id=bundle.bundle_id, plugin_id=plugin_id)
            real_plugin_name = i18n_text(plugin.bundle_id, plugin.name, lang)
            if bundle:
                tool["name"] = f"{real_bundle_name} / {real_plugin_name}"

        else:
            raise_request_validation_error(f"Invalid tool type: {tool['type']}")

    return tools
