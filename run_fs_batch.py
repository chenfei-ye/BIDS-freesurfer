# coding:utf8
# Authere: Chenfei 
# update Date:2022/05/07
# update: support session for parallel computation
# function: run freesurfer in paralell, one subject per cpu
# version: run_fs_batch:v1.1


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
import multiprocessing
import bids

def run(command, env={}, cwd=None):
    merged_env = os.environ
    merged_env.update(env)
    merged_env.pop("DEBUG", None)
    print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    shell=True, env=merged_env, cwd=cwd,
                    universal_newlines=True)
    while True:
        line = process.stdout.readline()
        print(line.rstrip())
        line = str(line)[:-1]
        if line == '' and process.poll() != None:
            break
    if process.returncode != 0:
        raise Exception("Non zero return code: %d"%process.returncode)

def recon(filename, fileabspath):

    print('running participant level analysis for subject ' + filename)
    command = 'recon-all -s ' + filename + ' -i ' + fileabspath + ' -all -notal-check -qcache'
    # fsid = 'sub-' + filename
    # command = "recon-all -subjid %s -sd %s %s  -all -notal-check -qcache %d" % (fsid,output_dir,input_args)
    print(command)
    run(command)


# main function
__version__ = open('/version').read()
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Convert individual T1 freesurfer output to HCPMMP label file (mgz format)')
    parser.add_argument('bids_dir', help='The directory with the input dataset '
                        'formatted according to the BIDS standard.')
    parser.add_argument('output_dir', help='The directory where the output files '
                        'should be stored. If you are running group level analysis '
                        'this folder should be prepopulated with the results of the'
                        'participant level analysis.')
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
    parser.add_argument('--acquisition_label', help='If the dataset contains multiple T1 weighted images from different acquisitions which one should be used? Corresponds to "acq-<acquisition_label>"')
    parser.add_argument('--reconstruction_label', help='If the dataset contains multiple T1 weighted images from different reconstructions which one should be used? Corresponds to "rec-<reconstruction_label>"')

    parser.add_argument('--n_cpus', help='Number of CPUs/cores available to use.', type=int)
    parser.add_argument('--skip_bids_validator', '--skip-bids-validator', action='store_true',
                        default=False,
                        help='assume the input dataset is BIDS compliant and skip the validation')
    
    parser.add_argument('-v', '--version', action='version',
                        version='Pipeline version {}'.format(__version__))
    

    args = parser.parse_args()

    start = time.time()

    # copy freesurfer license
    shutil.copyfile('/license.txt', '/opt/freesurfer/license.txt')
    
    # run bids-validator if necessary 
    if not args.skip_bids_validator:
        run("bids-validator " + args.bids_dir)

    # parse bids layout
    layout = bids.layout.BIDSLayout(args.bids_dir, derivatives=False, absolute_paths=True)
    subjects_to_analyze = []
    subject_dirs = glob.glob(os.path.join(args.bids_dir, "sub-*"))
    # only for a subset of subjects
    if args.participant_label:
        subjects_to_analyze = args.participant_label
    # for all subjects
    else:
        subjects_to_analyze = [subject_dir.split("-")[-1] for subject_dir in subject_dirs]
    # only use a subset of sessions
    if args.session_label:
        session_to_analyze = dict(session=args.session_label)
    else:
        session_to_analyze = dict()

    subjects_to_analyze.sort()

    #Got to combine acq_tpl and rec_tpl
    if args.acquisition_label and not args.reconstruction_label:
        ar_tpl = "*acq-%s*" % args.acquisition_label
    elif args.reconstruction_label and not args.acquisition_label:
        ar_tpl = "*rec-%s*" % args.reconstruction_label
    elif args.reconstruction_label and args.acquisition_label:
        ar_tpl = "*acq-%s*_rec-%s*" % (args.acquisition_label, args.reconstruction_label)
    else:
        ar_tpl = "*"


    # check if freesurfer has been finished for some subjects
    os.environ["SUBJECTS_DIR"] = args.output_dir
    subject_done_dirs = glob.glob(os.path.join(args.output_dir, "sub-*", 'mri', 'aparc.DKTatlas+aseg.mgz'))
    subjects_already_done = [subject_dir[:-28].split("-")[-1] for subject_dir in subject_done_dirs]
    if subjects_already_done:
        print('The following cases have been successfully processed, will jump them:')
        print(' '.join(subjects_already_done))
    subjects_to_analyze = list(set(subjects_to_analyze) - set(subjects_already_done))
    subjects_to_analyze.sort()
    print("subjects_to_analyze: ", subjects_to_analyze)


    # running participant level
    if args.analysis_level == "participant":
        t1ws_ls = []
        sub_ses_id_ls = []
        
        # find all T1w 
        for subject_label in subjects_to_analyze:
            t1ws = [f.path for f in layout.get(subject=subject_label,
                                                suffix='T1w',
                                                extension=["nii.gz", "nii"],
                                                **session_to_analyze)]
            if os.path.normpath(t1ws[0]).split(os.sep)[-3].split("-")[0] == 'ses':
                sessions = [os.path.normpath(t1).split(os.sep)[-3].split("-")[-1] for t1 in t1ws]
            else:
                sessions = []
            # if args.session_label:
            #     sessions = sessions.intersection(args.session_label)
            assert (len(t1ws) > 0), "No T1w files found for subject %s!"%subject_label
            for i in range(len(t1ws)):
                t1ws_ls.append(t1ws[i])
                if sessions and not args.session_label:
                    sub_ses_id = 'sub-' + subject_label + '_ses-' + sessions[i]
                else:
                    sub_ses_id = 'sub-' + subject_label
                sub_ses_id_ls.append(sub_ses_id)
        
        # init batch process
        if args.n_cpus:
            n_cpus = args.n_cpus
        else:
            n_cpus = min(len(t1ws_ls), multiprocessing.cpu_count())
        pool = multiprocessing.Pool(processes=n_cpus)
        for i in range(len(t1ws_ls)):
            pool.apply_async(recon, (sub_ses_id_ls[i], t1ws_ls[i],))
        pool.close()
        pool.join()

    end = time.time()
    running_time = end - start
    print('running time: {:.0f}min {:.0f}sec'.format(running_time//60, running_time % 60))