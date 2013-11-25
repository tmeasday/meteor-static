#! /usr/bin/env python
import sys
import os
import os.path
import shutil
import tarfile
import subprocess
import re

def bundle_static(app_dir, out_dir):
    """Create a static website from a meteor app
    """    # 
    out_dir = os.path.abspath(out_dir)
    temp_dir = os.path.join(out_dir, 'tmp')
    
    shutil.rmtree(out_dir)
    os.makedirs(temp_dir)
    
    # get the bundle into a directory
    bundle_file = os.path.join(temp_dir, 'bundle.tar.gz')
    bundle(app_dir, bundle_file)
    untar(bundle_file, temp_dir)
    
    # grab the HTML, JS, CSS
    client_app = os.path.join(temp_dir, 'bundle', 'programs', 'client')
    for file in os.listdir(client_app):
        if (re.match(r'.*.(html|js|css)$', file)):
            shutil.move(os.path.join(client_app, file), out_dir)
    
    # grab the assets
    client_app_files = os.path.join(client_app, 'app')
    for file in os.listdir(client_app_files):
        shutil.move(os.path.join(client_app_files, file), out_dir)
    
    # rewrite the html file
    html_file = os.path.join(out_dir, 'app.html')
    html = open(html_file).read()
    new_html = re.sub(r'##.*##', '', html)
    open(html_file, 'w').write(new_html)
    
    # remove the temporary files
    shutil.rmtree(temp_dir)

def bundle(app_dir, bundle_file):
    """Run meteorite to create a bundle
    """
    os.chdir(app_dir)
    meteorite_cmd = "mrt bundle %s --build-dev-bundle" % bundle_file
    subprocess.check_call(meteorite_cmd, shell=True)
    
def untar(bundle_file, out_dir):
    """Unzip the bundle into a directory
    """
    tar_cmd = "tar -zxvf %s -C %s" % (bundle_file, out_dir)
    subprocess.check_call(tar_cmd, shell=True)

if (len(sys.argv) <= 2):
    print 'Usage: bundle-static.py /path/to/meteor/app /path/to/bundled/site'
else:
    bundle_static(sys.argv[1], sys.argv[2])