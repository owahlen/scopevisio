import logging
from pathlib import Path
from typing import MutableMapping

from journal import write_journal
from scopevisio_api_iterator import ScopevisioApiIterator
from scopevisio_session import ScopevisioSession


def retrieve_accounting(config: MutableMapping,
                        export_folder_name: str,
                        skip_document_download: bool):
    with ScopevisioSession(config) as session:
        export_folder_path = Path(export_folder_name)
        export_folder_path.mkdir(exist_ok=True)
        documents_folder_path = Path(export_folder_name, 'documents')
        documents_folder_path.mkdir(exist_ok=True)
        journal = session.get_journal()
        write_journal(journal, export_folder_path=export_folder_path)
        if not skip_document_download:
            download_documents_from_journal(session, journal, documents_folder_path)


def download_documents_from_journal(session: ScopevisioSession,
                                    journal: ScopevisioApiIterator,
                                    documents_folder_path: Path):
    fetched_document_numbers = {}
    for j in journal:
        document_number = j['documentNumber']
        if document_number not in fetched_document_numbers:
            try:
                session.download_document(document_number, documents_folder_path)
                fetched_document_numbers[document_number] = True
            except IOError:
                logging.warning(f'Unable to download document {document_number}. Skipping to next document...')
                continue
