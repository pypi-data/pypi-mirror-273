from itertools import groupby
from typing import List

from vnerrant.model import Edit, EditCollection


def get_match_edits(alignment):
    """
    Get the match edits from an alignment.
    Args:
        alignment (Alignment): An Alignment object

    Returns: A list of match edits
    """
    orig, corr, align_edits = alignment.orig, alignment.cor, alignment.align_seq
    edits = []
    # Split alignment into groups of M, T and rest. (T has a number after it)
    for op, group in groupby(align_edits, lambda x: x[0][0] if x[0][0] in {"M", "T"} else False):
        group = list(group)
        if op == "M":
            for seq in group:
                edits.append(Edit.from_original_and_correction(orig, corr, seq[1:]))
    return edits


def update_edits(orig_doc, cor_doc, edits):
    """
    Postprocess the edits by updating text, the start and end character indices.
    Args:
        orig_doc (Doc): An original spacy Doc object
        cor_doc (Doc): A corrected spacy Doc object
        edits (list[Edit]): A list of Edit objects
    """
    orig_tokens = [token._.full_text for token in orig_doc]
    cor_tokens = [token._.full_text for token in cor_doc]
    for edit in edits:
        edit.original.text = "".join([token._.full_text for token in edit.original.tokens])
        edit.corrected.text = "".join([token._.full_text for token in edit.corrected.tokens])

        if edit.original.start_token != 0:
            edit.original.start_char = len("".join(orig_tokens[: edit.original.start_token]))
        if edit.original.end_token != 0:
            edit.original.end_char = len("".join(orig_tokens[: edit.original.end_token]))

        if edit.corrected.start_token != 0:
            edit.corrected.start_char = len("".join(cor_tokens[: edit.corrected.start_token]))
        if edit.corrected.end_token != 0:
            edit.corrected.end_char = len("".join(cor_tokens[: edit.corrected.end_token]))


def merge_edit_collection_with_space_edits(edit_collection: EditCollection, space_edits: List[Edit]):
    """
    Merge the space edits to the edit collection.
    Args:
        edit_collection (EditCollection): An EditCollection object
        space_edits (list[Edit]): A list of Edit objects
    """
    # Merge SPACE with PUNCTUATION
    remained_edits = []
    for space_edit in space_edits:
        for edit in edit_collection.edits:
            if space_edit.original.end_char == edit.original.start_char:
                # new_edit, edit
                # [5, 5, ''], [5, 6, ',']
                if (
                    space_edit.original.start_char == space_edit.original.end_char
                    and space_edit.original.end_char == edit.original.start_char
                ):
                    edit.corrected.start_token = space_edit.corrected.start_token
                    edit.corrected.start_char = space_edit.corrected.start_char
                    edit.corrected.text = edit_collection.cor[edit.corrected.start_char : edit.corrected.end_char]
                    break

                if (
                    space_edit.original.start_char == space_edit.original.end_char
                    and space_edit.original.start_char == edit.original.end_char
                ):
                    edit.corrected.end_token = space_edit.corrected.end_token
                    edit.corrected.end_char = space_edit.corrected.end_char
                    edit.corrected.text = edit_collection.cor[edit.corrected.start_char : edit.corrected.end_char]
                    break

                # [14, 15, ' '], [15, 15, '']
                if (
                    edit.original.start_char == edit.original.end_char
                    and space_edit.original.end_char == edit.original.start_char
                ):
                    edit.original.start_token = space_edit.original.start_token
                    edit.original.start_char = space_edit.original.start_char
                    edit.original.text = edit_collection.orig[edit.original.start_char : edit.original.end_char]

                    edit.corrected.start_token = space_edit.corrected.start_token
                    edit.corrected.start_char = space_edit.corrected.start_char
                    edit.corrected.text = edit_collection.cor[edit.corrected.start_char : edit.corrected.end_char]
                    break

                if (
                    edit.original.start_char == edit.original.end_char
                    and space_edit.original.start_char == edit.original.end_char
                ):
                    edit.original.end_token = space_edit.original.end_token
                    edit.original.end_char = space_edit.original.end_char
                    edit.original.text = edit_collection.orig[edit.original.start_char : edit.original.end_char]

                    edit.corrected.end_token = space_edit.corrected.end_token
                    edit.corrected.end_char = space_edit.corrected.end_char
                    edit.corrected.text = edit_collection.cor[edit.corrected.start_char : edit.corrected.end_char]
                    break
        else:
            remained_edits.append(space_edit)

    edit_collection.edits.extend(remained_edits)


def update_operator(edits: List[Edit]):
    """
    Update the operator of the edits.
    Args:
        edits (list[Edit]): A list of Edit objects to be updated.
    """
    for edit in edits:
        orig_text = edit.original.text
        cor_text = edit.corrected.text
        if orig_text and cor_text:
            edit.edit_type = "R" + edit.edit_type[1:]
        elif not orig_text and cor_text:
            edit.edit_type = "M" + edit.edit_type[1:]
        else:
            edit.edit_type = "U" + edit.edit_type[1:]

def upadte_span_edit(edits: List[Edit]): # noqa D103
    """
    Update the replace operator of the edits.
    Args:
        edits (list[Edit]): A list of Edit objects to be updated.
    """
    for edit in edits:
        edit.original.text = edit.original.tokens.text
        edit.original.end_char = edit.original.start_char + len(edit.original.text)
        edit.corrected.text = edit.corrected.tokens.text
        edit.corrected.end_char = edit.corrected.start_char + len(edit.corrected.text)
            
def process_space_edit(edit: Edit) -> Edit:
    """
    Process the space edit.
    Args:
        edit (Edit): An Edit object to be processed.

    Returns: An Edit object after processing.
    """
    space_edit = edit.copy()
    align = len(edit.original.text.strip())

    new_orig_text = space_edit.original.text[align:]
    new_cor_text = space_edit.corrected.text[align:]

    while new_orig_text and new_cor_text:
        if new_orig_text[0] != new_cor_text[0]:
            break
        new_orig_text = new_orig_text[1:]
        new_cor_text = new_cor_text[1:]
        align += 1

    space_edit.original.start_char += align
    space_edit.original.text = new_orig_text

    space_edit.corrected.start_char += align
    space_edit.corrected.text = new_cor_text

    if new_orig_text and new_cor_text:
        space_edit.edit_type = "R:SPACE"
    elif not new_orig_text and new_cor_text:
        space_edit.edit_type = "M:SPACE"
    else:
        space_edit.edit_type = "U:SPACE"

    return space_edit
