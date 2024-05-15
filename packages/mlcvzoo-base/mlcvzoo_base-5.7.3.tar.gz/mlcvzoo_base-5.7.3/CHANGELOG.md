# MLCVZoo mlcvzoo_base module Versions:

5.7.3 (2024-05-08):
-------------------
Implement uv as the package management tool

5.7.2 (2024-04-05):
-------------------
Correctly parse bounding boxes from annotation files in mot format:
- Correctly raise a ClassMappingNotFoundError
- Correctly raise a ForbiddenClassError

5.7.1 (2024-02-19):
-------------------
Catch all errors while registering models instead of only ImportErrors:
- Any error that is raised while registering one module should not affect
the other modules, which is the case when not all possible Exceptions are
catched

5.7.0 (2023-11-15):
-------------------
Add string constants for model runtime selection:
- Add runtime value for ONNX Runtime
- Add runtime value for ONNX Runtime for Float16 precision
- Add runtime value for TensorRT
- Add runtime value for TensorRT for Int8 precision
- Extend base model classes with a runtime attribute and a default value

5.6.0 (2023-11-06):
-------------------
Improve attribute handling for annotation data:
- Add "background" attribute for Pascal VOC, CVAT and COCO annotation format
- Add "use_occluded" and "use_background" filter possibilities for Pascal VOC, CVAT and COCO
  annotation format
- Add correct attribute parsing for Pascal VOC annotation format
- Fix parsing for the "content" attribute for CVAT annotation format
- Fix logic for parsing the "occluded" attribute for the CVAT annotation format

5.5.1 (2023-10-24):
-------------------
Optimize runtime for the Box.center() method.

5.5.0 (2023-10-16):
-------------------
Add the possibility to log Object Detection metrics with a MlflowClient object:
- Feature implement in mlcvzoo_base.evaluation.object_detection.metrics_logging.log_od_metrics_to_mlflow_run

5.4.0 (2023-09-26):
-------------------
Implement consistent clamping behaviours for all annotation parsers:
- Clamp based on the given shape of the image
- Replace usage of the nptyping package by numpy.typing
- Don't limit upper Version of mlflow

5.3.5 (2023-06-28):
-------------------
Adapt logging to be less verbose

5.3.4 (2023-05-24):
-------------------
Add py.typed so that mypy will use type annotations

5.3.3 (2023-05-11):
-------------------
Relicense to OLFL-1.3 which succeeds the previous license

5.3.2 (2023-03-15):
------------------
Fix color histogram computation for bounding boxes

5.3.1 (2023-03-09):
------------------
Remove direct versioned dependency on protobuf

5.3.0 (2023-02-24):
------------------
Enhance MOT parser: Allow to handover a custom definition of labels/classes for annotations parsed in MOT format

5.2.0 (2023-02-21):
------------------
Add annotation parser for the Label Studio json format

5.1.0 (2023-02-14):
------------------
Add data serialization methods (dict and json) for the API data classes

5.0.0(2023-02-10):
------------------
Enhance and extend the API
- New features:
  - NetBased (Interface):
    - Introduce method get_checkpoint_filename_suffix
    - Introduce a new generic Type NetConfigurationType to
      provide the generic property inference_config
  - Trainable (Interface): Introduce method get_training_output_dir
- Enhancements:
  - Besides having a registry for model constructors, provide a registry for model configurations
  - Use the attr package to have cleaner defined configuration classes

4.5.1 (2022-12-09):
------------------
Fix bug in PascalVOCAnnotationBuilder class regarding image shape reading
- Issue #101:
  - Correction of handling width and height attributes when assigning image_shape
    to match BaseAnnotation image_shape handling

4.5.0 (2022-12-09):
------------------
Add features to the Box class
- Provide width and height of the box as property
- Create a crop from an image
- Compute a histogram for the Box based on an image
- Compute iou between two Boxes
- Compute euclidean_distance between two Boxes

4.4.0 (2022-11-28):
------------------
Add mlcvzoo ConfigRegistry:
- Introduce a generic base class for mlcvzoo registries
- Add the ConfigRegistry as instance object in the ModelRegistry
- Adapt ReadFromFile configuration build: Allow the "from_yaml" constructor parameter to be optional

4.3.3 (2022-11-17):
------------------
Fix multiple bugs in the object detection evaluation module:
- Issue #105:
  - Ensure stable behavior of the "from_str" method of the ClassIdentifier class
- Issue #106:
  - Ensure correct drawing of ground-truth, false-positive and false-negative bounding-boxes
    in the tensorboard logs
- Issue #107:
  - Ensure that keys are existing in computation dictionaries before accessing them

4.3.2 (2022-11-14):
------------------
No code or behaviour changes

4.3.1 (2022-11-10):
------------------
- Remove dependency on backports.strenum
- Depend on pillow 8.2 or higher as well as pillow 9

4.3.0 (2022-10-17):
------------------
Correctly utilize reduction mapping for Object Detection evaluation:
- Don't run the evaluation based on a classes-id-dict, but on a list of class-identifiers
- Change the internal data structures to dictionaries to be more flexible

4.2.1 (2022-09-08):
------------------
Fix minor code smells
- Clarify annotation writer docstring
- Let annotation writers return the file path if applicable

4.2.0 (2022-09-05):
------------------
Minor enhancements and fixes:
- Adapt code to config-builder v7.0.0
- Add update methods for the model-config
- Add methods for calculating specific metrics
- Allow to log object detection metrics to mlflow with step
- Ensure PascalVOCAnnotationParser parses independently for every given input-data configuration

4.1.0 (2022-08-26):
------------------
Add parser for MOT Datasets:
- Allow to parse from datasets of the different MOT challenges: MOT15, MOT16, MOT17 and MOT20
- Fix check for valid class-IDs in the AnnotationClassMapper

4.0.1 (2022-08-03):
------------------
- Implemented a simple input data splitter and removed sklearn as dependency

4.0.0 (2022-08-02):
------------------
- Remove all tools and utility functions not intended to be used by other subprojects. Those will instead comprise another separate
  subproject "mlcvzoo-util" decoupling their development from -base
- Fix width/height confusion bug in CVAT Annotation Parser
- The "Net" class functionality is now built-in in "NetBased" and was removed
- The AnnotationClassMapper is now part of the MLCVZoo API package
- The AnnotationHandler now uses a ClassMapper to enable reduction mapping application during annotation parsing
- Major refactoring involving fixing the differing naming schemes of files and classes and moving some parts into
  more appropriate packages
- All Box objects of annotations are now checked on construction time. This prints a warning, as
  a grace period, before, instead of just the faulty bounding boxes, the entire offending
  annotation will be skipped in future version.
- Repair tensorboard logging

3.5.0 (2022-07-19):
------------------
Add ModelTimer tool for benchmarking the inference time of models.

3.4.0 (2022-07-19):
------------------
Refactor the mlcvzoo-preannotator:
- Don't use the cvat_annotation_handler directly, but add a dedicated module
  "PreAnnotationTool" which utilizes the cvat_annotation_handler functionality
- Besides handling the cvat_annotation_handler features, the PreAnnotationTool
  allows to run an Object Detector on top of the images defined by the configured CVAT tasks
- Provide the old functionality of the mlcvzoo-preannotator via the mlcvzoo-cvat-handler

3.3.0 (2022-07-18):
------------------
Add Feature to ReadFromFileModel: Allow to predict on images

3.2.1 (2022-07-11):
------------------
Prepare package for PyPi

3.2.0 (2022-06-30):
------------------
Add API feature: predict on many data-items

3.1.1 (2022-06-28):
------------------
Minor fixes and improvements of the CVATAnnotationHandler tool:
- Fix behavior of pre-clean up
- Improve gathering of xml files for the zip file that is created for the upload to CVAT

3.1.0 (2022-06-14):
------------------
Add cvat-annotation-handler tool that allows to download and upload CVAT tasks by utilizing
the commandline-interface of CVAT

3.0.0 (2022-05-16):
------------------
Refactor the mapping of class IDs/names via the AnnotationClassMapper:
- Add feature that enables the reduction / aggregation / redefinition of model class IDs/names
- Implement dedicated methods for mapping class IDs/names that have to be used
  from subprojects (mlcvzoo_yolox, mlcvzoo_mmdetection, etc.)

2.0.0 (2022-04-05)
------------------
- initial release of the package
