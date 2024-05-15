from __future__ import annotations

import re
from typing import Any, List, Literal, NotRequired, TypedDict

from loguru import logger


from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Skeb(Service):
    def __init__(self):
        super().__init__(
            name="Skeb",
            regex=re.compile(HTTP_REGEX + r"skeb\.jp/@(?P<id>[\w-]+)", re.IGNORECASE),
        )
        self.request_key: str | None = None

    async def fetch_request_key(self, context: Context, url: str) -> str:
        if self.request_key is not None:
            return self.request_key
        res = await context.session.get(url)
        request_key = res.cookies.get("request_key")
        if request_key is None:
            raise RuntimeError("Could not find request_key")
        self.request_key = request_key.value
        return self.request_key

    async def visit(self, context: Context, id: str):
        url = f"https://skeb.jp/@{id}"
        request_key = await self.fetch_request_key(context, url)
        api_endpoint = f"https://skeb.jp/api/users/{id}"

        cookies = {
            "request_key": request_key,
        }

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "ja",
            "authorization": "Bearer null",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": url,
        }
        res = await context.session.get(api_endpoint, cookies=cookies, headers=headers)
        res.raise_for_status()
        data: Root = await res.json()

        context.create_result(
            self,
            id=id,
            url=url,
            name=data["name"],
            description=data["description"],
            profile_picture=data["avatar_url"],
        )

        context.enqueue_visit(data["url"])

        NOT_SUPPORTED = None
        PROVIDERS = {
            "nijie_id": NOT_SUPPORTED,
            "dlsite_id": NOT_SUPPORTED,
            "fanza_id": NOT_SUPPORTED,
            "pixiv_id": "https://www.pixiv.net/member.php?id={id}",
            "booth_id": "https://{id}.booth.pm",
            "fantia_id": "https://fantia.jp/fanclubs/{id}",
            "fanbox_id": "https://{id}.fanbox.cc",
            "skima_id": "https://skima.jp/profile?id={id}",
            "coconala_id": "https://coconala.com/users/{id}",
            "patreon_id": "https://www.patreon.com/{id}",
            "wishlist_id": NOT_SUPPORTED,
            "youtube_id": "https://www.youtube.com/channel/{id}",
        }

        for key, template in PROVIDERS.items():
            if key not in data:
                logger.warning(f"Could not find {key} in {data}")
                continue
            value = data[key]
            if value is None:
                continue
            if template is NOT_SUPPORTED:
                logger.warning(f"{key} is not supported")
                continue
            formatted_url = template.format(id=value)
            context.enqueue_visit(formatted_url)

        SERVICES = {
            "twitter": "https://twitter.com/{screen_name}",
        }
        for user_service_link in data.get("user_service_links", {}):
            if user_service_link["provider"] not in SERVICES:
                logger.warning(
                    f"Could not find {user_service_link['provider']} in {data}"
                )
                continue
            formatted_url = SERVICES[user_service_link["provider"]].format(
                screen_name=user_service_link["screen_name"]
            )
            context.enqueue_visit(formatted_url)


type UnknownField = Any
type UnknownId = int | str


class UserServiceLinksItem(TypedDict):
    provider: str
    screen_name: str


class SkillsItem(TypedDict):
    genre: str
    default_amount: NotRequired[int]


class CreditCardsItem(TypedDict):
    nsfw: bool


class CreditCards(TypedDict):
    jcb: CreditCardsItem
    master_card: CreditCardsItem
    visa: CreditCardsItem
    discover: CreditCardsItem
    american_express: CreditCardsItem


class PaymentMethods(TypedDict):
    credit_cards: CreditCards


class ImageUrls(TypedDict):
    src: str
    srcset: str


type Genre = Literal["art"]


class WorksItem(TypedDict):
    path: str
    private_thumbnail_image_urls: ImageUrls
    private: bool
    genre: Genre
    tipped: bool
    creator_id: int
    client_id: int
    vtt_url: UnknownField
    thumbnail_image_urls: ImageUrls
    duration: UnknownField
    nsfw: bool
    hardcore: bool
    consored_thumbnail_image_urls: ImageUrls
    body: str
    word_count: int
    transcoder: Literal["image"]
    creator_acceptable_same_genre: bool


class SimilarCreatorsItem(TypedDict):
    id: int
    creator: bool
    nsfw_acceptable: bool
    acceptable: bool
    name: str
    screen_name: str
    avatar_url: str
    header_url: str
    appeal_receivable: bool
    popular_creator_rank: UnknownField
    request_master_rank: UnknownField
    first_requester_rank: UnknownField
    deleted_at: UnknownField
    tip_acceptable_by: Literal["all"]
    accept_expiration_days: int
    skills: List[SkillsItem]
    genre: Genre


class Root(TypedDict):
    id: int
    acceptable: bool
    creator: bool
    avatar_url: str
    name: str
    nsfw_acceptable: bool
    private_acceptable: bool
    screen_name: str
    language: str
    header_url: str
    body_size: str
    received_works_count: int
    received_private_works_count: int
    received_nsfw_works_count: int
    sent_requests_average_cancel_time: int
    appeal_receivable: bool
    request_master_rank: UnknownField
    first_requester_rank: UnknownField
    sent_first_works_count: int
    sent_public_works_count: int
    popular_creator_rank: UnknownField
    instruction: Literal["unspecified"]
    asct: UnknownField
    description: str
    nijie_id: UnknownId
    dlsite_id: UnknownId
    fanza_id: UnknownId
    pixiv_id: int
    booth_id: UnknownId
    fantia_id: UnknownId
    fanbox_id: UnknownId
    skima_id: UnknownId
    coconala_id: UnknownId
    patreon_id: UnknownId
    busy: bool
    url: str
    wishlist_id: UnknownField
    youtube_id: str
    complete_rate: float
    show_social_profile: bool
    accept_expiration_days: int
    complete_expiration_days: int
    twitter_uid: str
    user_service_links: List[UserServiceLinksItem]
    banned: bool
    banned_by: str
    og_image_url: str
    skills: List[SkillsItem]
    payment_methods: PaymentMethods
    genre: Genre
    default_amount: UnknownField
    acceptable_only_private: bool
    tip_acceptable: bool
    yearly_report_client_visible: bool
    received_works: List[WorksItem]
    sent_works: List[WorksItem]
    similar_creators: List[SimilarCreatorsItem]
