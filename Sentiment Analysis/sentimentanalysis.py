import streamlit as st
from textblob import TextBlob
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import cleantext
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

st.set_page_config(page_title="Sentiment Analysis Dashboard")

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

@st.cache_data
def load_data():
    return pd.read_csv("Reviews.csv")

df = load_data()

analyzer = SentimentIntensityAnalyzer()

def classify_sentiment(score):
    if score > 0.8:
        return "Highly Positive"
    elif score > 0.4:
        return "Positive"
    elif -0.4 <= score <= 0.4:
        return "Neutral"
    elif score > -0.8:
        return "Negative"
    else:
        return "Highly Negative"

@st.cache_data
def analyze_sentiment(texts):
    sentiment_scores = []
    blob_subj = []
    sentiment_classes = []
    for text in texts:
        score = analyzer.polarity_scores(text)["compound"]
        sentiment_scores.append(score)
        blob = TextBlob(text)
        blob_subj.append(blob.subjectivity)
        sentiment_classes.append(classify_sentiment(score))
    return sentiment_scores, blob_subj, sentiment_classes

sentiment_scores, blob_subj, sentiment_classes = analyze_sentiment(df["Text"])

st.title("📊 Sentiment Analysis Dashboard")

st.sidebar.header("Navigation")
page = st.sidebar.radio("", ["Home", "Data Overview", "User Input Analysis"])

if page == "Home":
    st.write("Welcome to the Sentiment Analysis Dashboard! This app analyzes customer feedback and provides insights into sentiment and subjectivity.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Reviews", len(df))
    with col2:
        st.metric("Average Sentiment Score", round(sum(sentiment_scores) / len(sentiment_scores), 2))
    with col3:
        st.metric("Average Subjectivity", round(sum(blob_subj) / len(blob_subj), 2))
    
    sentiment_counts = pd.Series(sentiment_classes).value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    wedges, texts, autotexts = ax.pie(sentiment_counts.values, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
    ax.axis('equal')

    ax.legend(wedges, sentiment_counts.index, title="Sentiment Classes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")
    st.subheader("Sentiment Distribution")
    st.pyplot(fig)

elif page == "Data Overview":
    st.subheader("Data Overview")
    
    df["Sentiment Class"] = sentiment_classes
    df["Sentiment Score"] = sentiment_scores
    df["Subjectivity"] = blob_subj
    
    new_df = df[["Score", "Text", "Sentiment Score", "Sentiment Class", "Subjectivity"]]
    st.dataframe(new_df.head(30), use_container_width=True)
    
    st.subheader("Correlation Heatmap")
    corr = new_df[["Score", "Sentiment Score", "Subjectivity"]].corr()
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
    
    st.subheader("Sentiment Score vs Subjectivity")
    chart = alt.Chart(new_df).mark_circle().encode(
        x='Sentiment Score',
        y='Subjectivity',
        color='Sentiment Class',
        tooltip=['Text', 'Sentiment Score', 'Subjectivity']
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

elif page == "User Input Analysis":
    st.subheader("Analyze Your Own Text")
    
    user_input = st.text_area("Enter customer feedback:")
    
    if user_input:
        blob = TextBlob(user_input)
        user_sentiment_score = analyzer.polarity_scores(user_input)["compound"]
        user_sentiment_class = classify_sentiment(user_sentiment_score)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**VADER Sentiment Analysis:**")
            st.write(f"Sentiment Class: {user_sentiment_class}")
            st.write(f"Sentiment Score: {user_sentiment_score:.2f}")
        
        with col2:
            st.write("**TextBlob Analysis:**")
            st.write(f"Polarity: {blob.sentiment.polarity:.2f}")
            st.write(f"Subjectivity: {blob.sentiment.subjectivity:.2f}")
        
        st.subheader("Cleaned Text")
        cleaned_text = cleantext.clean(user_input, clean_all=False, extra_spaces=True, 
                                       stopwords=True, lowercase=True, numbers=True, punct=True)
        st.write(cleaned_text)
    
    else:
        st.write("Please enter some text to analyze.")

st.markdown("---")
st.markdown("Thank You for viewing! ❤️")