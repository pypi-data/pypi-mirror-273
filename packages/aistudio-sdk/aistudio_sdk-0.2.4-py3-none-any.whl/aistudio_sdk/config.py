#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
config

Authors: xiangyiqing(xiangyiqing@baidu.com)
Date:    2023/07/24
"""
import os

ENV = os.environ.get("CURRENT_ENV", "online")  # sandbox or online

# Set to either 'debug' or 'info', controls console logging

DEFAULT_LOG_LEVEL = "info"
CONNECTION_TIMEOUT = 30     # second
CONNECTION_RETRY_TIMES = 1
CONNECTION_TIMEOUT_UPLOAD = 60 * 60     # second
CONNECTION_TIMEOUT_DOWNLOAD = 60 * 60     # second

COMMON_FILE_SIZE_LIMIT = 5 * 1024 * 1024  # 5M
LFS_FILE_SIZE_LIMIT = 50 * 1024 * 1024 * 1024 # 50G
LFS_FILE_SIZE_LIMIT_PUT = 5 * 1024 * 1024 * 1024 # 5G

# host
if ENV == "sandbox":
    STUDIO_GIT_HOST_DEFAULT = "http://sandbox-git.aistudio.baidu.com"
    STUDIO_MODEL_API_URL_PREFIX_DEFAULT = "https://sandbox-aistudio.baidu.com"
elif ENV == "online":
    STUDIO_GIT_HOST_DEFAULT = "http://git.aistudio.baidu.com"
    STUDIO_MODEL_API_URL_PREFIX_DEFAULT = "https://aistudio.baidu.com"
else:
    raise ValueError("Invalid ENV: {}".format(ENV))

# Hub API
HUB_URL = "/studio/model/sdk/add"
HUB_URL_VISIBLE_CHECK = "/modelcenter/v2/models/sdk/checkPermit"
APP_SERVICE_URL = "/serving/web/highapp/sdk/create"

# PP Pipeline API
MOUNT_DATASET_LIMIT = 3
PIPELINE_CODE_SIZE_LIMIT = 50 * 1024 * 1024     # bytes
PIPELINE_CREATE_URL = "/paddlex/v3/pipelines/sdk/create"
PIPELINE_CREATE_CALLBACK_URL = "/paddlex/v3/pipelines/sdk/create/callback"
PIPELINE_BOSACL_URL = "/paddlex/v3/file/api/bosacl"
PIPELINE_QUERY_URL = "/paddlex/v3/pipelines/sdk/list"
PIPELINE_STOP_URL = "/paddlex/v3/pipelines/sdk/stop"
