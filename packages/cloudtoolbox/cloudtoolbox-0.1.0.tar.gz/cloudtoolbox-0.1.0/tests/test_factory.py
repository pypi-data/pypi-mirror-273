import unittest
from unittest import mock

from cloud import factory
from cloud.amazon import s3
from cloud.google import pubsub, storage
from cloud.protocols import MessagePublisher, StorageUploader


class NotStorageUploader:
    def upload_file(self):
        pass


class NotMessagePublisher:
    def send_message(self):
        pass


class TestStorageUploaderFactory(unittest.TestCase):
    @mock.patch("google.cloud.storage.Client")
    def test_google_uploader(self, _):
        Uploader = factory.storage_uploader(storage.Uploader)
        uploader = Uploader()

        self.assertIsInstance(uploader, StorageUploader)
        self.assertIsInstance(uploader, storage.Uploader)

    @mock.patch("boto3.client")
    def test_amazon_uploader(self, _):
        Uploader = factory.storage_uploader(s3.Uploader)
        uploader = Uploader()

        self.assertIsInstance(uploader, StorageUploader)
        self.assertIsInstance(uploader, s3.Uploader)

    def test_uploader_protocol_validation(self):
        error = "NotStorageUploader does not implement StorageUploader protocol"

        with self.assertRaisesRegex(AssertionError, error):
            factory.storage_uploader(NotStorageUploader)  # type: ignore


class TestMessagePublisherFactory(unittest.TestCase):
    @mock.patch("google.cloud.pubsub_v1.PublisherClient")
    def test_google_publisher(self, _):
        Publisher = factory.message_publisher(pubsub.Publisher)
        publisher = Publisher()

        self.assertIsInstance(publisher, MessagePublisher)
        self.assertIsInstance(publisher, pubsub.Publisher)

    def test_publisher_protocol_validation(self):
        error = "NotMessagePublisher does not implement MessagePublisher protocol"

        with self.assertRaisesRegex(AssertionError, error):
            factory.message_publisher(NotMessagePublisher)  # type: ignore
