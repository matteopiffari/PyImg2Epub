from pathlib import Path
from ebooklib import epub

IMAGE_EXT= [".jpg", ".jpeg", ".png"]

# ------------------------ CHANGE ME -----------------------------------
TITLE = "My E-Book"
AUTHOR = "Author Name"
DESCRIPTION = "This is a sample e-book created from chapters."
OUTPUT_DIR = Path("output")
# ----------------------------------------------------------------------

# Ensure the output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    for subdir in sorted(Path("chapters").iterdir()):
        if subdir.is_dir():
            # Extract chapter number from the directory path
            chapterNumber = subdir.name
            if not chapterNumber.isdigit():
                print(f"Skipping non-numeric chapter directory: {subdir.name}")
                continue

            print(f"Processing chapter: {chapterNumber}")

            # Create a new EPUB book
            book = epub.EpubBook()

            book.set_title(f"{TITLE} - Chapter {chapterNumber}")
            book.set_language('en')
            book.add_author(AUTHOR)

            # Adding metadata for calibre
            book.add_metadata('DC', 'description', DESCRIPTION)
            book.add_metadata(None, 'meta', '', {'name': 'calibre:series', 'content': TITLE})
            book.add_metadata(None, 'meta', '', {'name': 'calibre:series_index', 'content': chapterNumber})

            # Storing images in the subdirectory
            images = []

            for image in sorted(subdir.iterdir()):
                if image.is_file():
                    images.append(image)
            
            createEpubFromImages(book, images, chapterNumber)


def createEpubFromImages(book, images, chapterNumber):
    chapterPages = []

    for i in range(0, len(images), 2):
        if(i + 1 < len(images)):
            # Create a two-column layout for two images
            ext1 = images[i].suffix.lower()
            ext2 = images[i + 1].suffix.lower()

            if(ext1 in IMAGE_EXT and ext2 in IMAGE_EXT):
                content1 = None
                content2 = None

                # Read the first image
                with open(images[i], 'rb') as img_file:
                    content1 = img_file.read()

                # Read the second image
                with open(images[i + 1], 'rb') as img_file:
                    content2 = img_file.read()

                if(not content1 or not content2):
                    print(f"Skipping empty file: {images[i].name} or {images[i + 1].name}")
                    continue

                # Create EpubImage objects for both images
                image1 = epub.EpubImage()
                image1.content = content1
                image1.file_name = f"images/{chapterNumber}_{images[i].name}"

                if(ext1 == ".png"):
                    image1.media_type = "image/PNG"
                else:
                    image1.media_type = "image/JPEG"
                
                book.add_item(image1)

                image2 = epub.EpubImage()
                image2.content = content2
                image2.file_name = f"images/{chapterNumber}_{images[i + 1].name}"
                if(ext2 == ".png"):
                    image2.media_type = "image/PNG"
                else:
                    image2.media_type = "image/JPEG"
                
                book.add_item(image2)

                # Add the image to the book
                html_page = epub.EpubHtml(title=images[i].stem, file_name=f"{chapterNumber}_{images[i].stem}.xhtml")
                html_page.content = f'''
                <html>
                <head>
                    <style>
                        body {{
                            display: flex;
                            flex-direction: row;
                            margin: 0;
                            padding: 0;
                        }}
                        .page {{
                            width: 50%;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                        }}
                        .page img {{
                            max-width: 100%;
                            max-height: 90vh;
                            object-fit: contain;
                        }}
                    </style>
                    </head>
                    <body>
                        <div class="page">
                            <img src="{image1.file_name}" style="width:100%;"/>
                        </div>
                        <div class="page">
                            <img src="{image2.file_name}" style="width:100%;"/>
                        </div>
                    </body>
                </html>
                '''
                    
                book.add_item(html_page)
                chapterPages.append(html_page)

            else:
                print(f"Skipping unsupported file: {images[i].name} or {images[i + 1].name}")
                continue
        else:
            # Create a single column layout for the last image
            ext = images[i].suffix.lower()

            if ext in IMAGE_EXT:
                content = None

                # Read the image
                with open(images[i], 'rb') as img_file:
                    content = img_file.read()

                if(not content):
                    print(f"Skipping empty file: {images[i].name}")
                    continue

                # Create EpubImage object for the image
                image = epub.EpubImage()
                image.content = content
                image.file_name = f"images/{chapterNumber}_{images[i].name}"

                if(ext == ".png"):
                    image.media_type = "image/PNG"
                else:
                    image.media_type = "image/JPEG"

                book.add_item(image)

                # Add the image to the book
                html_page = epub.EpubHtml(title=images[i].stem, file_name=f"{chapterNumber}_{images[i].stem}.xhtml")
                html_page.content = f'''
                <html>
                <head>
                    <style>
                        body {{
                            display: flex;
                            flex-direction: row;
                            margin: 0;
                            padding: 0;
                        }}
                        .page {{
                            width: 100%;
                        }}
                    </style>
                    </head>
                    <body>
                        <h2>{images[i].stem}</h2>
                        <img src="{image.file_name}" alt="{images[i].stem}"/>
                    </body>
                </html>
                '''
                
                book.add_item(html_page)
                chapterPages.append(html_page)
            else:
                print(f"Skipping unsupported file: {images[i].name}")
                continue
    
    # Add the images to the book's spine
    for page in chapterPages:
        book.spine.append(page)

    book.toc = chapterPages
    
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Save the book
    OutputFile = OUTPUT_DIR / f"{chapterNumber}.epub"
    epub.write_epub(str(OutputFile), book)
    print(f"Epub saved: {OutputFile}")



if __name__=="__main__":
    main()