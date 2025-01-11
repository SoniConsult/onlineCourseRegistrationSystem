from flask import Flask, request, jsonify
from models import db,Course,User,Registration
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Adding users 
@app.route('/user',methods=['POST'])
def add_new_user():
    userData=request.get_json()
    new_user_Data=User(
       username=userData['username'] ,
       email=userData['email'],
       role=userData['role']
    )
    db.session.add(new_user_Data)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})
# implementing Admin Routes
# adding courses
@app.route('/admin/courses', methods=['POST'])
def add_new_course():
    data = request.get_json()
    new_course = Course(
        role=data['role'],
        title=data['title'],
        description=data['description'],
        price=data['price']
    )
    if data['role']=='Admin':
        db.session.add(new_course)
        db.session.commit()
        return jsonify({'message': 'Course added successfully'})
    else:
        return jsonify({'message':'Invalid Access'})

# view all courses (getting courses)

@app.route('/admin/view',methods=['GET'])
def get_available_courses():
    courses = Course.query.all()
    return jsonify([{
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'price': course.price
        } for course in courses])


# update course details based on the endpoints


@app.route('/admin/courses/<int:id>', methods=['PUT'])
def update_course_details(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()
    course.title = data['title']
    course.description = data['description']
    course.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Course updated successfully'})


# delete the courses 

@app.route('/admin/courses/delete/<int:id>', methods=['DELETE'])
def delete_course_details(id):
    course=Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'})


# users endpoints


@app.route('/view/courses',methods=['GET'])
def get_available_courses():
    courses = Course.query.all()
    return jsonify([{
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'price': course.price
        } for course in courses])


# register for courses

@app.route('/admin/courses', methods=['POST'])
def registration_in_course():
    data = request.get_json()
    new_registration = Registration(
        id=data['id'],
        user_id=data['user_id'],
        course_id=data['course_id'],
       
    )
  
    db.session.add(new_registration)
    db.session.commit()
    return jsonify({'message': 'Registration successfully'})
    


# cancel Registration
def delete_registration(id):
    registration=Registration.query.get_or_404(id)
    db.session.delete(registration)
    db.session.commit()
    return jsonify({'message': 'Registration cancelled successfully'})



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)





