"""
MyBatis 语法处理插件

重写词法分析逻辑：
1. 增加自动机状态类型类（ASTParseStatusMyBatis）
2. 继承并重写支持 MaBatis 语法的状态机处理方法（ASTParserMyBatis）

重写句法分析逻辑：
1. 增加 MyBatis 元素节点作为一般表达式的子类（SQLMyBatisExpression）
2. 继承并重写解析器以支持 MyBatis 元素解析（SQLParserMyBatis）
"""

import dataclasses
from typing import Union, List

from metasequoia_sql import SQLType, ASTBase
from metasequoia_sql.analyzer import AnalyzerRecursionASTToListBase, CurrentUsedQuoteColumn
from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core import SQLParser, ASTExpressionBase, ASTSingleSelectStatement
from metasequoia_sql.errors import AMTParseError
from metasequoia_sql.lexical import FSMMachine, FSMStatus, AMTSingle, AMTMark


class FSMMachineMyBatis(FSMMachine):
    """继承并重写支持 MaBatis 语法的状态机处理方法"""

    def handle(self, ch: str) -> bool:
        """处理单个变化"""
        if self.status == FSMStatus.WAIT and ch == "#":
            self.cache.append(ch)
            self.status = FSMStatus.CUSTOM_1
            return True
        if self.status == FSMStatus.CUSTOM_1:  # 在 # 之后
            if ch == "{":
                self.cache.append(ch)
                self.status = FSMStatus.CUSTOM_2
                need_move = True
            elif ch == "<END>":
                self.stack[-1].append(AMTSingle(self._cache_get_and_reset(), {AMTMark.NAME, AMTMark.COMMENT}))
                need_move = False
            else:
                self.cache.append(ch)
                self.status = FSMStatus.IN_EXPLAIN_1
                need_move = True
            return need_move
        if self.status == FSMStatus.CUSTOM_2:  # MyBatis 匹配状态
            if ch == "}":
                self.cache.append(ch)
                self.stack[-1].append(AMTSingle(self._cache_get_and_reset(), {AMTMark.NAME, AMTMark.CUSTOM_1}))
                self.status = FSMStatus.WAIT
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现结束标记符")
            else:
                self.cache.append(ch)
                self.status = FSMStatus.CUSTOM_2
            return True
        return super().handle(ch)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class SQLMyBatisExpression(ASTExpressionBase):
    """增加 MyBatis 元素节点作为一般表达式的子类"""

    mybatis_source: str = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        return self.mybatis_source


class SQLParserMyBatis(SQLParser):
    """继承并重写解析器以支持 MyBatis 元素解析"""

    @classmethod
    def build_token_scanner(cls, string: str) -> TokenScanner:
        """构造词法扫描器"""
        return TokenScanner(FSMMachineMyBatis.parse(string), ignore_space=True, ignore_comment=True)

    @classmethod
    def parse_monomial_expression(cls, scanner_or_string: Union[TokenScanner, str],
                                  maybe_window: bool,
                                  sql_type: SQLType = SQLType.DEFAULT
                                  ) -> ASTExpressionBase:
        """重写一般表达式元素解析逻辑"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search(AMTMark.CUSTOM_1):
            return SQLMyBatisExpression(mybatis_source=scanner.pop_as_source())
        return super().parse_monomial_expression(scanner, maybe_window, sql_type=sql_type)


class GetAllMybatisParams(AnalyzerRecursionASTToListBase):
    """获取使用的 MyBatis 参数"""

    @classmethod
    def handle(cls, node: ASTBase) -> List[str]:
        """自定义的处理规则"""
        if isinstance(node, SQLMyBatisExpression):
            return [node.source()[2:-1]]
        return cls.default_handle_node(node)


class GetMybatisParamInWhereClause(AnalyzerRecursionASTToListBase):
    """获取 WHERE 子句中的 Mybatis 参数"""

    @classmethod
    def handle(cls, node: ASTBase) -> List[str]:
        """自定义的处理规则"""
        if isinstance(node, SQLMyBatisExpression):
            return [node.source()[2:-1]]
        if isinstance(node, ASTSingleSelectStatement):
            return cls.handle(node.where_clause)
        return cls.default_handle_node(node)


class GetMybatisParamInGroupByClause(AnalyzerRecursionASTToListBase):
    """获取 GROUP BY 子句中的 Mybatis 参数"""

    @classmethod
    def handle(cls, node: ASTBase) -> List[str]:
        """自定义的处理规则"""
        if isinstance(node, SQLMyBatisExpression):
            return [node.source()[2:-1]]
        if isinstance(node, ASTSingleSelectStatement):
            return cls.handle(node.group_by_clause)
        return cls.default_handle_node(node)


if __name__ == "__main__":
    def test_main():
        """测试主逻辑"""
        test_sql = "SELECT shohin_mei FROM Shohin WHERE #{hanbai_tanka} > 500 GROUP BY #{tanka};"

        statements = SQLParserMyBatis.parse_statements(test_sql)
        for statement in statements:
            if isinstance(statement, ASTSingleSelectStatement):
                print(statement)
                print(statement.source(SQLType.MYSQL))
                print(CurrentUsedQuoteColumn.handle(statement))
                print(GetAllMybatisParams().handle(statement))
                print(GetMybatisParamInWhereClause().handle(statement))
                print(GetMybatisParamInGroupByClause().handle(statement))


    test_main()
