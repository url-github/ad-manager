#!/usr/bin/env python
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Analiza efektywności kampanii reklamowych pod kątem osiągniętego zasięgu, czyli liczby unikalnych użytkowników, którzy zobaczyli reklamę w określonym czasie."""

import tempfile

# Import appropriate modules from the client library.
from googleads import ad_manager
from googleads import errors


def main(client):
  # Initialize a DataDownloader.
  report_downloader = client.GetDataDownloader(version='v202402')

  # gam_lineItem_id = LINE_ITEM_ID
  # Element zamówienia to zobowiązanie reklamodawcy do zakupu określonej liczby wyświetleń reklamy, kliknięć lub czasu.

    # gam_creative_id = CREATIVE_ID
    # Reprezentuje media dla wyświetlanej reklamy.
    # https://support.google.com/admanager/answer/3185155?hl=pl&sjid=2814258854508978251-EU

    # gam_campaign_id = Brak

  report_job = {
      'reportQuery': {
          'dimensions': ['DATE', 'CREATIVE_ID', 'LINE_ITEM_ID', 'LINE_ITEM_NAME'],
          'columns': ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS',
                      'AD_SERVER_CTR'],
          'dateRangeType': 'REACH_LIFETIME'
      }
  }

  try:
    # Run the report and wait for it to finish.
    report_job_id = report_downloader.WaitForReport(report_job)
  except errors.AdManagerReportError as e:
    print('Failed to generate report. Error was: %s' % e)

  # Change to your preferred export format.
  export_format = 'CSV_DUMP'

  report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False)

  # Download report data.
  report_downloader.DownloadReportToFile(
      report_job_id, export_format, report_file)

  report_file.close()

  # Display results.
  print('Report job with id "%s" downloaded to:\n%s' % (
      report_job_id, report_file.name))


if __name__ == '__main__':
  # Initialize client object.
  ad_manager_client = ad_manager.AdManagerClient.LoadFromStorage(r"C:\Users\pmackowka\OneDrive - Empik S.A\Dokumenty\Dokumenty\github\ad-manager\googleads.yaml")
  main(ad_manager_client)

# Output:
# Report job with id "14436793892" downloaded to:        
# C:\Users\PMACKO~1\AppData\Local\Temp\tmpvbeffdq7.csv.gz