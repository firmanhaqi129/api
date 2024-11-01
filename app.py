from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Contoh data awal untuk sepeda motor (data realistis)
motorcycles = [
    {"id": "1", "name": "Honda Beat", "description": "Skuter matic 110cc", "brand": "Honda", "model": "Beat", "price": 17000000, "engine_capacity": "110cc", "year": 2022},
    {"id": "2", "name": "Yamaha NMAX", "description": "Skuter matic 155cc", "brand": "Yamaha", "model": "NMAX", "price": 30000000, "engine_capacity": "155cc", "year": 2023},
    {"id": "3", "name": "Suzuki GSX-R150", "description": "Motor sport 150cc", "brand": "Suzuki", "model": "GSX-R150", "price": 35000000, "engine_capacity": "150cc", "year": 2021},
    {"id": "4", "name": "Kawasaki Ninja 250", "description": "Motor sport 250cc", "brand": "Kawasaki", "model": "Ninja 250", "price": 62000000, "engine_capacity": "250cc", "year": 2023},
    {"id": "5", "name": "Vespa Primavera", "description": "Skuter klasik 150cc", "brand": "Vespa", "model": "Primavera", "price": 45000000, "engine_capacity": "150cc", "year": 2022},
    # Tambahkan hingga 15 data
]

# Detail data untuk setiap motor (termasuk review customer)
details = {
    "1": {"name": "Honda Beat", "description": "Skuter matic 110cc", "brand": "Honda", "model": "Beat", "price": 17000000, "engine_capacity": "110cc", "year": 2022, "customerReviews": []},
    "2": {"name": "Yamaha NMAX", "description": "Skuter matic 155cc", "brand": "Yamaha", "model": "NMAX", "price": 30000000, "engine_capacity": "155cc", "year": 2023, "customerReviews": []},
    "3": {"name": "Suzuki GSX-R150", "description": "Motor sport 150cc", "brand": "Suzuki", "model": "GSX-R150", "price": 35000000, "engine_capacity": "150cc", "year": 2021, "customerReviews": []},
    "4": {"name": "Kawasaki Ninja 250", "description": "Motor sport 250cc", "brand": "Kawasaki", "model": "Ninja 250", "price": 62000000, "engine_capacity": "250cc", "year": 2023, "customerReviews": []},
    "5": {"name": "Vespa Primavera", "description": "Skuter klasik 150cc", "brand": "Vespa", "model": "Primavera", "price": 45000000, "engine_capacity": "150cc", "year": 2022, "customerReviews": []},
    # Tambahkan hingga 15 data
}

# Endpoint untuk mengambil daftar sepeda motor
class MotorcycleList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(motorcycles),
            "motorcycles": motorcycles
        }

# Endpoint untuk mengambil detail sepeda motor berdasarkan ID
class MotorcycleDetail(Resource):
    def get(self, motorcycle_id):
        if motorcycle_id in details:
            return {
                "error": False,
                "message": "success",
                "motorcycle": details[motorcycle_id]
            }
        return {"error": True, "message": "Motorcycle not found"}, 404

# Endpoint untuk mencari sepeda motor berdasarkan nama atau deskripsi
class MotorcycleSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [m for m in motorcycles if query in m['name'].lower() or query in m['description'].lower()]
        return {
            "error": False,
            "founded": len(result),
            "motorcycles": result
        }

# Endpoint untuk menambahkan review
class AddReview(Resource):
    def post(self):
        data = request.get_json()
        motorcycle_id = data.get('id')
        name = data.get('name')
        review = data.get('review')
        
        if motorcycle_id in details:
            new_review = {
                "name": name,
                "review": review,
                "date": datetime.now().strftime("%d %B %Y")
            }
            details[motorcycle_id]['customerReviews'].append(new_review)
            return {
                "error": False,
                "message": "success",
                "customerReviews": details[motorcycle_id]['customerReviews']
            }
        return {"error": True, "message": "Motorcycle not found"}, 404

# Endpoint untuk memperbarui review
class UpdateReview(Resource):
    def put(self):
        data = request.get_json()
        motorcycle_id = data.get('id')
        name = data.get('name')
        new_review_text = data.get('review')
        
        if motorcycle_id in details:
            reviews = details[motorcycle_id]['customerReviews']
            review_to_update = next((r for r in reviews if r['name'] == name), None)
            if review_to_update:
                review_to_update['review'] = new_review_text
                review_to_update['date'] = datetime.now().strftime("%d %B %Y")
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Motorcycle not found"}, 404

# Endpoint untuk menghapus review
class DeleteReview(Resource):
    def delete(self):
        data = request.get_json()
        motorcycle_id = data.get('id')
        name = data.get('name')
        
        if motorcycle_id in details:
            reviews = details[motorcycle_id]['customerReviews']
            review_to_delete = next((r for r in reviews if r['name'] == name), None)
            if review_to_delete:
                reviews.remove(review_to_delete)
                return {
                    "error": False,
                    "message": "success",
                    "customerReviews": reviews
                }
            return {"error": True, "message": "Review not found"}, 404
        return {"error": True, "message": "Motorcycle not found"}, 404

# Tambahkan endpoint ke API
api.add_resource(MotorcycleList, '/motorcycles')
api.add_resource(MotorcycleDetail, '/motorcycle/<string:motorcycle_id>')
api.add_resource(MotorcycleSearch, '/motorcycles/search')
api.add_resource(AddReview, '/motorcycle/review')
api.add_resource(UpdateReview, '/motorcycle/review/update')
api.add_resource(DeleteReview, '/motorcycle/review/delete')

if __name__ == '__main__':
    app.run(debug=True)
