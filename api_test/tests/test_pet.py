import http.client
import os

import pytest

from api_test.service.pet_service import PetService
from api_test.models.PetInfo import Pet

@pytest.fixture
def pet_service_fixture():
    return PetService()

@pytest.fixture
def pet_fixture():
    pet_service = PetService()
    create_rep, sent_data = pet_service.create_pet_and_resp()
    yield create_rep, sent_data
    resp_body = create_rep.json()
    pet_service.delete_pet(resp_body["id"])

@pytest.mark.positive
def test_create_pet(pet_fixture):
    create_rep, sent_data = pet_fixture

    # assert http status
    assert create_rep.status_code == http.client.OK, f"Expected status 200 but got {create_rep.status_code}"

    # Response body validations
    resp_obj = Pet.model_validate(create_rep.json())
    assert resp_obj.model_dump() == sent_data, "Response data does not match the sent pet data"

@pytest.mark.negative
@pytest.mark.parametrize(
    ("invalid_data", "expected_status", "expected_message"),
    [
        (
                {
                    "id": "invalid_id",  # invalid type
                    "category": {"id": 1, "name": "Dogs"},
                    "name": "TestPet",
                    "photoUrls": ["http://example.com/photo"],
                    "tags": [{"id": 1, "name": "tag1"}],
                    "status": "available"
                },
                http.client.INTERNAL_SERVER_ERROR,
                'something bad happened'
        ),
        (
                {
                    "id": 1234,
                    "category": {"id": 1, "name": "Dogs"},
                    "name": "TestPet",
                    "photoUrls": ["http://example.com/photo"],
                    "tags": {"id": 1, "name": "tag1"},   # invalid type, not a list
                    "status": "available"
                },
                http.client.INTERNAL_SERVER_ERROR,
                'something bad happened'
        )
    ]
)
def test_create_pet_negative(invalid_data, expected_status, expected_message, pet_service_fixture):
    # act
    create_resp = pet_service_fixture.create_pet(invalid_data)

    # assert http status
    assert create_resp.status_code == expected_status, (
        f"Expected status {expected_status} but got {create_resp.status_code}"
    )

    # assert response body
    resp_body = create_resp.json()
    actual_message = resp_body.get("message")
    assert actual_message == expected_message, \
        f"Expected error message '{expected_message}' but got '{actual_message}'"


@pytest.mark.positive
def test_get_pet_by_id_positive(pet_fixture, pet_service_fixture):
    create_rep, sent_data = pet_fixture
    resp_body = create_rep.json()
    pet_id = resp_body["id"]

    # act
    get_response = pet_service_fixture.get_pet(pet_id)

    # assert http status
    assert get_response.status_code == 200, f"Expected 200 but got {get_response.status_code}"

    # resp body validations
    get_resp_obj = Pet.model_validate(get_response.json())
    for key, value in sent_data.items():
        assert get_resp_obj.model_dump().get(key) == value, f"Mismatch in field '{key}'"


@pytest.mark.negative
@pytest.mark.parametrize(
    ("invalid_id", "error_code", "error_message", "error_type"),
    [
        (-1, 1, "Pet not found", "error"),  # Negative value
        (0, 1, "Pet not found", "error"), # Boundary value
        (9999999999, 1, "Pet not found", "error"), # Boundary value
        ("invalid_id", 404, 'java.lang.NumberFormatException: For input string: "invalid_id"', "unknown"),  # Different format value
        (None, 404, 'java.lang.NumberFormatException: For input string: "None"', "unknown")  # Empty value
    ]
)
def test_get_pet_by_id_negative(invalid_id, pet_fixture, pet_service_fixture, error_code, error_message, error_type):
    # Act
    get_response = pet_service_fixture.get_pet(invalid_id)

    # assert http status
    assert get_response.status_code == 404, f"Expected 404 but got {get_response.status_code}"

    # response body validations
    get_resp_body = get_response.json()
    expected = {
        'code': error_code,
        'message': error_message,
        'type': error_type
    }
    assert get_resp_body == expected, f"Expected {expected} but got {get_resp_body}"


@pytest.mark.positive
def test_update_pet_positive(pet_fixture, pet_service_fixture):
    create_resp, sent_data = pet_fixture
    pet_data = create_resp.json()

    pet_data["name"] = "UpdatedTestPet"
    pet_data["status"] = "sold"

    # act
    update_resp = pet_service_fixture.update_pet(pet_data)

    # Assert http status
    assert update_resp.status_code == http.client.OK, f"Expected 200 but got {update_resp.status_code}"

    # Validate updated fields
    updated_resp = update_resp.json()
    assert updated_resp["name"] == "UpdatedTestPet", f"Pet name was not updated correctly: {updated_resp['name']}"
    assert updated_resp["status"] == "sold", f"Pet status was not updated correctly:  {updated_resp['status']}"


@pytest.mark.negative
@pytest.mark.parametrize(
    ("update_data", "expected_status", "expected_message"),
    [
        (
                {
                    "id": "invalid_id",  # invalid: should be an integer
                    "category": {"id": 1, "name": "Dogs"},
                    "name": "InvalidPet",
                    "photoUrls": ["http://example.com/photo"],
                    "tags": [{"id": 1, "name": "tag1"}],
                    "status": "available"
                },
                http.client.INTERNAL_SERVER_ERROR,
                'something bad happened'
        ),
        (
                {
                    "id": 1234,
                    "category": {"id": 1, "name": "Dogs"},
                    "name": "InvalidPet",
                    "photoUrls": "not_a_list",  # invalid: should be a list
                    "tags": [{"id": 1, "name": "tag1"}],
                    "status": "available"
                },
                http.client.INTERNAL_SERVER_ERROR,
                'something bad happened'
        )
    ]
)
def test_put_pet_negative(update_data, expected_status, expected_message, pet_service_fixture):
    # act
    update_resp = pet_service_fixture.update_pet(update_data)

    # assert http status
    assert update_resp.status_code == expected_status, \
        f"Expected status {expected_status} but got {update_resp.status_code}"

    # assert response body
    resp_body = update_resp.json()
    actual_message = resp_body.get("message")
    assert actual_message == expected_message, \
        f"Expected error message '{expected_message}' but got '{actual_message}'"


@pytest.mark.positive
def test_update_pet_with_form_data(pet_fixture, pet_service_fixture):
    create_resp, sent_data = pet_fixture
    pet_id = create_resp.json()["id"]

    # act
    new_name = "FormUpdatedPet"
    new_status = "pending"
    update_resp = pet_service_fixture.update_pet_with_form_data(pet_id, name=new_name, status=new_status)

    # assert http status
    assert update_resp.status_code == http.client.OK, (
        f"Expected status 200 but got {update_resp.status_code}: {update_resp.text}"
    )

    # assert response body
    resp_body = update_resp.json()
    assert str(pet_id) in resp_body.get("message", ""), (
        f"Expected pet id {pet_id} in message, got: {resp_body.get('message')}"
    )

    # verify the update via a GET
    get_resp = pet_service_fixture.get_pet(pet_id)
    assert get_resp.status_code == http.client.OK, f"GET pet failed with status {get_resp.status_code}"
    pet_data = get_resp.json()
    assert pet_data["name"] == new_name, f"Expected name '{new_name}' but got '{pet_data['name']}'"
    assert pet_data["status"] == new_status, f"Expected status '{new_status}' but got '{pet_data['status']}'"


@pytest.mark.positive
def test_find_pet_by_status(pet_service_fixture, pet_fixture):
    create_resp, sent_data = pet_fixture
    pet_id = create_resp.json()["id"]

    # update current pet status
    desired_status = "available"
    update_resp = pet_service_fixture.update_pet_with_form_data(pet_id, status=desired_status)
    assert update_resp.status_code == http.client.OK, f"Status update failed with {update_resp.status_code}"

    # assert http status
    find_resp = pet_service_fixture.find_pet_by_status(desired_status)
    assert find_resp.status_code == http.client.OK, (
        f"Expected status 200 but got {find_resp.status_code}: {find_resp.text}"
    )

    # assert response body
    pets = find_resp.json()
    assert isinstance(pets, list), "Expected response to be a list of pets"
    matching = [pet for pet in pets if pet.get("id") == pet_id]
    assert matching, f"Updated pet with id {pet_id} not found in search results for status '{desired_status}'"


@pytest.mark.positive
def test_upload_pet_image(pet_fixture, pet_service_fixture):
    create_resp, _ = pet_fixture
    pet_id = create_resp.json()["id"]
    additional_metadata = "Test upload image"

    # determine the path to test.png relative to the repository
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(base_dir, "test.png")

    # act
    upload_resp = pet_service_fixture.upload_pet_image(pet_id, image_path, additional_metadata)

    # assert http status
    assert upload_resp.status_code == http.client.OK, (
        f"Expected status 200 but got {upload_resp.status_code}: {upload_resp.text}"
    )

    # assert response body
    upload_resp = upload_resp.json()
    assert additional_metadata in upload_resp.get("message", ""), (
        f"Expected metadata '{additional_metadata}' in response message, got: {upload_resp.get('message')}"
    )


@pytest.mark.positive
def test_delete_pet_positive(pet_fixture, pet_service_fixture):
    create_resp, sent_data = pet_fixture
    pet_data = create_resp.json()
    pet_id = pet_data["id"]

    # act
    delete_response = pet_service_fixture.delete_pet(pet_id)

    # assert http status
    assert delete_response.status_code == http.client.OK, f"Expected 200 but got {delete_response.status_code}"

    # verify deletion: subsequent GET should return 404
    get_response = pet_service_fixture.get_pet(pet_id)
    assert get_response.status_code == 404, f"Expected 404 but got {get_response.status_code}"

@pytest.mark.negative
@pytest.mark.parametrize(
    "invalid_id",
    [
        -1,           # Negative value
        999,          # Boundary value
        10000,        # Boundary value
        "invalid_id", # Different format value
        None          # Empty value
    ]
)
def test_delete_pet_negative(invalid_id, pet_fixture, pet_service_fixture):
    # act
    delete_resp = pet_service_fixture.delete_pet(invalid_id)

    # assert http status
    assert delete_resp.status_code == 404, f"Expected 404 but got {delete_resp.status_code}"