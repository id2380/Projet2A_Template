import datetime

from freezegun import freeze_time

from src.service.jwt_service import JwtService

jwt_service = JwtService("mysecret")


@freeze_time("2024-08-26 12:00:00")
def test_encode_jwt():
    user_id = "myUser"
    jwtResponse = jwt_service.encode_jwt(user_id=user_id)
    print(jwtResponse.access_token)
    assert (
        jwtResponse.access_token
        == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibXlVc2VyIiwiZXhwaXJ5X3RpbWVzdGFtcCI6MTcyNDY3NTQwMC4wfQ.HGQSpvCYTD3h7H9_Ys--ReQabvdOsdikeofkMHtHYMc"

    )

@freeze_time("2024-08-26 12:00:00")
def test_decode_jwt():
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoibXlVc2VyIiwiZXhwaXJ5X3RpbWVzdGFtcCI6MTcyNDY3NTQwMC4wfQ.HGQSpvCYTD3h7H9_Ys--ReQabvdOsdikeofkMHtHYMc"  
    decoded_jwt = jwt_service.decode_jwt(jwt)
    assert decoded_jwt.get("user_id") == "myUser"
    assert datetime.datetime.fromtimestamp(decoded_jwt.get("expiry_timestamp")) == datetime.datetime.fromisoformat(
        "2024-08-26 12:30:00"  # Expiration après 30 minutes
    )
