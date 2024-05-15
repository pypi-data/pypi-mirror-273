from typing import NotRequired, TypedDict


class WebCommandMetadata(TypedDict):
    apiUrl: str


class CommandMetadata(TypedDict):
    webCommandMetadata: WebCommandMetadata


class ContinuationCommand(TypedDict):
    token: str


class ContinuationEndpoint(TypedDict):
    commandMetadata: CommandMetadata
    continuationCommand: ContinuationCommand


class ContinuationItemRenderer(TypedDict):
    continuationEndpoint: ContinuationEndpoint


class ItemSectionRendererContentsItem(TypedDict):
    continuationItemRenderer: ContinuationItemRenderer


type ItemSectionRendererContents = list[ItemSectionRendererContentsItem]


class ItemSectionRenderer(TypedDict):
    contents: ItemSectionRendererContents


class SectionListRendererContentsItem(TypedDict):
    itemSectionRenderer: ItemSectionRenderer


type SectionListRendererContents = list[SectionListRendererContentsItem]


class SectionListRenderer(TypedDict):
    contents: SectionListRendererContents


class EngagementPanelSectionListRendererContent(TypedDict):
    sectionListRenderer: SectionListRenderer


class EngagementPanelSectionListRenderer(TypedDict):
    content: EngagementPanelSectionListRendererContent


class EngagementPanel(TypedDict):
    engagementPanelSectionListRenderer: EngagementPanelSectionListRenderer


class ShowEngagementPanelEndpoint(TypedDict):
    engagementPanel: EngagementPanel


class InnertubeCommand(TypedDict):
    showEngagementPanelEndpoint: ShowEngagementPanelEndpoint


class OnTap(TypedDict):
    innertubeCommand: InnertubeCommand


class CommandRunsItem(TypedDict):
    onTap: OnTap


type CommandRuns = list[CommandRunsItem]


class Suffix(TypedDict):
    commandRuns: CommandRuns


class AttributionViewModel(TypedDict):
    suffix: Suffix | None


class Attribution(TypedDict):
    attributionViewModel: AttributionViewModel


class PageHeaderViewModel(TypedDict):
    attribution: NotRequired[Attribution]


class Content(TypedDict):
    pageHeaderViewModel: PageHeaderViewModel


class PageHeaderRenderer(TypedDict):
    content: Content


class Header(TypedDict):
    pageHeaderRenderer: NotRequired[PageHeaderRenderer]


class ProfileRes2(TypedDict):
    header: Header


# data: ProfileRes = ...

# token: str | None = None
# for a in data['header']['pageHeaderRenderer']['content']['pageHeaderViewModel']['attribution']['attributionViewModel']['suffix']['commandRuns']:
#     for b in a['onTap']['innertubeCommand']['showEngagementPanelEndpoint']['engagementPanel']['engagementPanelSectionListRenderer']['content']['sectionListRenderer']['contents']:
#         for c in b['itemSectionRenderer']['contents']:
#             endpoint = c['continuationItemRenderer']['continuationEndpoint']
#             if endpoint['commandMetadata']['webCommandMetadata']['apiUrl'].startswith('/youtubei/v1/browse'):
#                 token = endpoint['continuationCommand']['token']
#                 break
