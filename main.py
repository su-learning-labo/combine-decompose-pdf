import streamlit as st

from pypdf import PdfReader, PdfWriter, PdfMerger


# PDFファイルのページ数を取得
def get_page_count(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    return len(pdf_reader.pages)


# ファイルサイズの取得（MB）
def format_size(size_bytes):
    size_mb = size_bytes / (1024 * 1024)
    return f'{round(size_mb, 1)}MB'


# PDfファイルの結合
def merge_pdf(base_pdf):
    file_name_str = st.text_input('出力するPDFファイル名を入力してください（拡張子.pdfは不要）', placeholder='Please enter file name.')
    output_file_name = f'{file_name_str}.pdf'

    add_pdfs = st.file_uploader(
        "結合するPDFファイルをアップロードしてください",
        type='pdf',
        accept_multiple_files=True
    )

    if add_pdfs:
        merger = PdfMerger()
        merger.append(base_pdf)

        for add_pdf in add_pdfs:
            merger.append(add_pdf)

        merger.write(output_file_name)

        st.success("PDFの結合が完了し、新しいPDFが保存されました。ダウンロードしてください")
        download_file(output_file_name)


# PDfファイルの削除
def delete_pages(pdf_file, count_pages):

    file_name_str = st.text_input('出力するPDFファイル名を入力してください（拡張子.pdfは不要）',
                                  placeholder='Please enter file name.')
    output_file_name = f'{file_name_str}.pdf'

    try:
        page_numbers = st.text_input(
            label='削除するページ番号をカンマ区切りで入力してください（例: 2, 5, 7）',
        )

        st.write(f'元ファイルページ番号: {count_pages}')

        if page_numbers:
            pages = [n for n in range(1, count_pages + 1)]
            pages_to_delete = sorted([int(page.strip()) for page in page_numbers.split(",")])

            pdf_reader = PdfReader(pdf_file)
            pdf_writer = PdfWriter()

            st.write(f'削除ページ: {pages_to_delete}')
            for page_num in range(1, count_pages + 1):
                if page_num not in pages_to_delete:
                    page = pdf_reader.pages[page_num - 1]
                    pdf_writer.add_page(page)

            pdf_writer.write(output_file_name)

            st.success("PDFの結合が完了し、新しいPDFが保存されました。ダウンロードしてください")
            download_file(output_file_name)

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")


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

        # 結合処理
        if selector == '結合':
            st.write('---')

            merge_pdf(base_pdf)

        # ページ削除
        if selector == 'ページ削除':
            st.write('---')

            delete_pages(base_pdf, count_pages)

        # 並び替え
        if selector == '並び替え':
            st.write('---')
            try:
                page_order = st.text_input(
                    label='ページの並びをカンマ区切りで指定してください（例: 2, 5, 7）',
                )
                st.write(f'元のページ順: {[n for n in range(1, count_pages + 1)]}')
                if page_order:
                    page_order = [int(page.strip()) for page in page_order.split(",")]

                    if set(page_order) == set(range(1, count_pages + 1)):

                        st.write(f' → 指定の並び順: {page_order}')

                        pdf_reader = PdfReader(pdf_file)
                        pdf_writer = PdfWriter()

                        for page_num in page_order:
                            page = pdf_reader.pages[page_num - 1]
                            pdf_writer.add_page(page)

                        # 新しいPDFファイルを保存
                        pdf_writer.write('./data/reordered.pdf')

                        with open("./data/reordered.pdf", "rb") as output_file:
                            PDFbyte = output_file.read()
                            st.success("ページの並び替えが完了し、新しいPDFが保存されました。ダウンロードしてください")

                        st.download_button(
                            label='ダウンロード',
                            data=PDFbyte,
                            file_name='reordered.pdf',
                            mime='application/octet-stream'
                        )

                    else:
                        st.warning('ページの指定が誤っています。確認してください。')

            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
