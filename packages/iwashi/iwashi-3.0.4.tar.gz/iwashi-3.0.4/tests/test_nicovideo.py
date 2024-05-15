import pytest
from iwashi.service.nicovideo import Nicovideo
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_nicovideo():
    service = Nicovideo()
    correct = Result(
        service=service,
        id="128134532",
        url="https://www.nicovideo.jp/user/128134532",
        name="ラベンダーP",
        description="岡山県備前市日生町に住む2006年生まれの人 <br>好きなもの（鉄道、東方、艦これ、ボカロ、ボイロ、野球、中日、阪神、西武、オリックス、ロッテ、railwars、すくすく白沢）",
        profile_picture="https://secure-dcdn.cdn.nimg.jp/nicoaccount/usericon/12813/128134532.jpg?1710066983",
        links={
            "https://www.youtube.com/channel/UC4jehnRY1GBPBpg-Np4WFNg",
            "https://twitter.com/lavenderp2018",
        },
    )
    await _test_service(service, correct, "https://www.nicovideo.jp/user/128134532")
