from project.tdd.factories import MemberFactory


def test_model(db_session):
    member = MemberFactory.build()

    db_session.add(member)
    db_session.commit()

    assert member.id
    assert member.avatar
    assert not member.avatar_thumbnail
