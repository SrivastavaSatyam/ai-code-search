# Create main project directory
mkdir ai-code-search
cd ai-code-search

# Create backend structure
mkdir -p backend/{models,search,api,utils}
mkdir -p backend/models/{training,inference}
mkdir -p backend/search/{faiss,milvus}
mkdir -p backend/api/{routes,middleware}

# Create frontend structure
mkdir -p frontend/{components,pages,styles,utils,hooks,context,public}

# Create data structure
mkdir -p data/{raw,processed}

# Create deployment structure
mkdir -p deployment/{k8s,cloud}

# Create tests structure
mkdir -p tests/{backend,frontend,performance}

# Create root level files
touch .env .gitignore README.md LICENSE CONTRIBUTING.md CODE_OF_CONDUCT.md setup.py 