import tempfile
import gzip
import shutil
import os
from datetime import datetime

from googleads import ad_manager
from googleads import errors


def main(client):
    # Initialize a DataDownloader.
    report_downloader = client.GetDataDownloader(version='v202402')

    report_job = {
        'reportQuery': {
            'dimensions': ['DATE', 'CREATIVE_ID', 'LINE_ITEM_ID', 'CAMPAIGN_ID', 'ORDER_ID', 'ORDER_NAME', 'LINE_ITEM_NAME'],
            'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS', 'AD_SERVER_CTR'],
            'dateRangeType': 'YESTERDAY'
        }
    }

    try:
        report_job_id = report_downloader.WaitForReport(report_job)
    except errors.AdManagerReportError as e:
        print('Failed to generate report. Error was: %s' % e)

    export_format = 'CSV_DUMP'

    report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False)

    report_downloader.DownloadReportToFile(report_job_id, export_format, report_file)

    report_file.close()

    # Wypakowanie pliku .gz do formatu CSV
    with gzip.open(report_file.name, 'rb') as f_in:
        with open(report_file.name[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Usunięcie pliku .gz
    os.remove(report_file.name)

    # Zmiana formatu daty w pliku CSV
    with open(report_file.name[:-3], 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(report_file.name[:-3], 'w', encoding='utf-8') as file:
        for line in lines:
            parts = line.split(',')
            if parts[0] != 'Dimension.DATE':
                date = datetime.strptime(parts[0], '%Y-%m-%d').strftime('%Y%m%d')
                parts[0] = date
                file.write(','.join(parts))
            else:
                file.write(line)

    print('Report job with id "%s" downloaded, extracted, and date format changed to:\n%s' % (
        report_job_id, report_file.name[:-3]))


if __name__ == '__main__':
    ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage(r"C:\Users\pmackowka\OneDrive - Empik S.A\Dokumenty\Dokumenty\github\ad-manager\googleads.yaml")
    main(ad_manager_client)