import streamlit as st
import pandas as pd

st.set_page_config(page_title="Book Recommendation System", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('books.csv')

books_df = load_data()

def search_books(keyword):
    """
    Search for books that match the keyword in the title, authors, or publisher.
    """
    keyword = keyword.lower()
    results = books_df[
        books_df['title'].str.lower().str.contains(keyword) |
        books_df['authors'].str.lower().str.contains(keyword) |
        books_df['publisher'].str.lower().str.contains(keyword)
    ]
    return results

st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .sidebar .sidebar-content {
        background: #ffffff
    }
    h1 {
        color: #1e3d59;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #1e3d59;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📚 Book Recommendation System")

st.sidebar.header("Search Options")
search_option = st.sidebar.radio("Search by:", ("Keyword", "ISBN"))

if search_option == "Keyword":
    keyword = st.sidebar.text_input("Enter a keyword to search for books:")
    if st.sidebar.button("Search"):
        if keyword:
            results = search_books(keyword)
            if results.empty:
                st.warning("No books found.")
            else:
                st.success(f"Found {len(results)} books matching your search.")
                for index, book in results.iterrows():
                    with st.expander(f"{book['title']} by {book['authors']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Title:** {book['title']}")
                            st.write(f"**Author:** {book['authors']}")
                            st.write(f"**Average Rating:** {book['average_rating']}")
                            st.write(f"**ISBN:** {book['isbn']}")
                            st.write(f"**ISBN13:** {book['isbn13']}")
                        with col2:
                            st.write(f"**Language:** {book['language_code']}")
                            if 'num_pages' in book:
                                st.write(f"**Number of Pages:** {book['num_pages']}")
                            st.write(f"**Ratings Count:** {book['ratings_count']}")
                            st.write(f"**Text Reviews Count:** {book['text_reviews_count']}")
                            st.write(f"**Publication Date:** {book['publication_date']}")
                            st.write(f"**Publisher:** {book['publisher']}")
        else:
            st.warning("Please enter a keyword to search.")
elif search_option == "ISBN":
    isbn = st.sidebar.text_input("Enter ISBN to search for a book:")
    if st.sidebar.button("Search"):
        if isbn:
            result = books_df[books_df['isbn'] == isbn]
            if result.empty:
                st.warning("No book found with this ISBN.")
            else:
                book = result.iloc[0]
                st.success("Book found!")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Title:** {book['title']}")
                    st.write(f"**Author:** {book['authors']}")
                    st.write(f"**Average Rating:** {book['average_rating']}")
                    st.write(f"**ISBN:** {book['isbn']}")
                    st.write(f"**ISBN13:** {book['isbn13']}")
                with col2:
                    st.write(f"**Language:** {book['language_code']}")
                    if 'num_pages' in book:
                        st.write(f"**Number of Pages:** {book['num_pages']}")
                    st.write(f"**Ratings Count:** {book['ratings_count']}")
                    st.write(f"**Text Reviews Count:** {book['text_reviews_count']}")
                    st.write(f"**Publication Date:** {book['publication_date']}")
                    st.write(f"**Publisher:** {book['publisher']}")
        else:
            st.warning("Please enter an ISBN to search.")

st.sidebar.markdown("---")
st.sidebar.markdown("Thank You for viewing! ❤️")