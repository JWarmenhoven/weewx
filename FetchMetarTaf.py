import pandas as pd


# Due to bug in pandas versions prior <0.25
pd.options.display.max_colwidth = 250


import syslog
import locale
import weewx.reportengine

def logmsg(lvl, msg):
    syslog.syslog(lvl, 'FetchMetarTaf: {}'.format(msg))

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)


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
        """Create pandas DataFrame"""

        # Write DataFrame
        stations_filter = [s.strip() for s in self.stations]
#        metar_subset = self.metar.loc[self.metar.index.intersection(stations_filter)]
        metar_subset = self.metar.drop_duplicates().reindex(stations_filter).dropna()
#        taf_subset = self.taf.loc[self.taf.index.intersection(stations_filter)]
        taf_subset = self.taf.drop_duplicates().reindex(stations_filter).dropna()

        try:
            metar_subset.to_html(self.metar_dataframe_path,
                    header=False,
                    index=False,
                    border=0,
                    table_id='metar'
                    )
        except:
            logerr('FetchMetarTaf: Could not write dataframe: {}'.format(self.metar_dataframe_path))
 
        try:
            taf_subset.to_html(self.taf_dataframe_path,
                    header=False,
                    index=False,
                    border=0,
                    table_id='taf'
                    )
        except:
            logerr('FetchMetarTaf: Could not write dataframe: {}'.format(self.taf_dataframe_path))




    def _download_records(self):
        """Download records from textserver"""

        try:
            self.metar = pd.read_csv(self.metar_url,
                    skiprows=5,
                    index_col=1,
                    usecols=[0,1]
                    ).sort_index()
        except:
            logerr('FetchMetarTaf: Unable to download METAR records from {}.'.format(self.metar_url))

        try:
            self.taf = pd.read_csv(self.taf_url,
                    skiprows=6,
                    header=None,
                    index_col=1,
                    usecols=[0,1],
                    names=['raw_text', 'station_id']
                    ).sort_index()
        except:
            logerr('FetchMetarTaf: Unable to download TAF records from {}.'.format(self.taf_url))

