This is a simulator that implements CO₂ emissions calculation for certain [mosaik] scenario and [pandapower] network configuration.

This simulator is still work in progress. In particular, not every desirable attribute is implemented yet. If you have need for a particular attribute, leave an [issue here].

[pandapower]: https://www.pandapower.org
[mosaik]: https://mosaik.offis.de
[issue here]: https://gitlab.com/mosaik/components/energy/mosaik-emissions/-/issues

## Methodology

CO₂ emissions are dynamically aggregated based on predefined pandapower network characteristics.

To obtain the emission factor for a particular fuel, we refer to [2006 IPCC](https://www.ipcc-nggip.iges.or.jp/public/2006gl/) and in particular to the chapter [Stationary Combustion](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf).

To obtain the carbon intensity depending on a country's energy mix, we refer to [OurWorldInData](https://ourworldindata.org/grapher/carbon-intensity-electricity?tab=table), which aggregates data from Ember's European Electricity Review and the Energy Institute's Statistical Review of World Energy.

For Germany, the state can be specified, in which case historical carbon intensity estimates from [co2map.de](https://co2map.de/) will be used.

### Units

* Power produced - [MW]
* Default emission factor - [tones CO₂eq. / MWh]
* Carbon intensity of the electricity - [tones CO₂eq. / MWh]
* Carbon emissions - [tones CO₂eq.]

## Installation and usage

```
pip install mosaik-emissions
```

If you don't want to install this through PyPI, you can use pip to install the requirements.txt file:
```
pip install -r requirements.txt # To use this, you have to install at least version 3.2.0 of mosaik.
```

The simulator uses `P[MW]` as an input and `E[tCO2eq]` as an output attribute.
For each connected *generator* or *external grid*, one of the parameters must be defined: the emission factor, the fuel used, the country, and the state, see *the configuration* section bellow. You can also use the *method* option, which is callable, directly transforms input data to output, and takes precedence over other options. Thus, each emissions model can be configured while creation by using `model_params`:
   
* method - callable that directly transforms input data to output 
* co2_emission_factor - float number that directly represents conversion factor [tones CO₂eq. / MWh]
* fuel - string that matches with a certain type of fuel used to produce electricity
* state - string that matches with a certain state of the country to filter the carbon intensity database out, it shuld be defined along with the country
* country - string that matches with a country to filter the carbon intensity database out
* coefficient - float number that multiplies emissions output, default is 1.0

```
    emission_config = {
        'co2_emission_factor' : 0.385, 
        'fuel' : 'Natural Gas Liquids',
        'country' : 'Germany',
        'state' : 'SN', # it shuld be defined along with the country if so
        'coefficient' : 2.0 # multiplies total emissions output
    }

    em = em_sim.Emission.create(1, **emission_config)
```

**Note**: the model applies the first option defined according to the order described, e.g. if `co2_emission_factor` is defined, it does not check `fuel` or `country`.

Specify simulators configurations within your scenario script:
```
sim_config = {
    'Grid': {
         'python': 'mosaik_components.pandapower:Simulator'
    },
    'Emissions': {
         'python': 'mosaik_components.emissions:Simulator'
    },
    ...
}
```

Initialize the pandapower grid and emissions simulator:
```
    gridsim = world.start('Grid', step_size=STEP_SIZE)
    em_sim = world.start('Emissions')
```

Instantiate model entities:
```
    grid = gridsim.Grid(json=GRID_FILE)
    em = em_sim.Emission.create(1, **emission_config)
```

Connect and run:
```
    gens = [e for e in grid.children if e.type in ['Gen', 'ControlledGen']]
    world.connect(gens[0], em[0], 'P[MW]')
    world.run(until=END)
```

You can see the demo scenario in the `demo` folder.

## Possible configuration

To relate to an emission factor derived from the country's energy mix, the full name of the country should be provided (see [OurWorldInData](https://ourworldindata.org/grapher/carbon-intensity-electricity?tab=table)), e.g.:
- Germany
- Greece
- Iceland
- ...

For Germany certain states are available (see [co2map.de](https://co2map.de/)): DE (country average), BB, BW, BY, HE, MV, NI, NW, RP, SH, SL, SN, ST, TH

To relate to certain fuel type, the fuel name should be provided (see [Stationary Combustion](https://gitlab.com/mosaik/components/energy/mosaik-emissions/-/blob/main/misc/fuel_combustion.pdf?ref_type=heads), Table 2.2):
- Crude Oil
- Natural Gas Liquids
- Natural Gas
- Charcoal
- Gas/Diesel Oil
- Ethane
- ...

## Developer notes

Note that emission factor and carbon intensity of electricity values for specific fuels and countries are stored in `data/data.csv` with the units specified in the source and are converted internally once been called.

Raw data files and `data.csv` preparation notebook can be found in the `misc` folder.

## Sources and References

* Ember - Yearly Electricity Data (2023); Ember - European Electricity Review (2022); Energy Institute - Statistical Review of World Energy (2023) – with major processing by Our World in Data. “Carbon intensity of electricity generation” [dataset]. Ember, “Yearly Electricity Data”; Ember, “European Electricity Review”; Energy Institute, “Statistical Review of World Energy” [original data]. Retrieved February 27, 2024 from https://ourworldindata.org/grapher/carbon-intensity-electricity

* Hourly consumption-based CO2 emissions intensity in Germany / [co2map.de](https://co2map.de/), INATECH, University of Freiburg. Retrieved February 27, 2024 from https://api.co2map.de/docs