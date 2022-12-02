import pandas as pd

import logging


def write_journal(journal, export_folder_path):
    logging.info('downloading journal...')
    records = [{
        'BuchungsId': j['pdeRowNumber'],
        'Buchungsnummer': j['documentNumber'],
        'Buchungsdatum': j['postingDate'],
        'Externe Belegnummer': j['externalDocumentNumber'],
        'Storno für BuchungsId': j['cancellationNumber'],

        'BuchungspositionsId': j['rowNumber'],
        'Konto': j['accountNumber'],
        'Kontoname': j['accountName'],
        'Kontotyp': j['accountType'],
        'Personenkonto': j['personalAccountNumber'],
        'Personenkontoname': j['personalAccountName'],
        'Soll': j['debitAmount'],
        'Haben': j['creditAmount'],
        'Erstelldatum': j['createdTS'],
        'Externes Belegdatum': j['externalDocumentTS'],
        'Steuerschlüssel': j['vatKey'],
        'Steuersatz': j['vatRate'],
        'Buchungstext': j['documentText'],

        'Buchungsposition': j['postingText']
    } for j in journal]
    spreadsheet_name = export_folder_path.joinpath('journal.xlsx')
    df = pd.DataFrame.from_records(records)
    df.to_excel(spreadsheet_name, index=False)
