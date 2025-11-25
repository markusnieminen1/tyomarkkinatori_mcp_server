from httpx import AsyncClient
from json import load as jload
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.logging import get_logger
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import logging

# CONSTANTS
API_URL = "https://tyomarkkinatori.fi/api/jobpostingfulltext/search/v1/search"

# PATHS
OCCUPATIONS_HIGH_LEVEL_FILE = Path(__file__).resolve().parent.parent / "data" / "ammatit_taso_1.json"
OCCUPATIONS_MEDIUM_LEVEL_FILE = Path(__file__).resolve().parent.parent / "data" / "ammatit_taso_2.json"
OCCUPATIONS_LOW_LEVEL_FILE = Path(__file__).resolve().parent.parent / "data" / "ammatit_taso_3.json"
OCCUPATIONS_LEVEL4_FILE = Path(__file__).resolve().parent.parent / "data" / "ammatit_taso_4.json"
MUNICIPALITIES_FILE= Path(__file__).resolve().parent.parent / "data" / "kunnat.json"
#LOG_PATH = Path(__file__).resolve().parent / "tyomarkkinatori_mcp.log"

# Server side logging
logging.basicConfig(level=logging.INFO, force=True, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = get_logger(__name__)

mcp = FastMCP(name="tyomarkkinatori")

# Assert necessary files exists
def assertFilesAndStructure(fileLocation: Path, keys: list = ["code", "preferredLabel"]):
    with fileLocation.open("r", encoding="utf-8") as f:
        key_values = jload(f)[0].keys()
        assert set(keys).issubset(key_values), f"{fileLocation} missing required keys"
for file, keys in [
    (OCCUPATIONS_HIGH_LEVEL_FILE, ["code", "preferredLabel"]),
    (OCCUPATIONS_MEDIUM_LEVEL_FILE, ["code", "preferredLabel"]),
    (OCCUPATIONS_LOW_LEVEL_FILE, ["code", "preferredLabel"]),
    (OCCUPATIONS_LEVEL4_FILE, ["code", "preferredLabel"]),
    (MUNICIPALITIES_FILE, ["code", "classificationName"])]:
    try:
        assertFilesAndStructure(fileLocation=file, keys=keys)
    except AssertionError:
        logger.error(f"Assertion error in resource file: {file}")
        raise AssertionError

def try_block_decorator(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            return {
                "isError": True,
                "content": [{
                    "type": "text",
                    "text": f"Tool failed. {e}"
                }]
            }
    return wrapper

 

def read_file_contents_tojson(filelocation: Path) -> list:
    """
    Reads file contents from a file and returns it with json.load()
    Args:
        filelocation (Path): Path to the JSON resource
    Returns:
        list: The JSON content loaded from the file. Assumes the top-level JSON structure is a list.

    """
    logger.info(f'reading {filelocation}')
    with open(file=filelocation, mode="r", encoding="utf-8") as f:
        return jload(f)


@mcp.tool()
@try_block_decorator
def get_location_codes(first_letters_of_the_city: str) -> list:
    """Get location codes for the api call. Use text to narrow down the search (and to waste less context)
    Only Finnish city names are included.
    Args:
        first_letters_of_the_city (str): "Helsinki" or "Vaasa" or "Hel" or "Tur"... 
    Returns:
        list: returns a list of the results. The list can be empty or contain JSON objects. 
    """
    def normalise(text : str):
        return text.lower()
    
    # In case of an empty input 
    if len(first_letters_of_the_city) < 1:
        logger.warning(f'get_location_codes: empty input')
        return []
    
    json_contents = read_file_contents_tojson(filelocation=MUNICIPALITIES_FILE)
    json_parsed = []
    for i in json_contents:
        if normalise(i["classificationName"][:len(first_letters_of_the_city)]) == normalise(first_letters_of_the_city):
            # Include cities that matches the criteria ("turku"[:3] == "tur") == True
            json_parsed.append(i)
        
    return json_parsed
    
    
@mcp.tool()
@try_block_decorator
def get_all_high_level_occupation_codes() -> list:
    """Returns all high level occupation codes. 
    Can be used for the API call or for getting medium level occupation codes. 

    Returns:
        list: list that contains all high level occupation categories and the related codes. 
    """
    return read_file_contents_tojson(OCCUPATIONS_LOW_LEVEL_FILE)


@mcp.tool()
@try_block_decorator
def get_medium_level_occupation_codes(high_level_code: int|str) -> list:
    """
    Returns medium level occupational category codes for the API call. 
    Generally using these codes will result in medium amount of results. 
    Uses high level code as a base criteria for the search.
    Args:
        high_level_code (int | str): 1 min - 9 max. Can be "str" int. 
    Raises:
        ValueError: Raises value error if the number does not fall within the range.
        e: Except never to be excepted
    Returns:
        list: If the function does not raise an error, it will return a list. 
        The list will have items as long as the input list is not altered. 
    """
    
    try:
        number = int(high_level_code)
        if not 0 < number < 10 :
            logger.error("Input error in get_medium_level_occupation_codes.")
            raise ValueError
        
    except Exception as e:
        logger.error(f"Something went wrong in get_medium_level_occupation_codes. {e}")
        raise e
    
    codes = read_file_contents_tojson(OCCUPATIONS_MEDIUM_LEVEL_FILE)
    return_list = []
    
    for i in codes:
        if int(i["code"][:1]) == number:
            return_list.append(i)

    return return_list


@mcp.tool()
@try_block_decorator
def get_low_level_occupation_codes(medium_level_code: int|str) -> list:
    
    """
    Returns low level occupational category codes for the API call. 
    Generally using these codes will result in lower amount of results from API call.
    Uses medium level code as a base criteria for the search.
    Args:
        high_level_code (int | str): 10 min - 99 max. Can be "str" int. 
    Raises:
        ValueError: Raises value error if the number does not fall within the range.
        e: Except never to be excepted
    Returns:
        list: If the function does not raise an error, it will return a list. 
        The list might be empty. 
    """
    
    try:
        number = int(medium_level_code)
        if not 9 < number < 100 :            
            logger.error("Input error in get_low_level_occupation_codes.")
            raise ValueError
        
    except Exception as e:
        logger.error(f"Something went wrong in get_medium_level_occupation_codes. {e}")
        raise e
    
    
    codes = read_file_contents_tojson(OCCUPATIONS_LOW_LEVEL_FILE)
    return_list = []
    for i in codes:
        if i["code"][:2] == str(medium_level_code):
            return_list.append(i)

    return return_list


class API_call(BaseModel):
    municipalities: list[int|str] = Field(default=[], min_length=0, max_length=10, description="list of the municipality numbers.")
    occupations: list[int|str] = Field(default=[], min_length=0, max_length=10, description="list of the occupations numbers.")


@mcp.tool()
@try_block_decorator
async def api_call(input: API_call):
    """
    Make an API call to the Työmarkkinatori API to receive job listings. 

    Args:
        input (API_call): API_call model containing two lists:
        - municipalities
        - occupations
            
    Notes:
    - Both fields default to empty lists.
    """
    
    def create_request(mun: List[str], isco: List[str]):
        def add_leading_zeros(value: str) -> str:
            return value.zfill(3)

        data = {
            "query": "",
            "paging": {"pageSize": 30, "pageNumber": 0},
            "filters": {
                "publishedAfter": "",
                "closesBefore": "",
                "municipalities": [add_leading_zeros(m) for m in mun],
                "iscoNotations": isco,
                "regions": [],
                "countries": [],
            },
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return headers, data

    async with AsyncClient() as client:
        try:
            municipalities_list = [str(m) for m in input.municipalities]
            occupations_list = [str(o) for o in input.occupations]

            headers, data = create_request(
                mun=municipalities_list, 
                isco=occupations_list
            )
            logger.info('Sending request to API.')
            response = await client.post(
                url=API_URL,
                headers=headers,
                json=data,
                timeout=5.0
            )
            logger.info(f'Response {response.status_code}')
            response.raise_for_status()
            return response.json()

        except Exception as e:
            logger.exception(f"API call failed: {e}")
            raise e


def main():
    logger.info("Server starting...")
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.exception(f"MCP server crashed. {e}")
    finally:
        logger.info("Server shutting down...")


if __name__ == "__main__":
    main()
