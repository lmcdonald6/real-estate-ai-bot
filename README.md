# Real Estate AI Bot

An intelligent real estate analysis bot with lead scoring and property insights, leveraging ATTOM data for comprehensive property analysis.

## Features

### 1. Property Analysis
- Market value estimates with confidence scores
- Property details (beds, baths, sqft)
- Construction and system details
- Historical price trends

### 2. Lead Scoring & Prioritization
- Financial Distress Score (0-100)
- Time Pressure Score (0-100)
- Property Condition Score (0-100)
- Market Position Score (0-100)
- Automated lead categorization (Hot/Warm/Cold)

### 3. Market Analysis
- Price trends and sales velocity
- Neighborhood comparisons
- Rental market analysis
- Investment metrics

### 4. Investment Analysis
- After Repair Value (ARV) calculations
- Repair cost estimates
- Maximum Allowable Offer (MAO)
- ROI projections

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/lmcdonald6/real-estate-ai-bot.git
cd real-estate-ai-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Create a `.env` file in the project root
- Add your ATTOM API key:
```
ATTOM_API_KEY=your_api_key_here
```

5. Run the bot:
```bash
python run_bot.py
```

## Query Examples

1. Property Value:
```
what is the value of 123 Main St Bessemer?
```

2. Property Details:
```
show me property details for 456 Oak Ave
```

3. Owner Information:
```
who owns 123 Main St?
```

4. Distressed Properties:
```
find distressed properties with high equity in Bessemer
```

5. Market Analysis:
```
show me market trends for Bessemer
```

## Project Structure

```
real-estate-ai-bot/
├── src/
│   ├── __init__.py
│   ├── chat_interface.py      # Main chat interface
│   ├── real_estate_agent.py   # Core analysis logic
│   ├── data/
│   │   └── manager.py         # Data caching and retrieval
│   └── utils/
│       └── formatter.py       # Response formatting
├── tests/
│   └── test_chat.py          # Test suite
├── run_bot.py                # Entry point
├── setup.py                  # Package configuration
├── requirements.txt          # Dependencies
└── README.md                # Documentation
```

## Dependencies

- Python 3.8+
- aiohttp: Async HTTP requests
- python-dotenv: Environment management
- requests: HTTP client
- See `requirements.txt` for complete list

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.
