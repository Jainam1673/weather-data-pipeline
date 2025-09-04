# Contributing to Mojo Weather Data Pipeline

Thank you for your interest in contributing to the Mojo Weather Data Pipeline! This project demonstrates high-performance weather data processing using Mojo and real-time weather data integration.

## 🌟 How to Contribute

### 1. Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mojo-weather-pipeline.git
   cd mojo-weather-pipeline
   ```
3. **Set up the development environment**:
   ```bash
   ./setup.sh
   ```

### 2. Development Setup

#### Prerequisites
- **Pixi** package manager ([Install here](https://pixi.sh/latest/))
- **Internet connection** (for Open-Meteo API)
- **Linux/macOS** (recommended)

#### Environment Setup
```bash
# Install dependencies
pixi install

# Enter development environment
pixi shell

# Run tests
./test_pipeline.sh
```

### 3. Making Changes

#### Code Style Guidelines
- **Python**: Follow PEP 8 guidelines
- **Mojo**: Follow Mojo language conventions
- **Documentation**: Update docstrings and comments
- **Testing**: Add tests for new features

#### Areas for Contribution

1. **🔥 Mojo Performance Improvements**
   - SIMD optimizations
   - Memory management enhancements
   - Algorithm optimizations

2. **📊 Analytics Features**
   - New weather analysis algorithms
   - Additional statistical metrics
   - Machine learning integrations

3. **🌐 API Enhancements**
   - Additional weather data sources
   - Caching improvements
   - Rate limiting optimizations

4. **🎨 UI/UX Improvements**
   - New visualization types
   - Mobile responsiveness
   - Accessibility features

5. **🧪 Testing & Quality**
   - Unit tests
   - Integration tests
   - Performance benchmarks

### 4. Submitting Changes

#### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test your changes**:
   ```bash
   # Run the test suite
   ./test_pipeline.sh
   
   # Test the complete pipeline
   ./start_pipeline.sh
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your descriptive commit message"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub with:
   - Clear description of changes
   - Screenshots (for UI changes)
   - Test results
   - Performance impact (if applicable)

#### Commit Message Convention
We use conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `perf:` - Performance improvements

### 5. Code Review Process

1. **Automated checks** will run on your PR
2. **Manual review** by maintainers
3. **Feedback incorporation** if needed
4. **Merge** once approved

### 6. Reporting Issues

#### Bug Reports
When reporting bugs, please include:
- **Environment details** (OS, Mojo version, Python version)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** and logs
- **Screenshots** (if applicable)

#### Feature Requests
For new features, please include:
- **Use case description**
- **Proposed implementation** (if you have ideas)
- **Examples** of similar features
- **Potential impact** on performance

### 7. Development Tips

#### Working with Mojo
- **Performance testing**: Use built-in benchmarking
- **Memory management**: Follow ownership guidelines
- **SIMD usage**: Leverage vectorization opportunities

#### Working with APIs
- **Rate limiting**: Respect Open-Meteo API limits
- **Error handling**: Implement robust error handling
- **Caching**: Consider performance implications

#### Testing Guidelines
- **Unit tests**: Test individual functions
- **Integration tests**: Test component interactions
- **Performance tests**: Benchmark critical paths
- **End-to-end tests**: Test complete workflows

### 8. Community Guidelines

- **Be respectful** and inclusive
- **Provide constructive feedback**
- **Help others** learn and contribute
- **Follow the code of conduct**

### 9. Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Documentation**: Check the README.md
- **Examples**: Look at existing code patterns

### 10. Recognition

Contributors will be recognized in:
- **README.md** contributor section
- **Release notes** for significant contributions
- **GitHub contributor graphs**

## 📚 Additional Resources

- [Mojo Documentation](https://docs.modular.com/mojo/)
- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pixi Documentation](https://pixi.sh/latest/)

Thank you for contributing to the Mojo Weather Data Pipeline! 🌤️🔥
