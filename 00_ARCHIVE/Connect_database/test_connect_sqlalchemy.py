from sqlalchemy import create_engine


engine = create_engine('postgresql://localhost/[test_python]')

print("ok")