import requests
from bs4 import BeautifulSoup
import re
import csv
import time

def get_emails_from_url(url):
    """Scrape emails from a given webpage."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Extract emails from the page content
        emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}', response.text))
        return emails
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return set()

def search_google(query, num_results=10):
    """Use Google search to find relevant company recruitment pages."""
    search_url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error accessing Google search: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for g in soup.find_all('a', href=True):
        href = g['href']
        if 'url?q=' in href and 'webcache' not in href:
            link = href.split('url?q=')[1].split('&')[0]
            links.append(link)
            if len(links) >= num_results:
                break
    
    # Ajouter une pause pour éviter d'être bloqué par Google
    time.sleep(2)
    return links

def main():
    keywords = ["recrutement RH Caen", "contact RH entreprise Caen", "offres d'emploi Caen"]
    all_emails = set()
    
    for keyword in keywords:
        print(f"Searching Google for: {keyword}")
        urls = search_google(keyword)
        print(f"Found URLs: {urls}")  # Debug: Voir les URLs trouvées
        
        for url in urls:
            print(f"Scraping: {url}")
            emails = get_emails_from_url(url)
            print(f"Emails found on {url}: {emails}")  # Debug: Emails récupérés
            all_emails.update(emails)
    
    # Save to CSV
    with open("rh_emails_caen.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Email", "Source URL"])
        for email in all_emails:
            writer.writerow([email])
    
    print(f"Scraping completed. {len(all_emails)} emails saved to rh_emails_caen.csv")

if __name__ == "__main__":
    main()
