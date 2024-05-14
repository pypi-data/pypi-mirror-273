import traceback
import tracemalloc
import logging
import os
import shutil
import yaml
import string
import requests
import httpx
import re
import time
import pytz
import datetime
import hashlib
import tempfile
import random
from markdown_it import MarkdownIt
import gradio as gr
import getpass
import asyncio
import uuid
import argparse
import mimetypes
import qrcode
from bs4 import BeautifulSoup
from pyppeteer import launch
from pypdf import PdfMerger, PdfWriter, PdfReader
from io import BytesIO
from Cryptodome.Hash import SHA256


def generate_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def hash_password(password, salt):
    key = SHA256.new(password.encode('utf-8') + salt).digest()
    return key

def merge_pdfs(output_file, input_files):
    try:
        merger = PdfMerger()
        for file in input_files:
            merger.append(file)
        with open(output_file, 'wb') as merged_pdf:
            merger.write(merged_pdf)
        print('[SUCCESS] Merge operation completed.')
    except Exception as e:
        print(e)

def extract_pages(input_file, output_file, start_page, end_page):
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        for page_num in range(start_page - 1, end_page):
            writer.add_page(reader.pages[page_num])

        with open(output_file, 'wb') as extracted_pdf:
            writer.write(extracted_pdf)
        print('[SUCCESS] Extract operation completed.')

    except Exception as e:
        print(f'[ERROR] {e}')

def split_pdf(input_file, output_prefix, split_page):
    reader = PdfReader(input_file)
    try:
        for page_num in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])

            output_file = f"{output_prefix}_{page_num + 1}.pdf"
            with open(output_file, 'wb') as output_pdf:
                writer.write(output_pdf)

        print('[SUCCESS] Split operation completed.')
    except Exception as e:
        print(f'[ERROR] {e}')

def extract_text(input_file, output_text_file):
    reader = PdfReader(input_file)
    text = ""
    try:
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extractText()
        with open(output_text_file, 'w', encoding='utf-8') as text_file:
            text_file.write(text)

        print('[SUCCESS] Text extraction operation completed.')
    except Exception as e:
        print(f'[ERROR] {e}')

def remove_metadata(input_file, output_file):
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        writer.removeMetadata()

        with open(output_file, 'wb') as output_pdf:
            writer.write(output_pdf)

        print('[SUCCESS] Remove metadata operation completed.')
    except Exception as e:
        print(f'[ERROR] {e}')

def select_remove_metadata(input_file, output_file, selected_metadata):
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        for page_num in range(len(reader.pages)):
            writer.add_page(reader.pages[page_num])

        writer.removeMetadata(selected_metadata)

        with open(output_file, 'wb') as output_pdf:
            writer.write(output_pdf)

        print('[SUCCESS] Selective metadata removal operation completed.')
    except Exception as e:
        print(f'[ERROR] {e}')

async def insert_img(pdf_page, image_path):
    c = canvas.Canvas(pdf_page)
    img = ImageReader(image_path)
    c.drawImage(img, 100, 100)
    c.showPage()
    c.save()

async def process_img_link(input_file, md_doc, tmp_dir):
    pattern = re.compile(r'\[(.*?)\]\((https?://[^\s\)]+|[^)]+)\)')
    links = pattern.findall(md_doc)

    image_mime_types = ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/webp"]

    tasks = []
    try:
        async with httpx.AsyncClient() as client:
            for idx, (link_text, url) in enumerate(links):
                image_file = f"img_{idx}.png"
                image_path = os.path.abspath(os.path.join(tmp_dir, image_file))
                if url.startswith('http://') or url.startswith('https://'):
                    response = await client.head(url)
                    if response.status_code == 200:
                        content_type = response.headers.get("content-type", "").lower()
                        if any(content_type.startswith(mime) for mime in image_mime_types):
                            response = await client.get(url)
                            image_data = response.content
                            with open(image_path, "wb") as file:
                                file.write(image_data)
                            tasks.append(image_path)
                        else:
                            print(f"[WARN] URL {idx} is not an image.")
                    else:
                        print(f"[ERROR] Cannot fetch image file {idx}.")
                elif os.path.isfile(url):
                    # url = os.path.dirname(url)
                    # image_path = os.path.dirname(image_path)
                    print(f'[INFO] Copy {url} to {image_path}')
                    shutil.copy(url, image_path)
                    tasks.append(url)
        print(tasks)
        return tasks

    except Exception as e:
        print(f'[ERROR] {e}')

async def add_qr(input_files, qr_params, tmp_dir, tmp_file):
    try:
        for input_file in input_files:
            temp_md_file = f'{tmp_file}.md'
            if input_file.lower().endswith(".md"):
                with open(input_file, "r") as file:
                    md_doc = file.read()

                    pattern = re.compile(r'\[(.*?)\]\((https?://[^\s\)]+|[^)]+)\)')
                    links = pattern.findall(md_doc)
                    tasks = []
                    for idx, (link_text, url) in enumerate(links):
                        qr_file = f"qr_{idx}.png" # TODO
                        qr_path = os.path.join(tmp_dir, f"qr_{idx}.png")
                        task = asyncio.ensure_future(gen_qr(link_text, qr_path, **qr_params))
                        tasks.append((link_text, url, qr_file, task))

                    for link_text, url, qr_file, task in tasks:
                        qr = await task
                        if qr:
                            qr_link = f"![]({qr_file})"
                            md_doc = md_doc.replace(f"[{link_text}]({url})", f"<div class='qr'>\n\n[{link_text}]({url}) {qr_link}\n</div>")

                with open(temp_md_file, "w") as file:
                    file.write(md_doc)

        return tmp_dir
        print(f'[INFO] Temporary markdown docs in: {temp_md_file}')
        print(f'[INFO] QRs in: {tmp_dir}')
    except Exception as e:
        print(f'[ERROR] {e}')

async def gen_qr(data, out_path, **qr_params):
    try:
        qr = qrcode.QRCode(**qr_params)
        qr.add_data(data)
        img = qr.make_image(fill_color="black", back_color="white")
        box_size = int(qr_params['box_size'])
        img = img.resize((box_size, box_size))
        img.save(out_path, 'PNG')
        return qr
    except Exception as e:
        print(f"Failed to generate QR code for {data}: {str(e)}")
        traceback.print_exc()
        return None

def encrypt_pdf(not_encrypted_file, encrypted_file, password):
    reader = PdfReader(open(not_encrypted_file, 'rb'))
    writer = PdfWriter()
    writer.encrypt(password)

    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        writer.add_page(page)
    with open(encrypted_file, 'wb') as output_pdf:
        writer.write(output_pdf)

def decrypt_pdf(input_pdf_path, output_pdf_path, params):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    if reader.is_encrypted:
        reader.decrypt(params['password'])
    for page in reader.pages:
        writer.add_page(page)

    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

async def generate_pdf(input_files, output_file, params, tmp_dir, tmp_file):
    html_dir = os.path.dirname(input_files[0])
    os.chdir(html_dir)
    browser = await launch(
        args=[
        '--headless',
        ]
    )
    page = await browser.newPage()
    merger = PdfMerger()

    md = MarkdownIt()
    try:
        for index, input_file in enumerate(input_files):
            temp_html_file = f'{tmp_file}.html'
            if input_file.lower().endswith(".md"):
                with open(input_file, "r", encoding="utf-8") as file:
                    markdown_data = file.read()
                    html_data = md.render(markdown_data)
            else:
                with open(input_file, "r", encoding="utf-8") as file:
                    html_data = file.read()

            await page.setContent(html_data)

            css_file = params.get('css')
            if css_file:
                if css_file.startswith('http://') or css_file.startswith('https://'):
                    css_link = f'<link rel="stylesheet" type="text/css" href="{css_file}">\n'
                    html_data = css_link + html_data
                    await page.goto(css_file)
                elif os.path.isfile(css_file):
                    with open(css_file, "r", encoding="utf-8") as css_file:
                        css_content = css_file.read()
                        css_style = f'<style>\n{css_content}\n</style>\n'
                        html_data = css_style + html_data
                    await page.addStyleTag({'path': os.path.abspath(css_file)})
                else:
                    # css_content = css_file.read() # TODO
                    css_style = f'<style>\n{css_file}\n</style>\n'
                    html_data = css_style + html_data
                    await page.addStyleTag({'content': css_file})

            await page.emulateMedia(params['emulateMedia'])

            with open(temp_html_file, "w", encoding="utf-8") as file:
                file.write(html_data)

            pdf_data = await page.pdf(params)

            pdf_buffer = BytesIO(pdf_data)

            tasks = await process_img_link(input_file, markdown_data, tmp_dir)
            for image_path in tasks:
                pass
                # await insert_img(pdf_buffer, image_path) # TODO
            merger.append(pdf_buffer)

            # if os.path.exists(temp_html_file):
            #     os.remove(temp_html_file)

        if params.get('metadata'):
            merger.add_metadata(params.get('metadata'))

        return output_file

    except Exception as e:
        print(f'[ERROR] {e}')

    finally:
        await browser.close()
        merger.write(output_file)

        merger.close()
        print(f'[INFO] Temporally html data : {temp_html_file}')
        print(f'[SUCCESS] Output : {output_file}')

def parse_input(files):
    ts, tmp_dir = Interface.get_tempdir()
    input_files = []

    for file in files:
        mime_type, _ = mimetypes.guess_type(file)
        if mime_type and mime_type.startswith('text'):
            try:
                if file.startswith("http://") or file.startswith("https://"):
                    response = requests.get(file)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        content = soup.get_text()
                        filename = os.path.join(tmp_dir, os.path.basename(file))
                        with open(filename, 'w', encoding='utf-8') as md_file:
                            md_file.write(content)

                        input_files.append(filename)
                        print(f"[INFO] Temporary file from '{file}' to {filename}")
                    else:
                        print(f"[FAILED] to retrieve content from {file}")
                else:
                    input_files.append(os.path.abspath(file))
            except Exception as e:
                print(f"[ERROR] {e}")
        elif mime_type and mime_type.startswith('application'):
            print(f"[INFO] File is application/* file.")
        else:
            print(f"[ERROR] File '{file}' is not a human-readable.")

    return input_files

def parse_margin(value):
    parts = value.split()
    result = {}
    i = 0
    key = None

    for i in range(len(parts)):
        if not re.match(r'\d+', parts[i]):
            key = parts[i]

        for j in range(i + 1, len(parts)):
            if re.match(r'\d+', parts[j]):
                if key is not None and key not in result:
                    result[key] = parts[j]
                break

    return result

def parse_metadata(value):
    parts = value.split()
    result = {}
    current_key = None

    for part in parts:
        if current_key is None:
            current_key = part
        else:
            result[current_key] = part
            current_key = None

    return result

def parse_template(template_str):
    if template_str.startswith("http://") or template_str.startswith("https://"):
        response = requests.get(template_str)
        if response.status_code == 200:
            return response.text
        else:
            raise ValueError("Failed to fetch template from URL.")

    elif os.path.isfile(template_str):
        with open(template_str, "r", encoding="utf-8") as file:
            return file.read()

    else:
        return template_str


class Interface:

    def get_tempdir():
        timestamp = int(time.time())
        temp_dir = tempfile.mkdtemp()
        return timestamp, temp_dir


class WebAPI:

    def share_file(cloud_service, username, password, input_file):
        if cloud_service == "google_drive":
            print("Using Google Drive for sharing.")
            try:
                file_url = WebAPI.upload_to_google_drive(username, password, input_file)
            except Exception as e:
                print(f"Error: {e}")
        elif cloud_service == "slideshare":
            print("Using SlideShare for sharing.")
            try:
                file_url = WebAPI.upload_to_slideshare(username, password, input_file)
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Unsupported cloud service")

    def upload_to_google_drive(username, password, input_file):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)
        file_name = os.path.basename(input_file)
        file_drive = drive.CreateFile({'title': file_name})
        file_drive.Upload()
        file_url = file_drive['alternateLink']
        print(f"File uploaded to Google Drive. URL: {file_url}")

        return file_url

    def upload_to_slideshare(username, password, input_file, title=None, description=None, tags=None):
        upload_url = 'https://www.slideshare.net/api/2/upload_slideshow'
        auth = (username, password)

        if f"SLIDESHARE_API_KEY" in os.environ and f"SLIDESHARE_API_SECRET" in os.environ  :
            api_key = os.getenv[f"SLIDESHARE_API_KEY"]
            api_secret = os.getenv[f"SLIDESHARE_API_SECRET"]
        else:
            api_key = getpass.getpass(f"Enter SLIDESHARE API KEY:")
            api_secret = getpass.getpass(f"Enter SLIDESHARE API SECRET:")

        tz = pytz.utc
        now = datetime.datetime.now(tz)
        utime = int(now.timestamp())
        hash_salt = api_secret+str(utime)
        hash_value = hashlib.sha1(hash_salt.encode('utf-8')).hexdigest()

        with open(input_file, 'rb') as file:
            files = {'slideshow': (input_file, file)}
            data = {
                'slideshow_title': title,
                'slideshow_description': description,
                'slideshow_tags': tags
            }
            params = {
                'api_key': api_key,
                'ts': str(utime),
                'hash': hash_value,
                'username_for': username
            }

            response = requests.post(upload_url, data=data, params=params, files=files, auth=auth)

            if response.status_code == 200:
                file_url = response.url # TODO
                return f"File uploaded to SlideShare.  URL: {file_url}"
            else:
                return f"Upload error: {response.status_code}"


def clear_directory():
    try:
        dir = "/tmp/"
        for root, dirs, files in os.walk(dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        gr.Info(f'Clear cache done.')
    except Exception as e:
        gr.Error(f'Failed to delete files in {dir}. Reason: {e}')

async def webui(params, usage_doc):
    async def wrapper(files, styles, header, footer, exec_clear):
        if exec_clear:
            clear_directory()

        ts, tmp_dir = Interface.get_tempdir()
        tmp_file = f'{tmp_dir}/{ts}'
        os.makedirs(tmp_dir, exist_ok=True)

        input_files = [os.path.abspath(file) for file in files[0].name]
        output_file = tmp_file + '.pdf'

        params = {
            'emulateMedia': 'screen',
            'scale': 1,
            'format': 'a4',
            'css': styles.name if styles else None,
            'headerTemplate': header.name if header else None,
            'footerTemplate': footer.name if footer else None,
        }

        processing_file = await generate_pdf(input_files, output_file, params, tmp_dir, tmp_file) # TODO

        gr.Info(f'[SUCCESS] Output to: {args.output}')

        return processing_file


    version = 'v0.1.0'
    with gr.Blocks(
        css='footer {visibility: hidden}', title='DocMaker Web UI'
        ) as app:
        gr.HTML(f"<div style='max-width:100%; max-height:360px; text-align: center; overflow:auto'><h1>DocMaker Web UI {version}</h1></div>")
        with gr.Row(variant='panel'):
            clr_cache_btn = gr.ClearButton(value='C')
            run_btn = gr.Button(value='▶', variant="primary")

        with gr.Tab('Processor') as tab1:
            with gr.Row():
                with gr.Column(variant='panel') as col1:
                    input_file = gr.Files(label="demo.md", elem_id=f'{uuid.uuid4()}')
                    with gr.Accordion("Style", open=True):
                        input_style = gr.File(label="style.css", elem_id=f'{uuid.uuid4()}')
                    with gr.Accordion("Template", open=True):
                        input_header_html = gr.File(label="header.html", elem_id=f'{uuid.uuid4()}')
                        input_footer_html = gr.File(label="footer.html", elem_id=f'{uuid.uuid4()}')

                with gr.Column(variant='panel'):
                    output_file = gr.File(elem_id=f'{uuid.uuid4()}')

        with gr.Tab('Help') as tab2:
            with gr.Row():
                gr.Markdown(f'''
                # Convert any document format to PDF format.

                ### CLI Usage

                ```bash
                {usage_doc}
            ```
                ''')

        inputs = [
            input_file,
            input_style,
            input_header_html,
            input_footer_html,
            clr_cache_btn
        ]

        outputs = [
            output_file,
        ]
        examples = [
            [['contents/markdown/demo_1.md'], 'static/style/style_01.css', 'static/templates/template_01.html'],
            [None, None, None, None],
        ]
        gr.Examples(examples, inputs)
        run_btn.click(wrapper, inputs, outputs)

    app.queue().launch(
        # inline=True,
        inbrowser=False,
        # share=True,
        # debug=True,
        # max_threads=40,
        # auth=('test','pass'),
        # auth_message=auth_message,
        # prevent_thread_lock=False,
        show_error=True,
        server_name=None,
        # server_port=None,
        # show_tips=False,
        # height=,
        # width=,
        # encrypt=,
        # favicon_path="assets/favicon.ico",
        ssl_keyfile=None,
        ssl_certfile=None,
        ssl_keyfile_password=None,
        ssl_verify=True,
        quiet=False,
        # show_api=False,
        # file_directories=False,
        # allowed_paths=False,
        # blocked_paths=False,
        # root_path=False,
        # app_kwargs=False
        )

def choose_file(input_files):
    while True:
        print("Which file would you like to process?")
        for i, input_file in enumerate(input_files):
            print(f"{i + 1}. {input_file}")

        choice = input()
        try:
            choice = int(choice)
            if 1 <= choice <= len(input_files):
                return input_files[choice - 1]
            else:
                print("Invalid choice. Please select a valid file.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

async def main():
    tracemalloc.start()
    logger = logging.getLogger("httpx")
    logger.setLevel(logging.ERROR)

    parser = argparse.ArgumentParser(description="Generate PDF from HTML pages.")

    parser.add_argument("-i", "--input", nargs="+", help="Input files.")
    parser.add_argument("-o", "--output", help="Output file path.")
    parser.add_argument("--scale", type=float, help="Scale of the printed page | 0.8 for 80 percent.")
    parser.add_argument("--displayHeaderFooter", action="store_true", help="Display header and footer.")
    parser.add_argument( "--headerTemplate", type=parse_template, help="Add header template as [url|path|content].", )
    parser.add_argument( "--footerTemplate", type=parse_template, help="Add footer template as [url|path|content].", )
    parser.add_argument("--printBackground", action="store_true", help="Print background images.")
    parser.add_argument("--landscape", action="store_true", help="Use landscape paper orientation.")
    parser.add_argument("--pageRanges", type=str, help="Page ranges to print | '1-5,8,11-13'.")
    parser.add_argument("--format", type=str, help="Paper format | 'A4'.")
    parser.add_argument("--width", type=str, help="Paper width | '10cm'.")
    parser.add_argument("--height", type=str, help="Paper height | '10mm'.")
    parser.add_argument("--margin", type=parse_margin, help="Margin values (e.g., 'top 10mm right 10mm')")
    parser.add_argument("--css", type=str, help="Add css as [url|path|content]")
    parser.add_argument("--config", type=str, help="Path to the config file.")
    parser.add_argument("--emulateMedia", type=str, choices=['screen', 'print'], default='screen', help="Type of emulate media.")
    parser.add_argument("--qr", type=int, help="Add QR after link.")

    parser.add_argument("--merge", nargs='+', help="Merge PDF files into an output file")
    parser.add_argument("--extract", help="Extract pages from a PDF file (e.g., '1-3')")
    parser.add_argument("--split", action='store_true', help="Split a PDF file at specified pages")
    parser.add_argument("--extract-text", action='store_true', help="Extract text from a PDF file") # TODO
    parser.add_argument("--redact-text", nargs='+', help="Redact text in the PDF files")
    parser.add_argument("--metadata", type=parse_metadata, help="Add metadata in the format '/Key: Value'. Example: '/Title Document'")
    parser.add_argument("--remove-metadata", action='store_true', help="Remove metadata from a PDF file")
    parser.add_argument("--select-remove-metadata", nargs='+', help="Selectively remove metadata fields")

    parser.add_argument("--verbose", action="store_true", help="Print parameters when verbose.")

    parser.add_argument("--encrypto", action="store_true", help="Encrypt PDF file.")
    parser.add_argument("--autogen", action="store_true", help="Automatically generate password for encryption.")
    parser.add_argument("--decrypto", action="store_true", help="Decrypt PDF file.")
    parser.add_argument("--regen", action="store_true", help="Regenerate and send recovery key for decryption.")

    parser.add_argument("--webui", action="store_true", help="[WIP] Launch Gradio web UI.")

    parser.add_argument("--share", choices=["google_drive", "slideshare"], help="Specify the cloud service to use for sharing")

    parser.usage = '''
        [Examples]

        Generate:
            From local file:
                python app.py -i in_*.html --verbose

            From remote file:
                set gist https://gist.githubusercontent.com/.../gistfile.md
                python app.py -i $gist

            Styling:
                python app.py -i in_*.html --scale 0.8 --css ' h1 { color: red }' --margin 'top bottom 50mm left right 20mm'

            Load Config:
                python app.py --config config.yaml

        Modify:
            Extract pages:
                python app.py -i in.pdf --extract 2-3

            Metadata
                python app.py -i in.md --metadata '/Title Untitled'

        Encrypt/Decrypto:
            python app.py -i demo.pdf -o demo.encrypted.pdf --encrypto --autogen
            python app.py -i demo.encrypted.pdf -o demo.decrypted.pdf --decrypto

        Share:
            python -i $gist -o out.pdf --share slideshare


        [Units]

        You can use the following units for width, height, and margin options:
        - px (pixels) - Default unit., in (inches)., cm (centimeters)., mm (millimeters).


        [Formats]

        The following paper formats are available for the format option:
        - Letter, Legal, Tabloid, Ledger, A0, A1, A2, A3, A4 (default), A5


        [PDF Metadata]

        Metadata format: "/Key Value" pairs separated by space.
        - /Title, /Author, /Subject, /Author, /Keyword, /Creator, /Producer, /CreateDate,  /ModDate, /Trapped
        '''

    args = parser.parse_args()
    params = {}

    if args.config:
        with open(args.config, "r") as config_file:
            config_data = yaml.safe_load(config_file)
            params = config_data.get("params", {})

    for key, value in vars(args).items():
        if value is not None and value is not False:
            params[key] = value

    if args.verbose:
        print('---')
        for key, value in params.items():
            print(f'{key}: {value}')
        print('---')

    if args.input:
        ts, tmp_dir = Interface.get_tempdir()
        tmp_dir = f'{tmp_dir}/{ts}'
        tmp_file = f'{tmp_dir}/{ts}'
        os.makedirs(tmp_dir, exist_ok=True)

        input_files = parse_input(args.input)
        processing_files = []

        if args.output:
            result_file = os.path.abspath(args.output)
        else:
            base = os.path.splitext(os.path.basename(file))[0] + f'.pdf'
            abspath_dir = os.path.abspath(base)
            result_file = os.path.join(abspath_dir, base)
            print(f'[INFO] Output will: {result_file}')

        for index, file in enumerate(input_files):
            mime_type, _ = mimetypes.guess_type(file)
            if mime_type and mime_type.startswith('application'):
                processing_files.append(result_file)
            elif mime_type and mime_type.startswith('text'):
                processing_files.append(result_file)
            else:
                print(f"[ERROR] Unsupported file type for {file}")
        print()

        if args.qr:
            qr_params = {
                'version': 1,
                'error_correction': qrcode.constants.ERROR_CORRECT_L,
                'box_size': params['qr'],
                'border': 1,
            }
            await add_qr(input_files, qr_params, tmp_dir, tmp_file)

        processing_file = await generate_pdf(input_files, result_file, params, tmp_dir, tmp_file)

        if args.merge:
            choosen_file = choose_file(processing_files)
            merge_pdfs(args.merge[0], args.merge[1:])

        if args.extract:
            choosen_file = choose_file(processing_files)
            page_range = args.extract
            start_page, end_page = map(int, page_range.split('-'))
            extract_pages(choosen_file, result_file, start_page, end_page)

        if args.split:
            choosen_file = choose_file(processing_files)
            split_pdf(choosen_file, result_file, 1)

        if args.extract_text:
            choosen_file = choose_file(processing_files)
            extract_text(choosen_file, result_file)
        if args.remove_metadata:
            choosen_file = choose_file(processing_files)
            remove_metadata(choosen_file, result_file)

        if args.select_remove_metadata:
            choosen_file = choose_file(processing_files)
            select_remove_metadata(choosen_file, result_file, args.select_remove_metadata)

        if args.encrypto and args.decrypto:
            print("[ERROR] Cannot specify both --encrypto and --decrypto options simultaneously.")

        elif args.encrypto:
            if processing_file:
                not_encrypted_file = processing_file
            else:
                choosen_file = choose_file(args.input)
                not_encrypted_file = choosen_file
            encrypted_file = result_file

            if args.autogen:
                password = generate_password()
                password_confirm = None
                print(f"[INFO] Output to: {args.output}")
                print("PASS:", password)
                encrypt_pdf(not_encrypted_file, encrypted_file, password)
                print(f"[SUCCESS] Encrypted file Output to: {args.output}")

            else:
                password = getpass.getpass("Enter password: ")
                password_confirm = None
                while password != password_confirm:
                    password_confirm = getpass.getpass("Confirm password: ")
                    if password != password_confirm:
                        print("[ERROR] Passwords do not match. Please try again.")
                encrypt_pdf(not_encrypted_file, encrypted_file, password)
                print(f"[SUCCESS] Encrypted file Output to: {args.output}")

        elif args.decrypto:
            if processing_file:
                encrypted_file = processing_file
            else:
                choosen_file = choose_file(args.input)
                encrypted_file = choosen_file
            not_encrypted_file = result_file

            if args.decrypto and args.regen:
                if not args.regen:
                    password = getpass.getpass("Enter password: ")
                    decrypt_pdf(encrypted_file, not_encrypted_file, password)
                else:
                    print("--regen: This feature is WIP.")

            else:
                password = getpass.getpass("Enter password: ")
                decrypt_pdf(encrypted_file, not_encrypted_file, password)

        if args.share:
            if f"{args.share.upper()}_ID" in os.environ and f"{args.share.upper()}_PASS" in os.environ:
                username = os.getenv[f"{args.share.upper()}_ID"]
                password = os.getenv[f"{args.share.upper()}_PASS"]
            else:
                print(f"Enter {args.share} ID:")
                username = input()
                password = getpass.getpass(f"Enter {args.share} password:")

            WebAPI.share_file(args.share, username, password, result_file)


    elif args.webui:
        await webui(params, parser.usage)

    else:
        logger.setLevel(logging.NOTSET)
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
