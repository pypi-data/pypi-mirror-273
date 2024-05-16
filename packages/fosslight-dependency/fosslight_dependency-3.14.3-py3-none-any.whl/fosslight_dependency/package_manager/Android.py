#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2021 LG Electronics Inc.
# SPDX-License-Identifier: Apache-2.0

import os
import logging
import fosslight_util.constant as constant
import fosslight_dependency.constant as const
from fosslight_dependency._package_manager import PackageManager, get_url_to_purl

logger = logging.getLogger(constant.LOGGER_NAME)

_plugin_output_file = 'android_dependency_output.txt'


class Android(PackageManager):
    package_manager_name = const.ANDROID

    app_name = const.default_app_name
    input_file_name = ''

    def __init__(self, input_dir, output_dir, app_name):
        super().__init__(self.package_manager_name, '', input_dir, output_dir)
        if app_name:
            self.app_name = app_name
        self.input_file_name = self.check_input_path(self.app_name, _plugin_output_file)
        self.append_input_package_list_file(self.input_file_name)

    def check_input_path(self, app_name, _plugin_output_file):
        if os.path.isfile(_plugin_output_file):
            return _plugin_output_file
        else:
            return os.path.join(app_name, _plugin_output_file)

    def parse_oss_information(self, f_name):
        with open(f_name, 'r', encoding='utf8') as input_fp:
            sheet_list = []

            for i, line in enumerate(input_fp.readlines()):
                comment = ''
                split_str = line.strip().split("\t")
                if i < 2:
                    continue

                if len(split_str) == 9:
                    idx, manifest_file, oss_name, oss_version, license_name, dn_loc, homepage, NA, NA = split_str
                elif len(split_str) == 7:
                    idx, manifest_file, oss_name, oss_version, license_name, dn_loc, homepage = split_str
                else:
                    continue
                purl = get_url_to_purl(dn_loc, 'maven')
                self.purl_dict[f'{oss_name}({oss_version})'] = purl

                comment_list = []
                deps_list = []
                if self.direct_dep:
                    dep_key = f"{oss_name}({oss_version})"
                    if self.total_dep_list:
                        if dep_key not in self.total_dep_list:
                            continue
                    if dep_key in self.direct_dep_list:
                        comment_list.append('direct')
                    else:
                        comment_list.append('transitive')
                    try:
                        if dep_key in self.relation_tree:
                            deps_list.extend(self.relation_tree[dep_key])
                    except Exception as e:
                        logger.error(f"Fail to find oss scope in dependency tree: {e}")
                comment = ','.join(comment_list)
                deps = ','.join(deps_list)

                sheet_list.append([purl, oss_name, oss_version, license_name, dn_loc, homepage,
                                  '', '', comment, deps])

        return sheet_list
