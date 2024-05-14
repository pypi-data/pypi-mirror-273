# vuv
[![Open in Code Ocean](https://codeocean.com/codeocean-assets/badge/open-in-code-ocean.svg)](https://codeocean.com/capsule/1476065/tree)

Takefuji, Y. (2023). vuv: vaccine effects on mortality between fully vaccinated and unvaccinated [Source Code]. https://doi.org/10.24433/CO.1329228.v1

Takefuji Y. (2023). Effectiveness of vaccination with symptoms by age groups. International immunopharmacology, 116, 109823. Advance online publication. https://doi.org/10.1016/j.intimp.2023.109823

vuv is a PyPI application to evaluate the vaccine effects on mortality by age group 
between fully vaccinated and unvaccinated. 
CDC dataset is automatically downloaded from the following site:

https://data.cdc.gov/api/views/3rge-nu2a/rows.csv

Five age groups include 18-29,30-49,50-64,65-79, and 80+. 
Choose one of five age groups and enter the age group with vuv command.

To install vuv, 

$ pip install vuv

To run vuv, enter one of five age groups.

$ vuv 80+

This command generates 80+.png image file.

<img src=https://github.com/y-takefuji/vuv/raw/main/80%2B.png  width=350 height=280>
