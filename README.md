# CGSRef - Clean Content Generation System

A refactored, clean architecture implementation of the Content Generation System following Domain-Driven Design principles.

## Architecture Overview

This project implements Clean Architecture with clear separation of concerns:

```
📁 core/                    # Business Logic (Domain + Application + Infrastructure)
├── 📁 domain/             # Pure business logic, framework-agnostic
├── 📁 application/        # Use cases and application services
└── 📁 infrastructure/     # External services and data persistence

📁 api/                    # Interface Adapters
├── 📁 rest/              # REST API endpoints
├── 📁 cli/               # Command line interface
└── 📁 websocket/         # Real-time communication

📁 web/                    # User Interfaces
├── 📁 react-app/         # Modern React frontend
└── 📁 streamlit-legacy/  # Legacy Streamlit interface

📁 data/                   # Data storage
📁 tests/                  # Testing suite
📁 scripts/               # Utility scripts
📁 docs/                  # Documentation
```

## Key Principles

1. **Dependency Inversion**: Core business logic depends only on abstractions
2. **Single Responsibility**: Each module has one clear purpose
3. **Open/Closed**: Extensible without modifying existing code
4. **Interface Segregation**: Small, focused interfaces
5. **Clean Separation**: UI, business logic, and data access are completely separated

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+ (for React frontend)
- Docker (optional, for containerized deployment)

### Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd web/react-app && npm install
```

### Running the System
```bash
# Start API server
python -m api.rest.main

# Start React frontend
cd web/react-app && npm start

# Use CLI interface
python -m api.cli.main generate --topic "AI in Finance" --workflow siebert
```

## Development

### Adding New Features
1. Start with domain entities and business rules
2. Create use cases in the application layer
3. Implement infrastructure adapters
4. Add API endpoints
5. Update frontend components

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

## Documentation

- [Architecture Guide](docs/architecture/README.md)
- [API Documentation](docs/api/README.md)
- [User Guide](docs/user_guide/README.md)

## Migration from Legacy System

This system is designed to gradually replace the existing FylleCGS implementation while maintaining compatibility. The legacy system serves as reference during development.
