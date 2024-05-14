import unittest
import shutil
import tempfile
import os
from ewoks import load_graph
from darfix.core.process import graph_data_selection
from darfix.app.__main__ import execute_graph
from silx.io.url import DataUrl

try:
    from importlib.resources import files as resource_files
except ImportError:
    from importlib_resources import files as resource_files


class EwoksTest(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.tmpdir)

    def test_darfix_example2_edf(self):
        from orangecontrib.darfix import tutorials

        filename = resource_files(tutorials).joinpath("darfix_example2.ows")
        graph = load_graph(str(filename))

        image0 = resource_files(tutorials).joinpath("edf_dataset", "strain_0000.edf")
        image1 = resource_files(tutorials).joinpath("edf_dataset", "strain_0001.edf")
        filenames = [str(image0), str(image1)]
        graph_data_selection(
            graph=graph,
            filenames=filenames,
            root_dir=str(self.tmpdir),
            in_memory=True,
        )
        results = graph.execute(output_tasks=True)
        for node_id, task in results.items():
            assert task.succeeded, node_id

    def test_darfix_example2_hdf5(self):
        from orangecontrib.darfix import tutorials

        filename = resource_files(tutorials).joinpath("darfix_example2.ows")
        graph = load_graph(str(filename))

        hdf5_dataset_file = resource_files(tutorials).joinpath(
            "hdf5_dataset", "strain.hdf5"
        )
        assert os.path.exists(str(hdf5_dataset_file))
        filenames = (
            DataUrl(
                file_path=str(hdf5_dataset_file),
                data_path="/1.1/instrument/my_detector/data",
                scheme="silx",
            ).path(),
        )
        graph_data_selection(
            graph=graph,
            filenames=filenames,
            root_dir=str(self.tmpdir),
            in_memory=False,
            metadata_url=DataUrl(
                file_path=str(hdf5_dataset_file),
                data_path="/1.1/instrument/positioners",
                scheme="silx",
            ).path(),
        )
        results = graph.execute(output_tasks=True)
        for node_id, task in results.items():
            assert task.succeeded, node_id

    def test_darfix_example2_cli(self):
        from orangecontrib.darfix import tutorials

        filename = resource_files(tutorials).joinpath("darfix_example2.ows")
        argv = [
            None,
            "-wf",
            str(filename),
            "-fd",
            os.path.join(str(filename.parent), "edf_dataset"),
            "-td",
            str(self.tmpdir),
        ]
        results = execute_graph(argv=argv, output_tasks=True)
        for node_id, task in results.items():
            assert task.succeeded, node_id
