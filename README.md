# hot_house

Wireless temperature collection, thermostat control, and data collection  
I didn't want to buy a dozen Nest thermostats, so here we gooooo  

## Requirements

### Hardware

- raspberry pi
- rtl tuner (R820T, ex: [NooElec NESDR Mini USB RTL-SDR & ADS-B Receiver Set, RTL2832U & R820T Tuner, MCX Input from Amazon](https://www.amazon.com/gp/product/B009U7WZCA/ref=oh_aui_detailpage_o04_s00?ie=UTF8&psc=1))

### Software

- python 2.7
- pip
- virtualenv
- postgres 9+
- node (recommend install via nvm)
- rtl-sdr (http://osmocom.org/projects/sdr/wiki/rtl-sdr)
- rtl_433 (https://github.com/merbanan/rtl_433)

## Installing
TODO, sorry  

1. Init the database: `postgres/reset.sh`
1. Setup collector: `cd collector; virtualenv venv; source venv/bin/activate; pip install -r requirements.txt; deactivate;`
1. Setup API: `cd api; virtualenv venv; source venv/bin/activate; pip install -r requirements.txt; deactivate;`

## Running HotHouse

HotHouse comprises several components. Don't have a deployment strategy yet. 

1. Run the collector: `collector/run.sh`
1. Run the API: `api/run.sh`

## Misc Notes

rtl_433 output for Ambient Weather sensor:  
```
{"time": "2017-12-27 00:00:42", "model": "Ambient Weather F007TH Thermo-Hygrometer", "device": 64, "battery": "Ok", "channel": 1, "humidity": 59, "temperature_F": 6.5}
```
