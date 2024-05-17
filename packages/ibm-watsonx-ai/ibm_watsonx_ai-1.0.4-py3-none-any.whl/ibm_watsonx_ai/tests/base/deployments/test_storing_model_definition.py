#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import os
import unittest
import io
import contextlib
import filecmp
import pandas as pd

from ibm_watsonx_ai.tests.base.abstract.abstract_client_test import AbstractClientTest


class TestStoreModelDefinition(AbstractClientTest, unittest.TestCase):
    """
    Test case checking the scenario of storing model definitions
    """
    SPACE_ONLY = True

    JENKINS_RUNTIME = os.getenv('JENKINS_RUNTIME')

    if JENKINS_RUNTIME == "rt23.1":
        software_specification_name = "tensorflow_rt23.1-py3.10"
        python_version = "3.10"
    elif JENKINS_RUNTIME == "rt24.1":
        software_specification_name = "tensorflow_rt24.1-py3.11"
        python_version = "3.11"
    else:
        print("No runtime specification was chose!")

    model_definition_name = "tensorflow_model_definition"
    training_name = "test_tensorflow_training"
    training_description = "TF-test-experiment"
    execution_command = "python3 mnist_mlp.py"

    model_def_path = os.path.join(os.getcwd(), "base", "artifacts", "tensorflow", "tf-model-definition.zip")
    model_definition_id = None

    def create_model_definition_payload(self):
        """
        Creates payload for model definition.
        """
        return {
            self.wml_client.model_definitions.ConfigurationMetaNames.NAME: self.model_definition_name,
            self.wml_client.model_definitions.ConfigurationMetaNames.COMMAND: self.execution_command,
            self.wml_client.model_definitions.ConfigurationMetaNames.PLATFORM: {"name": "python", "versions": [TestStoreModelDefinition.python_version]},
            self.wml_client.model_definitions.ConfigurationMetaNames.VERSION: "2.0",
        }

    def test_01_create_model_definition(self):
        meta_props = self.create_model_definition_payload()
        model_definitions_details = self.wml_client.model_definitions.store(
            self.model_def_path, meta_props
        )
        model_definition_id = self.wml_client.model_definitions.get_id(
            model_definitions_details
        )
        self.assertIsNotNone(model_definition_id)
        TestStoreModelDefinition.model_definition_id = model_definition_id

    def test_02_get_model_definition_details(self):
        details = self.wml_client.model_definitions.get_details(self.model_definition_id)
        print(details)
        self.assertIsNotNone(details)
        self.assertEqual(self.model_definition_name, details["metadata"]["name"])

    def test_03_download_model_definition(self):
        self.wml_client.model_definitions.download(self.model_definition_id, './model_def.zip')
        self.assertTrue(filecmp.cmp('./model_def.zip', self.model_def_path))

    def test_04_list_definitions(self):
        df = self.wml_client.model_definitions.list()
        self.assertTrue(self.model_definition_id in df.values)

    def test_05_create_definition_revision(self):
        TestStoreModelDefinition.definition_id = self.model_definition_id
        revision = self.wml_client.model_definitions.create_revision(self.definition_id)
        TestStoreModelDefinition.rev_id = revision['metadata'].get('revision_id')
        self.assertIsNotNone(self.rev_id)

    def test_06_list_definition_revisions(self):
        df = self.wml_client.model_definitions.list_revisions(self.definition_id)
        self.assertIn(self.rev_id, df['REV_ID'].values)

    def test_07_update_model_definition(self):
        details = self.wml_client.model_definitions.update(
            self.definition_id,
            {
                self.wml_client.model_definitions.ConfigurationMetaNames.NAME: "Updated model definition"
            }
        )
        self.assertIsNotNone(details)

    def test_08_download_model_definition_for_given_rev_id(self):
        definition_path = 'model.tar.gz'
        with contextlib.suppress(FileNotFoundError):
            os.remove(definition_path)

            self.wml_client.model_definitions.download(
                model_definition_uid=self.definition_id, filename=definition_path, rev_id=self.rev_id
            )

            os.remove(definition_path)

    def test_99_cleanup(self):
        self.wml_client.model_definitions.delete(self.model_definition_id)


if __name__ == "__main__":
    unittest.main()
