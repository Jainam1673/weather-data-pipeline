# Security Policy

## Supported Versions

We actively support the following versions of the Mojo Weather Data Pipeline:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in the Mojo Weather Data Pipeline, please report it responsibly:

### Reporting Process

1. **DO NOT** create a public issue for security vulnerabilities
2. Email security reports to: [your-email@example.com] (replace with actual email)
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

### Response Timeline

- **Initial Response**: Within 24-48 hours
- **Assessment**: Within 1 week
- **Fix Timeline**: Depends on severity
  - Critical: 1-3 days
  - High: 1-2 weeks
  - Medium: 2-4 weeks
  - Low: Next release cycle

### Security Considerations

#### API Security
- Open-Meteo API is public and requires no authentication
- No sensitive data is stored in the application
- All API calls are made over HTTPS

#### Data Privacy
- Weather data is public information
- No personal information is collected
- Local SQLite database stores only weather metrics

#### Infrastructure
- Application runs locally by default
- No cloud services required
- All dependencies managed through Pixi

### Safe Usage Guidelines

1. **Network Security**: Ensure your network connection is secure when fetching API data
2. **Local Access**: The web interface (port 8501) should not be exposed to public networks without proper security measures
3. **Dependencies**: Keep Pixi and Mojo environments updated
4. **API Limits**: Respect Open-Meteo API rate limits (10k requests/day)

### Known Security Considerations

- **Local Database**: SQLite database is stored locally without encryption (contains only public weather data)
- **API Keys**: Not required for Open-Meteo API (no authentication needed)
- **Network Traffic**: All external API calls are made over HTTPS

## Security Best Practices

When deploying or modifying this application:

1. **Keep dependencies updated**: Regularly update Pixi environment
2. **Secure deployment**: Don't expose internal ports to public networks
3. **Monitor API usage**: Stay within Open-Meteo rate limits
4. **Regular backups**: Backup your weather data if needed
5. **Environment isolation**: Use Pixi environments for dependency isolation

## Contact

For security-related questions or concerns, please contact:
- GitHub Issues: For non-security bugs
- Email: [your-email@example.com] for security vulnerabilities

Thank you for helping keep the Mojo Weather Data Pipeline secure!
