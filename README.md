

# BIDS-FreeSurfer

[freesurfer 6.0](https://surfer.nmr.mgh.harvard.edu/) brain parcellation on BIDS-format MRI-T1w images, including:
- parallel brain parcellation for multiple subjects
- mapping to [HCPMMP atlas](https://cjneurolab.org/2016/11/22/hcp-mmp1-0-volumetric-nifti-masks-in-native-structural-space/)
- morphological metrics extraction (e.g., cortical thickness, subcortical volume, euler number)

This pipeline was modified from [https://github.com/BIDS-Apps/freesurfer](https://github.com/BIDS-Apps/freesurfer).

Check details in bids-fmripost [brain atlases](resources/atlases.md)

Check bids-freesurfer version history in [Change Log](resources/CHANGELOG.md)

## Contents
* [Install](#Install)
* [Running](#running)
* [Input Argument](#input-argument)
* [Output Explanation](#output-explanation)

## Install
### install by pulling (recommend)
```
docker pull mindsgo-sz-docker.pkg.coding.net/neuroimage_analysis/base/bids-freesurfer:latest
docker tag  mindsgo-sz-docker.pkg.coding.net/neuroimage_analysis/base/bids-freesurfer:latest  bids-freesurfer:latest
```

### or install by docker build
```
cd BIDS-freesurfer
docker build -t  bids-freesurfer:latest .
```
## Running 
### sequential running
```
docker run -it --rm -v /input_bids_directory:/bids_dataset -v /input_bids_directory/derivatives/freesurfer:/outputs -v <localpath>/freesurfer_license.txt:/license.txt  bids-freesurfer:latest /bids_dataset /outputs participant --license_file "/license.txt" --skip_bids_validator
```

### parallel running (recommend)
```
docker run -it --rm --entrypoint python -v /input_bids_directory:/bids_dataset -v /input_bids_directory/derivatives/freesurfer:/outputs -v <localpath>/freesurfer_license.txt:/license.txt  bids-freesurfer:latest /run_fs_batch.py /bids_dataset /outputs participant --skip_bids_validator
```

### mapping to hcpmmp atlas
```
docker run -it --rm --entrypoint python -v /input_bids_directory:/bids_dataset -v /<localpath>/freesurfer_license.txt:/license.txt bids-freesurfer:latest /hcpmmp_conv.py /bids_dataset participant 
```

### morphological metrics extraction
```
docker run -it --rm -v /input_bids_directory:/bids_dataset -v /input_bids_directory/derivatives/freesurfer:/outputs -v <localpath>/freesurfer_license.txt:/license.txt  bids-freesurfer:latest /bids_dataset /outputs group2 --license_file "/license.txt"
```

## Input Argument
####   positional argument:
-   `/bids_dataset`: The root folder of a BIDS valid dataset (sub-XX folders should be found at the top level in this folder).
-  `/outputs`: The directory where the output files should be stored. If you are running group level analysis this folder should be prepopulated with the results of the participant level analysis.
- `participant`: run on individual level. 

####   optional argument:
-   `--participant_label [str]`: A space delimited list of participant identifiers or a single identifier (the sub- prefix can be removed)
- `--skip_bids_validator`: skips bids validation.
- `--n_cpus [int]`: Number of CPU cores available to use. ** For parallel mode, default values of n_cpus = min(number of subjects, number of cores)** (type `htop` in terminal to check the actual number of CPU cores in your computer). 
- `-v`: show program's version number and exit

## Output explanation
-  Default output directory: `bids_root/derivatives/freesurfer/sub-XX`
-  HCPMMP output directory: `bids_root/derivatives/freesurfer/sub-XX/mri/aparc.HCPMMP1+aseg.mgz` 
-  morphological metrics output directory: `input_bids_directory/derivatives/freesurfer/00_group2_stats_tables/`, including: 
	-   `lh.aparc.thickness.tsv`  cortical thickness
	-   `aseg.tsv`  subcortical volume
	-   `euler.tsv`  [euler number for segmentation QC](https://www.biorxiv.org/content/10.1101/125161v2)



