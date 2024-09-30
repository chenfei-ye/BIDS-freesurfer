# coding:utf8
# Authere: Chenfei 
# update Date:2024/09/30
# version: surf_conv:v1.2
# update: support session for parallel computation
# update: added Schaeferx7 and Schaeferx17 atlas
# https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/project_to_individual


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
import bids


def runSubject(freesurfer_dir, subject_id):
    label = subject_id
    freesurfer_path = os.path.join(freesurfer_dir, label)
    if not os.path.exists(freesurfer_path):
        print('subject-level freesurfer dir: ' + freesurfer_path)
        raise("Failed to detect /derivatives/freesurfer for subject " + label)
    
    os.environ["SUBJECTS_DIR"] = freesurfer_dir
    parc_image_path = os.path.join(freesurfer_path, 'mri') 

    parc_desikan_path = os.path.join(parc_image_path, 'aparc+aseg.mgz')
    parc_destrieux_path = os.path.join(parc_image_path, 'aparc.a2009s+aseg.mgz')
    parc_hcpmmp360_path = os.path.join(parc_image_path, 'aparc.HCPMMP1+aseg.mgz')
    parc_schaefer100x7_path = os.path.join(parc_image_path, 'aparc.schaefer100x7+aseg.mgz')
    parc_schaefer200x7_path = os.path.join(parc_image_path, 'aparc.schaefer200x7+aseg.mgz')
    parc_schaefer400x7_path = os.path.join(parc_image_path, 'aparc.schaefer400x7+aseg.mgz')
    parc_schaefer1000x7_path = os.path.join(parc_image_path, 'aparc.schaefer1000x7+aseg.mgz')
    parc_schaefer100x17_path = os.path.join(parc_image_path, 'aparc.schaefer100x17+aseg.mgz')
    parc_schaefer200x17_path = os.path.join(parc_image_path, 'aparc.schaefer200x17+aseg.mgz')
    parc_schaefer400x17_path = os.path.join(parc_image_path, 'aparc.schaefer400x17+aseg.mgz')
    parc_schaefer1000x17_path = os.path.join(parc_image_path, 'aparc.schaefer1000x17+aseg.mgz')


    # surface mapping to hcp
    if not os.path.exists(parc_hcpmmp360_path):
        for hemi in [ 'l', 'r' ]:
            subprocess.run(['mri_surf2surf --srcsubject fsaverage --trgsubject ' + label +
                ' --hemi ' + hemi + 'h --sval-annot ' + 
                '/' + hemi + 'h.HCPMMP1.annot' + ' --tval ' + os.path.join(
                freesurfer_path, 'label', hemi + 'h.HCPMMP1.annot')], check=True, shell=True)

        subprocess.run(['mri_aparc2aseg --s ' + label + ' --old-ribbon --annot HCPMMP1 --o ' + parc_hcpmmp360_path], check=True, shell=True)

    # surface mapping to schaefer100x7
    if not os.path.exists(parc_schaefer100x7_path):    
        for hemi in [ 'l', 'r' ]:
            subprocess.run(['mri_surf2surf --srcsubject fsaverage --trgsubject ' + label +
                ' --hemi ' + hemi + 'h --sval-annot ' + 
                '/' + hemi + 'h.Schaefer2018_100Parcels_7Networks_order.annot' + ' --tval ' + os.path.join(
                freesurfer_path, 'label', hemi + 'h.schaefer100x7.annot')], check=True, shell=True)

        subprocess.run(['mri_aparc2aseg --s ' + label + ' --old-ribbon --annot schaefer100x7 --o ' + parc_schaefer100x7_path], check=True, shell=True)

    # surface mapping to schaefer100x17
    if not os.path.exists(parc_schaefer100x17_path):    
        for hemi in [ 'l', 'r' ]:
            subprocess.run(['mri_surf2surf --srcsubject fsaverage --trgsubject ' + label +
                ' --hemi ' + hemi + 'h --sval-annot ' + 
                '/' + hemi + 'h.Schaefer2018_100Parcels_17Networks_order.annot' + ' --tval ' + os.path.join(
                freesurfer_path, 'label', hemi + 'h.schaefer100x17.annot')], check=True, shell=True)

        subprocess.run(['mri_aparc2aseg --s ' + label + ' --old-ribbon --annot schaefer100x17 --o ' + parc_schaefer100x17_path], check=True, shell=True)

    # surface mapping to schaefer200x7
    if not os.path.exists(parc_schaefer200x7_path):    
        for hemi in [ 'l', 'r' ]:
            subprocess.run(['mri_surf2surf --srcsubject fsaverage --trgsubject ' + label +
                ' --hemi ' + hemi + 'h --sval-annot ' + 
                '/' + hemi + 'h.Schaefer2018_200Parcels_7Networks_order.annot' + ' --tval ' + os.path.join(
                freesurfer_path, 'label', hemi + 'h.schaefer200x7.annot')], check=True, shell=True)

        subprocess.run(['mri_aparc2aseg --s ' + label + ' --old-ribbon --annot schaefer200x7 --o ' + parc_schaefer200x7_path], check=True, shell=True)
    
    # surface mapping to schaefer200x17
    if not os.path.exists(parc_schaefer200x17_path):    
        for hemi in [ 'l', 'r' ]:
            subprocess.run(['mri_surf2surf --srcsubject fsaverage --trgsubject ' + label +
                ' --hemi ' + hemi + 'h --sval-annot ' + 
                '/' + hemi + 'h.Schaefer2018_200Parcels_17Networks_order.annot' + ' --tval ' + os.path.join(
                freesurfer_path, 'label', hemi + 'h.schaefer200x17.annot')], check=True, shell=True)

        subprocess.run(['mri_aparc2aseg --s ' + label + ' --old-ribbon --annot schaefer200x17 --o ' + parc_schaefer200x17_path], check=True, shell=True)

    # surface mapping to schaefer400x7
    if not os.path.exists(parc_schaefer400x7_path):    
        for hemi in [ 'l', 'r' ]:
            subprocess.run(['mri_surf2surf --srcsubject fsaverage --trgsubject ' + label +
                ' --hemi ' + hemi + 'h --sval-annot ' + 
                '/' + hemi + 'h.Schaefer2018_400Parcels_7Networks_order.annot' + ' --tval ' + os.path.join(
                freesurfer_path, 'label', hemi + 'h.schaefer400x7.annot')], check=True, shell=True)

        subprocess.run(['mri_aparc2aseg --s ' + label + ' --old-ribbon --annot schaefer400x7 --o ' + parc_schaefer400x7_path], check=True, shell=True)

    # surface mapping to schaefer400x17
    if not os.path.exists(parc_schaefer400x17_path):    
        for hemi in [ 'l', 'r' ]:
            subprocess.run(['mri_surf2surf --srcsubject fsaverage --trgsubject ' + label +
                ' --hemi ' + hemi + 'h --sval-annot ' + 
                '/' + hemi + 'h.Schaefer2018_400Parcels_17Networks_order.annot' + ' --tval ' + os.path.join(
                freesurfer_path, 'label', hemi + 'h.schaefer400x17.annot')], check=True, shell=True)

        subprocess.run(['mri_aparc2aseg --s ' + label + ' --old-ribbon --annot schaefer400x17 --o ' + parc_schaefer400x17_path], check=True, shell=True)
    
    # surface mapping to schaefer1000x7
    if not os.path.exists(parc_schaefer1000x7_path):    
        for hemi in [ 'l', 'r' ]:
            subprocess.run(['mri_surf2surf --srcsubject fsaverage --trgsubject ' + label +
                ' --hemi ' + hemi + 'h --sval-annot ' + 
                '/' + hemi + 'h.Schaefer2018_1000Parcels_7Networks_order.annot' + ' --tval ' + os.path.join(
                freesurfer_path, 'label', hemi + 'h.schaefer1000x7.annot')], check=True, shell=True)

        subprocess.run(['mri_aparc2aseg --s ' + label + ' --old-ribbon --annot schaefer1000x7 --o ' + parc_schaefer1000x7_path], check=True, shell=True)
    

    # surface mapping to schaefer1000x17
    if not os.path.exists(parc_schaefer1000x17_path):    
        for hemi in [ 'l', 'r' ]:
            subprocess.run(['mri_surf2surf --srcsubject fsaverage --trgsubject ' + label +
                ' --hemi ' + hemi + 'h --sval-annot ' + 
                '/' + hemi + 'h.Schaefer2018_1000Parcels_17Networks_order.annot' + ' --tval ' + os.path.join(
                freesurfer_path, 'label', hemi + 'h.schaefer1000x17.annot')], check=True, shell=True)

        subprocess.run(['mri_aparc2aseg --s ' + label + ' --old-ribbon --annot schaefer1000x17 --o ' + parc_schaefer1000x17_path], check=True, shell=True)


    # convert from FreeSurfer Space Back to Native Anatomical Space (https://surfer.nmr.mgh.harvard.edu/fswiki/FsAnat-to-NativeAnat)
    parc_desikan_native_path = os.path.join(parc_image_path, 'native_desikan.mgz')
    parc_destrieux_native_path = os.path.join(parc_image_path, 'native_destrieux.mgz')
    parc_hcpmmp360_native_path = os.path.join(parc_image_path, 'native_hcpmmp360.mgz')
    parc_schaefer100x7_native_path = os.path.join(parc_image_path, 'native_schaefer100x7.mgz')
    parc_schaefer200x7_native_path = os.path.join(parc_image_path, 'native_schaefer200x7.mgz')
    parc_schaefer400x7_native_path = os.path.join(parc_image_path, 'native_schaefer400x7.mgz')
    parc_schaefer1000x7_native_path = os.path.join(parc_image_path, 'native_schaefer1000x7.mgz')
    parc_schaefer100x17_native_path = os.path.join(parc_image_path, 'native_schaefer100x17.mgz')
    parc_schaefer200x17_native_path = os.path.join(parc_image_path, 'native_schaefer200x17.mgz')
    parc_schaefer400x17_native_path = os.path.join(parc_image_path, 'native_schaefer400x17.mgz')
    parc_schaefer1000x17_native_path = os.path.join(parc_image_path, 'native_schaefer1000x17.mgz')

    if not os.path.exists(parc_desikan_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_desikan_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_desikan_native_path + ' --regheader ' + parc_desikan_path], check=True, shell=True)
    if not os.path.exists(parc_destrieux_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_destrieux_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_destrieux_native_path + ' --regheader ' + parc_destrieux_path], check=True, shell=True)
    if not os.path.exists(parc_hcpmmp360_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_hcpmmp360_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_hcpmmp360_native_path + ' --regheader ' + parc_hcpmmp360_path], check=True, shell=True)
        
    if not os.path.exists(parc_schaefer100x7_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_schaefer100x7_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_schaefer100x7_native_path + ' --regheader ' + parc_schaefer100x7_path], check=True, shell=True)
    if not os.path.exists(parc_schaefer200x7_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_schaefer200x7_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_schaefer200x7_native_path + ' --regheader ' + parc_schaefer200x7_path], check=True, shell=True)
    if not os.path.exists(parc_schaefer400x7_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_schaefer400x7_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_schaefer400x7_native_path + ' --regheader ' + parc_schaefer400x7_path], check=True, shell=True)
    if not os.path.exists(parc_schaefer1000x7_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_schaefer1000x7_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_schaefer1000x7_native_path + ' --regheader ' + parc_schaefer1000x7_path], check=True, shell=True)
    
    if not os.path.exists(parc_schaefer100x17_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_schaefer100x17_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_schaefer100x17_native_path + ' --regheader ' + parc_schaefer100x17_path], check=True, shell=True)
    if not os.path.exists(parc_schaefer200x17_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_schaefer200x17_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_schaefer200x17_native_path + ' --regheader ' + parc_schaefer200x17_path], check=True, shell=True)
    if not os.path.exists(parc_schaefer400x17_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_schaefer400x17_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_schaefer400x17_native_path + ' --regheader ' + parc_schaefer400x17_path], check=True, shell=True)
    if not os.path.exists(parc_schaefer1000x17_native_path):
        subprocess.run(['mri_label2vol  --seg ' + parc_schaefer1000x17_path + ' --temp ' + 
            os.path.join(parc_image_path, 'rawavg.mgz') + ' --o ' + parc_schaefer1000x17_native_path + ' --regheader ' + parc_schaefer1000x17_path], check=True, shell=True)

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
    parser.add_argument('--session_label', help='The label of the session that should be analyzed. The label '
                    'corresponds to ses-<session_label> from the BIDS spec '
                    '(so it does not include "ses-"). If this parameter is not '
                    'provided, all sessions should be analyzed. Multiple '
                    'sessions can be specified with a space separated list.',
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

    # only use a subset of sessions
    if args.session_label:
        session_to_analyze = dict(session=args.session_label)
    else:
        session_to_analyze = dict()
            
    layout = bids.layout.BIDSLayout(args.bids_dir, derivatives=False, absolute_paths=True)    
    # running participant level
    if args.analysis_level == "participant":
        # find all T1s and skullstrip them
        for subject_label in subjects_to_analyze:
            print('running participant level analysis for subject ' + subject_label)
            smri = [f.path for f in layout.get(subject=subject_label,suffix='T1w',extension=["nii.gz", "nii"],**session_to_analyze)]      

        if os.path.normpath(smri[0]).split(os.sep)[-3].split("-")[0] == 'ses':
            sessions = [os.path.normpath(t1).split(os.sep)[-3].split("-")[-1] for t1 in smri]
            sessions.sort()
        else:
            sessions = []

        if sessions:
            for s in range(len(sessions)):  
                session_label = sessions[s]
                subject_id = 'sub-' + subject_label + '_ses-' + session_label
                runSubject(freesurfer_dir, subject_id)
        else:
            session_label = []
            subject_id = 'sub-' + subject_label 
            runSubject(freesurfer_dir, subject_id)


    end = time.time()
    running_time = end - start
    print('running time: {:.0f}min {:.0f}sec'.format(running_time//60, running_time % 60))





    
