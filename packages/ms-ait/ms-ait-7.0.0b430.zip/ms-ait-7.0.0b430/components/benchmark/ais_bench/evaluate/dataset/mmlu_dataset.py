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

import pandas as pd

from ais_bench.evaluate.dataset.base_dataset import BaseDataset
from ais_bench.evaluate.measurement.measurement_factory import MeasurementFactory
from ais_bench.evaluate.log import logger
from ais_bench.infer.path_security_check import ms_open, MAX_SIZE_LIMITE_NORMAL_FILE


class MmluDataset(BaseDataset):
    def _gen_prompt(self, prompt_df, category_name):
        question_template = "Question: {question}\nA. {A}\nB. {B}\nC. {C}\nD. {D}\nAnswer: {answer}\n"

        prompt = f"The following are multiple choice questions (with answer) about {category_name}.\n\n"
        for _, row in prompt_df.iterrows():
            prompt += question_template.format(question=row[0], A=row[1], B=row[2],
                                               C=row[3], D=row[4], answer=row[5])
        prompt += "Please answer the following questions.\n"
        return prompt

    def load(self):
        if self.dataset_path is None:
            self._download()
        self._check()

        self.subject_mapping = dict()
        for root, _, files in os.walk(os.path.join(self.dataset_path, "val")):
            for file in files:
                subject_name = file.strip()[:-8]
                val_path = os.path.join(root, file)
                with ms_open(val_path, max_size=MAX_SIZE_LIMITE_NORMAL_FILE) as file:
                    prompt_df = pd.read_csv(file, header=None)[:self.shot + 1]
                self.subject_mapping[subject_name] = [self._gen_prompt(prompt_df, subject_name)]

        for root, _, files in os.walk(os.path.join(self.dataset_path, "test")):
            for file in files:
                subject_name = file.strip()[:-9]
                test_path = os.path.join(root, file)
                with ms_open(test_path, max_size=MAX_SIZE_LIMITE_NORMAL_FILE) as file:
                    test_df = pd.read_csv(file, header=None)
                self.subject_mapping[subject_name].append(test_df)
        self.subjects = list(self.subject_mapping.keys())

    def __len__(self):
        count = 0
        for value in self.subject_mapping.values():
            count += len(value[1])
        return count

    def __iter__(self):
        self.current_key = 0
        self.current_index = 0
        return self

    def __next__(self):
        if self.current_key >= len(self.subjects):
            raise StopIteration

        key = self.subjects[self.current_key]
        prompt = self.subject_mapping.get(key)[0]
        test_df = self.subject_mapping.get(key)[1]

        if self.current_index >= len(test_df):
            self.current_key += 1
            self.current_index = 0
            return self.__next__()

        test_row = test_df.loc[self.current_index]
        prompt += "Question: {question}\nA. {A}\nB. {B}\nC. {C}\nD. {D}\nAnswer:\n".format(
            question=test_row[0], A=test_row[1], B=test_row[2], C=test_row[3], D=test_row[4])

        result = {"id": self.current_index, "subject": key,
                  "prompt": prompt, "ground_truth": test_df.loc[self.current_index, 5]}
        index = [key]
        self.current_index += 1
        return index, result

    def compute(self, data, measurement="accuracy") -> dict:
        '''
        input: data in the form of pandas.DataFrame OR a list of metrics dictonary
        output: a dictionary containing accuracy, total number of entry, number of correct entry
        '''
        ground_truth_index = "ground_truth"
        answer_index = "answer"
        measurement_method = MeasurementFactory().get(measurement)()

        output = measurement_method(data, ground_truth_index, answer_index)
        return output