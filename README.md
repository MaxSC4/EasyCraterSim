# EasyCraterSim 1.2.2
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14911870.svg)](https://doi.org/10.5281/zenodo.14911870)

**EasyCraterSim** is a lightweight numerical simulation tool designed to model the formation and evolution of impact craters based on the equations and methodologies described in the paper:
***O'Keefe, J. D., & Ahrens, T. J. (1999). Complex craters: Relationship of stratigraphy and rings to impact conditions. Journal of Geophysical Research: Planets, 104(E11), 27091-27104.***
This project aims to provide a simple and accessible visualization of crater growth dynamics based on fundamental physical parameters.

[https://easycratersim.streamlit.app/]

# 🛰️ Scientific objectives
- Understand the processes involved in impact crater formation.
- Model the transition between simple and complex craters *(WIP)*
- Study the influence of physical parameters such as gravity, impactor velocity, surface strength, and planetary density.
- Visualize the evolution of a crater profile over time, normalized by impactor diameter.

# 📊 Features
- Choose pre-set crater types (Chicxulub, Meteor Crater, Tycho, Copernicus, and more).
- Customize key physical parameters (gravity, impactor size, velocity, angle, temperature, etc.).
- Visualize the crater shape at a specific time or animate its evolution.
- Graphical output showing normalized radius and depth of the crater.
- Download a GIF showcasing the evolution of the crater
- Choose between **Single Crater Simulation** or **Comparison Mode** *(WIP)*
- **ReverseSimulation :** Choose a crater and EasyCraterSim will estimate the impactor's parameters!
- **Guess the crater :** A quick game where you have to guess the crater based on hints!

# 🧠 Work in progress
- **Comparison Mode :** A new mode able to compare two craters, either side by side or by overlaying

## 🖼️ Interface Preview
![EasyCraterSim Interface](images/easycratersim.png)

# 🖥️ How to use

## Enjoy the latest up-to-date version
The interface, using the latest version, is available here : [https://easycratersim.streamlit.app/]

## Self hosting
If you want to host the interface by yourself

### Prerequisites
Ensure you have the following installed: 
- Python 3.x
- Streamlit
- Matplotlib
- Scipy
- Numpy

### Installation
```py
pip install streamlit matplotlib scipy numpy
```

### Running
```
streamlit run app.py
```

## Accessing the interface
The direct link to your *Streamlit* interface should be directly displayed into the terminal where you entered the streamlit prompt.


# ⚙️ Context
This program was developed as part of the course unit 'Mathematical Modeling,' supervised by E. Léger and H. Massol, during my Bachelor's degree in 'Earth and Universe Sciences' at the University of Paris-Saclay.
This project is based on the equations and impact crater formation models described in:
***O'Keefe, J. D., & Ahrens, T. J. (1999). Complex craters: Relationship of stratigraphy and rings to impact conditions. Journal of Geophysical Research: Planets, 104(E11), 27091-27104.***

## 📚 References
This project is based on scientific research on impact craters. Below are some key references:

- Reimold, W. U., & Gibson, R. L. (2006). *The Vredefort impact structure, South Africa*. Geological Society of America Special Papers, 405, 1-28. [DOI](https://doi.org/10.1130/2006.2405(01))
- Grieve, R. A. F., & Therriault, A. M. (2000). *The Sudbury impact structure: A century of discovery and research*. The Journal of Earth Sciences, 42(4), 339-362. [DOI](https://doi.org/10.1139/e99-080)
- Masaitis, V. L. (1998). *Popigai crater: Origin and distribution of diamond-bearing impactites*. Meteoritics & Planetary Science, 33(2), 349-359. [DOI](https://doi.org/10.1111/j.1945-5100.1998.tb01638.x)
- Schulte, P., & et al. (2010). *The Chicxulub asteroid impact and mass extinction at the Cretaceous-Paleogene boundary*. Science, 327(5970), 1214-1218. [DOI](https://doi.org/10.1126/science.1177265)
- Kring, D. A. (1997). *Airblast produced by the Meteor Crater impact event and a reconstruction of the affected environment*. Meteoritics & Planetary Science, 32(4), 517-530. [DOI](https://doi.org/10.1111/j.1945-5100.1997.tb01298.x)
- Grotzinger, J. P., & et al. (2015). *Deposition, exhumation, and paleoclimate of an ancient lake deposit, Gale crater, Mars*. Science, 350(6257), aac7575. [DOI](https://doi.org/10.1126/science.aac7575)
- Smith, D. E., & et al. (1999). *The global topography of Mars and implications for surface evolution*. Science, 284(5419), 1495-1503. [DOI](https://doi.org/10.1126/science.284.5419.1495)
- Petro, N. E., & Pieters, C. M. (2004). *Surviving the heavy bombardment: Ancient material at the surface of South Pole-Aitken Basin*. Journal of Geophysical Research: Planets, 109(E6). [DOI](https://doi.org/10.1029/2003JE002182)
- Head, J. W. (1974). *The geology of the Copernicus Quadrangle of the Moon*. US Geological Survey Professional Paper, 1049, 1-75. [Link](https://pubs.er.usgs.gov/publication/pp1049)
- Shoemaker, E. M. (1971). *Impact mechanics at Tycho crater, in The Moon*. Symposium 47 of the International Astronomical Union, 289-300. [DOI](https://doi.org/10.1007/978-3-642-65379-4_15)

# 📄 Citation
If you use this project, please cite as follows:
```latex
SOARES CORREIA, M. (2025). EasyCraterSim : Lightweight numerical simulation tool to model the formation and evolution of impact craters (v1.2.1). Université Paris-Saclay. https://doi.org/10.5281/zenodo.14911870
```

# 📧 Contact 
For questions or contributions: [maxime.soares-correia@universite-paris-saclay.fr]

# 📝 License
This project is licensed under the GNU GPL v3 License.
