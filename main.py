import argparse
import pypdf

from copy import copy
from pathlib import Path

# ファイルを変換する処理
# 成功したらTrue、それ以外はFalseを返す
def process(input_file_path: str, output_file_path: str):
    try:
        # PDFファイルを開く
        input_file = open(input_file_path, 'rb')

        # pypdfのPdfFileReaderオブジェクトを作成する
        pdf_reader = pypdf.PdfReader(input_file)

    except Exception as e:
        # PDFファイルが壊れている場合の処理
        print(f"Failed to read PDF file: {e}")

        return False

    # pypdfのPdfFileWriterオブジェクトを作成する
    pdf_writer = pypdf.PdfWriter()

    # 各ページを2分割して、新しいPDFに追加する
    for page in pdf_reader.pages:
        # ページのサイズを取得する
        page_width = page.mediabox.width
        page_height = page.mediabox.height

        # ページを2分割する
        if page_width < page_height:
            half_height = page_height / 2
            rect1 = pypdf.generic.RectangleObject((0, half_height, page_width, page_height))
            rect2 = pypdf.generic.RectangleObject((0, 0, page_width, half_height))
        else:
            half_width = page_width / 2
            rect1 = pypdf.generic.RectangleObject((0, 0, half_width, page_height))
            rect2 = pypdf.generic.RectangleObject((half_width, 0, page_width, page_height))

        half1 = page
        half1.cropbox = rect1
        half2 = copy(page)
        half2.cropbox = rect2

        # 2つの半分のページを新しいPDFに追加する
        pdf_writer.add_page(half1)
        pdf_writer.add_page(half2)

    # ファイルを閉じる
    input_file.close()

    try:
        # PDFファイルを保存する
        with open(output_file_path, 'wb') as output_file:
            # 新しいPDFを出力ファイルに書き込む
            pdf_writer.write(output_file)

    except Exception as e:
        # ファイルの書き込みに失敗した場合の処理
        print(f"Failed to write PDF file: {e}")

        return False
    
    return True

# コマンドライン引数をパースする
parser = argparse.ArgumentParser(description='Split a PDF file into half pages')
parser.add_argument('input_path', type=Path, help='path to the input PDF file or directory')
parser.add_argument('-s', '--suffix', default='_split', help='suffix of output file(s)')
args = parser.parse_args()

input_path: Path = args.input_path
input_file_paths = []

if input_path.is_dir():
    for input_file_path in input_path.iterdir():
        input_file_paths.append(input_file_path)
else:
    input_file_paths.append(input_path)

for input_file_path in input_file_paths:
    stem = input_file_path.stem + args.suffix
    output_file_path = input_file_path.with_stem(stem)

    process(input_file_path, output_file_path)
