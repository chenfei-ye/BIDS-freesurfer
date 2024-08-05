# coding:utf8
# Authere: Chenfei 
# update Date:2024/08/04
# update: fmriprep and xcp-d qc added 
# version: output_qc:v1.1
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


def runSubject(output_dir, subject_label, mode):
    qc_fail=False
    label = 'sub-' + subject_label
    output_path = os.path.join(output_dir, label)
    if not os.path.exists(output_path):
        qc_fail=True
    else:
        if mode == 'freesurfer':
            parc_image_path = os.path.join(output_path, 'mri') 
            key_file_path = os.path.join(parc_image_path, 'aparc.DKTatlas+aseg.mgz')
            if not os.path.exists(key_file_path):
                qc_fail=True
        elif mode == 'fmriprep':
            den91k_path = glob.glob(os.path.join(output_path, 'func', '*_space-fsLR_den-91k_bold.dtseries.nii'))
            if len(den91k_path) == 0:
                qc_fail=True
        elif mode == 'xcp-d':
            den91k_path = glob.glob(os.path.join(output_path, 'func', '*_space-fsLR_seg-4S456Parcels_den-91k_stat-coverage_boldmap.pscalar.nii'))
            if len(den91k_path) == 0:
                qc_fail=True
    return qc_fail


# main function
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='check integrity of freesurfer/fmriprep/xcp-d output')
    parser.add_argument('bids_dir', help='The directory with the input dataset '
                        'formatted according to the BIDS standard.')
    parser.add_argument('-mode', help='run freesurfer/fmriprep/xcp-d mode', default="freesurfer",
                        choices=['freesurfer', 'fmriprep', 'xcp-d'])

    args = parser.parse_args()

    start = time.time()

    mode = args.mode
    subjects_to_analyze = []

    if mode == 'freesurfer':
        output_dir = os.path.join(args.bids_dir, 'derivatives', 'freesurfer')
        if not os.path.exists(output_dir):
            raise('Unable to find /derivatives/freesurfer')
    elif mode == 'fmriprep':
        output_dir = os.path.join(args.bids_dir, 'derivatives', 'fmriprep')
        if not os.path.exists(output_dir):
            raise('Unable to find /derivatives/fmriprep')
    elif mode == 'xcp-d':
        output_dir = os.path.join(args.bids_dir, 'derivatives', 'xcp_d')
        if not os.path.exists(output_dir):
            raise('Unable to find /derivatives/xcp_d')
    
    subject_dirs = glob.glob(os.path.join(args.bids_dir, "sub-*"))
    subjects_to_analyze = [subject_dir.split("-")[-1] for subject_dir in subject_dirs]
    subjects_to_analyze.sort()

    failed_ls = []
    success_ls = []

    # find all image 
    for subject_label in subjects_to_analyze:
        qc_fail = runSubject(output_dir, subject_label, mode)
        if qc_fail:
            failed_ls.append(subject_label)
        else:
            success_ls.append(subject_label)
    
    if failed_ls:
        print('Failed ' + mode + ' output detected for the following cases:')
        print(' '.join(failed_ls))
    else:
        print('Great! No failed ' + mode + ' output detected')
    print('Successful ' + mode + ' output for the following cases:')
    print(' '.join(success_ls))

    end = time.time()
    running_time = end - start
    print('running time: {:.0f}min {:.0f}sec'.format(running_time//60, running_time % 60))





    
