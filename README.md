# weewx
WeeWX - weather station software - customizations

#### RWYplotgenerator
This is a custom generator for weewx that uses matplotlib to plot wind data onto an input image for every report update. This generator only creates the image and you will have to integrate it into a weewx report template yourself.<BR>
Example:<P>
Input: An image on which to plot the data. Below example shows runways for airfield ESMH, Sweden.<BR>
<IMG src='ESMH.png' height=40% width=40%><BR>
Output:<BR>
<IMG src='http://nsf.se/wx/ESMH_wind.png' height=50% width=50%>
<P>
Online example: http://www.nsf.se/wx/index.html

##### Requirements:<P>
- Weewx (on a <A href='https://www.raspberrypi.org/products'> Raspberry Pi</A> for example!)
- Python plotting module: matplotlib.<BR>
Can be installed using your package manager (```sudo apt-get install python-matplotlib```) or using pip/conda.

##### Configuration/Use:<P>
- Copy ```RWYplotgenerator.py``` to directory with user extensions. (```/usr/share/weewx/user``` in Debian)

- Insert following to your ```StdReport``` section in your ```weewx.conf``` file:

```
[[RWYplotgenerator]]
  skin = RWYplotgenerator
  enable = true 
```
- Copy ```skin.conf``` to the RWYplotgenerator skin directory. 

- Create and customize a ```skin.conf``` file:

```
[RWYplotGenerator]
    input_image = path to input image

    output_image_dpi = 300
    output_image_arrow_color = red      # http://matplotlib.org/api/colors_api.html
    output_image = path to output image
    output_image_fontsize = 12
    output_arrow_xpos = 350             # (pixel coordinates) You will need to adjust this to place the 
    output_arrow_ypos = 300             # arrow on a specific location on the input image

#
# The list of generators that are to be run:
#
[Generators]
        generator_list = user.RWYplotgenerator.RWYplotgenerator

```


#### FetchMetarTaf
Generator that fetches METAR & TAF data for airfields you select in the skin.conf file. It retrieves cached data from <A href='https://aviationweather.gov/data/api/#cache'>Aviation Weather Center</A>. The data is written to two files (raw HTML tables). You will need to create a .tmpl file to have weewx create formatted output.

Online example: https://nsf.se/wx/NSF_WX/nsf_metar_taf.html

##### Requirements:<P>
- Python pandas

##### Configuration/Use:<P>
- Copy ```FetchMetarTaf.py``` to directory with user extensions. (```/usr/share/weewx/user``` in Debian)

- Insert following to your ```StdReport``` section in your ```weewx.conf``` file:
```
[[FetchMetarTaf]]
  skin = FetchMetarTaf
  enable = true 
```

- Create and customize a ```skin.conf``` file for FetchMetarTaf:
```
[FetchMetarTaf]
	metar_url  = https://aviationweather.gov/data/cache/metars.cache.csv.gz
	taf_url = https://aviationweather.gov/data/cache/tafs.cache.csv.gz
 	stations = Comma separated list of Airport codes     # stations for which to retrieve METAR and TAF
	metar_dataframe_path = file path  # location to save the dataframe file (.html)
	taf_dataframe_path = file path

#
# The list of generators that are to be run:
#
[Generators]
        generator_list = user.FetchMetarTaf.MetarTafLoader
```
 

#### References:
WeeWX - Open source software for your weather station<BR>
http://weewx.com/<P>
Raspberry Pi<BR>
http://www.raspberrypi.org/products
