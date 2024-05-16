from typing import Dict, Any, List

from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition, FunctionParameters
from pydantic import BaseModel


class OpenaiFunction:
    """
    OpenaiFunction class contains method to create function definition for Openai
    """

    @staticmethod
    async def get_defination(func, description: str) -> ChatCompletionToolParam:
        func_name = func.__name__
        parameters_obj = await OpenaiFunction._get_func_parameters(func)
        function_obj = FunctionDefinition(name=func_name, description=description, parameters=parameters_obj)
        function_schema = ChatCompletionToolParam(type="function", function=function_obj)
        return function_schema

    @staticmethod
    async def _get_func_parameters(func) -> FunctionParameters:
        func_parameters = {}
        func_parameter_names = await OpenaiFunction._get_func_parameter_names(func)
        for func_parameter_name in func_parameter_names:
            if issubclass(func.__annotations__[func_parameter_name], BaseModel):
                model_json_schema = func.__annotations__[func_parameter_name].model_json_schema()
                func_param = await OpenaiFunction._get_func_parameter(model_json_schema)
                # TODO: Currently Openai does not support function with multiple arguments
                # func_parameters[func_parameter_name] = func_param
                func_parameters = func_param
                break
        return func_parameters

    @staticmethod
    async def _get_func_parameter(model_json_schema: Dict[str, Any]) -> FunctionParameters:
        # Fields of one function param (param is pydantic obj)
        param_type = model_json_schema["type"]
        properties = await OpenaiFunction._get_properties(model_json_schema)
        required = model_json_schema["required"]

        parameters_dict: FunctionParameters = {
            "type": param_type,
            "properties": properties,
            "required": required
        }
        # parameters_obj = FunctionParameters(**parameters_dict)
        return parameters_dict

    @staticmethod
    async def _get_func_parameter_names(func) -> List[str]:
        params: List[str] = []
        annotations: Dict[str, Any] = func.__annotations__
        for key in annotations.keys():
            if key is "return":
                continue
            params.append(key)
        return params

    @staticmethod
    async def _get_properties(model_json_schema: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        properties: Dict[str, Dict[str, object]] = {}
        properties_initial_state = model_json_schema["properties"]
        references = {}
        if "$defs" in model_json_schema:
            references = model_json_schema["$defs"]
        for property_name in properties_initial_state:
            property_value = properties_initial_state[property_name]
            de_referenced_property: Dict[str, object] = await OpenaiFunction._get_de_referenced_property(
                references,
                property_value,
                property_name
            )
            properties[property_name] = de_referenced_property
        return properties

    @staticmethod
    async def _get_de_referenced_property(references: Dict[str, Any], property_value: Dict[str, Any],
                                          property_name: str) -> Dict[str, object]:
        is_done = False
        expanded_property = property_value
        while True:
            if is_done:
                break
            if "anyOf" in expanded_property:
                option_list = expanded_property["anyOf"]
                for option_dict in option_list:
                    if "type" in option_dict:
                        option_dict["type"] = "null"
                    else:
                        expanded_property = option_dict
                        break
            if "allOf" in expanded_property:
                option_list = expanded_property["allOf"]
                for option_dict in option_list:
                    if "type" in option_dict:
                        option_dict["type"] = "null"
                    else:
                        expanded_property = option_dict
                        break
            if "$ref" not in expanded_property:
                # property_obj = PropertyObj(**expanded_property)
                return expanded_property
            elif "$ref" in expanded_property:
                ref_value = expanded_property["$ref"].split("/")[-1]
                expanded_property = references[ref_value]
