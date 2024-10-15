# nlp_mysql
基于通义千问实现的自然语言处理(NLP)查询数据库，替代传统报表开发，支持上下文对话，历史对话记录存储

## 所用技术
使用python语言，基于阿里云的通义千问大模型，实现对mysql数据库表的查询。

## 功能列表
1. 针对用户提问，回答数据库的相关数据查询问题。如果不涉及数据库查询，也可直接回答。
2. 数据库权限控制，用户只能查询数据库，不能做增删改操作。
3. 用户访问权限控制，每个用户只能查询自己的权限下的数据。
4. 基于上下文对话，用户可针对对话上下文提问。
5. 提供用户的聊天对话历史记录查询接口。
