import streamlit as st
from pypdf import PdfReader, PdfWriter, PdfMerger


# PDFファイルのページ数を取得
def get_page_count(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    return len(pdf_reader.pages)


# PDfファイルの結合
def merge_pdf(base_pdf, add_pdfs, output_file_name):
    merger = PdfMerger()
    merger.append(base_pdf)

    for add_pdf in add_pdfs:
        merger.append(add_pdf)

    merger.write(output_file_name)


# PDfファイルの削除
def delete_pages(pdf_file, page_numbers, output_file_name):
    pages_to_delete = sorted([int(page.strip()) for page in page_numbers.split(",")])

    pdf_reader = PdfReader(pdf_file)
    pdf_writer = PdfWriter()

    for page_num, page in enumerate(pdf_reader.pages, start=1):
        if page_num not in pages_to_delete:
            pdf_writer.add_page(page)

    pdf_writer.write(output_file_name)


# ファイルの並び替え
def reorder_pages(pdf_file, page_order, output_file_name):
    page_order = [int(page.strip()) for page in page_order.split(",")]

    pdf_reader = PdfReader(pdf_file)
    pdf_writer = PdfWriter()

    for page_num in page_order:
        page = pdf_reader.pages[page_num - 1]
        pdf_writer.add_page(page)

    pdf_writer.write(output_file_name)


def download_file(file_path):
    with open(file_path, 'rb') as f:
        file_bytes = f.read()

    st.download_button(
        label='Download',
        data=file_bytes,
        file_name=file_path,
        mime='application/pdf'
    )


# Streamlitアプリ
def main():
    st.title('PDF Manipulator')

    base_pdf = st.file_uploader("PDFファイルをアップロードしてください", type="pdf")

    if base_pdf:
        # アップロードファイルのページ数取得
        count_pages = get_page_count(base_pdf)

        st.write('---')
        selector = st.radio(
            '処理を選択してください',
            options=['結合', 'ページ削除', '並び替え'],
            captions=['アップロードした複数のPDFをつなげる', '指定したページを削除する', '指定順にページをソートする'],
            index=None
        )

        if selector == '結合':
            st.write('---')
            file_name_str = st.text_input('出力するPDFファイル名を入力してください（拡張子.pdfは不要）', placeholder='Please enter file name.')
            output_file_name = f'{file_name_str}.pdf'
            add_pdfs = st.file_uploader(
                "結合するPDFファイルをアップロードしてください",
                type='pdf',
                accept_multiple_files=True
            )

            if st.button("結合"):
                if add_pdfs:
                    merge_pdf(base_pdf, add_pdfs, output_file_name)
                    st.success("PDFの結合が完了し、新しいPDFが保存されました。ダウンロードしてください")
                    download_file(output_file_name)

        elif selector == 'ページ削除':
            st.write('---')
            page_number_list = [n for n in range(1, count_pages + 1)]
            file_name_str = st.text_input('出力するPDFファイル名を入力してください（拡張子.pdfは不要）',
                                          placeholder='Please enter file name.')
            output_file_name = f'{file_name_str}.pdf'
            page_numbers = st.text_input(
                        label='削除するページ番号をカンマ区切りで入力してください（例: 2, 5, 7）',
                        placeholder=f'削除対象ページ番号: {page_number_list}'
                    )

            if st.button("ページ削除"):
                if page_numbers:
                    delete_pages(base_pdf, page_numbers, output_file_name)
                    st.success("PDFのページ削除が完了し、新しいPDFが保存されました。ダウンロードしてください")
                    download_file(output_file_name)

        # 並び替え
        elif selector == '並び替え':
            st.write('---')
            file_name_str = st.text_input('出力するPDFファイル名を入力してください（拡張子.pdfは不要）', placeholder='Please enter file name.')
            output_file_name = f'{file_name_str}.pdf'
            page_number_list = [n for n in range(1, count_pages + 1)]
            page_order = st.text_input(
                label='ページの並び順をカンマ区切りで指定してください（例: 2, 5, 7）',
                placeholder=f'ページ番号: {page_number_list}'
            )

            if st.button("並び替え"):
                if page_order:
                    reorder_pages(base_pdf, page_order, output_file_name)
                    st.success("PDFのページ並び替えが完了し、新しいPDFが保存されました。ダウンロードしてください")
                    download_file(output_file_name)


if __name__ == "__main__":
    main()
