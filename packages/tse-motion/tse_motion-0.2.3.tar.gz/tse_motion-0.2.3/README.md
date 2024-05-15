# Installation
```
pip install tse-motion
```
# CLI

```
rate-motion sub-003_ses_01_acq_hipp_T2w.nii.gz

Input: sub-003_ses-01_acq-hipp_T2w.nii.gz | Motion Rating: 4.0
```
# Python
```python
from tse_rating import rate
input_path = 'tse.nii.gz'
score = rate_motion_artifact(input_path)
```