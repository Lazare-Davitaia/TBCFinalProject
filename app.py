from ext import app
from routes import register,login,add_news,news_page,like_news,edit_news,delete_news,logout,home,ranking,ranking2

app.run(debug=True, host="0.0.0.0")


