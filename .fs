{
    "project": "connected-api",
    "author": "Mubarak",
    "email": "mubee2004@gmail.com",
    "config": {
        "environment": "venv",
        "python": "3.12.5",
        "pip": "24.2",
        "fs": "0.7",
        "port": 5050,
        "entry-point": "main.py"
    },
    "packages": [
        {
            "name": "alembic",
            "version": "1.13.2",
            "dependencies": [
                {
                    "name": "Mako",
                    "version": "1.3.10"
                },
                {
                    "name": "SQLAlchemy",
                    "version": "2.0.41"
                },
                {
                    "name": "typing-extensions",
                    "version": "4.13.2"
                }
            ]
        },
        {
            "name": "amqp",
            "version": "5.2.0",
            "dependencies": [
                {
                    "name": "vine",
                    "version": "5.1.0"
                }
            ]
        },
        {
            "name": "bcrypt",
            "version": "4.2.0",
            "dependencies": []
        },
        {
            "name": "billiard",
            "version": "4.2.0",
            "dependencies": []
        },
        {
            "name": "blinker",
            "version": "1.8.2",
            "dependencies": []
        },
        {
            "name": "celery",
            "version": "5.4.0",
            "dependencies": [
                {
                    "name": "billiard",
                    "version": "4.2.0"
                },
                {
                    "name": "click",
                    "version": "8.1.8"
                },
                {
                    "name": "click-didyoumean",
                    "version": "0.3.1"
                },
                {
                    "name": "click-plugins",
                    "version": "1.1.1"
                },
                {
                    "name": "click-repl",
                    "version": "0.3.0"
                },
                {
                    "name": "kombu",
                    "version": "5.5.3"
                },
                {
                    "name": "python-dateutil",
                    "version": "2.9.0.post0"
                },
                {
                    "name": "tzdata",
                    "version": "2025.2"
                },
                {
                    "name": "vine",
                    "version": "5.1.0"
                }
            ]
        },
        {
            "name": "certifi",
            "version": "2024.8.30",
            "dependencies": []
        },
        {
            "name": "charset-normalizer",
            "version": "3.3.2",
            "dependencies": []
        },
        {
            "name": "click",
            "version": "8.1.7",
            "dependencies": []
        },
        {
            "name": "click-didyoumean",
            "version": "0.3.1",
            "dependencies": [
                {
                    "name": "click",
                    "version": "8.1.7"
                }
            ]
        },
        {
            "name": "click-plugins",
            "version": "1.1.1",
            "dependencies": [
                {
                    "name": "click",
                    "version": "8.1.7"
                }
            ]
        },
        {
            "name": "click-repl",
            "version": "0.3.0",
            "dependencies": [
                {
                    "name": "click",
                    "version": "8.1.7"
                },
                {
                    "name": "prompt-toolkit",
                    "version": "3.0.51"
                }
            ]
        },
        {
            "name": "colorama",
            "version": "0.4.6",
            "dependencies": []
        },
        {
            "name": "flask",
            "version": "3.0.3",
            "dependencies": [
                {
                    "name": "blinker",
                    "version": "1.8.2"
                },
                {
                    "name": "click",
                    "version": "8.1.7"
                },
                {
                    "name": "itsdangerous",
                    "version": "2.2.0"
                },
                {
                    "name": "Jinja2",
                    "version": "3.1.4"
                },
                {
                    "name": "Werkzeug",
                    "version": "3.0.4"
                }
            ]
        },
        {
            "name": "Flask-Cors",
            "version": "4.0.1",
            "dependencies": [
                {
                    "name": "Flask",
                    "version": "3.0.3"
                }
            ]
        },
        {
            "name": "Flask-JWT-Extended",
            "version": "4.6.0",
            "dependencies": [
                {
                    "name": "Flask",
                    "version": "3.0.3"
                },
                {
                    "name": "PyJWT",
                    "version": "2.10.1"
                },
                {
                    "name": "Werkzeug",
                    "version": "3.1.3"
                }
            ]
        },
        {
            "name": "flask-marshmallow",
            "version": "1.2.1",
            "dependencies": [
                {
                    "name": "Flask",
                    "version": "3.0.3"
                },
                {
                    "name": "marshmallow",
                    "version": "4.0.0"
                }
            ]
        },
        {
            "name": "Flask-Migrate",
            "version": "4.0.7",
            "dependencies": [
                {
                    "name": "alembic",
                    "version": "1.13.2"
                },
                {
                    "name": "Flask",
                    "version": "3.0.3"
                },
                {
                    "name": "Flask-SQLAlchemy",
                    "version": "3.1.1"
                }
            ]
        },
        {
            "name": "flask-setup",
            "version": "0.7",
            "dependencies": [
                {
                    "name": "typer",
                    "version": "0.15.4"
                }
            ]
        },
        {
            "name": "Flask-SQLAlchemy",
            "version": "3.1.1",
            "dependencies": [
                {
                    "name": "flask",
                    "version": "3.0.3"
                },
                {
                    "name": "sqlalchemy",
                    "version": "2.0.41"
                }
            ]
        },
        {
            "name": "greenlet",
            "version": "3.0.3",
            "dependencies": []
        },
        {
            "name": "gunicorn",
            "version": "22.0.0",
            "dependencies": [
                {
                    "name": "packaging",
                    "version": "25.0"
                }
            ]
        },
        {
            "name": "idna",
            "version": "3.8",
            "dependencies": []
        },
        {
            "name": "itsdangerous",
            "version": "2.2.0",
            "dependencies": []
        },
        {
            "name": "Jinja2",
            "version": "3.1.4",
            "dependencies": [
                {
                    "name": "MarkupSafe",
                    "version": "3.0.2"
                }
            ]
        },
        {
            "name": "kombu",
            "version": "5.4.0",
            "dependencies": [
                {
                    "name": "amqp",
                    "version": "5.2.0"
                },
                {
                    "name": "vine",
                    "version": "5.1.0"
                }
            ]
        },
        {
            "name": "Mako",
            "version": "1.3.5",
            "dependencies": [
                {
                    "name": "MarkupSafe",
                    "version": "3.0.2"
                }
            ]
        },
        {
            "name": "markdown-it-py",
            "version": "3.0.0",
            "dependencies": [
                {
                    "name": "mdurl",
                    "version": "0.1.2"
                }
            ]
        },
        {
            "name": "MarkupSafe",
            "version": "2.1.5",
            "dependencies": []
        },
        {
            "name": "marshmallow",
            "version": "3.22.0",
            "dependencies": [
                {
                    "name": "packaging",
                    "version": "25.0"
                }
            ]
        },
        {
            "name": "marshmallow-sqlalchemy",
            "version": "1.0.0",
            "dependencies": [
                {
                    "name": "marshmallow",
                    "version": "3.22.0"
                },
                {
                    "name": "SQLAlchemy",
                    "version": "2.0.41"
                }
            ]
        },
        {
            "name": "mdurl",
            "version": "0.1.2",
            "dependencies": []
        },
        {
            "name": "packaging",
            "version": "24.1",
            "dependencies": []
        },
        {
            "name": "pip",
            "version": "24.2",
            "dependencies": []
        },
        {
            "name": "prompt_toolkit",
            "version": "3.0.47",
            "dependencies": [
                {
                    "name": "wcwidth",
                    "version": "0.2.13"
                }
            ]
        },
        {
            "name": "psycopg2-binary",
            "version": "2.9.9",
            "dependencies": []
        },
        {
            "name": "Pygments",
            "version": "2.18.0",
            "dependencies": []
        },
        {
            "name": "PyJWT",
            "version": "2.9.0",
            "dependencies": []
        },
        {
            "name": "python-dateutil",
            "version": "2.9.0.post0",
            "dependencies": [
                {
                    "name": "six",
                    "version": "1.17.0"
                }
            ]
        },
        {
            "name": "python-dotenv",
            "version": "1.0.1",
            "dependencies": []
        },
        {
            "name": "redis",
            "version": "5.0.8",
            "dependencies": [
                {
                    "name": "async-timeout",
                    "version": "5.0.1"
                }
            ]
        },
        {
            "name": "requests",
            "version": "2.32.3",
            "dependencies": [
                {
                    "name": "certifi",
                    "version": "2024.8.30"
                },
                {
                    "name": "charset-normalizer",
                    "version": "3.3.2"
                },
                {
                    "name": "idna",
                    "version": "3.8"
                },
                {
                    "name": "urllib3",
                    "version": "2.4.0"
                }
            ]
        },
        {
            "name": "rich",
            "version": "13.8.0",
            "dependencies": [
                {
                    "name": "markdown-it-py",
                    "version": "3.0.0"
                },
                {
                    "name": "pygments",
                    "version": "2.18.0"
                }
            ]
        },
        {
            "name": "shellingham",
            "version": "1.5.4",
            "dependencies": []
        },
        {
            "name": "six",
            "version": "1.16.0",
            "dependencies": []
        },
        {
            "name": "SQLAlchemy",
            "version": "2.0.34",
            "dependencies": [
                {
                    "name": "greenlet",
                    "version": "3.0.3"
                },
                {
                    "name": "typing-extensions",
                    "version": "4.13.2"
                }
            ]
        },
        {
            "name": "typer",
            "version": "0.12.5",
            "dependencies": [
                {
                    "name": "click",
                    "version": "8.1.7"
                },
                {
                    "name": "rich",
                    "version": "13.8.0"
                },
                {
                    "name": "shellingham",
                    "version": "1.5.4"
                },
                {
                    "name": "typing-extensions",
                    "version": "4.13.2"
                }
            ]
        },
        {
            "name": "typing_extensions",
            "version": "4.12.2",
            "dependencies": []
        },
        {
            "name": "tzdata",
            "version": "2024.1",
            "dependencies": []
        },
        {
            "name": "urllib3",
            "version": "2.2.2",
            "dependencies": []
        },
        {
            "name": "vine",
            "version": "5.1.0",
            "dependencies": []
        },
        {
            "name": "wcwidth",
            "version": "0.2.13",
            "dependencies": []
        },
        {
            "name": "Werkzeug",
            "version": "3.0.4",
            "dependencies": [
                {
                    "name": "MarkupSafe",
                    "version": "2.1.5"
                }
            ]
        },
        {
            "name": "flask",
            "version": "3.0.3",
            "dependencies": [
                {
                    "name": "blinker"
                },
                {
                    "name": "click"
                },
                {
                    "name": "itsdangerous"
                },
                {
                    "name": "Jinja2"
                },
                {
                    "name": "Werkzeug"
                }
            ],
            "timestamp": "2024-09-10 00:45:44"
        },
        {
            "name": "africastalking",
            "version": "1.2.8",
            "dependencies": [
                {
                    "name": "requests",
                    "version": "2.32.3"
                },
                {
                    "name": "schema",
                    "version": "0.7.7"
                }
            ]
        },
        {
            "name": "africastalking",
            "version": "1.2.8",
            "dependencies": [
                {
                    "name": "requests"
                },
                {
                    "name": "schema"
                }
            ],
            "timestamp": "2024-09-12 21:58:46"
        },
        {
            "name": "weaviate-client",
            "version": "4.8.1",
            "dependencies": [
                {
                    "name": "authlib",
                    "version": "1.3.1"
                },
                {
                    "name": "grpcio",
                    "version": "1.71.0"
                },
                {
                    "name": "grpcio-health-checking",
                    "version": "1.71.0"
                },
                {
                    "name": "grpcio-tools",
                    "version": "1.71.0"
                },
                {
                    "name": "httpx",
                    "version": "0.27.0"
                },
                {
                    "name": "pydantic",
                    "version": "2.11.4"
                },
                {
                    "name": "requests",
                    "version": "2.32.3"
                },
                {
                    "name": "validators",
                    "version": "0.34.0"
                }
            ]
        },
        {
            "name": "pypdf",
            "version": "5.0.0",
            "dependencies": [
                {
                    "name": "typing_extensions",
                    "version": "4.12.2"
                }
            ]
        },
        {
            "name": "python-docx",
            "version": "1.1.2",
            "dependencies": [
                {
                    "name": "lxml",
                    "version": "5.4.0"
                },
                {
                    "name": "typing-extensions",
                    "version": "4.12.2"
                }
            ]
        },
        {
            "name": "boto3",
            "version": "1.35.32",
            "dependencies": [
                {
                    "name": "botocore",
                    "version": "1.35.99"
                },
                {
                    "name": "jmespath",
                    "version": "1.0.1"
                },
                {
                    "name": "s3transfer",
                    "version": "0.10.4"
                }
            ]
        },
        {
            "name": "unstructured",
            "version": "0.15.13",
            "dependencies": [
                {
                    "name": "backoff",
                    "version": "2.2.1"
                },
                {
                    "name": "beautifulsoup4",
                    "version": "4.13.4"
                },
                {
                    "name": "chardet",
                    "version": "5.2.0"
                },
                {
                    "name": "dataclasses-json",
                    "version": "0.6.7"
                },
                {
                    "name": "emoji",
                    "version": "2.14.1"
                },
                {
                    "name": "filetype",
                    "version": "1.2.0"
                },
                {
                    "name": "langdetect",
                    "version": "1.0.9"
                },
                {
                    "name": "lxml",
                    "version": "5.4.0"
                },
                {
                    "name": "nltk",
                    "version": "3.9.1"
                },
                {
                    "name": "numpy",
                    "version": "1.26.4"
                },
                {
                    "name": "psutil",
                    "version": "7.0.0"
                },
                {
                    "name": "python-iso639",
                    "version": "2025.2.18"
                },
                {
                    "name": "python-magic",
                    "version": "0.4.27"
                },
                {
                    "name": "python-oxmsg",
                    "version": "0.0.2"
                },
                {
                    "name": "rapidfuzz",
                    "version": "3.13.0"
                },
                {
                    "name": "requests",
                    "version": "2.32.3"
                },
                {
                    "name": "tabulate",
                    "version": "0.9.0"
                },
                {
                    "name": "tqdm",
                    "version": "4.67.1"
                },
                {
                    "name": "typing-extensions",
                    "version": "4.12.2"
                },
                {
                    "name": "unstructured-client",
                    "version": "0.35.0"
                },
                {
                    "name": "wrapt",
                    "version": "1.17.2"
                }
            ]
        },
        {
            "name": "pdfminer",
            "version": "20191125",
            "dependencies": [
                {
                    "name": "pycryptodome",
                    "version": "3.22.0"
                }
            ]
        },
        {
            "name": "pdfminer.six",
            "version": "20240706",
            "dependencies": [
                {
                    "name": "charset-normalizer",
                    "version": "3.3.2"
                },
                {
                    "name": "cryptography",
                    "version": "44.0.3"
                }
            ]
        },
        {
            "name": "pi_heif",
            "version": "0.18.0",
            "dependencies": [
                {
                    "name": "pillow",
                    "version": "11.2.1"
                }
            ]
        },
        {
            "name": "unstructured_inference",
            "version": "0.7.37",
            "dependencies": [
                {
                    "name": "huggingface-hub",
                    "version": "0.31.2"
                },
                {
                    "name": "layoutparser",
                    "version": "0.3.4"
                },
                {
                    "name": "matplotlib",
                    "version": "3.10.3"
                },
                {
                    "name": "numpy",
                    "version": "1.26.4"
                },
                {
                    "name": "onnx",
                    "version": "1.18.0"
                },
                {
                    "name": "onnxruntime",
                    "version": "1.22.0"
                },
                {
                    "name": "opencv-python",
                    "version": "4.11.0.86"
                },
                {
                    "name": "python-multipart",
                    "version": "0.0.20"
                },
                {
                    "name": "rapidfuzz",
                    "version": "3.13.0"
                },
                {
                    "name": "timm",
                    "version": "1.0.15"
                },
                {
                    "name": "torch",
                    "version": "2.7.0"
                },
                {
                    "name": "transformers",
                    "version": "4.51.3"
                }
            ]
        },
        {
            "name": "langchain_pinecone",
            "version": "0.2.0",
            "dependencies": [
                {
                    "name": "aiohttp",
                    "version": "3.9.5"
                },
                {
                    "name": "langchain-core",
                    "version": "0.3.60"
                },
                {
                    "name": "numpy",
                    "version": "1.26.4"
                },
                {
                    "name": "pinecone-client",
                    "version": "5.0.1"
                }
            ]
        },
        {
            "name": "langchain_community",
            "version": "0.3.7",
            "dependencies": [
                {
                    "name": "aiohttp",
                    "version": "3.9.5"
                },
                {
                    "name": "dataclasses-json",
                    "version": "0.6.7"
                },
                {
                    "name": "httpx-sse",
                    "version": "0.4.0"
                },
                {
                    "name": "langchain",
                    "version": "0.3.25"
                },
                {
                    "name": "langchain-core",
                    "version": "0.3.60"
                },
                {
                    "name": "langsmith",
                    "version": "0.1.147"
                },
                {
                    "name": "numpy",
                    "version": "1.26.4"
                },
                {
                    "name": "pydantic-settings",
                    "version": "2.9.1"
                },
                {
                    "name": "PyYAML",
                    "version": "6.0.2"
                },
                {
                    "name": "requests",
                    "version": "2.32.3"
                },
                {
                    "name": "SQLAlchemy",
                    "version": "2.0.34"
                },
                {
                    "name": "tenacity",
                    "version": "9.1.2"
                }
            ]
        },
        {
            "name": "googleapis-common-protos",
            "version": "1.65.0",
            "dependencies": [
                {
                    "name": "protobuf",
                    "version": "5.29.4"
                }
            ]
        },
        {
            "name": "grpcio",
            "version": "1.66.2",
            "dependencies": []
        },
        {
            "name": "pinecone",
            "version": "5.3.1",
            "dependencies": [
                {
                    "name": "certifi",
                    "version": "2024.8.30"
                },
                {
                    "name": "pinecone-plugin-inference",
                    "version": "1.1.0"
                },
                {
                    "name": "pinecone-plugin-interface",
                    "version": "0.0.7"
                },
                {
                    "name": "python-dateutil",
                    "version": "2.9.0.post0"
                },
                {
                    "name": "tqdm",
                    "version": "4.67.1"
                },
                {
                    "name": "typing-extensions",
                    "version": "4.12.2"
                },
                {
                    "name": "urllib3",
                    "version": "2.2.2"
                }
            ]
        },
        {
            "name": "pydantic",
            "version": "2.9.2",
            "dependencies": [
                {
                    "name": "annotated-types",
                    "version": "0.7.0"
                },
                {
                    "name": "pydantic-core",
                    "version": "2.23.4"
                },
                {
                    "name": "typing-extensions",
                    "version": "4.12.2"
                }
            ]
        },
        {
            "name": "pydantic_core",
            "version": "2.23.4",
            "dependencies": [
                {
                    "name": "typing-extensions",
                    "version": "4.12.2"
                }
            ]
        },
        {
            "name": "googleapis-common-protos",
            "version": "1.65.0",
            "dependencies": [
                {
                    "name": "protobuf"
                }
            ],
            "timestamp": "2024-11-15 19:58:00"
        },
        {
            "name": "grpcio",
            "version": "1.66.2",
            "dependencies": [],
            "timestamp": "2024-11-15 19:58:44"
        },
        {
            "name": "langchain-core",
            "version": "0.3.10",
            "dependencies": [
                {
                    "name": "jsonpatch",
                    "version": "1.33"
                },
                {
                    "name": "langsmith",
                    "version": "0.1.147"
                },
                {
                    "name": "packaging",
                    "version": "24.1"
                },
                {
                    "name": "pydantic",
                    "version": "2.9.1"
                },
                {
                    "name": "PyYAML",
                    "version": "6.0.2"
                },
                {
                    "name": "tenacity",
                    "version": "8.5.0"
                },
                {
                    "name": "typing-extensions",
                    "version": "4.12.2"
                }
            ]
        },
        {
            "name": "langchain-pinecone",
            "version": "0.2.0",
            "dependencies": [
                {
                    "name": "aiohttp",
                    "version": "3.9.5"
                },
                {
                    "name": "langchain-core",
                    "version": "0.3.10"
                },
                {
                    "name": "numpy",
                    "version": "1.26.4"
                },
                {
                    "name": "pinecone-client",
                    "version": "5.0.1"
                }
            ]
        },
        {
            "name": "langchain-text-splitters",
            "version": "0.3.0",
            "dependencies": [
                {
                    "name": "langchain-core",
                    "version": "0.3.10"
                }
            ]
        },
        {
            "name": "langdetect",
            "version": "1.0.9",
            "dependencies": [
                {
                    "name": "six",
                    "version": "1.16.0"
                }
            ]
        },
        {
            "name": "pinecone",
            "version": "5.3.1",
            "dependencies": [
                {
                    "name": "certifi"
                },
                {
                    "name": "pinecone-plugin-inference"
                },
                {
                    "name": "pinecone-plugin-interface"
                },
                {
                    "name": "python-dateutil"
                },
                {
                    "name": "tqdm"
                },
                {
                    "name": "typing-extensions"
                },
                {
                    "name": "urllib3"
                }
            ],
            "timestamp": "2024-11-15 20:16:09"
        },
        {
            "name": "protoc-gen-openapiv2",
            "version": "0.0.1",
            "dependencies": [
                {
                    "name": "googleapis-common-protos",
                    "version": "1.65.0"
                },
                {
                    "name": "protobuf",
                    "version": "5.29.4"
                }
            ]
        },
        {
            "name": "pydantic",
            "version": "2.9.2",
            "dependencies": [
                {
                    "name": "annotated-types"
                },
                {
                    "name": "pydantic-core"
                },
                {
                    "name": "typing-extensions"
                }
            ],
            "timestamp": "2024-11-15 20:19:13"
        },
        {
            "name": "pydantic-settings",
            "version": "2.5.2",
            "dependencies": [
                {
                    "name": "pydantic",
                    "version": "2.9.2"
                },
                {
                    "name": "python-dotenv",
                    "version": "1.0.1"
                }
            ]
        },
        {
            "name": "pydantic_core",
            "version": "2.23.4",
            "dependencies": [
                {
                    "name": "typing-extensions"
                }
            ],
            "timestamp": "2024-11-15 20:19:45"
        },
        {
            "name": "langchain",
            "version": "0.3.3",
            "dependencies": [
                {
                    "name": "aiohttp"
                },
                {
                    "name": "async-timeout"
                },
                {
                    "name": "langchain-core"
                },
                {
                    "name": "langchain-text-splitters"
                },
                {
                    "name": "langsmith"
                },
                {
                    "name": "numpy"
                },
                {
                    "name": "pydantic"
                },
                {
                    "name": "PyYAML"
                },
                {
                    "name": "requests"
                },
                {
                    "name": "SQLAlchemy"
                },
                {
                    "name": "tenacity"
                }
            ],
            "timestamp": "2024-11-16 16:43:00"
        },
        {
            "name": "langchain-community",
            "version": "0.3.2",
            "dependencies": [
                {
                    "name": "aiohttp",
                    "version": "3.9.5"
                },
                {
                    "name": "dataclasses-json",
                    "version": "0.6.7"
                },
                {
                    "name": "langchain",
                    "version": "0.3.25"
                },
                {
                    "name": "langchain-core",
                    "version": "0.3.60"
                },
                {
                    "name": "langsmith",
                    "version": "0.1.147"
                },
                {
                    "name": "numpy",
                    "version": "1.26.4"
                },
                {
                    "name": "pydantic-settings",
                    "version": "2.5.2"
                },
                {
                    "name": "PyYAML",
                    "version": "6.0.2"
                },
                {
                    "name": "requests",
                    "version": "2.32.3"
                },
                {
                    "name": "SQLAlchemy",
                    "version": "2.0.34"
                },
                {
                    "name": "tenacity",
                    "version": "8.5.0"
                }
            ]
        },
        {
            "name": "langchain-openai",
            "version": "0.2.2",
            "dependencies": [
                {
                    "name": "langchain-core"
                },
                {
                    "name": "openai"
                },
                {
                    "name": "tiktoken"
                }
            ],
            "timestamp": "2024-11-16 16:45:50"
        },
        {
            "name": "langsmith",
            "version": "0.1.134",
            "dependencies": [
                {
                    "name": "httpx",
                    "version": "0.27.0"
                },
                {
                    "name": "orjson",
                    "version": "3.10.18"
                },
                {
                    "name": "pydantic",
                    "version": "2.9.2"
                },
                {
                    "name": "requests",
                    "version": "2.32.3"
                },
                {
                    "name": "requests-toolbelt",
                    "version": "1.0.0"
                }
            ]
        },
        {
            "name": "pinecone-client",
            "version": "5.0.1",
            "dependencies": [
                {
                    "name": "certifi",
                    "version": "2024.8.30"
                },
                {
                    "name": "pinecone-plugin-inference",
                    "version": "1.1.0"
                },
                {
                    "name": "pinecone-plugin-interface",
                    "version": "0.0.7"
                },
                {
                    "name": "tqdm",
                    "version": "4.67.1"
                },
                {
                    "name": "typing-extensions",
                    "version": "4.12.2"
                },
                {
                    "name": "urllib3",
                    "version": "2.2.2"
                }
            ]
        },
        {
            "name": "pinecone-plugin-inference",
            "version": "1.1.0",
            "dependencies": [
                {
                    "name": "pinecone-plugin-interface",
                    "version": "0.0.7"
                }
            ]
        },
        {
            "name": "pinecone-plugin-interface",
            "version": "0.0.7",
            "dependencies": []
        },
        {
            "name": "pytesseract",
            "version": "0.3.13",
            "dependencies": [
                {
                    "name": "packaging",
                    "version": "24.1"
                },
                {
                    "name": "Pillow",
                    "version": "11.2.1"
                }
            ]
        },
        {
            "name": "unstructured_pytesseract",
            "version": "0.3.13",
            "dependencies": [
                {
                    "name": "packaging",
                    "version": "24.1"
                },
                {
                    "name": "Pillow",
                    "version": "11.2.1"
                }
            ]
        },
        {
            "name": "twilio",
            "version": "9.5.2",
            "dependencies": [
                {
                    "name": "aiohttp",
                    "version": "3.9.5"
                },
                {
                    "name": "aiohttp-retry",
                    "version": "2.9.1"
                },
                {
                    "name": "PyJWT",
                    "version": "2.9.0"
                },
                {
                    "name": "requests",
                    "version": "2.32.3"
                }
            ]
        },
        {
            "name": "paystack-sdk",
            "version": "1.0.1",
            "dependencies": [
                {
                    "name": "python-dateutil"
                },
                {
                    "name": "six"
                },
                {
                    "name": "urllib3"
                }
            ],
            "timestamp": "2025-05-28 20:59:33"
        }
    ],
    "modules": [
        {
            "name": "numbers",
            "fields": [
                {
                    "name": "number",
                    "type": "str"
                },
                {
                    "name": "language",
                    "type": "str"
                },
                {
                    "name": "area_id",
                    "type": "fk=areas.id"
                }
            ],
            "timestamp": "2024-09-10 18:08:32"
        },
        {
            "name": "areas",
            "fields": [
                {
                    "name": "name",
                    "type": "str"
                },
                {
                    "name": "numbers",
                    "type": "rel=numbers"
                }
            ],
            "timestamp": "2024-09-10 19:07:14"
        },
        {
            "name": "ussd",
            "fields": [
                {
                    "name": "session_id",
                    "type": "str"
                },
                {
                    "name": "stage",
                    "type": "str"
                },
                {
                    "name": "previous",
                    "type": "str"
                }
            ],
            "timestamp": "2024-09-30 08:37:52"
        },
        {
            "name": "whatsapp_number",
            "fields": [
                {
                    "name": "number",
                    "type": "str"
                },
                {
                    "name": "user_id",
                    "type": "fk=user.id"
                }
            ],
            "timestamp": "2025-05-08 11:16:08"
        }
    ]
}