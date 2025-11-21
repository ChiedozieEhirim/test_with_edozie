from test_with_edozie import app, db
from test_with_edozie.models import PythonTestAnswers, MathTestAnswers, Students, CryptographyTestAnswers, \
StudentCryptographyResults, StudentMathResults


with app.app_context():
    db.create_all()
    student = Students(
        username='TestUser', email='testuser@gmail.com', first_name='Test', last_name='User',
        gender='Male', password='password123'
    )

    cryptography_answers = CryptographyTestAnswers(
            subject='Basic Cryptography', question1='Cryptography', question2='Cryptanalyst', question3='Caesar Cipher',
            question4='Brute-Force', question5='The quick brown foxes jumped over the lazy dogs', question6='10',question7='Transposition Cipher', question8='Affine Cipher',
            question9='vpz sk w pfi', question10='20'
        )

    math_answers = MathTestAnswers(
        subject='Basic Maths', question1='30', question2='21', question3='sin2A',
        question4='(x-5)(x-2)', question5='2012', question6='45', question7='Hypotenuse', question8='Modulus',
        question9='5', question10='arctan(3/4)'
    )

    python_answers = PythonTestAnswers(
        subject='Basic Python', question1='String', question2='variable_name=variable_value', question3='Concatenation',
        question4='print(a)', question5='True', question6='#',question7='Triple Quotes', question8='name3',
        question9='Underscore(_)', question10='Each word excepts the first starts with a capital letter'
   )
    
    db.session.add(student)
    db.session.add(cryptography_answers)
    db.session.add(math_answers)
    db.session.add(python_answers)
        
    db.session.commit() 