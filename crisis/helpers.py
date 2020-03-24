import uuid


def generate_username_with_user_data(user_data):
    user_name_str = ""
    if user_data["first_name"]:
        user_first_name = user_data["first_name"].replace(" ", "_")
        user_name_str = f"{user_first_name}"
    if user_data["last_name"]:
        user_last_name = user_data["last_name"].replace(" ", "_")
        user_name_str = f"{user_name_str}_{user_last_name}"

    if not len(user_name_str):
        user_name_str = uuid.uuid4().hex[:10]
    else:
        user_name_str = f"{user_name_str}_{uuid.uuid4().hex[:3]}"

    return user_name_str
