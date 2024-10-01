from flask import Blueprint, request
from app.areas.schema import AreasSchema
from app.numbers.model import Numbers
from app.areas.model import Areas
from app.ussd.model import Ussd

bp = Blueprint('ussd', __name__)

ITEMS_PER_PAGE = 8

@bp.post('/ussd')
def listen_to_ussd():
    serviceCode = request.form.get('serviceCode')
    phone = request.form.get('phoneNumber')
    session_id = request.form.get('sessionId')
    networkCode = request.form.get('networkCode')
    selection = request.form.get('text')
    number = Numbers.get_by_phone(phone)
    if not number:
        number = Numbers.create(phone, 'english', None)  # Create without area_id and default language
    session = Ussd.get_by_session_id(session_id)
    if session:
        if selection.split('*')[-1] == '0':
            return globals()[session.previous](selection=selection, session_id=session_id, number=number)
        return globals()[session.stage](selection=selection, session_id=session_id, number=number)
    return start(selection=selection, session_id=session_id, number=number)

def start(**kwargs):
    number = kwargs['number']
    if number.area_id is None:
        return update_user_area(**kwargs)  # Force area selection if not set
    if number.is_set:
        Ussd.create_or_update(kwargs['session_id'], 'select_service', previous='start')
        response = f"CON Welcome back. What do you want to do today?\n"
        response += "1. Update your area\n"
        response += "2. Update your language\n"
    else:
        Ussd.create_or_update(kwargs['session_id'], 'select_service', previous='start')
        response = f"CON Welcome to ConnectED.\n"
        response += "1. Set your area\n"
        response += "2. Set your language\n"
    return response

def select_service(**kwargs):
    text = kwargs['selection'].split('*')[-1]
    number = kwargs['number']
    if text == '1':
        Ussd.create_or_update(kwargs['session_id'], 'update_user_area', previous='start')
        return update_user_area(**kwargs)
    elif text == '2':
        Ussd.create_or_update(kwargs['session_id'], 'update_user_language', previous='start')
        return update_user_language(**kwargs)

def update_user_area(**kwargs):
    response = "CON Select your area:\n"
    response += "1. List areas\n"
    response += "2. Search for area\n"
    response += "11. Main menu"
    Ussd.create_or_update(kwargs['session_id'], 'handle_area_selection', previous='start,1')
    return response

def handle_area_selection(**kwargs):
    selection = kwargs['selection'].split('*')[-1]
    if selection == '1':
        return list_areas(page=1, **kwargs)
    elif selection == '2':
        return search_area_prompt(**kwargs)
    elif selection == '11':
        Ussd.create_or_update(kwargs['session_id'], 'select_service', previous='update_user_area')
        return start(**kwargs)
    else:
        return "END Invalid selection. Please try again."

def list_areas(page, **kwargs):
    areas = Areas.get_all()
    start_index = (page - 1) * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    current_page_areas = areas[start_index:end_index]

    response = "CON Select your area:\n"
    for i, area in enumerate(current_page_areas, 1):
        response += f"{i}. {area.name}\n"

    if end_index < len(areas):
        response += "9. Next page\n"
    if page > 1:
        response += "0. Previous page\n"
    response += "10. Go back"

    Ussd.create_or_update(kwargs['session_id'], 'process_area_selection', previous=f'update_user_area,{page}')
    return response

def process_area_selection(**kwargs):
    selection = kwargs['selection'].split('*')[-1]
    session = Ussd.get_by_session_id(kwargs['session_id'])
    
    previous_parts = session.previous.split(',')
    current_page = int(previous_parts[1]) if len(previous_parts) > 1 else 1

    if selection == '9':
        return list_areas(page=current_page + 1, **kwargs)
    elif selection == '0':
        return list_areas(page=max(1, current_page - 1), **kwargs)
    elif selection == '10':
        Ussd.create_or_update(kwargs['session_id'], 'update_user_area', previous='start')
        return update_user_area(**kwargs)
    else:
        try:
            area_index = (current_page - 1) * ITEMS_PER_PAGE + int(selection) - 1
            areas = Areas.get_all()
            
            if 0 <= area_index < len(areas):
                selected_area = areas[area_index]
                return do_update_user_area(selected_area, **kwargs)
            else:
                return "END Invalid area selection. Please try again."
        except Exception as e:
            return f"END An error occurred: {str(e)}. Please try again."

def search_area_prompt(**kwargs):
    response = "CON Enter the first 3-5 letters of your area name:"
    Ussd.create_or_update(kwargs['session_id'], 'process_area_search', previous='update_user_area')
    return response

def process_area_search(**kwargs):
    search_term = kwargs['selection'].split('*')[-1].lower()
    if len(search_term) < 3:
        return "CON Please enter at least 3 letters to search."

    areas = Areas.get_all()
    matching_areas = [area for area in areas if area.name.lower().startswith(search_term)]

    if not matching_areas:
        return "END No matching areas found. Please try again."

    response = "CON Select your area:\n"
    for i, area in enumerate(matching_areas[:ITEMS_PER_PAGE], 1):
        response += f"{i}. {area.name}\n"

    if len(matching_areas) > ITEMS_PER_PAGE:
        response += f"{ITEMS_PER_PAGE + 1}. More results\n"

    Ussd.create_or_update(kwargs['session_id'], 'process_search_selection', previous='search_area_prompt')
    Ussd.create_or_update(kwargs['session_id'], 'process_search_selection', previous=','.join([str(area.id) for area in matching_areas]))
    return response

def process_search_selection(**kwargs):
    selection = kwargs['selection'].split('*')[-1]
    search_results = Ussd.get_by_session_id(kwargs['session_id']).previous.split(',')
    # print("Search result: ",search_results)
    
    if selection == str(ITEMS_PER_PAGE + 1):
        # print("No selection was made")
        return "END Feature not implemented. Please try a more specific search."
    
    try:
        # print("Area was selected", search_results, selection)
        selected_area_id = int(search_results[int(selection) - 1])
        # print("selected area id: ", selected_area_id)
        selected_area = Areas.get_by_id(selected_area_id)
        # print("selected area: ", selected_area)
        return do_update_user_area(selected_area, **kwargs)
    except (ValueError, IndexError):
        return "END Invalid selection. Please try again."

def do_update_user_area(selected_area, **kwargs):
    number = kwargs['number']
    # print("number details: ", number)
    # print("Selected area: ", selected_area)
    number.update(number=number.number, language=number.language, area_id=selected_area.id, is_set=number.is_set)
    if not number.is_set:
        number.update(number=number.number, language=number.language, area_id=selected_area.id, is_set=True)
        response = f"END Your area has been set to {selected_area.name}.\n"
        return update_user_language(**kwargs)
    else:
        response = f"END Your area has been updated to {selected_area.name}."
    Ussd.create_or_update(kwargs['session_id'], 'start', 'start')
    return response

def update_user_language(**kwargs):
    response = "CON Enter your preferred language:\n"
    response +="""
        1. English
        2. Hausa
        3. Igbo
        4. Yoruba
    """
    Ussd.create_or_update(kwargs['session_id'], 'do_update_user_language', 'start')
    return response

def do_update_user_language(**kwargs):
    language_index = kwargs['selection'].split('*')[-1]
    number = kwargs['number']
    language = find_language_by_index(language_index)
    number.update(number=number.number, language=language.lower(), area_id=number.area_id, is_set=number.is_set)
    if not number.is_set:
        number.update(number=number.number, language=language.lower(), area_id=number.area_id, is_set=True)
    Ussd.create_or_update(kwargs['session_id'], 'start', 'start')
    response = f"END Your language has been updated to {language}."
    return response

def find_language_by_index(index: str) -> str:
    languages = [
        "English",
        "Hausa",
        "Igbo",
        "Yoruba"
    ]
    return languages[int(index)-1]