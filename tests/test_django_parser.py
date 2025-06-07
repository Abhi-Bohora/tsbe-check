# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from tsbe_check.django_parser import extract_model_fields


def test_extract_model_fields(temp_django_model):
    fields = extract_model_fields(temp_django_model)

    assert "EventModel" in fields
    event_fields = fields["EventModel"]

    # Check that all non-private fields are extracted
    assert "title" in event_fields
    assert "description" in event_fields
    assert "date" in event_fields
    assert "is_active" in event_fields
    assert "organizer" in event_fields
    assert "participants" in event_fields

    # Check that private fields are ignored
    assert "_private_field" not in event_fields


def test_extract_model_fields_with_invalid_syntax(tmp_path):
    invalid_model = tmp_path / "invalid_model.py"
    invalid_model.write_text("this is not valid python syntax")

    with pytest.raises(SyntaxError):
        extract_model_fields(str(invalid_model))


def test_extract_model_fields_with_empty_file(tmp_path):
    empty_file = tmp_path / "empty.py"
    empty_file.write_text("")

    fields = extract_model_fields(str(empty_file))
    assert fields == {}
