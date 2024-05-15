from typing import TypedDict


class webCommandMetadata(TypedDict):
    apiUrl: str


class commandMetadata(TypedDict):
    webCommandMetadata: webCommandMetadata


class continuationCommand(TypedDict):
    token: str


class continuationEndpoint(TypedDict):
    commandMetadata: commandMetadata
    continuationCommand: continuationCommand


class continuationItemRenderer(TypedDict):
    continuationEndpoint: continuationEndpoint


class itemSectionRenderercontentsItem(TypedDict):
    continuationItemRenderer: continuationItemRenderer


type itemSectionRenderercontents = list[itemSectionRenderercontentsItem]


class itemSectionRenderer(TypedDict):
    contents: itemSectionRenderercontents


class contentsItem(TypedDict):
    itemSectionRenderer: itemSectionRenderer


type contents = list[contentsItem]


class sectionListRenderer(TypedDict):
    contents: contents


class content(TypedDict):
    sectionListRenderer: sectionListRenderer


class engagementPanelSectionListRenderer(TypedDict):
    content: content


class engagementPanel(TypedDict):
    engagementPanelSectionListRenderer: engagementPanelSectionListRenderer


class showEngagementPanelEndpoint(TypedDict):
    engagementPanel: engagementPanel


class innertubeCommand(TypedDict):
    showEngagementPanelEndpoint: showEngagementPanelEndpoint


class onTap(TypedDict):
    innertubeCommand: innertubeCommand


class commandRunsItem(TypedDict):
    onTap: onTap


type commandRuns = list[commandRunsItem]


class more(TypedDict):
    commandRuns: commandRuns


class channelHeaderLinksViewModel(TypedDict):
    more: more


class headerLinks(TypedDict):
    channelHeaderLinksViewModel: channelHeaderLinksViewModel


class c4TabbedHeaderRenderer(TypedDict):
    headerLinks: headerLinks


class header(TypedDict):
    c4TabbedHeaderRenderer: c4TabbedHeaderRenderer


class ProfileRes3(TypedDict):
    header: header


# data: ProfileRes2 = ...

# for a in data['header']['c4TabbedHeaderRenderer']['headerLinks']['channelHeaderLinksViewModel']['more']['commandRuns']:
#     for b in a['onTap']['innertubeCommand']['showEngagementPanelEndpoint']['engagementPanel']['engagementPanelSectionListRenderer']['content']['sectionListRenderer']['contents']:
#         for c in b['itemSectionRenderer']['contents']:
#             endpoint = c['continuationItemRenderer']['continuationEndpoint']
#             if endpoint['commandMetadata']['webCommandMetadata']['apiUrl'].startswith('/youtubei/v1/browse'):
#                 return endpoint['continuationCommand']['token']
