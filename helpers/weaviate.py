import os
import weaviate
from weaviate.util import generate_uuid5
import weaviate.classes as wvc
from weaviate.classes.init import AdditionalConfig, Timeout
from weaviate.classes.query import Filter
from weaviate.classes.config import Configure, Property, DataType

weaviate_url = os.environ.get("WEAVIATE_URL")
weaviate_api_key = os.environ.get("WEAVIATE_API_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Weaviate client initialization
wv_client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=weaviate.auth.AuthApiKey(weaviate_api_key),
    headers={'X-OpenAI-Api-key': openai_api_key},
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)
    ),
    skip_init_checks=True
)

def wv_create_class(wv_client, class_name):
    try:
        file_schema = wv_client.collections.create(
            name=class_name,
            # vectorizer_config=Configure.Vectorizer.text2vec_openai(),
            generative_config=Configure.Generative.openai(
                model="gpt-3.5-turbo",
                frequency_penalty=0,
                max_tokens=300,
                presence_penalty=0,
                temperature=0.1,
                top_p=0.7,
            ),
            properties=[
                Property(
                    name="content",
                    data_type=DataType.TEXT,
                ),
                Property(
                    name="filename",
                    data_type=DataType.TEXT,
                ),
            ]
        )
        print(file_schema.config.get(simple=False))
        return file_schema
    except Exception as e:
        print(f"Error creating class: {str(e)}")
        return None

def wv_upload_doc(wv_client, text, class_name, filename):
    try:
        collection = wv_client.collections.get(class_name)
        print(collection)
    except weaviate.exceptions.UnexpectedStatusCodeException:
        file_schema = wv_create_class(wv_client, class_name)
        print(file_schema)
        if file_schema is None:
            return
        collection = wv_client.collections.get(class_name)

    batch_size = 100
    paragraphs = text.split('\n\n')
    
    with collection.batch.dynamic() as batch:
        for i, paragraph in enumerate(paragraphs):
            properties = {
                "content": paragraph,
                "filename": filename
            }
            
            object_uuid = generate_uuid5(properties)
            
            batch.add_object(
                properties=properties,
                uuid=object_uuid,
            )
            
            if i % batch_size == 0:
                print(f"Imported {i} paragraphs...")
    
    print(f"Finished importing {len(paragraphs)} paragraphs.")
    print("Failed objects: ", collection.batch.failed_objects)
    print("Failed references: ", collection.batch.failed_references)
    # print("Batch number errors: ", collection.batch.number_errors)


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

# Add a new function to search documents
def wv_search_docs(wv_client, class_name, query, limit=5):
    try:
        collection = wv_client.collections.get(class_name)
        results = collection.query.near_text(
            query=query,
            limit=limit
        ).with_additional(["distance"]).do()
        
        return results["objects"]
    except Exception as e:
        print(f"Error searching documents in Weaviate: {str(e)}")
        return []

# Add a function to update a document
def wv_update_doc(wv_client, class_name, object_uuid, new_properties):
    try:
        collection = wv_client.collections.get(class_name)
        result = collection.data.update(
            uuid=object_uuid,
            properties=new_properties
        )
        print(f"Updated object with UUID {object_uuid} in class {class_name}")
        return result
    except Exception as e:
        print(f"Error updating document in Weaviate: {str(e)}")
        return None