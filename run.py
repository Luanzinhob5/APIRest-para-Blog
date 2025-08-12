from app import criar_app, db
from app.models import Post

app = criar_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)