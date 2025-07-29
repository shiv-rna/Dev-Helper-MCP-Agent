# Dev-Helper-MCP-Agent 🚀

> **Intelligent AI Agent for Developer Tools Research & Web Scraping**

A sophisticated AI-powered research assistant that combines web scraping, intelligent analysis, and structured recommendations to help developers discover and evaluate the best tools, libraries, and services for their projects.

## 🌟 What Makes This Special

This project demonstrates cutting-edge AI agent architecture using **LangGraph**, **MCP (Model Context Protocol)**, and **Firecrawl** to create intelligent research workflows. Unlike simple chatbots, this agent can:

- **Automatically discover** relevant developer tools through web research
- **Analyze pricing models** and technical capabilities in real-time
- **Provide structured recommendations** with actionable insights
- **Save research history** for future reference
- **Scale from simple** web scraping to **advanced multi-step workflows**

## 🏗️ Architecture Overview

The project consists of two complementary agents:

### 🎯 Simple Agent
- **Purpose**: Direct web scraping and data extraction
- **Tech Stack**: LangChain + MCP + Firecrawl
- **Use Case**: Quick website analysis and content extraction

### 🧠 Advanced Agent  
- **Purpose**: Intelligent research and recommendation engine
- **Tech Stack**: LangGraph + OpenAI + Firecrawl + Pydantic
- **Use Case**: Multi-step research workflows with structured analysis

## ✨ Key Features

### 🔍 Intelligent Research
- **Automated Tool Discovery**: Finds relevant developer tools through web search
- **Structured Analysis**: Extracts pricing, tech stack, API availability, and integrations
- **Smart Recommendations**: Provides actionable insights based on research findings

### 🌐 Web Scraping Capabilities
- **Firecrawl Integration**: High-quality web scraping with markdown output
- **Search Functionality**: Find relevant articles and company pages
- **Content Analysis**: Extract and analyze website content intelligently

### 📊 Structured Output
- **Pydantic Models**: Type-safe data structures for consistent analysis
- **JSON Export**: Save research results and conversation history
- **Developer-Focused**: Extracts relevant technical information (APIs, SDKs, integrations)

### 🔄 Workflow Management
- **LangGraph State Management**: Robust multi-step workflow orchestration
- **Error Handling**: Graceful failure recovery and fallback mechanisms
- **Progress Tracking**: Real-time status updates during research

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Node.js 18+** (for MCP functionality)
- **OpenAI API Key**
- **Firecrawl API Key**

### Installation

#### Option 1: Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Dev-Helper-MCP-Agent.git
   cd Dev-Helper-MCP-Agent
   ```

2. **Install uv (Python package manager)**
   ```bash
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file in each agent directory
   echo "OPENAI_API_KEY=your_openai_key_here" > src/simple-agent/.env
   echo "FIRECRAWL_API_KEY=your_firecrawl_key_here" >> src/simple-agent/.env
   
   echo "OPENAI_API_KEY=your_openai_key_here" > src/advanced-agent/.env
   echo "FIRECRAWL_API_KEY=your_firecrawl_key_here" >> src/advanced-agent/.env
   ```

4. **Install dependencies**
   ```bash
   # Simple Agent
   cd src/simple-agent
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   
   # Advanced Agent
   cd ../advanced-agent
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

5. **Install Node.js and MCP tools (for simple agent)**
   ```bash
   # Install Node.js 18+ (if not already installed)
   # On macOS with Homebrew
   brew install node
   
   # On Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo bash -
   sudo apt-get install -y nodejs
   
   # Install MCP tools
   npx firecrawl-mcp
   ```
   
   **Note**: The MCP tools installation is only needed for the simple agent. The advanced agent uses the Firecrawl Python SDK directly.
   ```

#### Option 2: Docker Installation (Recommended)

1. **Prerequisites**
   - [Docker](https://docs.docker.com/get-docker/) installed
   - [Docker Compose](https://docs.docker.com/compose/install/) (optional, for multi-container setup)

2. **Clone and build**
   ```bash
   git clone https://github.com/yourusername/Dev-Helper-MCP-Agent.git
   cd Dev-Helper-MCP-Agent
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file in each agent directory
   echo "OPENAI_API_KEY=your_openai_key_here" > src/simple-agent/.env
   echo "FIRECRAWL_API_KEY=your_firecrawl_key_here" >> src/simple-agent/.env
   
   echo "OPENAI_API_KEY=your_openai_key_here" > src/advanced-agent/.env
   echo "FIRECRAWL_API_KEY=your_firecrawl_key_here" >> src/advanced-agent/.env
   ```

4. **Build and run with Docker**
   ```bash
   # Build the development container
   docker build -f .devcontainer/Dockerfile -t dev-helper-agent .
   
   # Run the container
   docker run -it --rm \
     -v $(pwd):/workspace \
     -w /workspace \
     dev-helper-agent bash
   ```

#### Option 3: VS Code Dev Container (Easiest)

1. **Prerequisites**
   - [VS Code](https://code.visualstudio.com/) with [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
   - [Docker](https://docs.docker.com/get-docker/) installed

2. **Open in Dev Container**
   ```bash
   git clone https://github.com/yourusername/Dev-Helper-MCP-Agent.git
   cd Dev-Helper-MCP-Agent
   code .
   ```
   
   Then in VS Code:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
   - Select "Dev Containers: Reopen in Container"
   - Wait for the container to build and start

3. **Set up environment variables**
   ```bash
   # Create .env files in the container
   echo "OPENAI_API_KEY=your_openai_key_here" > src/simple-agent/.env
   echo "FIRECRAWL_API_KEY=your_firecrawl_key_here" >> src/simple-agent/.env
   
   echo "OPENAI_API_KEY=your_openai_key_here" > src/advanced-agent/.env
   echo "FIRECRAWL_API_KEY=your_firecrawl_key_here" >> src/advanced-agent/.env
   ```

4. **Install dependencies (automated in dev container)**
   The dev container automatically installs dependencies on first run.

### Usage Examples

#### 🎯 Simple Agent - Direct Web Scraping
```bash
# If using local installation
cd src/simple-agent
uv run main.py

# If using VS Code Dev Container, the terminal is already in the right context
cd src/simple-agent
uv run main.py
```

**Example queries:**
- "Scrape the pricing page of GitHub Copilot"
- "Extract the API documentation from Stripe's website"
- "Get the tech stack information from Vercel's homepage"

#### 🧠 Advanced Agent - Intelligent Research
```bash
# If using local installation
cd src/advanced-agent
uv run main.py

# If using VS Code Dev Container, the terminal is already in the right context
cd src/advanced-agent
uv run main.py
```

**Example queries:**
- "Find the best CI/CD tools for Python projects"
- "Compare code review tools for remote teams"
- "Research database monitoring solutions"

#### 🐳 Docker Quick Start
```bash
# Run simple agent in Docker
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace/src/simple-agent \
  dev-helper-agent uv run main.py

# Run advanced agent in Docker
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace/src/advanced-agent \
  dev-helper-agent uv run main.py
```

**Note**: Make sure you've set up your `.env` files before running the Docker commands.

## 📁 Project Structure

```
Dev-Helper-MCP-Agent/
├── src/
│   ├── simple-agent/           # Direct web scraping agent
│   │   ├── main.py            # MCP + LangChain integration
│   │   ├── pyproject.toml     # Dependencies
│   │   ├── .env               # Environment variables (create this)
│   │   └── data/              # Conversation history
│   │
│   └── advanced-agent/        # Intelligent research agent
│       ├── main.py            # Workflow orchestration
│       ├── src/
│       │   ├── workflow.py    # LangGraph workflow definition
│       │   ├── models.py      # Pydantic data models
│       │   ├── prompts.py     # LLM prompts
│       │   └── firecrawl.py   # Web scraping service
│       ├── pyproject.toml     # Dependencies
│       └── .env               # Environment variables (create this)
│
├── documentation/            # Shared documentation dir
└── .devcontainer/            # Development container setup
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM access | ✅ |
| `FIRECRAWL_API_KEY` | Firecrawl API key for web scraping | ✅ |

### API Keys Setup

1. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Firecrawl API Key**: Get from [Firecrawl](https://firecrawl.dev/)

## 🎯 Use Cases

### For Developers
- **Tool Discovery**: Find the best libraries and services for your stack
- **Pricing Research**: Compare costs across different solutions
- **Technical Evaluation**: Assess API availability and integration capabilities
- **Competitive Analysis**: Understand the landscape of available tools

### For Product Managers
- **Market Research**: Analyze competitor offerings and pricing
- **Feature Planning**: Identify gaps in current tool ecosystem
- **Technical Due Diligence**: Evaluate potential technology partners

### For Technical Writers
- **Documentation Research**: Gather information about tools and APIs
- **Comparison Guides**: Create comprehensive tool comparisons
- **Market Analysis**: Stay updated on latest developer tools

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Set up your development environment (follow installation steps above)
4. Make your changes and add tests
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Areas for Contribution
- **New Research Workflows**: Add specialized research patterns
- **Additional Data Sources**: Integrate more web scraping services
- **Enhanced Analysis**: Improve LLM prompts and analysis logic
- **UI/UX Improvements**: Create web interfaces or CLI enhancements
- **Documentation**: Improve docs, add examples, create tutorials

## 🔧 Troubleshooting

### Common Issues

#### **"uv: command not found"**
- Make sure you've installed `uv` correctly
- Restart your terminal after installation
- On Windows, you may need to add `uv` to your PATH

#### **"Module not found" errors**
- Ensure you're using `uv run main.py` instead of `python main.py`
- Check that you've installed dependencies with `uv pip install -e .`
- Verify your virtual environment is activated

#### **"API key not found" errors**
- Create `.env` files in both `src/simple-agent/` and `src/advanced-agent/` directories
- Ensure your API keys are correctly formatted
- Restart your terminal after creating `.env` files

#### **Docker build issues**
- Make sure Docker is running
- Check that you have sufficient disk space
- Try building with `--no-cache` flag: `docker build --no-cache -f .devcontainer/Dockerfile -t dev-helper-agent .`

#### **MCP tools not working**
- Ensure Node.js 18+ is installed
- Run `npx firecrawl-mcp` to install MCP tools
- Check that your Firecrawl API key is valid

### Getting Help

If you encounter issues not covered here:
1. Check the [Issues](https://github.com/yourusername/Dev-Helper-MCP-Agent/issues) page
2. Search existing discussions
3. Create a new issue with detailed error information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


