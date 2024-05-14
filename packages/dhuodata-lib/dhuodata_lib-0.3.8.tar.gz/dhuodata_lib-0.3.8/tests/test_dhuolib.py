from dhuolib.clients import DhuolibClient
import sys
import unittest
from unittest.mock import patch, mock_open
import base64
from dhuolib.config import logger

sys.path.append("src")


class TestDhuolibUtils(unittest.TestCase):
    def setUp(self):
        self.end_point = "http://localhost:5000"
        self.dhuolib = DhuolibClient(
            service_endpoint=self.end_point, project_name="Test Project")
        self.file_path = "tests/files/LogisticRegression_best.pickle"

    def test_1_deve_lancar_excecao_com_valores_run_params_incorretos(self):
        experiment_params = {
            "experiment_tags": {"version": "v1", "priority": "P1"},
        }
        response = self.dhuolib.create_experiment(experiment_params)
        self.assertEqual(list(response.keys()), ["error"])

    @patch("requests.post")
    def test_2_deve_criar_o_experimento_com_run_params_corretos(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {"experiment_id": "1"}

        experiment_params = {
            "experiment_name": "test_experiment",
            "experiment_tags": {"version": "v1", "priority": "P1"},
        }

        response = self.dhuolib.create_experiment(experiment_params)
        self.assertEqual(response, mock_response.json.return_value)

    @patch("requests.post")
    def test_3_deve_executar_o_experimento_com_run_params_corretos(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "experiment_id": "experiment_id",
            "run_id": "run_id",
            "model_uri": "model_uri",
        }

        run_params = {
            "experiment_id": "2",
            "model_pkl_file": "tests/files/LogisticRegression_best.pickle",
            "requirements_file": "tests/files/requirements.txt",
        }
        response = self.dhuolib.run_experiment(run_params)

        self.assertEqual(response, mock_response.json.return_value)

    @patch("requests.post")
    def test_4_deve_criar_modelo_com_run_params_corretos(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "current_stage": "Production",
            "last_updated_timestamp": 1713582060414,
            "model_version": "1",
            "run_id": "9434e517ed104958b6f5f47d33c79184",
            "status": "READY",
        }

        run_params = {
            "stage": "Production",
            "modelname": "nlp_framework",
            "modeltag": "v1",
            "run_id": "9434e517ed104958b6f5f47d33c79184",
            "requirements_file": "tests/files/requirements.txt",
            "model_uri": "model_uri",
        }

        response = self.dhuolib.create_model(run_params)

        self.assertEqual(response, mock_response.json.return_value)

    @patch("requests.post")
    def test_5_deve_fazer_o_predict_online_a_partir_de_um_dataset(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "model_name": "nlp_framework",
            "predictions": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        }

        run_params = {
            "stage": "Production",
            "data": "tests/files/data_predict.csv",
            "modelname": "nlp_framework",
        }

        response = self.dhuolib.predict_online(run_params)

        self.assertEqual(response, mock_response.json.return_value)

    @patch("requests.post")
    def test_6_create_batch_project_successful(self, mock_post):
        project_name = "Test Project"
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {"status": "success", "project_id": 123}
        response = self.dhuolib.create_batch_project(project_name)
        self.assertEqual(response, {"status": "success", "project_id": 123})

    def test_7_create_batch_project_raises_exception_on_none(self):
        with self.assertRaises(ValueError) as context:
            self.dhuolib.create_batch_project(None)
            self.assertIn("project_name is required" in str(context.exception))

    def test_8_deploy_batch_project_no_project_name(self):
        self.dhuolib = DhuolibClient(service_endpoint=self.end_point)
        with self.assertRaises(ValueError) as context:
            self.dhuolib.deploy_batch_project("script.py", "requirements.txt")
            self.assertIn("Batch project is required" in str(context.exception))

    def test_9_deploy_batch_project_missing_files(self):
        with self.assertRaises(ValueError) as context:
            self.dhuolib.deploy_batch_project(None, None)
            self.assertIn(
            "script_filename and requirements_filename are required" in str(context.exception))

    def test_10_deploy_batch_project_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            response = self.dhuolib.deploy_batch_project("script.py", "requirements.txt")
            self.assertEqual(response, {"error": "File not found"})
