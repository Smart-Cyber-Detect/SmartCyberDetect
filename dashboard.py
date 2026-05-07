import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
st.set_page_config(page_title="SmartCyberDetect", layout="wide")

st.title("🛡️ SmartCyberDetect platform")

st.write("AI Cyberattack Detection Platform")

# Load model
model = pickle.load(open("model.pkl", "rb"))

traffic = st.slider("Network Traffic", 0.0, 1.0, 0.5)

if st.button("Detect Attack"):

    prediction = model.predict([[traffic]])

    if prediction[0] == 1:
        st.error("⚠️ Attack Detected!")
    else:
        st.success("✅ Normal Traffic")
data = pd.read_csv("data.csv")
data.columns = data.columns.str.strip()
col1, col2, col3 = st.columns(3)

col1.metric("Total Logs", len(data))
col2.metric("Attacks", (data["status"]=="attack").sum())
col3.metric("Normal Traffic", (data["status"]=="normal").sum())
st.subheader("🚨 Live Threat Alerts")

if (data["status"]=="attack").any():
    st.error("Attack detected in network!")
else:
    st.success("Network Secure")
st.subheader("Network Activity")

status_counts = data["status"].value_counts().reset_index()
status_counts.columns=["status","count"]

fig = px.bar(
    status_counts,
    x="status",
    y="count",
    color="status"
)

st.plotly_chart(fig)
st.subheader("Top Attackers")

top_attackers = data[data["status"]=="attack"]["source_ip"].value_counts().head(5)

st.bar_chart(top_attackers)
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

data["source_ip"] = le.fit_transform(data["source_ip"])
data["dest_ip"] = le.fit_transform(data["dest_ip"])
data["protocol"] = le.fit_transform(data["protocol"])
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X = data.drop("status",axis=1)
y = (data["status"]=="attack").astype(int)

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train,y_train)
data["risk_score"] = model.predict_proba(X)[:,1]

st.subheader("IP Risk Score")

st.dataframe(
    data[["source_ip","risk_score"]]
    .sort_values(by="risk_score",ascending=False)
    .head(10)
)
import plotly.figure_factory as ff

st.subheader("Attack Heatmap")

heatmap_data = data.pivot_table(
index="source_ip",
columns="dest_ip",
values="risk_score",
fill_value=0
)

fig_heatmap = ff.create_annotated_heatmap(
z=heatmap_data.values,
x=heatmap_data.columns.astype(str),
y=heatmap_data.index.astype(str)
)

st.plotly_chart(fig_heatmap)
