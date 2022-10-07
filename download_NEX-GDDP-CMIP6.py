# -*- coding = utf-8 -*-
# Author: moulai
# Date: 2022-09-19

import os
import pandas as pd

# Read in the csv "gddp-cmip6-thredds-fileserver.csv" which contains the NEX-GDDP-CMIP6 urls
file_list = pd.read_csv('gddp-cmip6-files.csv')

# Let the user choose the Model, Experiment, and Variable to be downloaded
# Print the available Models
print('Available Models:')
print(file_list['Model'].unique())
print('Use commas to connect different model names, or enter "all" to indicate all models')
model = input('Model: ')
if model == 'all':
    model = file_list['Model'].unique()
else:
    model = model.split(',')
# Print the available Experiments
print('Available Experiments:')
print(file_list['Experiment'].unique())
print('Use commas to connect different experiment names, or enter "all" to indicate all experiments')
experiment = input('Experiment: ')
if experiment == 'all':
    experiment = file_list['Experiment'].unique()
else:
    experiment = experiment.split(',')
# Print the available Variables
print('Available Variables:')
print(file_list['Variable'].unique())
print('Use commas to connect different variable names, or enter "all" to indicate all variables')
variable = input('Variable: ')
if variable == 'all':
    variable = file_list['Variable'].unique()
else:
    variable = variable.split(',')

# Remove the spaces in the names
model = [x.strip() for x in model]
experiment = [x.strip() for x in experiment]
variable = [x.strip() for x in variable]

# Filter the file_list based on the user's choices
file_list = file_list[file_list['Model'].isin(model)]
file_list = file_list[file_list['Experiment'].isin(experiment)]
file_list = file_list[file_list['Variable'].isin(variable)]
# Reset the index
file_list = file_list.reset_index(drop=True)

# Print the user's choices
print('='*50)
print('Please confirm your choices:')
print('Model: ', model)
print('Experiment: ', experiment)
print('Variable: ', variable)
print('Total number of files to be downloaded: {}'.format(len(file_list)))

print('Do you want to check the MD5 checksums? (y/n) (Default: y)')
md5 = input('MD5 check: ')
if md5.strip() == 'n':
    md5 = False
else:
    md5 = True

print('If the file already exists, do you want to overwrite it? (y/n) (Default: n)')
overwrite = input('Overwrite: ')
if overwrite.strip() == 'y':
    overwrite = True
else:
    overwrite = False

print('Input the path to save the files. (Defalut: ./NEX-GDDP-CMIP6)')
root_path = input('Path: ')
if root_path == '':
    root_path = os.path.abspath('./NEX-GDDP-CMIP6')
else:
    root_path = os.path.abspath(root_path)

print('='*50)

def md5sum(file_path):
    '''
    Calculate the MD5 checksum of the file
    '''
    import hashlib
    with open(file_path, 'rb') as f:
        data = f.read()
        md5 = hashlib.md5(data).hexdigest()
    return md5

def download_file(url, path, file_md5, md5_check, overwrite):
    '''
    Download the file from the url to the path
    '''
    import hashlib
    import os
    file_name = url.split('/')[-1]
    path = os.path.join(path, file_name)
    # Check if the file already exists
    if os.path.exists(path):
        if overwrite:
            print('The file {} already exists, but will be overwritten.'.format(file_name))
        else:
            # Check if the file is complete
            if md5_check:
                if file_md5 == md5sum(path):
                    print('The file {} already exists and is complete.'.format(file_name))
                    return
                else:
                    print('The file {} already exists, but is incomplete. Trying to download it again.'.format(file_name))
                    os.remove(path)
            else:
                print('The file {} already exists, skip downloading. (MD5 not checked)'.format(file_name))
                return
    # Download the file, with progress bar
    import requests
    from tqdm import tqdm
    try:
        r = requests.get(url, stream=True, timeout=10)
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024*1024
        wrote = 0
        with open(path, 'wb') as f:
            for data in tqdm(r.iter_content(block_size), total=total_size//block_size, unit='MB', unit_scale=True):
                wrote = wrote  + len(data)
                f.write(data)
                f.flush()
    except requests.exceptions.RequestException as e:
        # Remove the incomplete file
        try:
            os.remove(path)
        except:
            pass
        print('Failed to download the file {}.'.format(file_name))
        return
    # Check the MD5 checksum
    if md5_check:
        print('Checking the MD5 checksum...')
        if file_md5 == md5sum(path):
            print('The MD5 checksum is correct.')
        else:
            print('The MD5 checksum is incorrect.')
            print('The correct checksum is {}'.format(file_md5))
            print('The downloaded file is removed.')
            os.remove(path)
            return
    print('The file is downloaded to {}'.format(path))

# Download the files in the path "./Model/Experiment/Variable/..."
for index, row in file_list.iterrows():
    # Create the path
    path = os.path.join(root_path, row['Model'], row['Experiment'], row['Variable'])
    # Create the path if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)
    # Download the file
    file_md5 = row['fileMD5']
    download_file(row['fileUrl'], path, file_md5=file_md5, md5_check=md5, overwrite=overwrite)
    # Print the progress
    print('Processed ' + str(index+1) + ' of ' + str(len(file_list)) + ' files')
    print()