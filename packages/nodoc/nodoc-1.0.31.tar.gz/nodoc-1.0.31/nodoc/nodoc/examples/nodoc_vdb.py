from nodoc import vectorDB
from nodoc import Markdown

message = {
    "metadata": {
        "filename": "foo.md"
    },
    "pipeline": [
        {
            "type": "title",
            "content": "标题 - A",
            "property": {
                "level": 1
            },
            "uuid": "0"
        },
        {
            "type": "title",
            "content": "## 副标题 - a",
            "property": {
                "level": 2
            },
            "uuid": "1",
            "parent": "0"
        },
        {
            "type": "text",
            "content": "我是一只小狗a",
            "property": {},
            "uuid": "2",
            "parent": "1"
        },
        {
            "type": "title",
            "content": "## 副标题 - b",
            "property": {
                "level": 2
            },
            "uuid": "3",
            "parent": "0"
        },
        {
            "type": "text",
            "content": "我是一只小狗a",
            "property": {},
            "uuid": "4",
            "parent": "3"
        }
    ]
}

document = Markdown.load_from_message(message)
document_tree = document.treeify()
database = vectorDB([document_tree], model='path/to/bge-large-zh-v1.5')

while True:
    query_text = input("输入查询内容：")
    output = database.query(query_text)
    print(output)