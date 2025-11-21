# Työmarkkinatori MCP-Server

![output](https://github.com/user-attachments/assets/a957d706-d66e-4b9c-9d88-ca2ec021777f)


This small project was created to explore the capabilities of an MCP-server and see how the different pieces can work together. There's room for improvement. 

## Features

LLMs can determine search criteria based on user chat input:

- Location code(s)
- Occupation code(s)

The server can also make a POST request to the Työmarkkinatori endpoint and return the first 30 results based on the given criteria.


**Disclaimer:** This server is experimental. All requests made using this server or project are at your own risk.

# Installation (To Claude Desktop)
Running the MCP is possible through two routes:
* Docker container 
* Python 

You should also have Claude Desktop installed.
https://www.claude.com/download

# Running MCP using docker

### Install Docker 
https://www.docker.com/products/docker-desktop/ 

### Pull container 
```
docker pull ghcr.io/markusnieminen1/tyomarkkinatori_mcp_server/tyomarkkinatori_mcp:latest
```

### Add config to Claude Desktop

Config file can be found by going to Claude Desktop -> settings -> Developer -> Local MCP servers: Edit config

```json
{
  "mcpServers": {
    "tyomarkkinatori": {
      "description": "This MCP server provides tools for querying Finnish labor market data (job listings based on municipality- and occupation codes).",
      "command": "docker",
      "args": [
          "run",
          "--interactive",
          "--rm",
          "--read-only",
          "--cap-drop=ALL",
          "--env",
          "-it",
          "ghcr.io/markusnieminen1/tyomarkkinatori_mcp_server/tyomarkkinatori_mcp:latest"
      ]
    }
  }
}

```
#### Save edits and restart the application. The MCP-server will automatically start when Claude Desktop is running. 

# Running MCP using Python

## Install python 3.12

Python Download: https://www.python.org/downloads/

## Clone the repository
```
git clone https://github.com/markusnieminen1/tyomarkkinatori_mcp_server.git
```

## Install uv and dependencies
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Create virtual environment and activate it
```
uv venv \
source .venv/bin/activate
```

### Install dependencies
```
uv sync --frozen
```
### Add config to Claude Desktop
Edit the path-to-the-project-folder and then paste it to claude_desktop_config.json. \
\
Can be found by going to Claude Desktop -> settings -> Developer -> Local MCP servers: Edit config
```json
{
  "mcpServers": {
    "tyomarkkinatori": {
      "description": "This MCP server provides tools for querying Finnish labor market data (job listings based on municipality- and occupation codes).",
      "args": [
        "--directory",
        "path-to-the-project-folder-where-main.py",
        "run",
        "main.py"
      ]
    }
  }
}
```

#### Save edits and restart the application. The MCP-server will automatically start when Claude Desktop is running. 



### More installation information
https://modelcontextprotocol.io/docs/develop/build-server

https://modelcontextprotocol.io/docs/develop/connect-local-servers


## License
This project is licensed under the MIT License.  

## Developing

#### Test the MCP server functionality
npx @modelcontextprotocol/inspector uv --directory path-to-folder-where-main.py run main.py

Might require "brew install uv" on macos. 