import nox


@nox.session(python=["3.10", "3.11", "3.12"])
@nox.parametrize("django", ["4.2", "5.1"])
def tests(session, django):
    session.install(f"django=={django}")
    session.run("pytest", external=True)


@nox.session(python=["3.10", "3.11", "3.12"])
def lint(session):
    session.install("ruff==0.5.7")
    session.run("ruff", "check", external=True)
