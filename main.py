import streamlit as st
import pypdf
import tempfile

from pypdf import PdfReader, PdfWriter, PdfMerger


# Streamlitアプリ
def main():

    st.title('PDF Manipulator')

    pdf_file = st.file_uploader("PDFファイルをアップロードしてください", type="pdf")

    if pdf_file:

        reader = PdfReader(pdf_file)
        writer = PdfWriter(pdf_file)
        count_pages = len(reader.pages)

        st.sidebar.subheader('ベースとなるPDFファイル:')
        st.sidebar.write(f'- Title: {pdf_file.name}')
        st.sidebar.write(f'- Pages: {count_pages}ページ')
        st.sidebar.write(f'- Size: {round(pdf_file.size/(1024*1024), 1)}MB')

        st.write('---')
        selector = st.radio(
            '処理を選択してください',
            options=['分割', '結合', 'ページ削除'],
            captions=['指定した箇所でページを分ける', 'アップロードした複数のPDFをつなげる', '指定したページを削除する'],
            index=None
        )

        # PDF分割処理
        if selector == '分割':
            st.write('---')
            split_page = st.number_input(
                '分割するページ番号を選択してください',
                min_value=1,
                max_value=count_pages
            )
            front_page = f':{split_page}'
            backend_page = f'{split_page +1}:'

            # merger = PdfMerger(pdf_file)
            # merger.append(pdf_file, pages=pypdf.PageRange(front_page))
            pass

        # PDF結合
        if selector == '結合':
            st.write('---')

            add_pdfs = st.file_uploader("結合するPDFファイルをアップロードしてください", type='pdf', accept_multiple_files=True)

            if add_pdfs:
                merger = PdfMerger()
                merger.append(pdf_file)
                for n in range(len(add_pdfs)):
                    merger.append(add_pdfs[n])

                merger.write('./data/merged.pdf')
                with open('./data/merged.pdf', 'rb') as pdf_file:
                    PDFbyte = pdf_file.read()

                st.download_button(
                    label='ダウンロード',
                    data=PDFbyte,
                    file_name ='merged.pdf',
                    mime='application/octet-stream'
                )


if __name__ == "__main__":
    main()
