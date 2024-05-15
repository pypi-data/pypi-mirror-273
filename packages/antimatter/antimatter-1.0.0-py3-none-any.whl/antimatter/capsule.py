import json
from dataclasses import dataclass
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Union

import antimatter_engine as ae

import antimatter.extra_helper as extra_helper
import antimatter.handlers as handlers
from antimatter.cell_path import cell_path
from antimatter.datatype.datatypes import Datatype
from antimatter.extra_helper import META_TYPE_KEY
from antimatter.fieldtype import converters
from antimatter.tags import SpanTag, ColumnTag, CapsuleTag


class CapsuleBindings:
    def __init__(self, capsule_session: ae.PySessionCapsule):
        """
        CapsuleBindings holds the capsule session for the underlying Antimatter Capsule.

        :param capsule_session: The bundle session for the underlying Antimatter Capsule Bundle
        :param failed: A list of capsules in the Antimatter Capsule Bundle that could not be opened.
        """
        self._capsule_session = capsule_session
        if capsule_session is not None:
            self.capsule_tags, self.column_names, self.column_tags, self.redacted_data, self.data_span_tags, self.extra_info = capsule_session.read_all_with_tags([])

    def read_extras(self) -> List[str]:
        """
        Get the extras field stored in the capsule.

        :return: The extras string.
        """
        return self.extra_info

    def read_all(self) -> Tuple[List[str], List[List[bytes]], str]:
        """
        Get the column definitions, redacted data and extras from the underlying capsule.

        :return: The column definition list, a 2D list of list of string containing the redacted data, and the extras
                 string.
        """
        return self.column_names, self.redacted_data, self.extra_info

    def read_all_with_tags(self) -> Tuple[
            List[ae.PyTag], 
            List[str], 
            List[List[ae.PyTag]], 
            List[List[List[bytes]]], 
            List[List[List[ae.PySpanTag]]], 
            str,
        ]:
        """
        Get the tag information (capsule, column, etc.), column definitions, redacted 
        data and extras from the underlying capsule. This method is meant to provide
        insight into what is being tagged along with the corresponding tag that was
        applied.

        :return: The list of capsule tags, column definition list, list of column tags,
                 a 2D list of list of string containing the redacted data, a list of data span 
                 tags, and the extras string.
        """
        return self.capsule_tags, self.column_names, self.column_tags, self.redacted_data, self.data_span_tags, self.extra_info

    def capsule_ids(self) -> List[str]:
        """
        Get a list capsule IDs associated with this CapsuleBinding.
        """
        return self._capsule_session.capsule_ids()

    def domain_id(self) -> str:
        """
        Get the domain ID associated with the capsule.
        """
        return self._capsule_session.domain_id()


@dataclass
class CapsuleMeta:
    datatype_in: Datatype
    extra: Dict[str, Any]


class Capsule:
    _capsule: CapsuleBindings

    def __init__(
        self,
        capsule_binding: CapsuleBindings,
    ):
        """
        Capsule holds the capsule bindings for the underlying Antimatter Capsule
        and converts it into various different supported formats.

        :param capsule_binding:
        The capsule bindings for the underlying Antimatter Capsule
        """
        self._capsule = capsule_binding

    @property
    def capsule(self) -> CapsuleBindings:
        """
        Get the capsule binding for the underlying Antimatter Capsule.

        :return: The Antimatter Capsule binding.
        """
        return self._capsule

    def data(self, **kwargs) -> Any:
        """
        Get the data from the underlying Antimatter Capsule using the supplied
        read parameters. This will raise an error if the capsule is sealed.

        :param kwargs: The extra arguments to pass to the data handler.
        :return: The data in its default format.
        """
        column_names, rows, extra = self._capsule.read_all()

        extra = json.loads(extra)
        default_dt_val = extra.get(META_TYPE_KEY, Datatype.Unknown.value)
        default_dt = Datatype(default_dt_val)

        h = handlers.factory(default_dt)  # TODO: try/except
        e = extra_helper.extra_for_capsule(default_dt, extra, **kwargs)
        d = h.from_generic(column_names, rows, e)
        return d

    def data_as(self, dt: Union[Datatype, str], **kwargs) -> Any:
        """
        Get the data from the underlying Antimatter Capsule using the supplied
        read parameters. This will raise an error if the capsule is sealed.

        :param dt: The datatype to use for reading data.
        :param kwargs: The extra arguments to pass to the data handler.
        :return: The data in the specified format.
        """
        dt = Datatype(dt)
        column_names, rows, extra = self._capsule.read_all()
        extra = json.loads(extra)

        h = handlers.factory(dt)  # TODO: try/except
        e = extra_helper.extra_for_capsule(dt, extra, **kwargs)
        d = h.from_generic(column_names, rows, e)
        return d

    def _iterate_columns_first(self, action, column_names, redacted_data, capsule_tags, column_tags, data_span_tags):
        """
        Helper method for self.data_with_tags to iterate and group data by column
        """
        for colidx, cname in enumerate(column_names):
            column_items = []
            for rowidx, row in enumerate(redacted_data):
                column_items.append(action(cname, colidx, row, rowidx, capsule_tags, column_tags, data_span_tags))
            yield column_items

    def _iterate_rows_first(self, action, column_names, redacted_data, capsule_tags, column_tags, data_span_tags):
        """
        Helper method for self.data_with_tags to iterate and group data by row
        """
        for rowidx, row in enumerate(redacted_data):
            row_items = []
            for colidx, cname in enumerate(column_names):
                row_items.append(action(cname, colidx, row, rowidx, capsule_tags, column_tags, data_span_tags))
            yield row_items

    def _process_data_item(self, cname, colidx, row, rowidx, capsule_tags, column_tags, data_span_tags, extra_info):
        """
        Helper method for self.data_with_tags to create a dictionary providing 
        insight into how an underlying data item has been tagged.
        """
        ft = extra_helper.get_field_type(cname, extra_info)
        conv = converters.Standard.field_converter_from_generic(ft)

        item = {
            "capsule_tags": [CapsuleTag(name=t.name, tag_type=t.tag_type, tag_value=t.value) for t in capsule_tags],
            "column": cname,
            "column_tags": [
                ColumnTag(column_name=cname, tag_names=[t.name], tag_type=t.tag_type, tag_value=t.value)
                for t in column_tags[colidx]
            ],
            "data": conv(row[colidx]),
            "bytes": row[colidx],
            "span_tags": [
                SpanTag(name=t.tag.name, cell_path=cell_path(cname, rowidx), 
                        start=t.start, end=t.end, tag_type=t.tag.tag_type, tag_value="")
                for t in data_span_tags[rowidx][colidx]
            ],
            "row": rowidx,
        }
        return item

    def data_with_tags(self, column_major: bool=False, inline=False, **kwargs) -> List[List[Dict]]:
        """
        Get the data and related tag information from the underlying Antimatter 
        Capsule using the supplied read parameters. This will raise an error if 
        the capsule is sealed.

        :param column_major: The orientation to use for the return list. A value of True
                     results in data being grouped together by column versus a value
                     of False which results in data being grouped together by row.
        :param inline: The option to markup the data with SpanTag information similar
                       to applying HTML blocks.
        :param kwargs: The extra arguments to pass to the data handler.
        :return: The list of dictionaries providing insight to the Tags that were
                 found within a data item.
        """
        capsule_tags, column_names, column_tags, redacted_data, data_span_tags, extra_info = \
            self._capsule.read_all_with_tags()
        
        extra_info = json.loads(extra_info)

        if not column_major:  
            iterate_func = self._iterate_rows_first
        else:
            iterate_func = self._iterate_columns_first

        action = lambda cname, colidx, row, rowidx, capsule_tags, column_tags, data_span_tags: \
            self._process_data_item(cname, colidx, row, rowidx, capsule_tags, column_tags, data_span_tags, extra_info)

        rv = list(
            iterate_func(
                action, column_names, redacted_data, capsule_tags, column_tags, data_span_tags
            )
        )

        if inline:
            for group in rv:
                for item in group:
                    if item["span_tags"]:
                        item["bytes"] = _markup_bytes(item["bytes"], item["span_tags"])

        return rv

    def capsule_ids(self) -> List[str]:
        """
        Get a list capsule IDs associated with this capsule bundle.
        """
        return self._capsule.capsule_ids()

    def domain_id(self) -> str:
        """
        Get the domain ID associated with this capsule.
        """
        return self._capsule.domain_id()


def _markup_bytes(text: bytes, span_tags: List[SpanTag]) -> bytes:
    """
    Marks up a byte string with `<span></span>` block elements according to the
    provided SpanTag list. While SpanTags are not expected to overlap, this 
    function is compatible with overlapping SpanTag as a possible future 
    requirement.
    """
    # map positions to opening and closing tag names
    open_tags = defaultdict(list)
    close_tags = defaultdict(list)
    span_tags = sorted(span_tags, key=lambda tag: (tag.start, tag.end))
    for tag in span_tags:
        open_tags[tag.start].append(tag.name)
        close_tags[tag.end].append(tag.name)

    result = bytearray()
    for i in range(len(text)):
        # close tags at this position
        if close_tags[i]:
            result.extend(f"</span>".encode('utf-8'))

        # open tags at this position
        if open_tags[i]:
            names = open_tags[i]
            result.extend(f"<span tags={names}>".encode('utf-8'))

        result.append(text[i])

    # handle closing tags at the end of the string
    if close_tags[len(text)]:
        result.extend(f"</span>".encode('utf-8'))

    return bytes(result)
