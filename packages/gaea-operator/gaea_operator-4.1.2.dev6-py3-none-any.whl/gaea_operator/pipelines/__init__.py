#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__init__.py
"""
from gaea_operator.pipelines.ocrnet_pipeline.pipeline import pipeline as ocrnet_pipeline
from gaea_operator.pipelines.ppyoloe_plus_pipeline.pipeline import pipeline as ppyoloe_plus_pipeline
from gaea_operator.pipelines.resnet_pipeline.pipeline import pipeline as resnet_pipeline
from gaea_operator.pipelines.change_ppyoloe_plus_pipeline.pipeline import pipeline as change_ppyoloe_plus_pipeline
from gaea_operator.pipelines.change_ocrnet_pipeline.pipeline import pipeline as change_ocrnet_pipeline

category_to_ppls = {
    "Image/SemanticSegmentation": [ocrnet_pipeline],
    "Image/ObjectDetection": [ppyoloe_plus_pipeline],
    "Image/ImageClassification/MultiClass": [resnet_pipeline],
    "Image/ChangeDetection/ObjectDetection": [change_ppyoloe_plus_pipeline],
    "Image/ChangeDetection/SemanticSegmentation": [change_ocrnet_pipeline]
}
