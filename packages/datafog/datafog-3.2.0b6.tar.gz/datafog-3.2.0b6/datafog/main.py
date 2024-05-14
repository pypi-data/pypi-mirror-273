import asyncio
import json
from typing import List

import aiohttp

from .config import OperationType
from datafog.processing.image_processing.donut_processor import DonutProcessor
from datafog.processing.text_processing.spacy_pii_annotator import SpacyPIIAnnotator
from datafog.services.image_service import ImageService
from datafog.services.spark_service import SparkService
from datafog.services.text_service import TextService



class DataFog:
    def __init__(self, operations: List[OperationType] = [OperationType.ANNOTATE_PII]):
        self.image_service = ImageService()
        self.text_service = TextService()
        self.spark_service = SparkService()
        self.operations: List[OperationType] = operations

    async def run_ocr_pipeline(self, image_urls: List[str]):
        """Run the OCR pipeline asynchronously."""
        extracted_text = await self.image_service.ocr_extract(image_urls)
        if OperationType.ANNOTATE_PII in self.operations:
            annotated_text = await self.text_service.batch_annotate_texts(
                extracted_text
            )
            return annotated_text
        return extracted_text

    async def run_text_pipeline(self, texts: List[str]):
        """Run the text pipeline asynchronously."""
        if OperationType.ANNOTATE_PII in self.operations:
            annotated_text = await self.text_service.batch_annotate_texts(texts)
            return annotated_text
        return texts


class OCRPIIAnnotator:
    def __init__(self):
        self.spark_processor: SparkService = None
        self.image_service = DonutProcessor()
        self.text_annotator = SpacyPIIAnnotator.create()

    def run(self, image_url, output_path=None):
        try:
            # Download and process the image to extract text
            downloaded_image = self.image_service.download_image(image_url)
            extracted_text = self.image_service.parse_image(downloaded_image)

            # Annotate the extracted text for PII
            annotated_text = self.text_annotator.annotate(extracted_text)

            # Optionally, output the results to a JSON file
            if output_path:
                with open(output_path, "w") as f:
                    json.dump(annotated_text, f)

            return annotated_text

        finally:
            # Ensure Spark resources are released
            # self.spark_processor.spark.stop()
            pass


class TextPIIAnnotator:
    def __init__(self):
        self.text_annotator = SpacyPIIAnnotator.create()
        self.spark_processor: SparkService = None

    def run(self, text, output_path=None):
        try:
            annotated_text = self.text_annotator.annotate(text)

            # Optionally, output the results to a JSON file
            if output_path:
                with open(output_path, "w") as f:
                    json.dump(annotated_text, f)

            return annotated_text

        finally:
            # Ensure Spark resources are released
            pass
