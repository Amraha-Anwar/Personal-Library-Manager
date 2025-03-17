import streamlit as st
import pandas as pd
import database as db
import plotly.express as px
import base64


st.set_page_config(page_title="NovelNest - Your Personal Library Manager", page_icon="📚")

# st.markdown for styling
def set_bg_hack(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(255, 255, 255, 0.7); /* Semi-transparent white overlay */
            z-index: -1;
            filter: blur(5px); /* Blur only the background image */
        }}
        .stContainer {{
            background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent white background for text containers */
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .stContainer img {{
            margin-left: 20px;
            border-radius: 10px;
            max-width: 150px; /* Increased image size */
            max-height: 200px; /* Increased image size */
        }}
        h1, h2, h3, h4, h5, h6, p, div, span {{
            color: #000000 !important; /* Dark black text color */
        }}
        .stButton button {{
            background-color: #2196F3; /* Blue background */
            color: white; /* White text */
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }}
        .stButton button:hover {{
            background-color: #1976D2; /* Darker blue on hover */
            transform: scale(1.05); /* Slightly enlarge on hover */
        }}
        .sidebar .sidebar-content {{
            background-color: #f0f2f6; /* Light gray background for sidebar */
            padding: 20px;
            border-radius: 10px;
        }}
        .sidebar .sidebar-content .stButton button {{
            width: 100%;
            margin-bottom: 10px;
            background-color: #2196F3; /* Blue background */
            color: white; /* White text */
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }}
        .sidebar .sidebar-content .stButton button:hover {{
            background-color: #1976D2; /* Darker blue on hover */
            transform: scale(1.05); /* Slightly enlarge on hover */
        }}
        .sidebar .sidebar-content .stRadio div[role="radiogroup"] label {{
            display: block;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }}
        .sidebar .sidebar-content .stRadio div[role="radiogroup"] label:hover {{
            background-color: #e0e0e0; /* Light gray on hover */
            transform: scale(1.02); /* Slightly enlarge on hover */
        }}
        .sidebar .sidebar-content .stRadio div[role="radiogroup"] label[data-testid="stRadioLabel"]:has(input:checked) {{
            background-color: #2196F3; /* Blue background for active menu item */
            color: white; /* White text for active menu item */
        }}
        .sidebar .sidebar-content .stRadio div[role="radiogroup"] label[data-testid="stRadioLabel"]:has(input:checked):hover {{
            background-color: #1976D2; /* Darker blue on hover for active menu item */
        }}
        .sidebar .sidebar-content .stRadio div[role="radiogroup"] label i {{
            margin-right: 10px; /* Add spacing between icon and text */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to show genre distribution
def show_genre_distribution(df):
    genre_counts = df['Genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']
    fig = px.bar(genre_counts, x='Genre', y='Count', title="Genre Distribution", color='Genre')
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',  
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',  
    })
    st.plotly_chart(fig)

# Function to show reading progress
def show_reading_progress(df):
    status_counts = df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig = px.pie(status_counts, values='Count', names='Status', title="Reading Progress", color='Status')
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    st.plotly_chart(fig)

# Function to display rating as stars
def display_rating(rating):
    stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
    return stars

# Function to display books in a card layout
def display_books(books):
    if books:
        df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year", "Rating", "Status", "Image"])
        
        # Display one book per line
        for index, row in df.iterrows():
            with st.container():
                # Convert binary image data to base64
                image_base64 = base64.b64encode(row['Image']).decode() if row['Image'] else ""
                
                st.markdown(
                    f"""
                    <div class="stContainer">
                        <div>
                            <h3>{row['Title']}</h3>
                            <p><strong>Author:</strong> {row['Author']}</p>
                            <p><strong>Genre:</strong> {row['Genre']}</p>
                            <p><strong>Year:</strong> {row['Year']}</p>
                            <p><strong>Rating:</strong> {display_rating(row['Rating'])}</p>
                            <p><strong>Status:</strong> {row['Status']}</p>
                        </div>
                        {"<img src='data:image/png;base64,{}' width='150'>".format(image_base64) if image_base64 else ""}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Add to Book Bucket List button with validation
                if st.button(f"Add to Book Bucket List", key=f"add_{row['ID']}"):
                    # Check if the book is already in the bucket list
                    if db.is_book_in_bucket_list(row['ID']):
                        st.warning(f"'{row['Title']}' is already in your Book Bucket List!")
                    else:
                        db.add_to_book_bucket_list(row['ID'])
                        st.success(f"Added '{row['Title']}' to your Book Bucket List!")
    else:
        st.info("No books found.")

# Home Page
def home_page():
    st.title("📚 Welcome to NovelNest - Your Personal Library Manager!")
    st.write("""
        Manage your book collection with ease! Add new books, track your reading progress, 
        and organize your library with just a few clicks.
    """)

    # Display total number of books in the library
    total_books = len(db.get_all_books())
    st.subheader(f"📊 Total Books in Library: {total_books}")

    # Display existing books in a card format
    st.subheader("📖 Your Books")
    books = db.get_all_books()
    display_books(books)

    # Interactive Feature: Reading Quote
    st.markdown(
        """
        <style>
        .quote-container {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #2196F3;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .quote-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .quote-text {
            font-family: 'Georgia', serif;
            font-size: 1.5em;
            font-style: italic;
            color: #333;
            line-height: 1.6;
        }
        .quote-author {
            text-align: right;
            font-family: 'Arial', sans-serif;
            font-size: 1.2em;
            color: #555;
            margin-top: 10px;
        }
        .quote-heading {
            font-family: 'Arial', sans-serif;
            font-size: 1.8em;
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 10px;
        }
        </style>
        <div class="quote-heading">
            💡 Today's Reading Quote
        </div>
        <div class="quote-container">
            <div class="quote-text">
                "A reader lives a thousand lives before he dies. The man who never reads lives only one."
            </div>
            <div class="quote-author">
                – George R.R. Martin
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


set_bg_hack("https://images.unsplash.com/photo-1497633762265-9d179a990aa6")

# Sidebar for navigation
st.sidebar.title("📂 Navigation")
menu_options = [
    {"label": "🏠 Home", "value": "Home"},
    {"label": "📖 Add Book", "value": "Add Book"},
    {"label": "📚 View Library", "value": "View Library"},
    {"label": "🔄 Update Status", "value": "Update Status"},
    {"label": "🗑️ Delete Book", "value": "Delete Book"},
    {"label": "🔍 Search Book", "value": "Search Book"},
    {"label": "🎭 Filter by Genre", "value": "Filter by Genre"},
    {"label": "📥 Book Bucket List", "value": "Book Bucket List"}
]
menu = st.sidebar.radio("Choose an option", [option["value"] for option in menu_options], format_func=lambda x: [option["label"] for option in menu_options if option["value"] == x][0])

# Home Page
if menu == "Home":
    home_page()

# Add Book
elif menu == "Add Book":
    st.title("📖 Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title*", placeholder="Enter the book title")
        author = st.text_input("Author*", placeholder="Enter the author's name")
        genre = st.text_input("Genre*", placeholder="Enter the genre")
        year = st.number_input("Year*", min_value=1900, max_value=2025, placeholder="Enter the publication year")
        rating = st.slider("Rating*", 1, 5, 3)
        status = st.selectbox("Status*", ["Unread", "Reading", "Completed"])
        image = st.file_uploader("Upload Book Cover Image (Optional)", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Add Book")

        if submit:
            if not title or not author or not genre or not year:
                st.error("Please fill in all required fields.")
            else:
                image_bytes = image.read() if image else None
                db.add_book(title, author, genre, year, rating, status, image_bytes)
                st.success("Book added successfully!")

# View Library
elif menu == "View Library":
    st.title("📚 My Library")
    books = db.get_all_books()
    display_books(books)

    # Visualizations
    st.subheader("Library Insights")
    if books:
        df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year", "Rating", "Status", "Image"])
        show_genre_distribution(df)
        show_reading_progress(df)

# Search Book
elif menu == "Search Book":
    st.title("🔍 Search Book")
    query = st.text_input("Enter title or author")
    if query:
        books = db.get_all_books()
        df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year", "Rating", "Status", "Image"])
        results = df[df['Title'].str.contains(query, case=False) | df['Author'].str.contains(query, case=False)]
        if not results.empty:
            display_books(results.values.tolist())
        else:
            st.info("No matching books found.")

# Filter by Genre
elif menu == "Filter by Genre":
    st.title("🎭 Filter by Genre")
    books = db.get_all_books()
    if books:
        df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year", "Rating", "Status", "Image"])
        genres = df['Genre'].unique()
        selected_genre = st.selectbox("Select a genre", genres)
        filtered_books = df[df['Genre'] == selected_genre]
        display_books(filtered_books.values.tolist())
    else:
        st.info("No books in your library yet!")

# Update Status
elif menu == "Update Status":
    st.title("🔄 Update Book Status")
    books = db.get_all_books()
    if books:
        df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year", "Rating", "Status", "Image"])
        book_options = {f"{book[1]} by {book[2]}": book[0] for book in books}
        selected_book = st.selectbox("Select a book", list(book_options.keys()))
        new_status = st.selectbox("New Status", ["Unread", "Reading", "Completed"])
        if st.button("Update Status"):
            db.update_book_status(book_options[selected_book], new_status)
            st.success("Status updated successfully!")
    else:
        st.info("No books in your library yet!")

# Delete Book
elif menu == "Delete Book":
    st.title("🗑️ Delete a Book")
    books = db.get_all_books()
    if books:
        df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year", "Rating", "Status", "Image"])
        book_options = {f"{book[1]} by {book[2]}": book[0] for book in books}
        selected_book = st.selectbox("Select a book to delete", list(book_options.keys()))
        if st.button("Delete Book"):
            db.delete_book(book_options[selected_book])
            st.success("Book deleted successfully!")
    else:
        st.info("No books in your library yet!")

# Book Bucket List
elif menu == "Book Bucket List":
    st.title("📥 Book Bucket List")
    books = db.get_all_books()
    if books:
        df = pd.DataFrame(books, columns=["ID", "Title", "Author", "Genre", "Year", "Rating", "Status", "Image"])
        book_options = {f"{book[1]} by {book[2]}": book[0] for book in books}
        selected_book = st.selectbox("Select a book to add to your list", list(book_options.keys()))
        
        # Add to Book Bucket List button with validation
        if st.button("Add to Book Bucket List"):
            book_id = book_options[selected_book]
            if db.is_book_in_bucket_list(book_id):
                st.warning(f"'{selected_book}' is already in your Book Bucket List!")
            else:
                db.add_to_book_bucket_list(book_id)
                st.success(f"Added '{selected_book}' to your Book Bucket List!")

        st.subheader("Your Book Bucket List")
        book_bucket_list = db.get_book_bucket_list()
        display_books(book_bucket_list)
    else:
        st.info("No books in your library yet!")