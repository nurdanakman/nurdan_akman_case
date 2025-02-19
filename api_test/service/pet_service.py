import sys
import os
import random

import pytest
import requests

from api_test.api_config import BackendConfig
from api_test.utils.logger import get_logger
from api_test.models.PetInfo import Pet, StatusTypes, Details


class PetService:
    def __init__(self):
        self.project_url = BackendConfig.API_BASE_URL
        self.headers = {"Content-Type": "application/json"}
        self.logger = get_logger()


    def create_pet_and_resp(self):
        # arrange
        pet_data = self.generate_random_pet_data().model_dump()

        # act
        response = requests.post(self.project_url, json=pet_data, headers=self.headers)
        self.logger.info(f"Create Pet Response: {response.status_code} - {response.json()}")
        return response, pet_data


    def create_pet(self, pet_data: dict) -> requests.Response:
        response = requests.post(self.project_url, json=pet_data, headers=self.headers)
        self.logger.info(f"Create Pet Response: {response.status_code} - {response.json()}")
        return response


    def get_pet(self, pet_id):
        response = requests.get(f"{self.project_url}{pet_id}")
        self.logger.info(f"Get Pet Response: {response.status_code} - {response.json()}")
        return response


    def update_pet(self, pet):
        response = requests.put(f"{self.project_url}", json=pet)
        self.logger.info(f"Update Pet Response: {response.status_code} - {response.json()}")
        return response


    def update_pet_with_form_data(self, pet_id: int, name: str = None, status: str = None):
        url = f"{self.project_url}{pet_id}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {}
        if name is not None:
            data["name"] = name
        if status is not None:
            data["status"] = status
        response = requests.post(url, data=data, headers=headers)
        self.logger.info(f"Update Pet with Form Data Response: {response.status_code} - {response.text}")
        return response


    def find_pet_by_status(self, status: str):
        url = f"{self.project_url}findByStatus"
        params = {"status": status}
        response = requests.get(url, params=params)
        self.logger.info(f"Find Pet by Status Response: {response.status_code} - {response.text}")
        return response


    def upload_pet_image(self, pet_id: int, file_path: str, additional_metadata: str = ""):
        url = f"{self.project_url}{pet_id}/uploadImage"
        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {"additionalMetadata": additional_metadata}
            response = requests.post(url, files=files, data=data)
        self.logger.info(f"Upload Pet Image Response: {response.status_code} - {response.text}")
        return response


    def delete_pet(self, pet_id):
        response = requests.delete(f"{self.project_url}{pet_id}")
        self.logger.info(f"Delete Response: {response.status_code}")
        return response


    def generate_random_pet_data(self):
        pet_id = random.randint(1000, 9999)

        possible_categories = [
            {"id": random.randint(1, 10), "name": "Dogs"},
            {"id": random.randint(1, 10), "name": "Cats"},
            {"id": random.randint(1, 10), "name": "Birds"}
        ]
        category = random.choice(possible_categories) if random.choice([True, False]) else None
        category_data = Details(**category) if category is not None else None

        pet_names = ["Buddy", "Max", "Charlie", "Bella", "Lucy", "Molly"]
        name = random.choice(pet_names)

        photo_url = f"https://example.com/photos/{random.randint(1, 100)}.jpg"
        photo_urls = [photo_url] if random.choice([True, False]) else []

        possible_tags = [
            {"id": random.randint(1, 10), "name": "Friendly"},
            {"id": random.randint(1, 10), "name": "Energetic"},
            {"id": random.randint(1, 10), "name": "Cute"}
        ]
        tags = random.choice(possible_tags) if random.choice([True, False]) else None
        tags_data = [Details(**tags)] if tags is not None else []

        status = random.choice(list(StatusTypes)).value

        pet_instance = Pet(
            id=pet_id,
            category=category_data,
            name=name,
            photoUrls=photo_urls,
            tags=tags_data,
            status=status
        )

        return pet_instance
