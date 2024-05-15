from typing import List, Dict, Any, Union

class CapabilityConverter:
    @staticmethod
    def _process_string_capability(capability: str) -> Dict[str, str]:
        """
        Process a capability provided as a string and return it as a dictionary.
        """
        if "=" in capability:
            split_pairs = capability.split("=")
            return {split_pairs[0]: '='.join(split_pairs[1:])}
        else:
            return {capability: None}

    @staticmethod
    def _process_dict_capability(capability: Dict[str, Any]) -> Dict[str, str]:
        """
        Process a capability provided as a dictionary and return it as a dictionary.
        """
        if "name" in capability and "value" in capability:
            return {capability["name"]: str(capability["value"]) if capability["value"] is not None else None}
        elif "name" in capability or "value" in capability:
            raise ValueError("Capability dictionary must have both 'name' and 'value' fields")
        else:
            return capability

    @staticmethod
    def convert_capabilities(capabilities: List[Union[str, Dict[str, Any]]]) -> Dict[str, str]:
        """
        Convert a list of capabilities into a dictionary.
        """
        capability_dict = {}
        for capability in capabilities:
            if isinstance(capability, dict):
                capability_dict.update(CapabilityConverter._process_dict_capability(capability))
            elif isinstance(capability, str):
                capability_dict.update(CapabilityConverter._process_string_capability(capability))
            else:
                raise ValueError("Capability must be a string or dictionary")
        return capability_dict
