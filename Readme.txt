📌 Project Overview

This project uses web scraping techniques to collect:

* Latest news headlines
* Article URLs
* Full article content

The data is saved as a structured JSON file and can be used for:

* Data analysis
* News aggregation
* Building dashboards (Power BI / Tableau)
* NLP projects

⚙️ Technologies Used

* Python
* requests
* BeautifulSoup (bs4)
* pandas
* lxml

 🚀 Features

* Safe HTTP requests with retry mechanism
* Automatic extraction of article links
* Duplicate link removal
* Article content scraping
* JSON data export
* Simple and clean output display

 📂 Project Structure

```
toi-news-scraper/
│
├── toi_scraper.py     # Main script
├── toi_YYYY-MM-DD.json  # Output file (generated)
└── README.md          # Project documentation
```

🛠️ Installation

1. Clone the repository or download the code

2. Install required libraries:

```
pip install requests beautifulsoup4 pandas lxml
```

 ▶️ Usage

Run the script using:

```
python toi_scraper.py
```

📄 Output

The script generates a JSON file like:

```
toi_2024-05-06.json
```

Each record contains:

* `title` → News headline
* `link` → Article URL
* `content` → Full article text

 ⚠️ Important Notes

* The website structure may change, which can affect scraping
* Some content may not load if it is rendered using JavaScript
* Use delays (`time.sleep`) to avoid getting blocked
* This script is for educational purposes only
