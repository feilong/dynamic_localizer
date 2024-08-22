This repository contains scripts to run dynamic object category localizers using PsychoPy and Python 3.

## Usage
**Run `main.py` with PsychoPy for the experiment. Update `sid.txt` in the parent folder at the start of each scanning session.**
**The task for the participant is a 1-back task.**

The script was tested using Standalone PsychoPy 2021.2.3 for macOS.

## Design
The localizer comprises 5 categories, namely faces, bodies, scenes, objects, and scrambled objects. It uses a fully counterbalanced design and has 5 runs in total.

Each run comprises 10 blocks, 2 per category. In each run, the categories in the last 5 blocks are those of the first 5 blocks in reverse order (but with different video clips). Each block lasts 18 seconds. It comprises 6 clips, 3 seconds each. There is one repeated clip per category per run.

Besides the object category blocks, there are three fixation blocks in the beginning, in the middle, and at the end of each run. Each fixation block also lasts 18 seconds.

In total, each run lasts 234 seconds ((5 * 2 + 3) * 18 seconds).


## Citation
The same set stimuli used in this code repository has been used in [Jiahui et al. (2020)](https://doi.org/10.1016/j.neuroimage.2019.116458):
```bib
@article{jiahui2020,
  title = {Predicting individual face-selective topography using naturalistic stimuli},
  journal = {NeuroImage},
  volume = {216},
  pages = {116458},
  year = {2020},
  issn = {1053-8119},
  doi = {https://doi.org/10.1016/j.neuroimage.2019.116458},
  url = {https://www.sciencedirect.com/science/article/pii/S1053811919310493},
  author = {Guo Jiahui and Ma Feilong and Matteo {Visconti di Oleggio Castello} and J. Swaroop Guntupalli and Vassiki Chauhan and James V. Haxby and M. Ida Gobbini},
  keywords = {Hyperalignment, Functional topography, Faces, Naturalistic stimuli, Localizer},
  abstract = {Subject-specific, functionally defined areas are conventionally estimated with functional localizers and a simple contrast analysis between responses to different stimulus categories. Compared with functional localizers, naturalistic stimuli provide several advantages such as stronger and widespread brain activation, greater engagement, and increased subject compliance. In this study we demonstrate that a subject’s idiosyncratic functional topography can be estimated with high fidelity from that subject’s fMRI data obtained while watching a naturalistic movie using hyperalignment to project other subjects’ localizer data into that subject’s idiosyncratic cortical anatomy. These findings lay the foundation for developing an efficient tool for mapping functional topographies for a wide range of perceptual and cognitive functions in new subjects based only on fMRI data collected while watching an engaging, naturalistic stimulus and other subjects’ localizer data from a normative sample.}
}
```

We thank [Sarah B. Herald](https://scholar.google.com/citations?hl=en&user=I2ms_fUAAAAJ) and [Guo Jiahui](https://scholar.google.com/citations?hl=en&user=JBd1p1QAAAAJ) for providing the stimuli. Based on Sarah and Jiahui's unpublished results, this design provides good contrasts (for both between categories and between category and fixation) in a short scan time. Part of the stimuli was from [Pitcher et al. (2011)](http://web.mit.edu/bcs/nklab/media/pdfs/Pitcher2011_Neuropsychologia.pdf). The parameters were set to be the same as the [Python 2 version](https://github.com/mvdoc/pitcher_localizer).
