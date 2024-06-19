# coding:utf8
# Authere: Chenfei 
# update Date:2024/06/19
# version: output_qc:v1.0
# funcion: check integrity of freesurfer output


import os
import sys
import nibabel as nib
import json
import numpy as np
import argparse
import time
import subprocess
import shutil
import glob


def runSubject(freesurfer_dir, subject_label):
    qc_fail=False
    label = 'sub-' + subject_label
    freesurfer_path = os.path.join(freesurfer_dir, label)
    if not os.path.exists(freesurfer_path):
        qc_fail=True
    else:
        parc_image_path = os.path.join(freesurfer_path, 'mri') 
        parc_DKT_path = os.path.join(parc_image_path, 'aparc.DKTatlas+aseg.mgz')
        if not os.path.exists(parc_DKT_path):
            qc_fail=True
    return qc_fail


# main function
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check integrity of freesurfer output')
    parser.add_argument('bids_dir', help='The directory with the input dataset '
                        'formatted according to the BIDS standard.')
    

    args = parser.parse_args()

    start = time.time()


    subjects_to_analyze = []
    freesurfer_dir = os.path.join(args.bids_dir, 'derivatives', 'freesurfer')
    if not os.path.exists(freesurfer_dir):
        raise('Unable to find /derivatives/freesurfer')
    
    subject_dirs = glob.glob(os.path.join(args.bids_dir, "sub-*"))
    subjects_to_analyze = [subject_dir.split("-")[-1] for subject_dir in subject_dirs]
    subjects_to_analyze.sort()

    failed_ls = []
    # find all T1s and skullstrip them
    for subject_label in subjects_to_analyze:
        qc_fail = runSubject(freesurfer_dir, subject_label)
        if qc_fail:
            failed_ls.append(subject_label)
    
    if failed_ls:
        print('Failed freesurfer output detected for the following cases:')
        print(','.join(failed_ls))
    else:
        print('Great! No failed freesurfer output detected')

    end = time.time()
    running_time = end - start
    print('running time: {:.0f}min {:.0f}sec'.format(running_time//60, running_time % 60))





    
