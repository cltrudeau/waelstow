import nox

@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"])
def test(session):
    session.install("-e", ".")
    session.run("./load_tests.py", external=True)
