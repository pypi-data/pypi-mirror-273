import pytest

from iwashi import tree


@pytest.mark.asyncio
async def test_error():
    urls = {
        "https://www.youtube.com/shorts/BwG8SE77nww",
    }
    for url in urls:
        result = await tree(url)
        assert result, f"Failed to get {url}"
