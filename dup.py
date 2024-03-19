def check_duplicates(links):
    # Convert the list to a set to remove duplicates
    unique_links = set(links)
    
    # Check if the length of the original list and the set are the same
    if len(links) == len(unique_links):
        print("No duplicate links found.")
    else:
        print("Duplicate links found.")

# List of links
links = [
            "https://edition.cnn.com/article/sitemap-2021.html",
            "https://edition.cnn.com/article/sitemap-2018.html",
            "https://edition.cnn.com/gallery/sitemap-2015.html",
            "https://edition.cnn.com/gallery/sitemap-2013.html",
            "https://edition.cnn.com/gallery/sitemap-2024.html",
            "https://edition.cnn.com/gallery/sitemap-2014.html",
            "https://edition.cnn.com/gallery/sitemap-2023.html",
            "https://edition.cnn.com/article/sitemap-2012.html",
            "https://edition.cnn.com/article/sitemap-2019.html",
            "https://edition.cnn.com/video/sitemap-2019.html",
            "https://edition.cnn.com/article/sitemap-2011.html",
            "https://edition.cnn.com/article/sitemap-2014.html",
            "https://edition.cnn.com/article/sitemap-2023.html",
            "https://edition.cnn.com/article/sitemap-2020.html",
            "https://edition.cnn.com/article/sitemap-2013.html",
            "https://edition.cnn.com/gallery/sitemap-2017.html",
            "https://edition.cnn.com/gallery/sitemap-2018.html",
            "https://edition.cnn.com/special/sitemap-2014.html",
            "https://edition.cnn.com/gallery/sitemap-2019.html",
            "https://edition.cnn.com/gallery/sitemap-2011.html",
            "https://edition.cnn.com/gallery/sitemap-2021.html",
            "https://edition.cnn.com/special/sitemap-2015.html",
            "https://edition.cnn.com/special/sitemap-2023.html",
            "https://edition.cnn.com/article/sitemap-2024.html",
            "https://edition.cnn.com/special/sitemap-2016.html",
            "https://edition.cnn.com/special/sitemap-2021.html",
            "https://edition.cnn.com/gallery/sitemap-2016.html",
            "https://edition.cnn.com/special/sitemap-2019.html",
            "https://edition.cnn.com/special/sitemap-2017.html",
            "https://edition.cnn.com/video/sitemap-2021.html",
            "https://edition.cnn.com/gallery/sitemap-2022.html",
            "https://edition.cnn.com/gallery/sitemap-2020.html",
            "https://edition.cnn.com/video/sitemap-2020.html",
            "https://edition.cnn.com/article/sitemap-2016.html",
            "https://edition.cnn.com/article/sitemap-2017.html",
            "https://edition.cnn.com/special/sitemap-2018.html",
            "https://edition.cnn.com/special/sitemap-2022.html",
            "https://edition.cnn.com/video/sitemap-2022.html",
            "https://edition.cnn.com/special/sitemap-2020.html",
            "https://edition.cnn.com/gallery/sitemap-2012.html",
            "https://edition.cnn.com/article/sitemap-2022.html",
            "https://edition.cnn.com/article/sitemap-2015.html",
]

# Call the function to check for duplicates
check_duplicates(links)
