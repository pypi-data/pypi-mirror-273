import json
import re
from typing import Any
from urllib import parse

import bs4

from iwashi.helper import HTTP_REGEX, normalize_url, traverse
from iwashi.service.youtube.types.ytinitialdata2 import ProfileRes2
from iwashi.service.youtube.types.ytinitialdata3 import ProfileRes3
from iwashi.visitor import Context, Service

from .types import thumbnails, ytinitialdata
from .types.about import AboutRes

VANITY_ID_REGEX = re.compile(r"youtube.com/@(?P<id>[\w\-.]+)")


class Youtube(Service):
    def __init__(self):
        super().__init__(
            name="Youtube",
            regex=re.compile(
                HTTP_REGEX + r"((m|gaming)\.)?(youtube\.com|youtu\.be)",
            ),
        )

    async def resolve_id(self, context: Context, url: str) -> str | None:
        normalized_url = normalize_url(url)
        if normalized_url is None:
            return None
        uri = parse.urlparse(normalized_url)
        if uri.hostname == "youtu.be":
            return await self._channel_by_video(context, uri.path[1:])
        type = next(filter(None, uri.path.split("/")))
        if type.startswith("@"):
            return self._id_from_vanity_url(url)
        if type == "playlist":
            return None
        if type == "watch":
            return await self._channel_by_video(
                context, parse.parse_qs(uri.query)["v"][0]
            )
        if type == "shorts":
            video_id = uri.path.split("/")[-1]
            return await self._channel_by_video(context, video_id)
        if type in ("channel", "user", "c"):
            return await self._channel_by_url(context, url)
        if len(uri.path) > 1:
            maybe_vanity = uri.path.split("/")[1]
            return self._id_from_vanity_url(f"https://youtube.com/@{maybe_vanity}")
        return None

    async def _channel_by_video(self, context: Context, video_id: str) -> str | None:
        result = await self._channel_by_oembed(context, video_id)
        if result is not None:
            return result
        response = await context.session.get(
            f"https://www.youtube.com/watch?v={video_id}"
        )
        response.raise_for_status()
        soup = bs4.BeautifulSoup(await response.text(), "html.parser")
        element = soup.select_one('span[itemprop="author"] > link[itemprop="url"]')
        if element is None:
            return None
        href = element.attrs.get("href")
        if href is None:
            return None
        return self._id_from_vanity_url(href)

    async def _channel_by_oembed(self, context: Context, video_id: str) -> str | None:
        res = await context.session.get(
            "https://www.youtube.com/oembed",
            params={
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "format": "json",
            },
        )
        if not res.ok:
            return None
        data = await res.json()
        author_url = data.get("author_url")
        if author_url is None:
            return None
        return self._id_from_vanity_url(author_url)

    async def _channel_by_url(self, context: Context, url: str) -> str | None:
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        data = self.extract_initial_data(soup)
        vanity_url = data["metadata"]["channelMetadataRenderer"]["vanityChannelUrl"]
        return self._id_from_vanity_url(vanity_url)

    def _id_from_vanity_url(self, url: str) -> str | None:
        match = VANITY_ID_REGEX.search(url)
        if match is None:
            return None
        return match.group("id")

    def parse_thumbnail(self, thumbnails: thumbnails) -> str:
        size = 0
        url: str | None = None
        for thumbnail in thumbnails["thumbnails"]:
            if thumbnail["width"] > size:
                size = thumbnail["width"]
                url = thumbnail["url"]
        if url is None:
            raise RuntimeError("Thumbnail not found")
        return url

    async def get_token(self, data: Any) -> str | None:
        data2: ProfileRes2 = data
        if "pageHeaderRenderer" in data2["header"]:
            pageHeaderViewModel = data2["header"]["pageHeaderRenderer"]["content"][
                "pageHeaderViewModel"
            ]
            if "attribution" not in pageHeaderViewModel:
                return None
            suffix = pageHeaderViewModel["attribution"]["attributionViewModel"][
                "suffix"
            ]
            if not suffix:
                return None
            for a in suffix["commandRuns"]:
                for b in a["onTap"]["innertubeCommand"]["showEngagementPanelEndpoint"][
                    "engagementPanel"
                ]["engagementPanelSectionListRenderer"]["content"][
                    "sectionListRenderer"
                ]["contents"]:
                    for c in b["itemSectionRenderer"]["contents"]:
                        endpoint = c["continuationItemRenderer"]["continuationEndpoint"]
                        if endpoint["commandMetadata"]["webCommandMetadata"][
                            "apiUrl"
                        ].startswith("/youtubei/v1/browse"):
                            return endpoint["continuationCommand"]["token"]
        else:
            data3: ProfileRes3 = data
            c4TabbedHeaderRenderer = data3["header"]["c4TabbedHeaderRenderer"]
            if "headerLinks" not in c4TabbedHeaderRenderer:
                return None
            channelHeaderLinksViewModel = c4TabbedHeaderRenderer["headerLinks"][
                "channelHeaderLinksViewModel"
            ]
            if "more" not in channelHeaderLinksViewModel:
                return None
            for a in channelHeaderLinksViewModel["more"]["commandRuns"]:
                for b in a["onTap"]["innertubeCommand"]["showEngagementPanelEndpoint"][
                    "engagementPanel"
                ]["engagementPanelSectionListRenderer"]["content"][
                    "sectionListRenderer"
                ]["contents"]:
                    for c in b["itemSectionRenderer"]["contents"]:
                        endpoint = c["continuationItemRenderer"]["continuationEndpoint"]
                        if endpoint["commandMetadata"]["webCommandMetadata"][
                            "apiUrl"
                        ].startswith("/youtubei/v1/browse"):
                            return endpoint["continuationCommand"]["token"]
        return None

    def parse_redirect(self, url: str) -> str:
        uri = parse.urlparse(url)
        if uri.hostname != "www.youtube.com":
            return url
        if uri.path == "/redirect":
            return parse.parse_qs(uri.query)["q"][0]
        return url

    async def visit(self, context: Context, id: str):
        url = f"https://www.youtube.com/@{id}"
        res = await context.session.get(url)

        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        data = self.extract_initial_data(soup)
        vanity_id = data["metadata"]["channelMetadataRenderer"]["vanityChannelUrl"]
        name = data["metadata"]["channelMetadataRenderer"]["title"]
        description = data["metadata"]["channelMetadataRenderer"]["description"]
        profile_picture = self.parse_thumbnail(
            data["metadata"]["channelMetadataRenderer"]["avatar"]
        )
        context.create_result(
            self,
            id=id,
            url=f"https://www.youtube.com/@{vanity_id.split('@')[1]}",
            name=name,
            description=description,
            profile_picture=profile_picture,
        )
        token = await self.get_token(data)
        if token is None:
            return
        about_res = await context.session.post(
            "https://www.youtube.com/youtubei/v1/browse",
            json={
                "context": {
                    "client": {
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36,gzip(gfe)",
                        "clientName": "WEB",
                        "clientVersion": "2.20240509.00.00",
                    },
                },
                "continuation": token,
            },
        )
        about_res.raise_for_status()
        about_data: AboutRes = await about_res.json()
        links: list[str] = []
        for a in about_data["onResponseReceivedEndpoints"]:
            for b in a["appendContinuationItemsAction"]["continuationItems"]:
                for c in b["aboutChannelRenderer"]["metadata"]["aboutChannelViewModel"][
                    "links"
                ]:
                    for d in c["channelExternalLinkViewModel"]["link"]["commandRuns"]:
                        url = d["onTap"]["innertubeCommand"]["urlEndpoint"]["url"]
                        links.append(url)

        for link in links:
            context.enqueue_visit(self.parse_redirect(link))

    def extract_initial_data(self, soup: bs4.BeautifulSoup) -> ytinitialdata:
        for script in soup.select("script"):
            if script.string is None:
                continue
            match = re.search(r"ytInitialData\s*=\s*({.*?});", script.string)
            if match is not None:
                data: ytinitialdata = json.loads(match.group(1))
                break
        else:
            raise RuntimeError("ytInitialData not found")
        return data
