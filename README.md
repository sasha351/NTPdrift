
# NTP Drift

UMass Amherst - ECE 371 Honors project:

Assignment given by Professor Taqi Raza and supervized by teaching assistant Shayan Nazeer

Goal: Synchronize time of Sixfab Pico LTE with an NTP server. NTP is network time protocol and all
devices connected to internet sync their local clock with NTP server using NTP protocol 

## Report, Findings, and Progression

The board we chose to use was the Sixfab Pico LTE and all analysis was performed in micropython. 

The intial setup was done following the documentation and startup guides on the SixFab Pico website. At start with the setup, we first wrote boardBlink.py to ensure that we were able to upload files properly. We reccomend using Thonny, an open-source python IDE, to interface with the Pico.

To accomplish our first task of connecting the board to the internet, our group sent several sample HTTP requests utilizing the tool Webhook.site. 
The tool allowed us to send GET, POST, and PUT requests to and from the board and allow us to view the responses in real time. 
Once we verified that the signals were being property sent and received, we moved on to establishing the connection with the NTP server.
The NTP server we chose was from NTP Pool Project, as it seems to be the most popular tool for NTP-related projects and experiments. 

We also noticed that upon powering up and connecting to LTE, the Pico automatically synchronized its time with the network.

## Associated Links

[Sixfab Pico](https://sixfab.com/product/sixfab-pico-lte/?aelia_cs_currency=USD&gad_source=1)

[Webhooks](https://webhook.site/#!/view/668411be-19ef-49e1-85cf-9ccfb0d3f7c3)

[Pool NPT](https://www.ntppool.org/en/)
## Authors

- [Owen Raftery](https://github.com/realraft)
- [Sasha Shikhanovich](https://github.com/sasha351)
- [Thomas Murphy](https://github.com/thocmurphy)
- Kyle Belanger

