import re
from typing import Literal, TypeAlias, Self, Union

import torch
from .database import dataBase
from ..const import Embedding, c_source
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import faiss
import ctypes


def __import():
    global docNode, docTree
    from nodoc import docNode
    from nodoc import docTree


_docNodes: TypeAlias = list['docNode']
_Forest: TypeAlias = list['docTree']


class c_methods:
    
    def __init__(self, path: str) -> None:
        """
        - path: str, dll的扩展路径
        """
        if c_methods.is_available():
            self.cls = ctypes.CDLL(path)

    def search(self, query_matrix: np.ctypeslib._ndptr, query_text: np.ctypeslib._ndptr, rows: int, columns: int) -> int:
        """
        搜索查询矩阵与query_text最相似的向量的索引。
        - query_matrix: _ndptr, 传入一个查询矩阵的指针。
        - query_text: _ndptr, 传入待查询文本嵌入的指针。
        - rows: int, 行数。
        - columns: 列数。
        返回一个整型索引值。
        """
        if c_methods.is_available():
            return self.cls.search(query_matrix ,query_text, rows, columns)
        else:
            raise FileExistsError(f'{c_source.vectordb} 扩展不存在。')
    
    @staticmethod
    def is_available() -> bool:
        if os.path.exists(c_source.vectordb):
            return True
        return False


class vectorDB(dataBase):

    def __init__(self, forest: _Forest = [], mode: Literal['exact', 'low'] = 'exact', cache_folder='./', *, model: SentenceTransformer | None | str = None) -> None:
        """
        实例化一个向量数据库对象。
        - forest: _Forest, 树列表，作为数据库的查询树。
        - mode: Literal['exact', 'low'], `exact`为准确模式，`low`为低耗模式，决定数据库使用的Embedding模型。
        - cache_folder: str = './', 数据库模型的缓存路径。
        """
        super().__init__()
        if model is None:
            match mode:
                case 'low':
                    __model = 'BAAI/bge-small-zh'
                case _:
                    __model = 'BAAI/bge-large-zh-v1.5'
            device = 'cuda' if torch.cuda.is_available() else None
            self.model = SentenceTransformer(
                __model, cache_folder=cache_folder, device=device)
            "该数据库使用的模型（该模型必须是或继承自SentenceTransformer）。"
        elif isinstance(model, SentenceTransformer):
            self.model = model
        elif isinstance(model, str):
            device = 'cuda' if torch.cuda.is_available() else None
            self.model = SentenceTransformer(
                model, device = device
            )
        else:
            raise TypeError(f'期望：{SentenceTransformer}, 实际：{type(model)}')

        self.ebmapping: _docNodes = [
            node for tree in forest for node in tree.DFT()]
        "Eb节点映射，包含了数据库中所有的节点，可通过索引的方式直接顺序访问这些节点（不推荐）。"

        self.embeddings: Embedding = self.model.encode([
            node.data['content']
            for node in self.ebmapping
        ], normalize_embeddings=True)
        self.embeddings = self.embeddings.astype(np.double)
        "文本嵌入查询矩阵，用于计算查询相似度，不推荐读取。"

        self.c_methods: c_methods = c_methods(c_source.vectordb)

    def insert(self, index: int, node: 'docNode'):
        self.ebmapping.insert(index, node)
        self.embeddings = np.insert(
            self.embeddings, index,
            self.model.encode(node.data['content']),
            axis=0
        )

    def query_by_faiss(self, text: str, count: int = 1, threshold: float = 0.5) -> Union['docNode', list['docNode']]:
        """
        从数据库中查询节点。（基于faiss的查询）
        - text: str, 查询的文本，作为相似性判断的根据。
        - count: int, 查询节点的数量。
        - threshold: float = 0.5, 查询阈值，低于阈值将被抛弃。
        """
        query_text = self.__find_chinese(text)
        if query_text == '':
            return None
        final_text = self.model.encode(
            query_text, normalize_embeddings=True)
        text_vector = np.array([final_text])
        # pytorch -> fairs
        dimension = self.embeddings.shape[-1]
        indexs = faiss.IndexFlatIP(dimension)
        indexs.add(self.embeddings)
        _, indices = indexs.search(text_vector, count)
        indexs = list(indices.flatten())

        nodes = []
        for index in indexs:
            nodes.append(self.ebmapping[index])
        if len(nodes) == 1:
            return nodes[0]
        return nodes

    def query_by_cpp(self, text: str, count: int = 1, threshold: float = 0.5) -> Union['docNode', list['docNode']]:
        query_text = self.__find_chinese(text)
        if query_text == '':
            return None
        final_text = self.model.encode(
            query_text, normalize_embeddings=True)
        text_vector = np.array(final_text, dtype=np.double)
        query_matrix = self.embeddings.ctypes.data_as(np.ctypeslib.ndpointer(
            ctypes.c_double, self.embeddings.ndim, self.embeddings.shape))
        query_text = text_vector.ctypes.data_as(np.ctypeslib.ndpointer(
            ctypes.c_double, text_vector.ndim, text_vector.shape))
        index = self.c_methods.search(
            query_matrix, query_text, *self.embeddings.shape)

        nodes = []
        nodes.append(self.ebmapping[index])
        if len(nodes) == 1:
            return nodes[0]
        return nodes

    def query(self, text: str, count: int = 1, threshold: float = 0.5) -> Union['docNode', list['docNode']]:
        """
        从数据库中查询节点。
        - text: str, 查询的文本，作为相似性判断的根据。
        - count: int, 查询节点的数量。
        - threshold: float = 0.5, 查询阈值，低于阈值将被抛弃。
        """
        query_text = self.__find_chinese(text)
        if query_text == '':
            return None
        final_text = self.model.encode(
            query_text, normalize_embeddings=True)
        text_vector = np.array([final_text])
        # pytorch -> faiss
        similarity = (self.embeddings @ text_vector.T).flatten()
        indexs = torch.from_numpy(similarity).topk(count).indices
        indexs = list(indexs)
        _max = similarity.max()
        if _max < threshold:
            return None
        for position, index in enumerate(indexs):
            if similarity[index] < threshold:
                del indexs[position]

        nodes = []
        for index in indexs:
            nodes.append(self.ebmapping[index])
        if len(nodes) == 1:
            return nodes[0]
        return nodes

    def __query(self, text: str) -> int:
        text = self.model.encode(text, normalize_embeddings=True)
        text_vector = np.array([text])
        index = (self.embeddings @ text_vector.T).argmax()
        return index

    def __find_chinese(self, text: str):
        pattern = re.compile(r'[^\u4e00-\u9fa50-9]+')
        chinese = re.sub(pattern, '', text)
        return chinese

    def delete(self, text_or_index: str | int) -> Self:
        """
        **警告**：不推荐使用该方法删除节点，其具有不可预见性。
        删除节点，并返回被删除的节点。
        - text_or_index: str | int, 为文本时，根据相似度删除节点，为索引时删除对应索引位置的节点。
        """

        if isinstance(text_or_index, int):
            index = text_or_index
        elif isinstance(text_or_index, str):
            index = self.__query(text_or_index)
        else:
            raise ValueError('只能接收索引或字符串。')

        self.embeddings = np.delete(self.embeddings, index, axis=0)
        result = self.ebmapping[index]
        del self.ebmapping[index]

        return result

    def export(self, name: str, directory: str = './'):
        return super().export(name, directory)

    def save(self):
        return super().save()
    
    @staticmethod
    def load(path: str) -> Self:
        return super(vectorDB, vectorDB).load(path)

    @property
    def data(self):
        return super().data
