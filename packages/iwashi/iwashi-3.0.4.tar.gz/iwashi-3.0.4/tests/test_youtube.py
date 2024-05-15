import pytest
from iwashi.service.youtube import Youtube
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_youtube():
    service = Youtube()
    correct = Result(
        service=service,
        id="Femtanyl03",
        url="https://www.youtube.com/@Femtanyl03",
        name="Femtanyl",
        description="Online! \nbusiness inquiries only: noellemansbridge@gmail.com\n",
        profile_picture="https://yt3.googleusercontent.com/_h7l3oeXeWpUfONKDid-FgmSZ8sx9WLTgNn-uMtaD42twSqidbnjPoZI4wuGwhcTpi6OOxyFLw=s900-c-k-c0x00ffffff-no-rj",
        links={
            "https://femtanyl.bandcamp.com/",
            "https://twitter.com/femtanylll",
        },
    )
    await _test_service(
        service,
        correct,
        "https://www.youtube.com/@Femtanyl03",
        "https://www.youtube.com/@Femtanyl03/community",
        "https://www.youtube.com/watch?v=MjhFNWBpiZ8",
        "https://youtu.be/MjhFNWBpiZ8?si=3nQomEKByaNZjtPQ",
        "youtu.be/MjhFNWBpiZ8",
    )
