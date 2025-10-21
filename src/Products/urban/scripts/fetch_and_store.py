import requests
import json

def fetch_and_store_data(url, storage_path):
    """
    Fetch data from the given URL and store it as JSON in a local file.
    """
    try:
        response = requests.get(url, headers={"Accept": "application/json"})
        response.raise_for_status()
        data = response.json()

        with open(storage_path, 'w') as f:
            json.dump(data, f, indent=2)

        return "Saved JSON data to "
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching data: {e}",e)
    except IOError as e:
        print("An error occurred while writing to file: {e}")


if __name__ == "__main__":   
    """
    Example usage of fetch_and_store_data function. 
    """
    #url = 'https://permis-environnement.spw.wallonie.be/home/ressources/choix-des-rubriques/pagecontent/liste-tabulaire/recherche-libre/recherche-libre.searchRubrics.do?code=&expression=&type=all&active=true' 
    url = "https://permis-environnement.spw.wallonie.be/modules/permis-environnement-environmentalLicence/javascript/json/environmentalLicence_fr-FR.json"
    storage_path = 'src/Products.urban/src/Products/urban/profiles/extra/rubrics1.json'
    result = fetch_and_store_data(url, storage_path)
    print(result)    
