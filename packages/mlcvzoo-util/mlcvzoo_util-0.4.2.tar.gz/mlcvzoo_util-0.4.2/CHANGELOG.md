# MLCVZoo mlcvzoo-utils module Versions:

0.4.2 (2024-05-16):
-------------------
Implement uv as the python package manager

0.4.1 (2024-02-07):
-------------------
Updated links in pyproject.toml

0.4.0 (2023-10-26):
-------------------
Add LabelStudioTrackingTaskConverter:
- Extract images from the video of a tracking data set
- Convert annotations of a tracking data set to be used as a detection dataset
- Tidy up dependencies:
  - Replace usage of the nptyping package by numpy.typing
  - Don't limit upper Version of mlflow

0.3.1 (2023-05-11):
-------------------
Relicense to OLFL-1.3 which succeeds the previous license

0.3.0 (2023-02-15):
------------------
Adapt to mlcvzoo_base v5 API changes
Other changes:
- Return trained model in model_trainer
- More type hints
- Move evaluation code out of model_evaluator main()
  into a new public run_evaluation() function

0.2.0 (2022-11-24):
------------------
Enhance MetricFactory:
- Add optional parameter 'logging_configs' to MetricFactory.log_results
- Add tensorboard false-positive and false-negative image logging to the ODMetricFactory
- Fix a bug in log_false_positive_info_to_tb where bounding boxes where
  drawn incorrectly

0.1.1 (2022-11-10):
------------------
Remove dependency on backports.strenum

0.1.0 (2022-09-13):
------------------
Minor ModelEvaluator enhancements:
- Adapt method interface of _post_evaluation_step in order to make it
  available for mlflow logging
- Add missing typing stub

0.0.1 (2022-09-08):
------------------
Initial release of the mlcvzoo-util module with its features:
- cvat_annotation_handler: Handle the download and upload of zip files to CVAT via its
  commandline interface
- logger: Handle python logging
- model_evaluator: Evaluate mlcvzoo models
- model_timer: Generic component for measuring runtimes of mlcvzoo models
- model_trainer: Handle the training of mlcvzoo models
- pre_annotation_tool: Handle the generation and uploading of annotations to CVAT
- video_image_creator: Extract frames from videos to build training datasets
- image_io_utils: Utility operations regarding image (picture) objects
- mlcvzoo_cli_tool: Definition of a super class for any mlcvzoo module that is
  providing a commandline interface
