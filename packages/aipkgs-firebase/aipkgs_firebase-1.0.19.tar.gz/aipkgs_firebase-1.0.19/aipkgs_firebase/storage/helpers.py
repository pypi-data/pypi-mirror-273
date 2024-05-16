from typing import Dict, List, Optional

from aipkgs_firebase.storage.core import FirebaseStorageCore


# Use the application default credentials

class FirebaseStorageHelper:

    @staticmethod
    def document_exists(collection_name: str, filters: Dict[str, any]) -> bool:
        docs = FirebaseStorageCore.get_documents(
            collection_name=collection_name, filters=filters
        )

        if docs:
            return True

        return False

    @staticmethod
    def get_document(collection_name: str, document_id: str) -> Optional[dict]:
        doc = FirebaseStorageCore.get_document(
            collection_name=collection_name, document_id=document_id
        )

        if doc.exists:
            dictionary = doc.to_dict()
            dictionary["document_id"] = doc.id
            return dictionary

        return None

    @staticmethod
    def get_document_where(collection_name: str, filters: Dict[str, any] = None) -> Optional[dict]:
        docs = FirebaseStorageCore.get_documents(
            collection_name=collection_name, filters=filters
        )

        if docs:
            doc = docs[0]
            dictionary = doc.to_dict()
            dictionary["document_id"] = doc.id
            return dictionary

        return None

    @staticmethod
    def get_document_realtime(collection_name: str, document_id: str, callback):
        def temp_callback(doc_snapshot, changes, read_time):
            if len(doc_snapshot) == 1:
                doc = doc_snapshot[0]

                if doc.exists:
                    dictionary = doc.to_dict()
                    dictionary["document_id"] = doc.id

                    callback(dictionary)
                else:
                    callback(None)
            else:
                callback(None)

        doc_watch = FirebaseStorageHelper.get_documents_changes_realtime(collection_name=collection_name, document_id=document_id, callback=temp_callback)

        return doc_watch

    @staticmethod
    def get_document_changes_realtime(collection_name: str, document_id: str, callback):
        def temp_callback(doc_snapshot, changes, read_time):
            if len(doc_snapshot) == 1:
                doc = doc_snapshot[0]

                if doc.exists:
                    dictionary = doc.to_dict()
                    dictionary["document_id"] = doc.id

                    callback(dictionary, changes, read_time)
                else:
                    callback(None, changes, read_time)
            else:
                callback(None, changes, read_time)

        doc_watch = FirebaseStorageHelper.get_documents_changes_realtime(collection_name=collection_name, document_id=document_id, callback=temp_callback)

        return doc_watch

    @staticmethod
    def get_documents_changes_realtime(collection_name: str, document_id: str, callback):
        def temp_callback(doc_snapshot, changes, read_time):
            callback(doc_snapshot, changes, read_time)

        doc_watch = FirebaseStorageCore.get_document_realtime(
            collection_name=collection_name, document_id=document_id, callback=temp_callback
        )

        return doc_watch

    def get_documents(collection_name: str, filters: Dict[str, any] = None) -> List[dict]:
        docs = FirebaseStorageCore.get_documents(
            collection_name=collection_name, filters=filters
        )

        if docs:
            docs_dict: List[dict] = []
            for doc in docs:
                dictionary = doc.to_dict()
                dictionary["document_id"] = doc.id
                docs_dict.append(dictionary)
            return docs_dict

        return []
