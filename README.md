# Fibrosis Estimation
![ptchelec](ptchhdgrid.png) \
Repository containing carptuils scripts and files to study intracardiac signals.

All simulations were run using https://opencarp.org/

# License

All source code is subject to the terms of the GPL-3.0 License.
Copyright 2021 Jorge Sanchez, Karlsruhe Institute of Technology.

# Citation
```
@article{Sanchez2021,
abstract = {In patients with atrial fibrillation, intracardiac electrogram signal amplitude is known to decrease with increased structural tissue remodeling, referred to as fibrosis. In addition to the isolation of the pulmonary veins, fibrotic sites are considered a suitable target for catheter ablation. However, it remains an open challenge to find fibrotic areas and to differentiate their density and transmurality. This study aims to identify the volume fraction and transmurality of fibrosis in the atrial substrate. Simulated cardiac electrograms, combined with a generalized model of clinical noise, reproduce clinically measured signals. Our hybrid dataset approach combines in silico and clinical electrograms to train a decision tree classifier to characterize the fibrotic atrial substrate. This approach captures different in vivo dynamics of the electrical propagation reflected on healthy electrogram morphology and synergistically combines it with synthetic fibrotic electrograms from in silico experiments. The machine learning algorithm was tested on five patients and compared against clinical voltage maps as a proof of concept, distinguishing non-fibrotic from fibrotic tissue and characterizing the patient's fibrotic tissue in terms of density and transmurality. The proposed approach can be used to overcome a single voltage cut-off value to identify fibrotic tissue and guide ablation targeting fibrotic areas.},
author = {S{\'{a}}nchez, Jorge and Luongo, Giorgio and Nothstein, Mark and Unger, Laura A. and Saiz, Javier and Trenor, Beatriz and Luik, Armin and D{\"{o}}ssel, Olaf and Loewe, Axel},
doi = {10.3389/fphys.2021.699291},
issn = {1664-042X},
journal = {Frontiers in Physiology},
month = {jul},
title = {{Using Machine Learning to Characterize Atrial Fibrotic Substrate From Intracardiac Signals With a Hybrid in silico and in vivo Dataset}},
url = {https://www.frontiersin.org/articles/10.3389/fphys.2021.699291/full},
volume = {12},
year = {2021}
}
```
