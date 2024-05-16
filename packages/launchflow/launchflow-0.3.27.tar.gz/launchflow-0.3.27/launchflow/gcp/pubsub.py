try:
    from google.cloud.pubsub import PublisherClient
    from google.pubsub_v1.services.publisher import PublisherAsyncClient
    from google.pubsub_v1.types import PubsubMessage
except ImportError:
    PublisherClient = None
    PublisherAsyncClient = None
    PubsubMessage = None


from typing import Union

from launchflow.depends import Depends
from launchflow.gcp.resource import GCPResource
from pydantic import BaseModel


class PubsubTopicConnectionInfo(BaseModel):
    topic_id: str


class PubsubTopic(GCPResource[PubsubTopicConnectionInfo]):
    """A GCP Cloud Pub/Sub Topic.

    **Example usage:**
    ```python
    import launchflow as lf

    topic = lf.gcp.PubsubTopic("my-pubsub-topic")

    topic.publish(b"Hello, world!")
    ```
    """

    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            product_name="gcp_pubsub_topic",
            create_args={},
        )

    def publish(self, data: bytes, ordering_key: str = ""):
        """Publish a message to the topic.

        Args:
        - `data`: The bytes to publish in the message
        - `ordering_key`: An optional ordering key for the message

        **Example usage:**

        ```python
        import launchflow as lf

        topic = lf.gcp.PubsubTopic("my-pubsub-topic")

        topic.publish(b"Hello, world!")
        ```
        """
        if PublisherClient is None:
            raise ImportError(
                "google-cloud-pubsub not installed. Please install it with "
                "`pip install launchflow[gcp]`."
            )
        connection = self.connect()
        client = PublisherClient()
        return client.publish(connection.topic_id, data, ordering_key=ordering_key)

    async def publish_async(self, data: bytes, ordering_key: str = ""):
        """Asynchronously publish a message to the topic.

        Args:
        - `data`: The bytes to publish in the message
        - `ordering_key`: An optional ordering key for the message

        **Example usage:**

        ```python
        import launchflow as lf

        topic = lf.gcp.PubsubTopic("my-pubsub-topic")

        await topic.publish_async(b"Hello, world!")
        ```
        """
        if PublisherAsyncClient is None:
            raise ImportError(
                "google-cloud-pubsub not installed. Please install it with "
                "`pip install launchflow[gcp]`."
            )
        connection = await self.connect_async()
        client = PublisherAsyncClient()
        return await client.publish(
            messages=[PubsubMessage(data=data, ordering_key=ordering_key)],
            topic=connection.topic_id,
        )


class PubsubSubscriptionConnectionInfo(BaseModel):
    subscription_id: str


class PubsubSubscription(GCPResource[PubsubSubscriptionConnectionInfo]):
    """A GCP Cloud Pub/Sub Topic.

    **Example usage:**
    ```python
    import launchflow as lf

    topic = lf.gcp.PubsubTopic("my-pubsub-topic")
    subscription = lf.gcp.PubsubSubscription("my-pubsub-sub", topic=topic)

    topic.publish(b"Hello, world!")
    ```
    """

    def __init__(self, name: str, topic: Union[PubsubTopic, str]) -> None:
        depends_on = []
        create_args = {}
        if isinstance(topic, PubsubTopic):
            create_args["pubsub_topic_id"] = Depends(lambda: topic.connect().topic_id)
            depends_on.append(topic)
        elif isinstance(topic, str):
            create_args["pubsub_topic_id"] = topic
        else:
            # TODO: revisit this when we have generics
            raise ValueError("topic must be a PubsubTopic or a str")
        super().__init__(
            name=name,
            product_name="gcp_pubsub_subscription",
            create_args=create_args,
            depends_on=depends_on,
        )
