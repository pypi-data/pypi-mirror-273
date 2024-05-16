from typing import Dict, List, Optional

from google.cloud.firestore_v1 import DocumentSnapshot

from aipkgs_firebase.storage.core import FirebaseStorageCore
from aipkgs_firebase.storage.helpers import FirebaseStorageHelper


class FirebaseRootModel:
    collection_name = ""

    def __init__(self, collection_name: str = None) -> None:
        self.collection_name = collection_name

    def exists(self, document_id: str) -> bool:
        return FirebaseStorageCore.document_exists(
            collection_name=self.collection_name, document_id=document_id
        )

    def exists_where(self, filters: Dict[str, any]) -> bool:
        return FirebaseStorageHelper.document_exists(
            collection_name=self.collection_name, filters=filters
        )

    def get_document(self, document_id: str) -> Optional[dict]:
        return FirebaseStorageHelper.get_document(
            collection_name=self.collection_name, document_id=document_id
        )

    def get_document_where(self, filters: Dict[str, any]) -> dict:
        return FirebaseStorageHelper.get_document_where(
            collection_name=self.collection_name, filters=filters
        )

    def get_document_realtime(self, document_id: str, callback):
        def temp_callback(document):
            callback(document)

        return FirebaseStorageHelper.get_document_realtime(
            collection_name=self.collection_name, document_id=document_id, callback=temp_callback
        )

    def get_document_changes_realtime(self, document_id: str, callback):
        def temp_callback(document, changes, read_time):
            callback(document, changes, read_time)

        return FirebaseStorageHelper.get_document_changes_realtime(
            collection_name=self.collection_name, document_id=document_id, callback=temp_callback
        )

    def get_documents_changes_realtime(self, document_id: str, callback):
        def temp_callback(doc_snapshot, changes, read_time):
            callback(doc_snapshot, changes, read_time)

        return FirebaseStorageHelper.get_documents_changes_realtime(
            collection_name=self.collection_name, document_id=document_id, callback=temp_callback
        )

    def get_documents(self, filters: Dict[str, any] = None) -> List[dict]:
        return FirebaseStorageHelper.get_documents(
            collection_name=self.collection_name, filters=filters
        )

    def create(self, dictionary: dict, document_id: str = None) -> bool:
        return self.create_document(dictionary, document_id)

    def create_document(self, dictionary: dict, document_id: str = None) -> bool:
        return FirebaseStorageCore.create_document_from_data(
            dictionary_data=dictionary,
            collection_name=self.collection_name,
            document_id=document_id,
        )

    def create_document_from_snapshot(self, snapshot: DocumentSnapshot):
        return FirebaseStorageCore.create_document_from_snapshot(
            collection_name=self.collection_name, snapshot=snapshot
        )

    def update(self, dictionary: dict, document_id: str):
        FirebaseStorageCore.update_document_with_data(
            dictionary_data=dictionary,
            collection_name=self.collection_name,
            document_id=document_id,
        )

    def remove(self, document_id: str):
        FirebaseStorageCore.remove_document(
            collection_name=self.collection_name, document_id=document_id
        )

    def remove_all(self):
        FirebaseStorageCore.remove_documents(
            collection_name=self.collection_name)
