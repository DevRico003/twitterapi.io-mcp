# TwitterAPI.io MCP Server

![Model Context Protocol](https://img.shields.io/badge/MCP-Compatible-blue)
![Python Version](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

A Model Context Protocol (MCP) server that provides LLM applications with access to Twitter data through the TwitterAPI.io service. This server enables AI assistants like Claude to retrieve and analyze tweets, user profiles, and other Twitter data in a structured way.

## 🚀 Features

### Resources
- Tweet data by ID (`tweet://{tweet_id}`)
- Tweet replies (`tweet://{tweet_id}/replies`)
- Tweet retweeters (`tweet://{tweet_id}/retweeters`)
- User profiles (`user://{username}`)
- User tweets (`user://{username}/tweets`)
- User followers (`user://{username}/followers`)
- User following (`user://{username}/following`)

### Tools
- Basic Twitter operations (get tweet, get user profile, search tweets)
## 📋 Requirements

- Python 3.8 or higher
- TwitterAPI.io API key

## 🔧 Installation

### Option 1: Direct Installation from PyPI (Recommended)
```bash
# Install with pip
pip install twitterapi-mcp

# or with uv for better performance
uv pip install twitterapi-mcp
```

### Option 2: Use with MCP in Claude Desktop (No Installation)
You can use the server directly through uv run by adding to your `.mcp.json` file:
```json
"twitterapi-mcp": {
  "command": "uv",
  "args": [
    "run",
    "twitterapi-mcp"
  ],
  "env": {
    "TWITTER_API_KEY": "your_api_key_here"
  }
}
```

### Option 3: From Source
1. Clone this repository:
```bash
git clone https://github.com/DevRico003/twitterapi.io-mcp.git
cd twitterapi.io-mcp
```

2. Install as development package:
```bash
pip install -e .
```

3. Configure your TwitterAPI.io API key using environment variables or a `.env` file:
```
TWITTER_API_KEY=your_api_key_here
LOG_LEVEL=INFO
CACHE_TTL=3600
MAX_TWEETS=100
```

## 🚀 Usage

### Running the Server

Run directly with Python:
```bash
# Run the server package as a module
python -m twitterapi_server
```

Or use the MCP development mode:
```bash
mcp dev twitterapi_server
```

### Install in Claude Desktop

```bash
# If you have the package installed:
mcp install -m twitterapi-mcp --name "Twitter API"

# Or directly from the code:
mcp install twitterapi_server --name "Twitter API"
```

## ⚙️ Configuration

The server supports the following environment variables:
- `TWITTER_API_KEY` (required): Your TwitterAPI.io API key
- `LOG_LEVEL` (optional): Logging level (default: INFO)
- `CACHE_TTL` (optional): Cache timeout in seconds (default: 3600/1 hour)
- `MAX_TWEETS` (optional): Maximum tweets per request (default: 100)

## 📁 Project Structure

```
.
├── .gitignore
├── LICENSE
├── MANIFEST.in
├── README.md              # This file
├── pyproject.toml         # Project configuration and dependencies
├── requirements.txt       # Dependencies (alternative format)
├── setup.py               # Build script (legacy compatibility)
├── twitterapi/            # Main package source code
│   ├── __init__.py
│   ├── api_client.py
│   ├── config.py
│   ├── mcp_server.py
│   ├── utils.py
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── tweet_resources.py
│   │   └── user_resources.py
│   └── tools/
│       ├── __init__.py
│       └── basic_tools.py
└── twitterapi_server/     # Server entry point package
    └── __init__.py        # Contains main() function
```

## 🧪 Testing

Run the tests with pytest:
```bash
## 📦 Publishing to PyPI (Developer Notes)

To publish a new version of this package to PyPI:

1.  **Increment Version:** Update the `version` number in `pyproject.toml`.
2.  **Install Tools:** Make sure you have the necessary tools installed:
    ```bash
    pip install --upgrade build twine
    ```
3.  **Configure Credentials:** Ensure you have a `.pypirc` file in your home directory (`~/.pypirc`) configured with your PyPI API token or username/password. Example:
    ```ini
    [pypi]
      username = __token__
      password = pypi-your-api-token-here
    ```
4.  **Build the Package:** Generate the distribution archives:
    ```bash
    python -m build
    ```
    This will create `sdist` (.tar.gz) and `wheel` (.whl) files in the `dist/` directory.
5.  **Upload to PyPI:** Upload the generated files using twine:
    ```bash
    # Replace X.Y.Z with the new version number
    python -m twine upload dist/twitterapi_mcp-X.Y.Z*

    # Or upload all files in dist/ (be careful if old versions exist)
    # python -m twine upload dist/*
    ```
python -m pytest
```

You can run specific test modules:
```bash
python -m pytest tests/test_utils.py
python -m pytest tests/test_api_client.py
```

## 📊 API Cost Considerations

TwitterAPI.io charges approximately $0.15 per 1,000 tweets retrieved. This server implements caching with a configurable TTL to reduce API costs while maintaining fresh data. The cache is particularly effective for frequently monitored influencers and popular searches.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.