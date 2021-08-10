#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mnefun preprocessing of face-to-face data (for connectivity analysis).

authors: Daniel McCloy
license: MIT
"""

import mnefun
from f2f_helpers import load_paths, load_subjects, scale_mri
from f2f_score import f2f_score

# load general params
data_root, subjects_dir, _ = load_paths()
subjects = load_subjects()

# load mnefun params from YAML
params = mnefun.read_params('mnefun_params.yaml')

# set additional params: general
params.score = f2f_score
params.subjects_dir = subjects_dir
params.subjects = subjects
params.structurals = subjects
params.subject_indices = list(range(len(params.subjects)))
params.work_dir = data_root

# set additional params: report
kwargs = dict(analysis='Conditions', cov=f'%s-{params.lp_cut}-sss-cov.fif')
params.report['whitening'] = [dict(name=c, **kwargs) for c in params.in_names]

# scale the surrogate MRI to each subj (skipped automatically if already done)
for subject in subjects:
    scale_mri(subject, subjects_dir, subject_from='14mo_surr',
              target_file='T1.mgz')

# run it
mnefun.do_processing(
    params,
    fetch_raw=False,      # go get the Raw files
    do_sss=True,          # tSSS / maxwell filtering
    do_score=False,       # run scoring function to extract events
    gen_ssp=False,        # create SSP projectors
    apply_ssp=False,      # apply SSP projectors
    write_epochs=False,   # epoching & filtering
    gen_covs=False,       # make covariance
    gen_fwd=False,        # generate fwd model
    gen_inv=False,        # generate inverse
    gen_report=False,     # print report
    print_status=True     # show status
)