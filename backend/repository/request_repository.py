from backend.domain import AssetRequest


def get_existing_requests(session):
    return session.query(AssetRequest)

