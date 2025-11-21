from test_with_edozie import app, db
from test_with_edozie.models import PythonTestAnswers, MathTestAnswers, StudentCryptographyResults, Students, OneTimePassword


# with app.app_context():
#     for answer in PythonTestAnswers.query.all():
#         db.session.delete(answer)
#         db.session.commit()

# with app.app_context():
#     for answer in MathTestAnswers.query.all():
#         db.session.delete(answer)
#         db.session.commit()

# with app.app_context():
#     for answer in StudentCryptographyResults.query.all():
#         db.session.delete(answer)
#         db.session.commit()

with app.app_context():
    students = Students.query.all()
    for student in students:
        db.session.delete(student)
        db.session.commit()
    # codes = OneTimePassword.query.all()
    # for code in codes:
    #     db.session.delete(code)
    #     db.session.commit()