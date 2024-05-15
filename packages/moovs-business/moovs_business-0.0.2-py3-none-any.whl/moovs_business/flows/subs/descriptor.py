import json
from typing import List, Tuple

import numpy as np
from pyqflow import QBatching, QClassicMap, QCombine, QRemoteMap, QWorkFlow
from pyqflow.actor import QActor
from pyqflow.functools import fst, partial, validcheck
from moovs_business.constants import URL, MOOVS_BUSINESS_API_KEY
from moovs_business.utils.helpers import sort_within_batch
from moovs_business.utils.serialize import descriptor_preprocess_and_serialize


class DescriptorFlow(QWorkFlow):
    """This workflow is used to perform descriptor estimation."""

    def __init__(
        self,
        ch: bool = True,
        img_size: List[int] = [640, 640, 3],
        batch_size: int = 40,
        endpoint: str = "descriptor",
        host: str = URL,
        **kwargs,
    ):
        """
        Initialize the DescriptorFlow class.

        Args:
            ch (bool, optional): Channel first. Defaults to True.
            img_size (List[int], optional): Image size. Defaults to [640, 640, 3].
            batch_size (int, optional): Batch size. Defaults to 40.
            endpoint (str, optional): Endpoint. Defaults to "descriptor".
            host (str, optional): Host. Defaults to "http://127.0.0.1:8000"
        """
        super().__init__(name="Descriptor")

        self.img_size = img_size
        self.batch = batch_size
        self.endpoint = f"{host}/{endpoint}"
        self.ch = ch

        params = (self.__dict__).copy()
        name = params.pop("name")
        params = json.dumps(params)

        self.pipeline = (
            QBatching(
                self.batch,
                select=validcheck(fst),
                name="Descriptor:Batching",
            )  # Creates batches of images.
            | QRemoteMap(
                url=self.endpoint,
                pack_function=partial(
                    descriptor_preprocess_and_serialize,
                    channel_first=self.ch,
                    size=self.img_size,
                ),
                unpack_function=(lambda data, outputs, _: list(zip(data, outputs))),
                name="Descriptor:Request",
                many=False,
                headers={
                    "x-api-key": MOOVS_BUSINESS_API_KEY,
                },
            )  # Send the data to the remote server
            | QCombine(name="Descriptor:Combine")  # Combine the predictions
            | QClassicMap(
                name="sort_within_batch", func=sort_within_batch
            )  # Sort the predictions
        )

        self.metadata_packet = (name, params)

    def get_metadata(self):
        """
        Get the metadata packet for the DescriptorFlow class.

        Returns:
            Tuple[str, str]: A tuple containing the name and the parameters in JSON format.
        """
        return self.metadata_packet

    def forward(self, input: QActor) -> QActor:
        """
        Process the input through the descriptor estimation pipeline.

        Args:
            input: The input data.

        Returns:
            The processed input data.
        """
        return self.pipeline(input)
