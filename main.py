import streamlit as st
import pypdf


# Streamlitアプリ
def main():

    st.title('PDF Manipulator')

    pdf_file = st.file_uploader("PDFファイルをアップロードしてください", type="pdf")

    if pdf_file:

        file = pypdf.PdfReader(pdf_file)

        st.sidebar.subheader('選択したPDFファイル:')
        st.sidebar.write(f'- Title: {pdf_file.name}')
        st.sidebar.write(f'- Pages: {len(file.pages)}ページ')
        st.sidebar.write(f'- Size: {round(pdf_file.size/(1024*1024), 1)}MB')

        selector = st.radio(
            '処理を選択してください',
            options=['分割', '結合', 'ページ削除'],
            captions=['指定した箇所でページを分ける', 'アップロードした複数のPDFをつなげる', '指定したページを削除する'],
            index=None
        )



if __name__ == "__main__":
    main()
