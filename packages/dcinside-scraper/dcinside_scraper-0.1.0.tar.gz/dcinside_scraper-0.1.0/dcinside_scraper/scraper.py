import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import argparse

def scrape_dcinside(gallery_url, start_page, end_page, output_file, sleep_time=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    data = []

    for page in range(start_page, end_page + 1):
        url = f"{gallery_url}&page={page}"
        print(f"Fetching page: {page}")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('tr', class_='ub-content')
        print(f"Number of posts found: {len(posts)}")

        for post in posts:
            title_tag = post.find('td', class_='gall_tit').find('a')
            author_tag = post.find('td', class_='gall_writer')
            ip_tag = author_tag.find('span', class_='ip') if author_tag else None
            date_tag = post.find('td', class_='gall_date')
            view_tag = post.find('td', class_='gall_count')
            recommend_tag = post.find('td', class_='gall_recommend')

            title = title_tag.text.strip() if title_tag else 'N/A'
            author = author_tag.get('data-nick', 'N/A') if author_tag else 'N/A'
            ip = ip_tag.text.strip() if ip_tag else 'N/A'
            date = date_tag.get('title', 'N/A') if date_tag else 'N/A'
            views = view_tag.text.strip() if view_tag else 'N/A'
            recommends = recommend_tag.text.strip() if recommend_tag else 'N/A'

            print(f"Title: {title}, Author: {author}, IP: {ip}, Date: {date}, Views: {views}, Recommends: {recommends}")
            data.append([title, author, ip, date, views, recommends])
        
        if sleep_time > 0:
            time.sleep(sleep_time)

    df = pd.DataFrame(data, columns=['Title', 'Author', 'IP', 'Date', 'Views', 'Recommends'])
    df.to_csv(output_file, sep='\t', index=False)
    print(f"Data saved to '{output_file}'")

def main():
    parser = argparse.ArgumentParser(description='Scrape posts from DCInside')
    parser.add_argument('gallery_url', type=str, help='The URL of the DCInside gallery')
    parser.add_argument('start_page', type=int, help='The starting page number')
    parser.add_argument('end_page', type=int, help='The ending page number')
    parser.add_argument('output_file', type=str, help='The output TSV file')
    parser.add_argument('--sleep', type=int, default=0, help='Time to sleep between page requests (in seconds)')

    args = parser.parse_args()
    scrape_dcinside(args.gallery_url, args.start_page, args.end_page, args.output_file, args.sleep)

if __name__ == "__main__":
    main()
