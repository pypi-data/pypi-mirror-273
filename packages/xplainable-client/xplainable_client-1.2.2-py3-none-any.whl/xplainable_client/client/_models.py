from ._client_cog_base import *
import pandas as pd
from xplainable_client.utils.encoders import force_json_compliant


class Models(Client_Cog):

    def create_model(self, model_name: str, model_description: str, model, x: pd.DataFrame, y: pd.Series):
        """ Creates a new model if the model does not already exist.

        Args:
            model_name (str): The name of the model
            model_description (str): The description of the model
            model (XClassifier | XRegressor): The model to create
            x (pd.DataFrame): The feature matrix
            y (pd.Series): The target variable

        Returns:
            str: The model id
            str: The version id

        Raises:
            Exception: If the model creation fails.
        """
        model_id = self.create_model_id(model, model_name, model_description)
        try:
            version_id = self.create_model_version(model, model_id, x, y)
        except Exception as e:
            self.delete_model(model_id)
            raise e
        return model_id, version_id
    
    def create_model_id(
            self, model, model_name: str, model_description: str) -> str:
        """ Creates a new model and returns the model id.
        Args:
            model_name (str): The name of the model
            model_description (str): The description of the model
            model (XClassifier | XRegressor): The model to create.
        Returns:
            int: The model id
        """
        model_type, target = self._detect_model_type(model)
        payoad = {
            "model_name": model_name,
            "model_description": model_description,
            "model_type": model_type,
            "target_name": target,
            "algorithm": model.__class__.__name__
        }

        response = self.session._session.post(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/create-model',
            json=payoad
        )

        model_id = self.session.get_response_content(response)

        return model_id

    
    #TODO: Refactor this based on notion instructions.
    def create_model_version(self, model, model_id: str, x: pd.DataFrame, y: pd.Series) -> str:
        """ Creates a new model version and returns the version id.
        Args:
            model_id (int): The model id
            partition_on (str): The partition column name
            ruleset (dict | str): The feeature ruleset
            health_info (dict): Feature health information
            versions (dict): Versions of current environment
        Returns:
            int: The model version id
        """
        # Get current versions
        versions = {
                "xplainable_version": self.xplainable_version,
                "python_version": self.python_version
            }
        partition_on = model.partition_on if 'Partitioned' in \
            model.__class__.__name__ else None
        payload = {
            "partition_on": partition_on,
            "versions": versions,
            "partitions": []
            }
        partitioned_models = ['PartitionedClassifier', 'PartitionedRegressor']
        independent_models = ['XClassifier', 'XRegressor']
        # get all partitions
        if model.__class__.__name__ in partitioned_models:
            for p, m in model.partitions.items():
                if p == '__dataset__':
                    part_x = x
                    part_y = y
                else:
                    part_x = x[x[partition_on].astype(str) == str(p)]
                    part_y = y[y.index.isin(part_x.index)]
                pdata = self._get_partition_data(m, p, part_x, part_y)
                payload['partitions'].append(pdata)

        elif model.__class__.__name__ in independent_models:
            pdata = self._get_partition_data(model, '__dataset__', x, y)
            payload['partitions'].append(pdata)

        # Create a new version and fetch id
        url = f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/add-version'
        response = self.session._session.post(
            url=url, json=force_json_compliant(payload))
        version_id = self.session.get_response_content(response)
        return version_id
        

    def list_models(self) -> list:
        """ Lists all models of the active user's team.

        Returns:
            dict: Dictionary of saved models.
        """

        response = self.session._session.get(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models'
            )

        data = self.session.get_response_content(response)

        # For better readability
        [i.pop('user') for i in data]
        [i.pop('contributors') for i in data]

        return data
    

    def __get_model__(self, model_id: int, version_id: int):
        """ Gets a model with a specific version.

        Args:
            model_id (int): The model id
            version_id (int): The version id

        Returns:
            dict: The model information

        Raises:
            ValueError: If the model does not exist.
        """
        try:
            response = self.session._session.get(
                url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}'
            )
            return self.session.get_response_content(response)
        except Exception as e:
            raise ValueError(f'Model with ID {model_id}:{version_id} does not exist')

    #TODO: Refactor this based on notion instructions.
    def _detect_model_type(self, model):
        """ Determines the type of model and target.
        
        Args:
            model (XClassifier | XRegressor): The existing model.

        Return:
            tuple:
                - model_type (str): The model type, either 'binary_classification' or 'regression'
                - model.target (str): The model target. 
        """


        if 'Partitioned' in model.__class__.__name__:
            model = model.partitions['__dataset__']
        cls_name = model.__class__.__name__
        if cls_name == "XClassifier":
            model_type = "binary_classification"
        elif cls_name == "XRegressor":
            model_type = "regression"
        else:
            raise ValueError(
                f'Model type {cls_name} is not supported')

        return model_type, model.target

    def list_model_versions(self, model_id: int) -> list:
        """ Lists all versions of a model.
        Args:
            model_id (int): The model id
        Returns:
            dict: Dictionary of model versions.
        """
        response = self.session._session.get(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions'
            )
        data = self.session.get_response_content(response)
        [i.pop('user') for i in data]
        return data
    
    def list_model_version_partitions(self, model_id: str, version_id: str):
        """ Lists all partitions of a model version.

        Args:
            model_id (str): The model id.
            version_id (str): The version id.
        
        Return:
            dict: Dictionary of model partitions.

        """
        response = self.session._session.get(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}'
        )
        partitions = self.session.get_response_content(response)
        return partitions


    def get_model_version_partition(self, model_id: str, version_id: str, partition_id: str):
        """ Gets a partition of a model version.
        Args:
            model_id (str): The model id.
            version_id (str): The version id.
            partition_id (str): The partition id.
        Returns:
            json: A json payload.
        """
        response = self.session._session.get(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}/partitions/{partition_id}'
        )
        partition_data = self.session.get_response_content(response)
        return partition_data


    def delete_model_version(self, model_id: str, version_id: str):
        """ Deletes a model version.
        Args:
            model_id (str): The model id.
            version_id (str): The version id.
        Return:
            json: A json payload.
        """
        response = self.session._session.delete(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}'
        )
        return response

    def restore_model_version(self, model_id: str, version_id: str):
        """ Restores a model version.
        Args:
            model_id (str): The model id.
            version_id (str): The version id.
        Return:
            json: A json payload.
        """
        response = self.session._session.post(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}/restore'
        )
        return response

    def delete_model(self, model_id: str):
        """ Deletes an existing model.
        Args:
            model_id (str): The id of the model to be deleted.
        Return:
            json: A json payload
        """
        response = self.session._session.delete(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}'
        )
        return response
    
    def restore_deleted_model(self, model_id: str):
        """ Restores a deleted model.
        Args:
            model_id (str): The id of the model to be restored.
        Return:
            json: A json payload
        """
        response = self.session._session.patch(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/restore-deleted'
        )
        return response

    def activate_model(self, model_id: str):
        """ Activates a model.
        Args:
            model_id (str): The id of the model to be activated.
        Return:
            json: A json payload
        """
        response = self.session._session.patch(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/activate'
        )
        return response

    def deactivate_model(self, model_id: str):
        """ Deactivates a model.
        Args:
            model_id (str): The id of the model to be deactivated.
        Return:
            json: A json payload
        """
        response = self.session._session.patch(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/deactivate'
        )
        return response

    def archive_model(self, model_id: str):
        """ Archives a model.
        Args:
            model_id (str): The id of the model to be archived.
        Return:
            json: A json payload
        """
        response = self.session._session.patch(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/archive'
        )
        return response

    def restore_archived_model(self, model_id: str):
        """ Restores an archived model.
        Args:
            model_id (str): The id of the model to be restored.
        Return:
            json: A json payload
        """
        response = self.session._session.patch(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/restore-archived'
        )
        return response

    def publish_model_version(self, model_id: str, version_id: str):
        """ Publishes a model version.
        Args:
            model_id (str): The model id.
            version_id (str): The version id.
        Return:
            json: A json payload.
        """
        response = self.session._session.post(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}/publish'
        )
        return response


    def unpublish_model_version(self, model_id: str, version_id: str):
        """ Unpublishes a model version.
        Args:
            model_id (str): The model id.
            version_id (str): The version id.
        Return:
            json: A json payload.
        """
        response = self.session._session.post(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}/unpublish'
        )
        return response

    def update_model_description(self, model_id: str, description: str):
        """ Updates the description of a model.
        Args:
            model_id (str): The model id.
            description (str): The new description of the model.
        Return:
            json: A json payload.
        """
        payload = {
            "description": description
        }

        response = self.session._session.patch(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/description',
            json=payload
        )
        return response

    def update_model_name(self, model_id: str, name: str):
        """ Updates the name of a model.
        Args:
            model_id (str): The model id.
            name (str): The new name of the model.
        Return:
            json: A json payload.
        """
        payload = {
            "name": name
        }

        response = self.session._session.patch(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/name',
            json=payload
        )
        return response

    def get_model_profile(self, model_id: str, version_id: str):
        """ Gets the profile of a model.
        Args:
            model_id (str): The model id.
            version_id (str): The version id.
        Return:
            list: A list of model profiles.
        """
        response = self.session._session.get(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}/profile'
        )
        profile = self.session.get_response_content(response)
        return profile

    def get_model_evaluation_data(self, model_id: str, version_id: str, partition_id: str):
        """ Gets the evaluation data of a model.
        Args:
            model_id (str): The model id.
            version_id (str): The version id.
            partition_id (str): The partition id.
        Return:
            dict: A dictionary of model evaluation data.
        """
        response = self.session._session.get(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}/partitions/{partition_id}/evaluation'
        )
        evaluation_data = self.session.get_response_content(response)
        return evaluation_data

    def link_model_preprocessor(self, model_id: str, version_id: str, preprocessor_id: str, preprocessor_version_id: str):
        """ Links a model to a preprocessor.
        Args:
            model_id (str): The model id.
            version_id (str): The version id.
            preprocessor_id (str): The preprocessor id.
            preprocessor_version_id (str): The preprocessor version id.
        Return:
            json: A json payload.
        """
        payload = {
            "preprocessor_id": preprocessor_id,
            "preprocessor_version_id": preprocessor_version_id

        }

        response = self.session._session.put(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}/preprocessor',
            json=payload
        )
        return response

    def get_model_preprocessor(self, model_id: str, version_id: str):
        """ Gets the preprocessor of a model.
        Args:
            model_id (str): The model id.
            version_id (str): The version id.
        Return:
            dict: A dictionary of model preprocessor.
        """
        response = self.session._session.get(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/versions/{version_id}/preprocessor'
        )
        preprocessor = self.session.get_response_content(response)
        return preprocessor

    def set_active_version(self, model_id: str, version_id: str):
        """ Sets the active version of a model.
        Args:
            model_id (str): The model id.
            version_id (str): The version id.
        Return:
            json: A json payload.
        """
        payload = {
            "version_id": version_id
        }

        response = self.session._session.patch(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/active-version',
            json=payload
        )
        return response

    def move_model(self, model_id: str, new_team_id: str):
        """ Moves a model to a new team.
        Args:
            model_id (str): The model id.
            new_team_id (str): The new team id.
        Return:
            json: A json payload.
        """
        payload = {
            "new_team_id": new_team_id
        }

        response = self.session._session.patch(
            url=f'{self.session.hostname}/v1/{self.session.__ext}/models/{model_id}/move',
            json=payload
        )
        return response



    

       
