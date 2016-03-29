from __future__ import with_statement

import math
import matplotlib
matplotlib.use('Cairo')
import matplotlib.pyplot as plt
import syslog
import time

import weewx.reportengine


def logmsg(lvl, msg):
    syslog.syslog(lvl, 'RWYplotgenerator: %s' % msg)


def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)


class RWYplotgenerator(weewx.reportengine.ReportGenerator):
    """Class for drawing a windvector on airport runway diagram"""

    def run(self):
        """Main entry point for plot generation"""

        loginf('RWYplotgenerator started!')

        t1 = time.time()
        self.setup()
        self.generateplot()

        elapsed_time = time.time() - t1
        loginf('Generated RWYplot in %.2f seconds' % elapsed_time)

    def setup(self):
        pass

    def generateplot(self):
        """Draw plot"""
        #loginf('Start plotting!')

        inputimg = self.skin_dict['RWYplotGenerator']['source_image']
        outputimg = self.skin_dict['RWYplotGenerator']['output_image']
        outputdpi = self.skin_dict['RWYplotGenerator']['output_image_dpi']
        outputarrowcolor = self.skin_dict['RWYplotGenerator']['output_image_arrow_color']

        default_archive = self.db_binder.get_manager()
        record = default_archive.getRecord(default_archive.lastGoodStamp())
        #loginf(record)

        # Wind direction from database record
        windw = record['windDir']

        # Wind speed from database record
        windv = record['windSpeed']

        # Polar coordinates: convert angle so that vector (wind) with 0 degrees is 'pointing down' (negative
        # Y-axis and not to the right (postive X-axis), which is customary in a polar grid.
        angle = math.radians(270 - windw)

        # Create figure - set up container
        fig = plt.figure(figsize=(3, 3))
        ax = fig.add_subplot(111)

        # Read background image of Runways & insert in plot
        # wrap in try block!
        img = plt.imread(inputimg)
        ax.imshow(img, origin='lower', zorder=0)

        # Disable the axis
        ax.axis('off')

        # Set title
        timestamp = time.strftime("%a, %d %b %H:%M", time.localtime())
        title = timestamp + ' LT' + '\n' + str(int(windw)) + ' degrees - ' + str(int(round(windv))) + ' knots'
        fontdict = {'fontsize': 8}
        ax.set_title(title, fontdict)

        # Quiver plot
        # Wind speed (arrow length) is fixed to create constant arrow length
        windv = 200
        ax.quiver(350, 400, windv * math.cos(angle), windv * math.sin(angle),
                  angles='xy',
                  scale=1.0,
                  scale_units='xy',
                  pivot='middle',
                  width=0.02,
                  color=outputarrowcolor
                  )
        # wrap in try block!
        plt.savefig(outputimg, dpi=int(outputdpi))
        plt.close('all')