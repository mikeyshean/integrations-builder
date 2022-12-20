from mappers.models import FieldTypeChoices


class MappingRepository:
    def __init__(self):
        self.remote_data = {
            "m1": {
                "id": "m1",
                "model_name": "Employee",
                "target_model_id": "t1",
                "fields": [
                    {
                        "id": "f1",
                        "name": "id",
                        "type": FieldTypeChoices.NUMBER,
                        "list_item_type": None,
                        "object_model_id": None,
                        "choices": None,
                        "target_field_id": "tf-1",
                    },
                    {
                        "id": "f2",
                        "name": "first_name",
                        "type": FieldTypeChoices.STRING,
                        "list_item_type": None,
                        "object_model_id": None,
                        "choices": None,
                        "target_field_id": "tf-2",
                    },
                    {
                        "id": "f3",
                        "name": "last_name",
                        "type": FieldTypeChoices.STRING,
                        "list_item_type": None,
                        "object_model_id": None,
                        "choices": None,
                        "target_field_id": "tf-3",
                    },
                    {
                        "id": "f4",
                        "name": "date_of_birth",
                        "type": FieldTypeChoices.STRING,
                        "datetime_format": "%Y-%M-%DT%H:%M:%SZ",
                        "list_item_type": None,
                        "object_model_id": None,
                        "choices": None,
                        "target_field_id": "tf-4",
                    },
                    {
                        "id": "f5",
                        "name": "skills",
                        "type": FieldTypeChoices.ARRAY,
                        "list_item_type": FieldTypeChoices.OBJECT,
                        "object_model_id": "m2",
                        "choices": None,
                        "target_field_id": "tf-5",
                    },
                    {
                        "id": "f6",
                        "name": "jobs",
                        "type": FieldTypeChoices.ARRAY,
                        "list_item_type": FieldTypeChoices.STRING,
                        "object_model_id": None,
                        "choices": None,
                        "target_field_id": "tf-6",
                    },
                    {
                        "id": "f7",
                        "name": "address",
                        "type": FieldTypeChoices.OBJECT,
                        "list_item_type": None,
                        "object_model_id": "m3",
                        "choices": None,
                        "target_field_id": "tf-7",
                    },
                    {
                        "id": "f8",
                        "name": "gender",
                        "type": FieldTypeChoices.STRING,
                        "choices": ["MALE", "FEMALE"],
                        "list_item_type": None,
                        "object_model_id": None,
                        "target_field_id": "tf-8",
                    },
                ],
            },
            "m2": {
                "id": "m2",
                "model_name": "Skill",
                "fields": [
                    {
                        "id": "f9",
                        "name": "id",
                        "type": FieldTypeChoices.STRING,
                        "choices": None,
                        "list_item_type": None,
                        "object_model_id": None,
                        "target_field_id": "tf-9",
                    },
                    {
                        "id": "f10",
                        "name": "name",
                        "type": FieldTypeChoices.STRING,
                        "choices": None,
                        "list_item_type": None,
                        "object_model_id": None,
                        "target_field_id": "tf-10",
                    },
                ],
            },
            "m3": {
                "id": "m3",
                "model_name": "Location",
                "fields": [
                    {
                        "id": "f11",
                        "name": "id",
                        "type": FieldTypeChoices.STRING,
                        "choices": None,
                        "list_item_type": None,
                        "object_model_id": None,
                        "target_field_id": "tf-11",
                    },
                    {
                        "id": "f12",
                        "name": "street",
                        "type": FieldTypeChoices.STRING,
                        "choices": None,
                        "list_item_type": None,
                        "object_model_id": None,
                        "target_field_id": "tf-12",
                    },
                ],
            },
        }

        self.target_data = {
            "tm-1": {
                "id": "tm-1",
                "model_name": "TargetEmployee",
                "fields": [
                    {
                        "id": "tf-1",
                        "name": "target_id",
                        "type": FieldTypeChoices.NUMBER,
                        "list_item_type": None,
                        "object_model_id": None,
                        "choices": None,
                    },
                    {
                        "id": "tf-2",
                        "name": "target_first_name",
                        "type": FieldTypeChoices.STRING,
                        "list_item_type": None,
                        "object_model_id": None,
                        "choices": None,
                    },
                    {
                        "id": "tf-3",
                        "name": "target_last_name",
                        "type": FieldTypeChoices.STRING,
                        "list_item_type": None,
                        "object_model_id": None,
                        "choices": None,
                    },
                    {
                        "id": "tf-4",
                        "name": "target_date_of_birth",
                        "type": "DATETIME",
                        "datetime_format": "%Y-%M-%DT%H:%M:%SZ",
                        "list_item_type": None,
                        "object_model_id": None,
                        "choices": None,
                    },
                    {
                        "id": "tf-5",
                        "name": "target_skills",
                        "type": FieldTypeChoices.ARRAY,
                        "list_item_type": FieldTypeChoices.OBJECT,
                        "object_model_id": "tm-2",
                        "choices": None,
                    },
                    {
                        "id": "tf-6",
                        "name": "target_jobs",
                        "type": FieldTypeChoices.ARRAY,
                        "list_item_type": FieldTypeChoices.STRING,
                        "object_model_id": None,
                        "choices": None,
                    },
                    {
                        "id": "tf-7",
                        "name": "target_address",
                        "type": FieldTypeChoices.OBJECT,
                        "list_item_type": None,
                        "object_model_id": "tm-3",
                        "choices": None,
                    },
                    {
                        "id": "tf-8",
                        "name": "target_gender",
                        "type": FieldTypeChoices.STRING,
                        "choices": ["MALE", "FEMALE"],
                        "list_item_type": None,
                        "object_model_id": None,
                    },
                ],
            },
            "tm-2": {
                "id": "tm-2",
                "model_name": "TargetSkill",
                "fields": [
                    {
                        "id": "tf-9",
                        "name": "target_id",
                        "type": FieldTypeChoices.STRING,
                        "choices": None,
                        "list_item_type": None,
                        "object_model_id": None,
                    },
                    {
                        "id": "tf-10",
                        "name": "target_name",
                        "type": FieldTypeChoices.STRING,
                        "choices": None,
                        "list_item_type": None,
                        "object_model_id": None,
                    },
                ],
            },
            "tm-3": {
                "id": "tm-3",
                "model_name": "TargetLocation",
                "fields": [
                    {
                        "id": "tf-11",
                        "name": "target_id",
                        "type": FieldTypeChoices.STRING,
                        "choices": None,
                        "list_item_type": None,
                        "object_model_id": None,
                    },
                    {
                        "id": "tf-12",
                        "name": "target_street",
                        "type": FieldTypeChoices.STRING,
                        "choices": None,
                        "list_item_type": None,
                        "object_model_id": None,
                    },
                ],
            },
        }

        self.target_fields = self._create_target_fields()
        self.remote_fields = self._create_remote_fields()

    def _create_target_fields(self):
        result = {}
        for _, target_model in self.target_data.items():
            for field in target_model["fields"]:
                result[field["id"]] = field

        return result

    def _create_remote_fields(self):
        result = {}
        for _, remote_model in self.remote_data.items():
            for field in remote_model["fields"]:
                result[field["id"]] = field

        return result

    def get_remote_model_by_id(self, id: str):
        return self.remote_data[id]

    def get_target_field_by_id(self, id: str):
        return self.target_fields[id]

    def get_remote_field_by_id(self, id: str):
        return self.remote_fields[id]
