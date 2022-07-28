# -*- coding: utf-8 -*-
"""
It contains the YamlDataTransferObject class.
This class is used to parse the yaml files.

Example:
    from yaml_service import YamlDataTransferObject
    
    YDTO = YamlDataTransferObject()

    # List of data providers

    provider_list = YDTO.get_providers()

    # Contents of the yaml-file for the provider

    provider_dict = YDTO.get_provider_content(provider_list[0])

"""

import yaml
import os

from config import default_yaml_directory, mandatory_yaml_keys

class YamlDataTransferObject:
    """
    No se que hace esta clase
    """

    def __init__(self, path=default_yaml_directory):
        """
        No se que hace esto
        """
        def read_and_validate_yaml(yaml_filename):
            """
            Read and validate the yaml-file.

            Parameters
            ----------
            yaml_filename:  Name of the yaml-file.

            Raises
            ------
            Exception
                Exceptions are raised if:
                - The yaml parser finds an error
                - Mandatory keys in the configuration are missing.
                - Mandatory keys has no value.

            Returns
            -------
            data: dict
                Dictionary with the data from the yaml-file.
            """
            with open(os.path.join(self._path, yaml_filename), 'r') as stream:
                try:
                    data = yaml.safe_load(stream)
                    # Check for mandatory keys
                    if not mandatory_yaml_keys.issubset(data.keys()):
                        raise Exception(
                            f"{yaml_filename} doesn't contain all the " + \
                                f"mandatory info - {mandatory_yaml_keys}:")
                    # Check for empty values
                    if None in [data[x] for x in mandatory_yaml_keys]:
                        raise Exception(
                            f"{yaml_filename} contains empty values for " + \
                                f"mandatory info - {mandatory_yaml_keys}:")
                except yaml.YAMLError as exc:
                    raise Exception(
                        'Error opening and validatinf the yaml file ' + \
                        f'{yaml_filename}: {exc}')
            return data

        self._path = path
        # Scientific Dashboard Providers
        self._SD_providers = []
        # Dict with the content of the yaml-files
        # Example:
        # {'ICOS':{config-data from ICOS}, 'MARIS':{config-data from MARIS},...}
        self._SD_content = {}
        
        # Create a list with all the yaml-files in the directory
        yaml_list = [
            filename for filename in os.listdir(self._path)
            if filename.split(".")[-1] == "yaml"
        ]
        for yaml_file in yaml_list:
            # Read the yaml-file
            yaml_data = read_and_validate_yaml(yaml_file)
            self._SD_providers.append(yaml_data.pop('SD_provider_abbreviation'))
            self._SD_content[self._SD_providers[-1]] = yaml_data

    def get_providers(self) -> list:
        """
        Return the list of providers.

        Returns
        -------
        list
            List of providers.
        """
        return self._SD_providers
    
    def get_provider_content(self, provider: str) -> dict:
        """
        Return the content of a provider.

        Parameters
        ----------
        provider: str
            Name of the provider.
        
        Raises
        ------
        Exception
            Exception is raised if the provider is not in the list of providers.

        Returns
        -------
        dict
            Dictionary with the content of the provider.
        """
        if provider in self._SD_providers:
            return self._SD_content[provider]
        else:
            raise Exception(f"Provider {provider} not found.")