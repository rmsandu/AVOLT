# AVOLT
Ablation VOLume Tumor - Compute radiomics and modelling for liver tumor cancer

## Radiomics extraction using [PyRadiomics](https://pyradiomics.readthedocs.io/en/latest/)

PyRadiomics was used to extract tumor and ablation features describing shape, size and volume in `extract_radiomics.py`.
Additionally, an inner an outer ellipsoid are computed using convex optimization methods.

You can find more about ablation treatments for liver cancer in the following open access book chapter ["Stereotactic Image-Guidance for Ablation of Malignant Liver Tumors"](https://www.intechopen.com/online-first/stereotactic-image-guidance-for-ablation-of-malignant-liver-tumors) from Liver Pathology.


![image](https://api.intechopen.com/media/chapter/69658/media/F1.png)


## Usage

To compute radiomics a segmentation mask of the tumor, ablation and the original images from which they were extracted need to be provided. Although PyRadiomics provides a "mask correction" option, for smooth running all images provided as input should to be in the same spacing, and co-registered.

### Usage on the command line

    python -m AVOLT -t tumor_filepath -a ablation_filepath -tct tumorCTsource_filepath -act ablationCTsource_filepath -om output_filepath_xlsx


### Usage with automation like Snakemake

It is possible to use the code in an automated way for batch processing when multiple instances are available. An example using Snakemake is provided in the `Snakefile`.

### Data visualization of extracted radiomics

