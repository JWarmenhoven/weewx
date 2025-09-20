import pandas as pd


# Due to bug in pandas versions prior <0.25
pd.options.display.max_colwidth = 250


import syslog
import traceback
import locale
import weewx.reportengine
from urllib.error import URLError

def logmsg(lvl, msg):
    syslog.syslog(lvl, 'FetchMetarTaf: {}'.format(msg))

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)

def log_exception(context, exception):
    """Helper function to log detailed exception info."""
    logerr(f"{context}: {exception}")
    logerr(traceback.format_exc())


class MetarTafLoader(weewx.reportengine.ReportGenerator):
    """Class for downloading metar & taf records"""


    def run(self):
        """Main entry point for downloading records"""
        self.metar_url = self.skin_dict['FetchMetarTaf']['metar_url']
        self.taf_url = self.skin_dict['FetchMetarTaf']['taf_url']
        self.stations = self.skin_dict['FetchMetarTaf']['stations']
        self.metar_dataframe_path = self.skin_dict['FetchMetarTaf']['metar_dataframe_path']
        self.taf_dataframe_path = self.skin_dict['FetchMetarTaf']['taf_dataframe_path']


        self._download_records()
        self._create_dataframe()

    def _create_dataframe(self):
        """Create pandas DataFrame and write to HTML"""

        stations_filter = [s.strip() for s in self.stations]

        try:
            metar_subset = self.metar.drop_duplicates().reindex(stations_filter).dropna()
            metar_subset.to_html(self.metar_dataframe_path,
                    header=False,
                    index=False,
                    border=0,
                    table_id='metar'
                    )
        except (AttributeError, OSError, ValueError) as e:
            log_exception(f"Could not write METAR dataframe to {self.metar_dataframe_path}", e)
 
        try:
            taf_subset = self.taf.drop_duplicates().reindex(stations_filter).dropna()
            taf_subset.to_html(self.taf_dataframe_path,
                    header=False,
                    index=False,
                    border=0,
                    table_id='taf'
                    )
        except (AttributeError, OSError, ValueError) as e:
            log_exception(f"Could not write TAF dataframe to {self.taf_dataframe_path}", e)


    def _download_records(self):
        """Download records from textserver"""

        try:
            self.metar = pd.read_xml(self.metar_url, xpath=".//METAR"
                                     ).set_index('station_id').sort_index()['raw_text'].to_frame()
        except (pd.errors.EmptyDataError, pd.errors.ParserError, URLError, FileNotFoundError) as e:
            log_exception(f"Unable to download METAR records from {self.metar_url}", e)
            self.metar = pd.DataFrame(columns=['raw_text']) # fallback to empty DF

        try:
            self.taf = pd.read_xml(self.taf_url, xpath=".//TAF"
                                   ).set_index('station_id').sort_index()['raw_text'].to_frame()
        except (pd.errors.EmptyDataError, pd.errors.ParserError, URLError, FileNotFoundError) as e:
            log_exception(f"Unable to download TAF records from {self.taf_url}", e)
            self.taf = pd.DataFrame(columns=['raw_text']) # fallback to empty DF




