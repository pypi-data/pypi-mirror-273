# resources/recommender.py
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, Dict, Any
from .._constants import (BASE_URL_V2)

import httpx

if TYPE_CHECKING:
    from .._client import PigeonsAI
    from .data_connector import DataConnector


class Recommender:
    def __init__(self, client: PigeonsAI):
        self.client = client
        self._vae = VAE(client)
        self._transformer = Transformer(client)

    @property
    def vae(self):
        return self._vae

    @property
    def transformer(self):
        return self._transformer


class BaseModelTrainer:
    def __init__(self, client: PigeonsAI, model_architecture: str):
        self.client = client
        self.model_architecture = model_architecture

    def _train(self, custom_model_name: str, train_set_uri: Optional[str] = None, **kwargs):
        if not train_set_uri and DataConnector.train_set_uri_global:
            train_set_uri = DataConnector.train_set_uri_global

        if not train_set_uri:
            raise ValueError("train_set_uri must be provided")

        data = {
            'custom_model_name': custom_model_name,
            'train_dataset_uri': train_set_uri,
            'original_model_name': 'Recommender',
            'model_architecture': self.model_architecture,
        }
        data.update(kwargs)

        url = BASE_URL_V2 + '/train'
        headers = self.client.auth_headers

        print(f'\033[38;2;229;192;108m      Initializing {custom_model_name} training \033[0m')

        response = self.client._request("POST", url, headers=headers, data=data)
        response_json = response.json()

        print(f'\033[38;2;85;87;93m Training job creation successful.\033[0m')

        print(
            f'\033[38;2;85;87;93m Unique Identifier:\033[0m \033[92m{response_json["data"]["unique_identifier"]}\033[0m')
        print(f'\033[38;2;85;87;93m Endpoint:\033[0m \033[92m{response_json["data"]["endpoint"]}\033[0m')
        print(f'\033[38;2;85;87;93m Message:\033[0m \033[92m{response_json["message"]}\033[0m')

        return response

    def _inference(
        self,
        user_id,
        user_interactions,
        k,
        recommend_seen,
        candidate_ids,
        model_endpoint,
        model_name,
    ):
        if not (user_id or user_interactions):
            raise ValueError("Either user_id or user_interactions must be provided.")
        if user_id and user_interactions:
            raise ValueError("Provide either user_id or user_interactions, not both.")
        if not model_name and not model_endpoint:
            raise ValueError("Either model_name or model_endpoint must be provided.")

        model_endpoint = _construct_model_url(model_name, model_endpoint, user_id, user_interactions)

        data = {
            "k": k,
            "recommend_seen": recommend_seen,
            "candidate_ids": candidate_ids
        }
        if user_id:
            data["user_id"] = user_id
        else:
            data["user_interactions"] = user_interactions

        headers = self.client.auth_headers

        try:
            response = self.client._http_client.post(model_endpoint, headers=headers, json=data, timeout=300.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"Status code: {e.response.status_code}, Error: {e.response.text}"
            print(error_message)
        except Exception as e:
            raise e

    def _retrain(
        self,
        unique_identifier: str,
        pull_latest_data: bool,
    ):
        if not unique_identifier:
            print('unique_identifier is required.')
            return
        if pull_latest_data is None:
            print('pull_latest_data is required.')
            return

        data = {
            'unique_identifier': unique_identifier,
            'pull_latest_data': pull_latest_data,
        }

        url = BASE_URL_V2 + '/retrain'
        headers = self.client.auth_headers

        print(f'\033[38;2;229;192;108m Initializing {unique_identifier} re-training \033[0m')

        response = self.client._request("POST", url, headers=headers, data=data)
        response_json = response.json()

        print(f'\033[38;2;85;87;93m Re-training job creation successful.\033[0m')
        print(f'\033[38;2;85;87;93m Detail:\033[0m \033[92m{response_json["data"]}\033[0m')

        return response


class Transformer(BaseModelTrainer):
    def __init__(self, client: PigeonsAI):
        super().__init__(client, model_architecture='transformer')

    def train(
        self,
        custom_model_name: str,
        train_set_uri: str,
        n_epochs: Optional[int] = None,
        batch_size: Optional[int] = None,
        learning_rate: Optional[float] = None,
        sequence_len: Optional[int] = None,
        train_num_negatives: Optional[int] = None,
        valid_num_negatives: Optional[int] = None,
        random_cut_prob: Optional[float] = None,
        replace_user_prob: Optional[float] = None,
        replace_item_prob: Optional[float] = None,
        random_seed: Optional[int] = None,
        hidden_dim: Optional[int] = None,
        temporal_dim: Optional[int] = None,
        num_proxy_item: Optional[int] = None,
        num_known_item: Optional[int] = None,
        num_layers: Optional[int] = None,
        num_heads: Optional[int] = None,
        dropout_prob: Optional[float] = None,
        temperature: Optional[float] = None,
        every: Optional[int] = None,
        patience: Optional[int] = None,
        optimizer_algorithm: Optional[str] = None,
        beta1: Optional[float] = None,
        beta2: Optional[float] = None,
        weight_decay: Optional[float] = None,
        subset: Optional[float] = None,
        threshold: Optional[float] = None
    ):
        kwargs = {
            'n_epochs': n_epochs,
            'batch_size': batch_size,
            'learning_rate': learning_rate,
            'sequence_len': sequence_len,
            'train_num_negatives': train_num_negatives,
            'valid_num_negatives': valid_num_negatives,
            'random_cut_prob': random_cut_prob,
            'replace_user_prob': replace_user_prob,
            'replace_item_prob': replace_item_prob,
            'random_seed': random_seed,
            'hidden_dim': hidden_dim,
            'temporal_dim': temporal_dim,
            'num_proxy_item': num_proxy_item,
            'num_known_item': num_known_item,
            'num_layers': num_layers,
            'num_heads': num_heads,
            'dropout_prob': dropout_prob,
            'temperature': temperature,
            'every': every,
            'patience': patience,
            'optimizer_algorithm': optimizer_algorithm,
            'beta1': beta1,
            'beta2': beta2,
            'weight_decay': weight_decay,
            'subset': subset,
            'threshold': threshold,
        }

        # get rid of None
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        return self._train(custom_model_name, train_set_uri, **filtered_kwargs)

    def inference(
        self,
        user_id: Optional[Union[str, int]] = None,
        user_interactions: Optional[Dict[str, Any]] = None,
        k: Optional[int] = 10,
        recommend_seen: Optional[bool] = True,
        candidate_ids: Optional[List[int]] = None,
        model_endpoint: str = None,
        model_name: str = None
    ):
        return self._inference(
            user_id=user_id,
            user_interactions=user_interactions,
            k=k,
            recommend_seen=recommend_seen,
            candidate_ids=candidate_ids,
            model_endpoint=model_endpoint,
            model_name=model_name
        )

    def retrain(
        self,
        unique_identifier: str,
        pull_latest_data: bool,
    ):
        return self._retrain(
            unique_identifier=unique_identifier,
            pull_latest_data=pull_latest_data,
        )


class VAE(BaseModelTrainer):
    def __init__(self, client: PigeonsAI):
        super().__init__(client, model_architecture='autoencoder')

    def train(
        self,
        custom_model_name: str,
        train_set_uri: str,
        n_epochs: Optional[str] = None,
        batch_size: Optional[str] = None,
        learn_rate: Optional[str] = None,
        beta: Optional[str] = None,
        verbose: Optional[str] = None,
        train_prop: Optional[str] = None,
        random_seed: Optional[str] = None,
        latent_dims: Optional[str] = None,
        hidden_dims: Optional[str] = None,
        eval_user_percent: Optional[str] = None,
        recall_at_k: Optional[str] = None,
        eval_iterations: Optional[str] = None,
        act_fn: Optional[str] = None,
        likelihood: Optional[str] = None,
        data_subset_percent: Optional[str] = None,
    ):
        kwargs = {
            'n_epochs': n_epochs,
            'batch_size': batch_size,
            'learn_rate': learn_rate,
            'beta': beta,
            'verbose': verbose,
            'train_prop': train_prop,
            'random_seed': random_seed,
            'latent_dims': latent_dims,
            'hidden_dims': hidden_dims,
            'eval_user_percent': eval_user_percent,
            'recall_at_k': recall_at_k,
            'eval_iterations': eval_iterations,
            'act_fn': act_fn,
            'likelihood': likelihood,
            'data_subset_percent': data_subset_percent,
        }

        # get rid of None
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        return self._train(custom_model_name, train_set_uri, **filtered_kwargs)

    def inference(
        self,
        user_id: Optional[int] = None,
        user_interactions: Optional[str] = None,
        recommend_seen: Optional[bool] = None,
        k: int = 10,
        model_endpoint: str = None,
        model_name: str = None
    ):
        if user_interactions is None and user_id is None:
            raise ValueError("Either user_id or user_history_ids must be provided.")

        if model_name and model_endpoint:
            raise ValueError("Both model_name and model_endpoint are provided. Either one of them will be used.")

        model_endpoint = _construct_model_url(model_name, model_endpoint, user_id, user_interactions)

        headers = self.client.auth_headers
        data = {
            "user_id": user_id,
            "user_interactions": user_interactions,
            "k": k,
            "recommend_seen": recommend_seen,
        }

        try:
            response = self.client._http_client.post(model_endpoint, headers=headers, json=data, timeout=300.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"Status code: {e.response.status_code}, Error: {e.response.text}"
            print(error_message)
        except Exception as e:
            raise e

    def retrain(
        self,
        unique_identifier: str,
        pull_latest_data: bool,
    ):
        return self._retrain(
            unique_identifier=unique_identifier,
            pull_latest_data=pull_latest_data,
        )


def _construct_model_url(
    model_name: Optional[str] = None,
    model_endpoint: Optional[str] = None,
    user_id: Optional[str] = None,
    user_interactions: Optional[Dict[str, Any]] = None
) -> str:
    base_endpoint = f"https://{model_name}.apps.pigeonsai.cloud" if model_name else model_endpoint.rstrip('/')
    if user_interactions:
        endpoint_suffix = "iid_recommend"
    elif user_id:
        endpoint_suffix = "uid_recommend"
    return f"{base_endpoint}/{endpoint_suffix}"
