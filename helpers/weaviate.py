import os
import weaviate
from weaviate.util import generate_uuid5
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.query import Filter
# from weaviate.classes.config import Property, DataType



weaviate_url = os.environ.get("WEAVIATE_URL")
weaviate_api_key=os.environ.get("WEAVIATE_API_KEY")
openai_api_key=os.environ.get("OPENAI_API_KEY")

# Weaviate client initialization
wv_client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=weaviate.auth.AuthApiKey(weaviate_api_key),
    headers={'X-OpenAI-Api-key':openai_api_key},
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    )
)

def wv_create_class(wv_client, class_name):
    class_obj = {
        "class": class_name,
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            "text2vec-openai": {
                "model": "ada",
                "modelVersion": "002",
                "type": "text"
            },
            "generative-openai": {
                "model": "gpt-3.5-turbo"
            }
        },
    }
    # wv_client.schema.create_class(class_obj)
    wv_client.collections.create(class_obj)
    print(f"Collection {class_name} created successfully")


def wv_upload_doc(wv_client, text, class_name, filename):
    # Create collection if it doesn't exist
    try:
        wv_client.collections.get(class_name)
    except weaviate.exceptions.UnexpectedStatusCodeException:
        schema = {
            "classes": [{
                "class": class_name,
                "vectorizer": "text2vec-openai",
                "moduleConfig": {
                    "text2vec-openai": {
                        "model": "ada",
                        "modelVersion": "002",
                        "type": "text"
                    },
                    "generative-openai": {
                        "model": "gpt-3.5-turbo"
                    }
                },
                "properties": [
                    {"name": "content", "dataType": ["text"]},
                    {"name": "filename", "dataType": ["string"]}
                ]
            }]
        }
        wv_client.collections.create(schema)
    
    # Stream text into Weaviate
    batch_size = 100
    paragraphs = text.split('\n\n')
    
    collection = wv_client.collections.get(class_name)
    
    with collection.batch.dynamic() as batch:
        for i, paragraph in enumerate(paragraphs):
            properties = {
                "content": paragraph,
                "filename": filename
            }
            
            object_uuid = generate_uuid5({
                "paragraph": paragraph,
                "filename": filename
            })
            
            batch.add_object(
                properties,
                # class_name,
                uuid=object_uuid
            )
            
            if i % batch_size == 0:
                print(f"Imported {i} paragraphs...")
    
    print(f"Finished importing {len(paragraphs)} paragraphs.")
    print("Failed objects: ", wv_client.batch.failed_objects)
    print("Failed objects: ", collection.batch.failed_objects)
    print("Failed references: ", collection.batch.failed_references)
    print("Failed references: ", wv_client.batch.failed_references)


def wv_delete_doc(wv_client, class_name, filename):
    try:
        # where_filter = {
        #     "path": ["filename"],
        #     "operator": "Equal",
        #     "valueString": filename
        # }
        collection = wv_client.collections.get(class_name)
        collection.data.delete_many(
            where=Filter.by_property("filename").equal(filename)
        )
        # wv_client.batch.delete_objects(
        #     class_name=class_name,
        #     where=where_filter
        # )
        print(f"Deleted document with filename {filename} from class {class_name}")
    except Exception as e:
        print(f"Error deleting document from Weaviate: {str(e)}")

# wv_client.close()