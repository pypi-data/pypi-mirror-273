# hystfit
`hystfit` is a Python library designed to calculate the soil water retention curve (SWRC) with hysteresis, building upon the model proposed by Zhou (2013). It extends the functionality of [unsatfit](https://sekika.github.io/unsatfit/).

Although Zhou's model is complex, `hystfit` simplifies the plotting of SWRCs that incorporate hysteresis and aids in parameter optimization. Once parameters are determined, it enables the calculation of changes in pressure head based on changes in water content.

## Document
- [Instruction](https://sekika.github.io/hystfit/instruction.html)

## Example output
Here are some figures calculated using `hystfit`. For more detailed information, please refer to the [example documentation](https://sekika.github.io/hystfit/example.html), which provides sample codes for generating these figures.

<img src="https://sekika.github.io/hystfit/zhou/zhou-2013-fig6a.png" />
<img src="https://sekika.github.io/hystfit/unsoda/unsoda1410.png" />
<img src="https://sekika.github.io/hystfit/unsoda/unsoda4940.png" />

## Reference
- Zhou, A. (2013). A contact angle-dependent hysteresis model for soil–water retention behaviour. Computers and Geotechnics, 49, 36-42. https://doi.org/10.1016/j.compgeo.2012.10.004
