tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "find_restaurants",
            "description": "Find restaurants based on city, cuisine, and seat requirement.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "cuisine": {"type": "string"},
                    "seats_required": {"type": "integer"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "make_reservation",
            "description": "Book a table at a restaurant.",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_name": {"type": "string"},
                    "user_name": {"type": "string"},
                    "time": {"type": "string"}
                },
                "required": ["restaurant_name", "user_name", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_reservation",
            "description": "Cancel an existing reservation by reservation ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reservation_id": {"type": "string"}
                },
                "required": ["reservation_id"]
            }
        }
    }
]


