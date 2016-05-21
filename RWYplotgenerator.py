import math
import matplotlib as mpl
mpl.use('Cairo')
import matplotlib.pyplot as plt
import syslog
import time
import weewx.reportengine

def logmsg(lvl, msg):
    syslog.syslog(lvl, 'RWYplotgenerator: {}'.format(msg))

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)


class RWYplotgenerator(weewx.reportengine.ReportGenerator):
    """Class for drawing a windvector on airport runway diagram"""

    def run(self):
        """Main entry point for plot generation"""

        if self._get_rwy_diagram():
            self.generateplot(self.img)
        else:
            logerr('RWYplotgenerator skipped')

    def generateplot(self, input_image):
        """Draw plot"""

        outputimg = self.skin_dict['RWYplotGenerator']['output_image']
        outputdpi = int(self.skin_dict['RWYplotGenerator']['output_image_dpi'])
        outputarrowcolor = self.skin_dict['RWYplotGenerator']['output_image_arrow_color']
        outputimg_fontsize = self.skin_dict['RWYplotGenerator']['output_image_fontsize']
        outputarrow_xpos = int(self.skin_dict['RWYplotGenerator']['output_arrow_xpos'])
        outputarrow_ypos = int(self.skin_dict['RWYplotGenerator']['output_arrow_ypos'])

        default_archive = self.db_binder.get_manager()
        record = default_archive.getRecord(default_archive.lastGoodStamp())

        # Wind direction from database record
        windw = record['windDir']
        windv = record['windSpeed']

        # Polar coordinates: convert angle so that vector (wind) with 0 degrees is
        # 'pointing down' (negative Y-axis) and not to the right (postive X-axis),
        # which is customary in a polar grid.
        angle = math.radians(270 - windw)

        # Plot input image
        plt.imshow(input_image)
        # Disable the axis
        plt.axis('off')

        # Set title
        timestamp = time.strftime('%a, %d %b %H:%M', time.localtime())
        title = '{} LT\n{} degrees - {:.0f} knots'.format(timestamp, windw, windv)
        fontdict = {'fontsize': outputimg_fontsize}
        plt.title(title, fontdict)

        # Quiver plot
        # Currently, the wind speed from database record is not used for shaping the arrow.
        # Wind speed (arrow length) is fixed to create constant arrow length
        windv = 200
        plt.quiver(outputarrow_xpos, outputarrow_ypos, windv * math.cos(angle),
                   windv * math.sin(angle), angles='uv', scale=1.0, scale_units='xy',
                   pivot='middle', width=0.02, color=outputarrowcolor)

        # Write output image
        try:
            plt.savefig(outputimg, dpi=outputdpi)
        except:
            logerr('Could not write output image: {}'.format(outputimg))
        finally:
            plt.close('all')

    def _get_rwy_diagram(self):

        inputimg = self.skin_dict['RWYplotGenerator']['input_image']

        # Read input image
        try:
            self.img = plt.imread(inputimg)
        except IOError:
            logerr('Input image not found: {}'.format(inputimg))
            return (False)
        else:
            return (True)
