import pytest
from iwashi.service.skeb import Skeb
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_skeb():
    service = Skeb()
    correct = Result(
        service=service,
        id="adultfear",
        url="https://skeb.jp/@adultfear",
        name="nerrin ☀️",
        description="Nerr (she/they) 20+ 🌺 EN/中文/日本語・Writer, GM, sometimes Artist・OCs, d&d, ttrpg, type-moon, toku, horror・yellow 🧡💛",
        profile_picture="https://pbs.twimg.com/profile_images/1648903417262403584/IOswj0Xs.jpg",
        links={
            "https://twitter.com/adultfear",
            "http://adultfear.carrd.co",
        },
    )
    await _test_service(
        service,
        correct,
        "https://skeb.jp/@adultfear",
    )
