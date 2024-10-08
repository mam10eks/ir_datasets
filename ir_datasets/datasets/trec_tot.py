import ir_datasets
from ir_datasets.util import ZipExtract, Cache, Lazy, DownloadConfig
from ir_datasets.formats import TrecQrels, JsonlQueries, JsonlDocs, TrecQrels
from ir_datasets.datasets.base import Dataset, FilteredQueries, FilteredQrels, YamlDocumentation, Deprecated
from typing import NamedTuple, List, Dict

NAME = 'trec-tot'


class TipOfTheTongueDoc(NamedTuple):
    doc_id: str
    page_title: str
    wikidata_id: str
    wikidata_classes: List[str]
    text: str
    sections: Dict[str, str]
    infoboxes: List[Dict[str, str]]

    def default_text(self):
        """
        We use the title and text of the TipOfTheTongueQuery as default_text because that is everything available for users who want to respond to such an information need.
        """
        return self.page_title + ' ' + self.text

class TipOfTheTongueDoc2024(NamedTuple):
    doc_id: str
    title: str
    wikidata_id: str
    text: str
    sections: Dict[str, str]

    def default_text(self):
        """
        We use the title and text of the TipOfTheTongueQuery as default_text because that is everything available for users who want to respond to such an information need.
        """
        return self.title + ' ' + self.text

class TipOfTheTongueQuery2024(NamedTuple):
    query_id: str
    query: str

    def default_text(self):
        return self.query


class TipOfTheTongueQuery(NamedTuple):
    query_id: str
    url: str
    domain: str
    title: str
    text: str
    sentence_annotations: List[Dict[str, str]]

    def default_text(self):
        return self.title + ' ' + self.text


QUERY_MAP = {'query_id': 'id', 'url': 'url', 'domain': 'domain', 'title': 'title', 'text': 'text', 'sentence_annotations': 'sentence_annotations'}


def _init():
    documentation = YamlDocumentation(f'docs/{NAME}.yaml')
    base_path = ir_datasets.util.home_path()/NAME
    dlc = DownloadConfig.context(NAME, base_path)
    subsets = {}

    main_dlc = dlc['2023']
    base = Dataset(
        documentation('_'),
    )
    ir_datasets.registry.register(NAME, base)

    docs_2023_handler = JsonlDocs(Cache(ZipExtract(main_dlc, 'TREC-TOT/corpus.jsonl'), base_path/'2023/corpus.jsonl'), doc_cls=TipOfTheTongueDoc, lang='en')
    subsets['2023'] = Dataset(
        docs_2023_handler,
        documentation('2023'),
    )

    ir_datasets.registry.register(f'{NAME}/2023', subsets['2023'])
    for s in ['train', 'dev']:
        subsets[f'2023/{s}'] = Dataset(
            docs_2023_handler,
            JsonlQueries(Cache(ZipExtract(main_dlc, f'TREC-TOT/{s}/queries.jsonl'), base_path/f'2023/{s}/queries.jsonl'), query_cls=TipOfTheTongueQuery, mapping=QUERY_MAP, lang='en'),
            TrecQrels(Cache(ZipExtract(main_dlc, f'TREC-TOT/{s}/qrel.txt'), base_path/f'2023/{s}/qrel.txt'), {0: 'Not Relevant', 1: 'Relevant'}),
            documentation(f'2023/{s}'),
        )
        ir_datasets.registry.register(f'{NAME}/2023/{s}', subsets[f'2023/{s}'])

    main_dlc = dlc['2024']

    docs_2024_handler = JsonlDocs(Cache(ZipExtract(main_dlc, 'corpus.jsonl'), base_path/'2024/corpus.jsonl'), doc_cls=TipOfTheTongueDoc2024, lang='en')
    subsets['2024'] = Dataset(
        docs_2024_handler,
        documentation('2024'),
    )
    ir_datasets.registry.register(f'{NAME}/2024', subsets['2024'])
    for s in ['test']:
        subsets[f'2024/{s}'] = Dataset(
            docs_2024_handler,
            JsonlQueries(Cache(ZipExtract(dlc[f'2024-{s}'], f'{s}-2024/queries.jsonl'), base_path/f'2024/{s}-2024/queries.jsonl'), query_cls=TipOfTheTongueQuery2024, lang='en'),
            documentation(f'2024/{s}'),
        )
        ir_datasets.registry.register(f'{NAME}/2024/{s}', subsets[f'2024/{s}'])


    return base, subsets


base, subsets = _init()
