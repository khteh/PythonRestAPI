from flask import request, g, Blueprint, json, Response
from common.Authentication import Authentication
from models.BlogModel import BlogModel, BlogSchema
from common.Response import custom_response

blog_api = Blueprint("blogs", __name__)
blog_schema = BlogSchema()

@blog_api.route("/", methods=["POST"])
@Authentication.auth_required
def create():
    """
    Create Blog
    """
    req_data = request.get_json()
    req_data["owner_id"] = g.user.get("id")
    data, error = blog_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    blog = BlogModel(data)
    blog.save()
    return custom_response(blog_schema.dump(blog).data, 201)

@blog_api.route("/")
@Authentication.auth_required
def get_all():
    """
    Get All Blogs
    """
    return custom_response(blog_schema.dump(BlogModel.get_blogs(), many=True).data, 200)

@blog_api.route("/<int:id>")
@Authentication.auth_required
def get_blog():
    """
    Get Blog 'id'
    """
    blog = BlogModel.get_blog(id)
    if not blog:
        return custom_response({"error": f"Blog {id} not found!"}, 404)
    return custom_response(blog_schema.dump(blog).data, 200)

@blog_api.route("/<int:id>", methods=["PUT"])
@Authentication.auth_required
def update(id):
    """
    Update Blog 'id'
    """
    blog = BlogModel.get_blog(id)
    if not blog:
        return custom_response({"error": f"Blog {id} not found!"}, 404)
    data = blog_schema.dump(blog).data
    if data.get("owner_id") != g.user.get("id"):
        return custom_response({"error": "permission denied!"}, 400)
    data, error = blog_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    blog.update(data)
    return custom_response(blog_schema.dump(blog), 200)

@blog_api.route("/<int:id>", methods=["DELETE"])
@Authentication.auth_required
def delete(id):
    """
    Delete Blog 'id'
    """
    blog = BlogModel.get_blog(id)
    if not blog:
        return custom_response({"error": f"Blog {id} not found!"}, 404)
    data = blog_schema.dump(blog).data
    if data.get("ownder_id") != g.user.get("id"):
        return custom_response({"error": "permission denied!"}, 400)
    blog.delete()
    print(f"Blog {id} deleted successfully!")
    return custom_response({"message": f"Blog {id} deleted successfully!"}, 204)