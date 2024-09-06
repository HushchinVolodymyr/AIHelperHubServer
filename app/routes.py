from app import views

def setup_routes(app):
   app.router.add_post("/", views.index)