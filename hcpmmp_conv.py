# coding:utf8
# Authere: Chenfei 
# update Date:2021/11/11
# version: hcpmmp_conv:v1.0


import os
import sys
import nibabel as nib
import json
import numpy as np
import argparse
import inspect
import time
import subprocess
import shutil
import glob


def runSubject(freesurfer_dir, subject_label):
    label = 'sub-' + subject_label
    freesurfer_path = os.path.join(freesurfer_dir, label)
    if not os.path.exists(freesurfer_path):
        raise("Failed to detect /derivatives/freesurfer for subject " + label)
    
    os.environ["SUBJECTS_DIR"] = freesurfer_dir
    parc_image_path = os.path.join(freesurfer_path, 'mri') 

    parc_desikan_path = os.path.join(parc_image_path, 'aparc+aseg.mgz')
    parc_destrieux_path = os.path.join(parc_image_path, 'aparc.a2009s+aseg.mgz')
    parc_hcpmmp360_path = os.path.join(parc_image_path, 'aparc.HCPMMP1+aseg.mgz')

    # surface mapping to hcp
    for hemi in [ 'l', 'r' ]:
        subprocess.run(['mri_surf2surf --srcsubject fsaverage --trgsubject ' + label +
            ' --hemi ' + hemi + 'h --sval-annot ' + 
            '/' + hemi + 'h.HCPMMP1.annot' + ' --tval ' + os.path.join(
            freesurfer_path, 'label', hemi + 'h.HCPMMP1.annot')], check=True, shell=True)

    subprocess.run(['mri_aparc2aseg --s ' + label + ' --old-ribbon --annot HCPMMP1 --o ' + parc_hcpmmp360_path], check=True, shell=True)

    # convert from FreeSurfer Space Back to Native Anatomical Space (https://surfer.nmr.mgh.harvard.edu/fswiki/FsAnat-to-NativeAnat)
    parc_desikan_native_path = os.path.join(parc_image_path, 'native_desikan.mgz')
    parc_destrieux_native_path = os.path.join(parc_image_path, 'native_destrieux.mgz')
    parc_hcpmmp360_native_path = os.path.join(parc_image_path, 'native_hcpmmp360.mgz')

    subprocess.run(['mri_label2vol  --seg ' + parc_desikan_path + ' --temp ' + 
        os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_desikan_native_path + ' --regheader ' + parc_desikan_path], check=True, shell=True)
    subprocess.run(['mri_label2vol  --seg ' + parc_destrieux_path + ' --temp ' + 
        os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_destrieux_native_path + ' --regheader ' + parc_destrieux_path], check=True, shell=True)
    subprocess.run(['mri_label2vol  --seg ' + parc_hcpmmp360_path + ' --temp ' + 
        os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_hcpmmp360_native_path + ' --regheader ' + parc_hcpmmp360_path], check=True, shell=True)

    print('Finished participant-level analysis for subject \'' + label + '\'')
    

# main function
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert individual T1 freesurfer output to HCPMMP label file (mgz format)')
    parser.add_argument('bids_dir', help='The directory with the input dataset '
                        'formatted according to the BIDS standard.')
    parser.add_argument('analysis_level', help='Level of the analysis that will be performed. '
                        'Multiple participant level analyses can be run independently '
                        '(in parallel) using the same output_dir.',
                        choices=['participant', 'group'])
    parser.add_argument('--participant_label', help='The label(s) of the participant(s) that should be analyzed. The label '
                        'corresponds to sub-<participant_label> from the BIDS spec '
                        '(so it does not include "sub-"). If this parameter is not '
                        'provided all subjects should be analyzed. Multiple '
                        'participants can be specified with a space separated list.',
                        nargs="+")
    

    args = parser.parse_args()

    start = time.time()
    # copy freesurfer license
    shutil.copyfile('/license.txt', '/opt/freesurfer/license.txt')

    subjects_to_analyze = []
    freesurfer_dir = os.path.join(args.bids_dir, 'derivatives', 'freesurfer')
    if not os.path.exists(freesurfer_dir):
        raise('Unable to find /derivatives/freesurfer')
    
    # only for a subset of subjects
    if args.participant_label:
        subjects_to_analyze = args.participant_label
    # for all subjects
    else:
        subject_dirs = glob.glob(os.path.join(args.bids_dir, "sub-*"))
        subjects_to_analyze = [subject_dir.split("-")[-1] for subject_dir in subject_dirs]
    subjects_to_analyze.sort()
            
        
    # running participant level
    if args.analysis_level == "participant":
        # find all T1s and skullstrip them
        for subject_label in subjects_to_analyze:
            print('running participant level analysis for subject ' + subject_label)
            runSubject(freesurfer_dir, subject_label)

    end = time.time()
    running_time = end - start
    print('running time: {:.0f}min {:.0f}sec'.format(running_time//60, running_time % 60))





    
