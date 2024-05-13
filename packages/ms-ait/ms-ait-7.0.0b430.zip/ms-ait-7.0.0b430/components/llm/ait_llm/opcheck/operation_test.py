# Copyright (c) 2023-2023 Huawei Technologies Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import re
import unittest
import json
import numpy as np
import torch
import torch_npu

from ait_llm.common.tool import read_atb_data
from ait_llm.common.log import logger
from ait_llm.compare.cmp_algorithm import CMP_ALG_MAP, CUSTOM_ALG_MAP


FLOAT_EPSILON = torch.finfo(torch.float).eps


class OperationTest(unittest.TestCase):
    def __init__(self, methodName='opTest', case_info=None, excuted_ids=None):
        super(OperationTest, self).__init__(methodName)

        self.case_info = case_info
        self.case_info['res_detail'] = []
        self.excuted_ids = excuted_ids
        self.op_id = case_info['op_id']
        self.op_name = case_info['op_name']
        self.op_param = case_info['op_param']
        self.tensor_path = case_info['tensor_path']
        self.in_tensors = []
        self.out_tensors = []
        self.rerun = self.case_info["rerun"]

        error1 = 'Error0.1‰'
        error2 = 'Error0.5‰'
        error3 = 'Error1‰'
        error4 = 'Error4‰'
        error5 = 'Error5‰'
        error6 = 'Error+/-1'

        self.precision_standard = {
            'torch.double': [error1, 99.99], 'torch.uint32': [error1, 99.99], 'torch.int64': [error1, 99.99],
            'torch.float': [error1, 99.99], 'torch.int32': [error1, 99.99], 'torch.uint64': [error1, 99.99],
            'torch.float16': [error3, 99.9], 'torch.bfloat16': [error4, 99.6], 'torch.int8': [error6, 99.9],
            'torch.uint8': [error6, 99], 'torch.int16': [error6, 99.9], 'torch.uint16': [error6, 99.9],
            'torch.bool': [error1, 100]
        }

        self.erol_dict = {
            error1: 0.0001,
            error2: 0.0005,
            error3: 0.001,
            error4: 0.004,
            error5: 0.005,
            error6: 1
        }

    @staticmethod
    def parametrize(optest_class, case_info=None, excuted_ids=None):
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(optest_class)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(optest_class(name, case_info=case_info, excuted_ids=excuted_ids))
        return suite

    def setUp(self):
        def get_tensor_path(tensor_type):
            _tensor_path = [x for x in os.listdir(self.tensor_path) if x.startswith(tensor_type)]
            _tensor_path.sort(key=lambda x:int(x.split(tensor_type)[1].split('.')[0]))  
            _tensor_path = [os.path.join(self.tensor_path, x) for x in _tensor_path]
            return _tensor_path

        if self.tensor_path:
            if os.path.isdir(self.tensor_path):
                _in_tensor_path = get_tensor_path("intensor")
                for path in _in_tensor_path:
                    _in_tensor = read_atb_data(path).npu()
                    self.in_tensors.append(_in_tensor)
                _out_tensor_path = get_tensor_path("outtensor")
                for path in _out_tensor_path:
                    _out_tensor = read_atb_data(path).npu()
                    self.out_tensors.append(_out_tensor)
            else:
                raise RuntimeError(f"{self.tensor_path} not valid")
        else:
            raise RuntimeError(f"{self.tensor_path} not valid")

    def tearDown(self):
        self.excuted_ids.put(self.op_id)
        if self.case_info['excuted_information'] != 'PASS':
            self.case_info['excuted_information'] = 'FAILED'

    def rerun_op(self, excute_type): 
        operation = torch.classes.OperationTorch.OperationTorch(self.op_name)
        if isinstance(self.op_param, dict):
            operation.set_param(json.dumps(self.op_param))
        elif isinstance(self.op_param, str):
            operation.set_param(self.op_param)
        if excute_type == "inplace":
            operation.execute(self.in_tensors)
            out_tensors = []
            for index in self.case_info['inplace_idx']:
                out_tensors.append(self.in_tensors[index])
        elif excute_type == "with_param":
            operation.set_varaintpack_param(self.case_info['run_param'])
            out_tensors = operation.execute(self.in_tensors)
        else:
            out_tensors = operation.execute(self.in_tensors)
        return out_tensors

    def excute_common(self, excute_type):
        logger_text = f"———————— {self.op_id} {self.op_name} test start ————————"
        logger.info(logger_text)
        if self.rerun:
            out_tensors = self.rerun_op(excute_type)
        else:
            out_tensors = self.out_tensors
        
        if self.op_name == "AllGatherOperation":
            rank = self.op_param.get("rank", 0)
            out_tensors[0] = out_tensors[0][rank]

        golden_out_tensors = self.golden_calc(self.in_tensors)
        try:
            logger.debug("out_tensor", out_tensors[0].size())
            logger.debug("golden_out_tensor", golden_out_tensors[0].size())
        except TypeError as e:
            logger_text = "The output is abnormal. Please check! Exception: {}".format(e)
            logger.debug(logger_text)

        self.__golden_compare_all(out_tensors, golden_out_tensors)

    def execute(self):
        self.excute_common("common")

    def execute_with_param(self):
        self.excute_common("with_param")

    def execute_inplace(self):
        self.excute_common("inplace")

    def get_rel_pass_rate(self, out, golden, etol):
        out, golden = out.reshape(-1).cpu(), golden.reshape(-1).cpu()
        size = out.shape[0]
        rel_errors = torch.where(
            torch.abs(golden) > FLOAT_EPSILON,
            torch.abs(out / golden - 1),  # abs(aa - bb) / abs(bb) -> abs(aa / bb - 1)
            torch.tensor(0, dtype=out.dtype),
        )
        rel_pass_rate = torch.sum(rel_errors <= etol) / size if size != 0 else 0
        max_rel_error = torch.max(rel_errors)
        return rel_pass_rate.item() * 100, max_rel_error.item()

    def get_abs_pass_rate(self, out, golden, etol):
        out, golden = out.cpu(), golden.cpu()
        size = out.shape[0]
        abs_errors = torch.where(
            torch.abs(golden) > FLOAT_EPSILON,
            torch.abs(out - golden),  # abs(aa - bb) / abs(bb) -> abs(aa / bb - 1)
            torch.tensor(0, dtype=out.dtype),
        )
        abs_pass_rate = torch.sum(abs_errors <= etol) / size if size != 0 else 0
        max_abs_error = torch.max(abs_errors)
        return abs_pass_rate.item() * 100, max_abs_error.item()

    def get_other_precisions(self, out, golden, etol):
        message = []
        precision_type = self.case_info['precision_type']
        default_str = 'NaN'
        abs_pass_rate, max_abs_error, cos_sim, kl = None, None, None, None

        out, golden = out.reshape(-1), golden.reshape(-1)
        if 'abs' in precision_type:
            abs_pass_rate, max_abs_error = self.get_abs_pass_rate(out, golden, etol)
        if 'cos_sim' in precision_type:
            cos_sim, cur_message = CMP_ALG_MAP["cosine_similarity"](golden, out)
            if cur_message:
                message.append('cos_sim: ' + cur_message)
        if 'kl' in precision_type:
            kl, cur_message = CMP_ALG_MAP["kl_divergence"](golden, out)
            if cur_message:
                message.append('kl_div: ' + cur_message)
        abs_pass_rate_str = "%.16f" % float(abs_pass_rate) if abs_pass_rate is not None else default_str
        max_abs_error_str = "%.16f" % float(max_abs_error) if max_abs_error is not None else default_str
        cos_sim_str = "%.10f" % cos_sim if cos_sim is not None else default_str
        kl_div_str = "%.16f" % kl if kl is not None else default_str

        return (abs_pass_rate_str, max_abs_error_str, cos_sim_str, kl_div_str), ", ".join(message)

    def get_npu_device(self):
        npu_device = os.environ.get("NPU_DEVICE")
        if npu_device is None:
            npu_device = "npu:0"
        else:
            npu_device = f"npu:{npu_device}"
        return npu_device

    def get_soc_version(self):
        device_name = torch.npu.get_device_name()
        if re.search("Ascend910B", device_name, re.I):
            soc_version = 'Ascend910B'
        elif re.search("Ascend310P", device_name, re.I):
            soc_version = 'Ascend310P'
        else:
            raise RuntimeError(f"{device_name} is not supported")
        device_count = torch.npu.device_count()
        current_device = torch.npu.current_device()
        logger_text = "Device Properties: device_name: {}, soc_version: {}, device_count: {}, current_device: {}" \
                    .format(device_name, soc_version, device_count, current_device)
        logger.debug(logger_text)
        return soc_version

    def __golden_compare_all(self, out_tensors, golden_out_tensors):
        message, pass_flag = [], True

        my_data_len, golden_data_len = len(out_tensors), len(golden_out_tensors)
        if my_data_len != golden_data_len:
            pass_flag = False
            logger.info(f"Data count not equal, {my_data_len} != {golden_data_len}. Will compare only partial")

        tensor_count = len(out_tensors)
        for out_tensor, golden_out_tensor in zip(out_tensors, golden_out_tensors):
            out_dtype = str(out_tensor.dtype)
            p_s = self.precision_standard.get(out_dtype, [])
            if len(p_s) != 2:
                cur_message = f"{out_dtype} not supported!"
                self.case_info['fail_reason'] = cur_message
                raise RuntimeError(cur_message)

            etol = self.erol_dict.get(p_s[0], 0.001)
            err_rate = p_s[1]
            ps_standard = f"{err_rate}%(error<{etol})"

            rel_pass_rate, max_rel = self.get_rel_pass_rate(out_tensor, golden_out_tensor, etol)

            if err_rate >= rel_pass_rate:
                pass_flag = False
                cur_message = f"relative pass rate: {rel_pass_rate} not met standart: {err_rate}."
                message.append(cur_message)
                logger.debug(cur_message)

            rel_pass_rate = "%.16f" % float(rel_pass_rate)
            max_rel = "%.16f" % float(max_rel)
            (abs_pass_rate, max_abs, cos_sim, kl_div), cur_message = self.get_other_precisions(
                out_tensor, golden_out_tensor, etol
            )
            if cur_message:
                message.append(cur_message)

            cur_result = {
                "precision_standard": ps_standard,
                "rel_pass_rate": rel_pass_rate,
                "max_rel": max_rel,
                "abs_pass_rate": abs_pass_rate,
                "max_abs": max_abs,
                "cos_sim": cos_sim,
                "kl_div": kl_div,
            }
            for name, compare_func in CUSTOM_ALG_MAP.items():
                cur_result[name], cur_message = compare_func(golden_out_tensor, out_tensor)
                if cur_message:
                    message.append(f"{name}: {cur_message}")
            self.case_info['res_detail'].append(cur_result)

            if pass_flag:
                self.case_info['excuted_information'] = 'PASS'
                
            else:
                self.case_info['excuted_information'] = 'FAILED'
            self.case_info['fail_reason'] = ", ".join(message)