#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import os
import unittest

import scipy

from ibm_watsonx_ai.tests.base.abstract.abstract_online_deployment_test import AbstractOnlineDeploymentTest


class TestXGBoostDeployment(AbstractOnlineDeploymentTest, unittest.TestCase):
    """
    Test case checking the scenario of storing & deploying xgboost
    using compressed_file.
    """
    JENKINS_RUNTIME = os.getenv('JENKINS_RUNTIME')

    if JENKINS_RUNTIME == "rt23.1":
        software_specification_name = "runtime-23.1-py3.10"
        deployment_type = "xgboost_1.6"
    elif JENKINS_RUNTIME == "rt24.1":
        software_specification_name = "runtime-24.1-py3.11"
        deployment_type = "xgboost_2.0"
    else:
        print("No runtime specification was chose!")
    model_name = deployment_name = "xgboost_model_from_gz"
    file_name = 'xgboost_model.tar.gz'
    IS_MODEL = True

    def get_model(self):
        return os.path.join(os.getcwd(), 'base', 'artifacts', 'xgboost', self.file_name)

    def create_model_props(self):
        return {
            self.wml_client.repository.ModelMetaNames.NAME: self.model_name,
            self.wml_client.repository.ModelMetaNames.TYPE: self.deployment_type,
            self.wml_client.repository.ModelMetaNames.SOFTWARE_SPEC_ID:
                self.wml_client.software_specifications.get_id_by_name(self.software_specification_name)
        }

    def create_scoring_payload(self):
        data_path = os.path.join(os.getcwd(), 'base', 'datasets', 'xgboost', 'agaricus.txt.test')

        labels = []
        row = []
        col = []
        dat = []
        with open(data_path) as f:
            for i, l in enumerate(f):
                arr = l.split()
                labels.append(int(arr[0]))
                for it in arr[1:]:
                    k, v = it.split(':')
                    row.append(i)
                    col.append(int(k))
                    dat.append(float(v))
        csr = scipy.sparse.csr_matrix((dat, (row, col)))
        return {
            self.wml_client.deployments.ScoringMetaNames.INPUT_DATA: [{
                'values': csr.getrow(0).toarray().tolist()
            }]
        }


if __name__ == "__main__":
    unittest.main()
