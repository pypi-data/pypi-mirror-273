from typing import TypedDict


class UrlEndpoint(TypedDict):
    url: str


class InnertubeCommand(TypedDict):
    urlEndpoint: UrlEndpoint


class OnTap(TypedDict):
    innertubeCommand: InnertubeCommand


class CommandRunsItem(TypedDict):
    onTap: OnTap


type CommandRuns = list[CommandRunsItem]


class Link(TypedDict):
    commandRuns: CommandRuns


class ChannelExternalLinkViewModel(TypedDict):
    link: Link


class LinksItem(TypedDict):
    channelExternalLinkViewModel: ChannelExternalLinkViewModel


type Links = list[LinksItem]


class AboutChannelViewModel(TypedDict):
    links: Links


class Metadata(TypedDict):
    aboutChannelViewModel: AboutChannelViewModel


class AboutChannelRenderer(TypedDict):
    metadata: Metadata


class ContinuationItemsItem(TypedDict):
    aboutChannelRenderer: AboutChannelRenderer


type ContinuationItems = list[ContinuationItemsItem]


class AppendContinuationItemsAction(TypedDict):
    continuationItems: ContinuationItems


class OnResponseReceivedEndpointsItem(TypedDict):
    appendContinuationItemsAction: AppendContinuationItemsAction


class AboutRes(TypedDict):
    onResponseReceivedEndpoints: list[OnResponseReceivedEndpointsItem]
