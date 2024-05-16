# Documentation
# https://firebase.google.com/docs/firestore

from datetime import datetime
import threading
from typing import Dict, List

import firebase_admin
from google.cloud.firestore_v1 import FieldFilter, CollectionReference, DocumentReference, DocumentSnapshot

from aipkgs_firebase import helpers


class FirebaseStorageCore:
    @staticmethod
    def collection_ref(
            collection_name: str,
    ) -> CollectionReference:
        return helpers.firebase_db().collection("{}".format(collection_name))

    @staticmethod
    def document_ref(
            collection_name: str, document_id: str
    ) -> DocumentReference:
        doc_ref = FirebaseStorageCore.collection_ref(collection_name=collection_name).document(
            document_id=document_id
        )
        return doc_ref

    @staticmethod
    def document_exists(collection_name: str, document_id: str) -> bool:
        doc_ref = FirebaseStorageCore.document_ref(
            collection_name=collection_name, document_id=document_id)
        doc = doc_ref.get()

        if doc.exists:
            return True

        return False

    @staticmethod
    def get_document(
            collection_name: str, document_id: str
    ) -> DocumentSnapshot:
        doc_ref = FirebaseStorageCore.document_ref(
            collection_name=collection_name, document_id=document_id)
        doc = doc_ref.get()

        return doc

    @staticmethod
    def get_document_realtime(
            collection_name: str, document_id: str, callback):
        doc_ref = FirebaseStorageCore.document_ref(
            collection_name=collection_name, document_id=document_id)

        callback_done = threading.Event()

        # Create a callback on_snapshot function to capture changes
        def on_snapshot(doc_snapshot, changes, read_time):
            callback(doc_snapshot, changes, read_time)
            callback_done.set()

        # Watch the document
        doc_watch = doc_ref.on_snapshot(on_snapshot)

        return doc_watch

    @staticmethod
    def get_documents(
            collection_name: str, filters: Dict[str, any] = None
    ) -> List[DocumentSnapshot]:
        col_ref = FirebaseStorageCore.collection_ref(collection_name=collection_name)
        if filters:
            for key, value in filters.items():
                col_ref = col_ref.where(filter=FieldFilter(field_path=f"{key}", op_string="==", value=value))

        docs = col_ref.get()

        return docs

    @staticmethod
    def create_document_from_data(
            dictionary_data: dict, collection_name: str, document_id: str = None
    ) -> bool:
        data = dictionary_data

        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y %I:%M:%S %p")
        data["timestamp"] = firebase_admin.firestore.SERVER_TIMESTAMP
        data["created_at"] = timestamp

        # current_time = time.time()
        if document_id is not None:
            # If the document ID is provided, use it to create or update the document
            if not FirebaseStorageCore.document_exists(
                    collection_name=collection_name, document_id=document_id
            ):
                doc_ref = FirebaseStorageCore.document_ref(
                    collection_name=collection_name, document_id=document_id
                )
                data["document_id"] = document_id  # Add document_id to data
                doc_ref.set(data, merge=True)
                return True
        else:
            # If no document ID is provided, let Firestore generate one
            doc_ref = FirebaseStorageCore.collection_ref(
                collection_name=collection_name
            ).document()

            document_id = doc_ref.id  # Get the auto-generated document ID
            data["document_id"] = document_id  # Update data with the generated document ID
            doc_ref.set(data, merge=False)

            # doc_ref.set(data, merge=True)  # Resave the data with the document ID included

            return True

        return False

    @staticmethod
    def create_document_from_snapshot(
            collection_name: str, snapshot: DocumentSnapshot
    ):
        data = snapshot.to_dict()

        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y %I:%M:%S %p")
        data["timestamp"] = firebase_admin.firestore.SERVER_TIMESTAMP
        data["created_at"] = timestamp

        document_id = snapshot.id

        if not FirebaseStorageCore.document_exists(
                collection_name=collection_name, document_id=document_id
        ):
            doc_ref = FirebaseStorageCore.document_ref(
                collection_name=collection_name, document_id=document_id
            )
            data["document_id"] = document_id
            doc_ref.set(data, merge=True)

    # @staticmethod
    # def create_collection_in_collection(
    #         root_collection_name: str, sub_collection_name:str, dictionary_data: dict, document_id: str = None):
    #     data = dictionary_data
    #
    #     now = datetime.now()
    #     timestamp = now.strftime("%d-%m-%Y %I:%M:%S %p")
    #     data["timestamp"] = firebase_admin.firestore.SERVER_TIMESTAMP
    #     data["created_at"] = timestamp
    #
    #     if document_id is not None:
    #         if not FirebaseStorageCore.document_exists(
    #                 collection_name=root_collection_name, document_id=document_id
    #         ):
    #             doc_ref = FirebaseStorageCore.document_ref(
    #                 collection_name=root_collection_name, document_id=document_id
    #             )
    #             data["document_id"] = document_id

    @staticmethod
    def update_document_with_data(
            dictionary_data: dict, collection_name: str, document_id: str
    ):
        data = dictionary_data

        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y %I:%M:%S %p")
        data["updated_at"] = timestamp

        if document_id is not None:
            if FirebaseStorageCore.document_exists(collection_name=collection_name, document_id=document_id):
                doc_ref = FirebaseStorageCore.document_ref(
                    collection_name=collection_name, document_id=document_id
                )
                doc_ref.update(field_updates=data)

    @staticmethod
    def remove_document(collection_name: str, document_id: str):
        if document_id is not None:
            if FirebaseStorageCore.document_exists(collection_name=collection_name, document_id=document_id):
                doc_ref = FirebaseStorageCore.document_ref(
                    collection_name=collection_name, document_id=document_id
                )
                doc_ref.delete()

    @staticmethod
    def remove_documents(collection_name: str):
        documents = FirebaseStorageCore.get_documents(collection_name=collection_name)
        for document in documents:
            FirebaseStorageCore.remove_document(collection_name=collection_name,
                                                document_id=document.id)
