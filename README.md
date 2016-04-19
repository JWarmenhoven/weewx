# weewx
WeeWX - weather station software - customizations

#### RWYplotgenerator (work in progress)
This is a custom generator that uses matplotlib to plot wind data onto an input image for every report update.<BR>
Example:<P>
Input:<BR>
<IMG src='ESMH.png', height=40%, width=40%><BR>
Output:<BR>
<IMG src='http://nsf.se/wx/ESMH_wind.png', height=50%, width=50%>


#####Configuration/Use:<P>
- Copy ```RWYplotgenerator.py``` to ```/usr/share/weewx/user```

- Insert following to your ```StdReport``` section in your ```weewx.conf``` file:

```
[[RWYplotgenerator]]
  	skin = RWYplotgenerator 
```
- Copy ```skin.conf``` to a your skin directory in 

- Customize the ```skin.conf``` file:

```
[RWYplotGenerator]
    input_image = path to input image

    output_image_dpi = 300
    output_image_arrow_color = red      # http://matplotlib.org/api/colors_api.html
    output_image = path to output image
    output_image_fontsize = 12
    output_arrow_xpos = 350             # (pixel coordinates) You will need to adjust this to place the 
    output_arrow_ypos = 300             # arrow on a specific location on the input image

```

####References:
WeeWX - Open source software for your weather station<BR>
http://weewx.com/
