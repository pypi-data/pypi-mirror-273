from marshmallow import Schema, fields


class DataSchema(Schema):
    """Schema for event data entries to ensure expected structure"""

    value = fields.Float(required=True)
    units = fields.Str(required=False, allow_none=True)
