import requests
import json

def list_datasets(api_key):
    """
    List all datasets
    :param api_key: The API key of the user
    :return: The list of dataset of the user
    """
    base_url = "https://api-infer.thya-technology.com/api/v1"
    url = f"{base_url}/datasets/all"
    
    headers = {
        'accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json',
    }

    data = {
        'page': 1,
        'size': 1000,
        'sortBy': 'id',
        'sortOrder': 'ASC',
        'search': ''
    }

    response = requests.post(url, headers=headers, json=data)

    return json.loads(response.text)


def create_dataset(api_key,
                name, #string # The name of the dataset.
                description, #string # A detailed description of the dataset.
                tagIds=None, #array # An array of IDs representing existing tags in the system database.
                projectIds=None, #array # Link the dataset to multiple projects by their IDs. The user must have the appropriate role to perform this action.
                fee=0, # number #A positive number representing the fee associated with the dataset.
                newTags=None, #object # Create new tags and associate them with the dataset. Tag names should be unique and non-existing in the system database.
                image=None, #file # The cover image of the dataset.
        ):
    """
    create a dataset
    :param api_key: The API key of the user
    :param name: The name of the dataset.
    :param description: A detailed description of the dataset.
    :param tagIds: An array of IDs representing existing tags in the system database.
    :param projectIds: Link the dataset to multiple projects by their IDs. The user must have the appropriate role to perform this action.
    :param fee: A positive number representing the fee associated with the dataset.
    :param newTags: Create new tags and associate them with the dataset. Tag names should be unique and non-existing in the system database.
    :param image: The cover image of the dataset.
    :return: The list of dataset of the user
    """

    base_url = "https://api-infer.thya-technology.com/api/v1"
    url = f"{base_url}/datasets"
    
    headers = {
        'accept': 'application/json',
        'x-api-key': api_key,
        # 'Content-Type': 'application/json',
    }
    data = {
        'name': 'name',
        'description': 'desc',
        'tagIds': '',
        'projectIds': '',
        'fee': fee,
        'newTags': '[]',
    }
    files = {
        'image': (None, ''),
    }

    response = requests.post(url, headers=headers, data=data, files=files)


    return json.loads(response.text)

def delete_dataset(api_key, dataset_id):
    """
    Delete a dataset
    :param api_key: The API key of the user
    :param dataset_id: The dataset id
    :return: The response from the server
    """
    headers = {
        'accept': '*/*',
        'x-api-key': api_key,
    }
    base_url = "https://api-infer.thya-technology.com/api/v1"
    url = f"{base_url}/datasets/{dataset_id}"
    response = requests.delete(url=url,headers=headers)
    return json.loads(response.text)


def get_dataset_info(api_key, dataset_id):
    """
    get information about a dataset
    :param api_key: The API key of the user
    :param dataset_id: The dataset id
    :return: The response from the server
    """
    headers = {
        'accept': '*/*',
        'x-api-key': api_key,
    }
    base_url = "https://api-infer.thya-technology.com/api/v1"
    url = f"{base_url}/datasets/{dataset_id}"
    response = requests.request("GET", url=url, headers=headers)
    return json.loads(response.text)


def upload_image(dataset_id, api_key, image_path, anno=None):
    """
    Uploads an image to a dataset
    :param dataset_id: The dataset id
    :param api_key: The API key of the user
    :param image_path: The path to the image
    :param anno: dictionary with annotations
    :return: The response from the server
    """
    headers = {
        'x-api-key': api_key,
    }
    files = {
        'file': (image_path, open(image_path, 'rb'), 'image/jpeg'),
    }
    if anno is not None:
        files['jsonText'] = (None, json.dumps(anno), 'application/json')
        
    base_url = "https://api-infer.thya-technology.com/api/v1"
    url = f"{base_url}/datasets/{dataset_id}/images"
    response = requests.request("POST",
                                url=url,
                                headers=headers,
                                files=files)
    return json.loads(response.text)



if __name__ == "__main__":
    # define argparser
    import argparse
    parser = argparse.ArgumentParser()

    # # Test listing datasets
    # parser.add_argument("--api_key", type=str, required=True)
    # args = parser.parse_args()
    # datasets = list_datasets(args.api_key)
    # for dataset in datasets["body"]["data"]:
    #     print(dataset["id"], dataset["name"])


    # # Test creating dataset
    # parser.add_argument("--api_key", type=str, required=True)
    # parser.add_argument("--name", type=str, required=True)
    # parser.add_argument("--description", type=str, required=True)
    # args = parser.parse_args()
    # response = create_dataset(args.api_key, args.name, args.description)
    # print(response)


    # # Test deleting dataset
    # parser.add_argument("--api_key", type=str, required=True)
    # parser.add_argument("--dataset_id", type=int, required=True)
    # args = parser.parse_args()
    # response = delete_dataset(args.api_key, args.dataset_id)
    # print(response)

        
    # Test upload images
    parser.add_argument("--api_key", type=str, required=True)
    parser.add_argument("--dataset_id", type=int, required=True)
    parser.add_argument("--image_path", type=str, required=True)
    args = parser.parse_args()
    response = upload_image(args.dataset_id, args.api_key, args.image_path)
    print(response)
        