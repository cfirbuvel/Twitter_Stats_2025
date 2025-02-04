# Twitter Mention Analyzer Bot 🐦📊

A powerful bot that analyzes Twitter mentions through the Twitter API v2 and delivers insights via Telegram. Features real-time analysis, sentiment detection, and customizable filters.

![Bot Demo](https://via.placeholder.com/800x400.png?text=Twitter+Analysis+Bot+Demo) *Add actual demo screenshot/gif here*

## Features ✨

- **Smart Filters** 🔍
  - Minimum mentions threshold
  - Custom date ranges (24h/7d/30d/custom)
  - Result count limits
  - Hashtag filtering

- **Rich Analytics** 📈
  - Sentiment analysis (Positive/Neutral/Negative)
  - Top mentioned users
  - Popular hashtags
  - Mention frequency trends
  - Engagement metrics

- **Telegram UI** 💬
  - Interactive buttons/menus
  - Paginated results
  - CSV/JSON exports
  - Scheduled reports

- **Enterprise Ready** 🔒
  - Redis caching
  - Rate limiting
  - Docker support
  - Configurable thresholds

## Installation 🛠️

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Twitter API v2 Bearer Token
- Telegram Bot Token

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/twitter-bot.git
cd twitter-bot

# Copy environment file
cp .env.example .env

# Install dependencies
docker-compose build

# Run the bot
docker-compose up -d
```

## Configuration ⚙️

1. **Get API Keys** 🔑
   - Twitter: [Developer Portal](https://developer.twitter.com/)
   - Telegram: [@BotFather](https://t.me/BotFather)

2. **Edit .env file**
```env
TELEGRAM_TOKEN=your_telegram_bot_token
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
REDIS_URL=redis://redis:6379/0
```

3. **Build & Run** 🚀
```bash
docker-compose up --build -d
```

## Usage 📲

1. Start the bot in Telegram: `/start`
2. Set parameters through interactive menu:
   - 🔍 Search username
   - 🔢 Set minimum mentions
   - 📈 Choose result count
   - ⏳ Select time range
3. Click "Start Scrape" to begin analysis

**Example Commands**:
```
/analyze @elonmusk --min-mentions 20 --days 7
/stats @openai --format csv
/alerts set 50 --daily
```

## Features in Development 🚧
- [ ] Automated daily/weekly reports
- [ ] Competitor comparison analysis
- [ ] Network graph visualization
- [ ] Multi-language support
- [ ] Trending topic integration

## Contributing 🤝
1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```
3. Commit your changes:
```bash
git commit -m 'Add some amazing feature'
```
4. Push to the branch:
```bash
git push origin feature/amazing-feature
```
5. Open a pull request

## License 📄
Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments 🏆
- Twitter API v2 - For the powerful social data
- Telegram Bot API - For the intuitive messaging platform
- Redis - For blazing fast caching
- Python-Telegram-Bot - For excellent bot framework
