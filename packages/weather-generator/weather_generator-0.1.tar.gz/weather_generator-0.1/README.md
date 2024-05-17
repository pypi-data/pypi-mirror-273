# WEATHER GENERATOR 
```
from weather_generator import Rain_WeatherGenerator

rain_WG = Rain_WeatherGenerator()
rain_WG.import_data(data_list= rain_data, start_date= "1991-01-01", end_date= "2020-12-31")
daily_rain_generated = rain_WG.run_weath_gen(2024, month=02, nb_real=100, rain_occ_model= "mixed_order", rain_quant_model= "gamma"):

```

Stochastic generation of daily weather data. 

# About
Generate stochastic daily weather data using this Python package. 
Simulate realistic weather conditions for various locations, based on the climatology. 
Useful for data analysis, modeling, and simulation in fields such as meteorology, climate science, agriculture, and urban planning.
lease note that currently, the method specifically focuses on rainfall data generation. 
Weather generators for other parameters are in development for future updates.

The data needed for the calculation include historical daily weather data, covering at least 30 years
The input data must have the same timestep and length.

For daily rainfall generation, users can choose from different methods (types of models):
* Rain Occurrence Model: Choose between first order Markov chain, second order Markov chain, or mixed order Markov chain.
* Daily Rain Quantity Model: Choose from Weibull, exponential, gamma, or hyperexponential (sum of two exponential distributions).

It's important to note that the input data must have the same timestep and length

# Install
```
pip install weather_generator 
```