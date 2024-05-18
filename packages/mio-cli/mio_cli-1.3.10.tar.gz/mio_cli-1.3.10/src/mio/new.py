# Copyright 2021-2023 Datum Technology Corporation
# SPDX-License-Identifier: GPL-3.0
########################################################################################################################


from mio import common
from mio import cfg
from mio import cov
from mio import dox
from mio import results
from mio import sim
from mio import user

import jinja2
from jinja2 import Template
import zipfile
import shutil
import os
import sys
import glob
import requests
import json
from ezodf import opendoc, Sheet
from base64 import b64encode
import tarfile
import pathlib 
from base64 import b64decode


uvmx_gen_endpoint = "https://76mxx43uea5d7tlvwxigar54zq0xdbyi.lambda-url.us-east-1.on.aws/"


def main(ip_list, type, preview):
    payloads = {}
    target_dir = cfg.docs_dir
    spreadsheets = []
    for root, directories, file in os.walk(target_dir):
        for file in file:
            if (file.endswith(".dtc.ods")):
                spreadsheets.append(file)
            if (file.endswith(".uvmx.ods")):
                spreadsheets.append(file)
    
    if len(spreadsheets) == 0:
        common.fatal(f"Did not find any UVMx generator input spreadsheets under the project docs directory ({target_dir})")
    else:
        for sheet in spreadsheets:
            try:
                with open(f"{target_dir}/{sheet}",'rb') as f:
                    payload = b64encode(f.read())
                    payloads[sheet] = payload.decode()
            except Exception as e:
                common.fatal(f"Could not open '{sheet}': {e}")
    
    preview_str = "false"
    if preview:
        preview_str = "true"

    query = json.dumps({
        'project_name'            : cfg.project_name,
        'ip_list'                 : ip_list,
        'preview'                 : preview_str,
        'type'                    : type,
        'docs_dir_rel_path'       : cfg.docs_dir_rel_path,
        'payloads'                : payloads          ,
        'vendor'                  : user.org_name     ,
        'name_of_copyright_owner' : user.org_full_name
    })
    common.dbg(f"Query for UVMx code generation:\n{query}")
    auth_headers = {
        'Accept-Encoding'  : 'gzip, deflate, br',
        'Content-Type'     : 'application/json; charset="UTF-8"'
    }
    common.dbg(f"Authorization headers for UVMx code generation:\n{auth_headers}")
    common.info(f"Generating code from {len(payloads)} file(s) ...")
    response = requests.get(uvmx_gen_endpoint, data=query, headers=auth_headers)
    if response.status_code != 200:
        # TODO Print prettier error logs:
        #            json_object = json.loads(response.text)
        #            ...
        common.fatal(f"Error during UVMx code generation.\n'{response.text}'")
        return
    else:
        json_data = response.json()
        body = json_data['payload']
        result = json_data['result']
        common.dbg(f"Response from UVMx code generator:\n{body}")
    
    payload = json_data['payload']
    filename = pathlib.Path(cfg.temp_path + "/uvmx.tgz")
    filename.write_bytes(b64decode(payload))
    tar = tarfile.open(filename, "r:gz")
    tar.extractall(cfg.project_dir)
    tar.close()
    #common.remove_file(filename)
    common.banner("Generated code successfully")



