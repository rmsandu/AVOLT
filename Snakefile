import os
from snakemake.utils import validate, min_version
# To run snakemake:
# 1. install module setup.py of the Python package into the virtual repository
# 2. run : snakemake --profile profiles/local --directory ../../tests/test_data _output/Aggregated.xlsx
##### set minimum snakemake version #####
min_version("5.17.0")

def get_patient_ids():
    patient_ids = list(filter(lambda x: os.path.isdir(x) and not x.startswith('_')
                               and not x.startswith('.'), os.listdir('.')))
    return patient_ids

def get_lesion_ids(patient_folder):
    lesion_ids = list(filter(lambda x: os.path.isdir(os.path.join(patient_folder,x))and not x.startswith('_')
                               and not x.startswith('.') , os.listdir(patient_folder)))
    return lesion_ids

rule calc_margin:
    input:
        tumor = "{patient_id}/{lesion_id}/{patient_id}_L{lesion_id}_Tumor.nii.gz",
        ablation = "{patient_id}/{lesion_id}/{patient_id}_L{lesion_id}_Ablation.nii.gz",
        ablation_source = "{patient_id}/{lesion_id}/{patient_id}_L{lesion_id}_Ablation_Source.nii.gz",
        tumor_source = "{patient_id}/{lesion_id}/{patient_id}_L{lesion_id}_Tumor_Source.nii.gz",

    params:
        patient_id = "{patient_id}",
        lesion_id = "{lesion_id}",

    log:
        "_logs/{patient_id}_L{lesion_id}_calc_margin.log"
    output:
        radiomics = "_intermediate/radiomics/{patient_id}_L{lesion_id}_Radiomics.xlsx",
    shell:
          "python -m AVOLT \
            --tumor {input.tumor} \
            --ablation {input.ablation} \
            --ablation-source {input.ablation_source}\
            --tumor-source {input.tumor_source}\
            --patient-id {params.patient_id} \
            --lesion-id {params.lesion_id} \
            --output-radiomics {output.radiomics}"


def input_aggregate_margins_patient(wildcards):
    lesion_ids = get_lesion_ids(wildcards.patient_id)
    return expand("_intermediate/radiomics/{patient_id}_L{lesion_id}_Radiomics.xlsx",
               lesion_id = lesion_ids,
               patient_id = wildcards.patient_id)

rule aggregate_margins_patient:
    input:
        input_aggregate_margins_patient
    output:
        "_aggregated/{patient_id}_Radiomics.xlsx"
    script:
        "aggregate_data.py"

def input_aggregate_margins_all(wildcards):
    patient_ids = get_patient_ids()
    return expand("_aggregated/{patient_id}_Radiomics.xlsx",
               patient_id = patient_ids)

rule aggregate_margins_all:
    input:
        input_aggregate_margins_all
    output:
        "_output/Aggregated.xlsx"
    script:
        "aggregate_data.py"
