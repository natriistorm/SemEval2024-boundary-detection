import re
import difflib
import json
import random
import pandas as pd
from splitter import split_into_sentences


def find_index_of_word(target_sentence: str, check_trio: tuple) -> int:
    """

    Args:
        target_sentence: whitespace-splitted boundary sentence
        check_trio: neighbouring words for boundary words

    Returns: index of boundary word within whitespace-splitted boundary sentence

    """
    # boundary word is the first in the sentence
    if target_sentence[0:3] == check_trio:
        return 0

    # boundary word is the last in the sentece
    if target_sentence[-2:] == check_trio:
        return len(target_sentence) - 1

    for i in range(1, len(target_sentence) - 1):
        if target_sentence[i - 1] == check_trio[0] and target_sentence[i] == check_trio[1] and \
                target_sentence[i + 1] == check_trio[2]:
            return i

def create_example(sentences: list, idx_begin: int, idx_end: int,
                   idx_boundary: int, position: int, target_word: str) -> tuple:
    """

    Args:
        sentences: list of sentences
        idx_begin: index of first sentence for new text
        idx_end: index of last sentence for new text
        idx_boundary: index of target sentence
        position: position of boundary word in target sentence
        target_word: boundary word to check

    Returns:

    """
    text = " ".join(sentences[idx_begin:idx_end])
    num_of_words_before_last_sent = " ".join(sentences[idx_begin:idx_boundary]).split(" ")
    new_position_of_target = len(num_of_words_before_last_sent) + position
    new_target_word = text.split(" ")[new_position_of_target]
    assert new_target_word == target_word
    return text, new_position_of_target

def create_new_examples(splitted_sentences: list, target_sentence: str,
                        idx: int, check_trio: tuple, position=0) ->  list:
    """

    Args:
        splitted_sentences: list of all sentences, whitespace-splitted
        target_sentence: sentence where change of author occurs
        idx: index of traget sentence in splitted_sentences
        check_trio: three words containing boundary word for search of position
        position: position of boundary word

    Returns: list of tuples (new_text, new_label)

    """
    # need to add a check that check trio is shifted when boundary word is on the border
    sentences = [" ".join(sentence) for sentence in splitted_sentences]
    num_sent = len(splitted_sentences)
    word_to_check = check_trio[1]
    text1 = text2 = text3 = text4 = ""
    new_position_of_target1 = new_position_of_target2 = new_position_of_target3 = new_position_of_target4 = position
    if num_sent == 1:
        return [(text1, new_position_of_target1), (text2, new_position_of_target2),
               (text3, new_position_of_target3), (text4, new_position_of_target4)]
    if idx == 0:
        idx1 = num_sent // 2
        text1 = " ".join(sentences[:idx1])
        new_position_of_target1 = position
    elif idx == num_sent - 1:
        idx1 = num_sent // 2
        if idx1 != 0:
            text1 = " ".join(sentences[idx1:])
            position = find_index_of_word(target_sentence, check_trio)
            num_of_words_before_last_sent = " ".join(sentences[idx1:idx]).split(" ")
            new_position_of_target1 = len(num_of_words_before_last_sent) + position
    else:
        position = find_index_of_word(target_sentence, check_trio)
        idx1_begin = max(0, idx - 1)
        idx1_end = min(num_sent - 1, idx + 2)
        if idx1_end - idx1_begin > 1:
            text1, new_position_of_target1 = create_example(sentences, idx1_begin, idx1_end,
                                                            idx, position, word_to_check)

        idx2_begin = max(0, idx - 2)
        idx2_end = min(num_sent - 1, idx + 3)
        if (idx2_begin == 0 and idx2_end == num_sent - 1) or \
                (idx2_begin == idx1_begin and idx2_end == idx1_end) or \
                (idx1_begin == idx2_begin and idx1_begin == 0):
            return [(text1, new_position_of_target1), (text2, new_position_of_target2),
                   (text3, new_position_of_target3), (text4, new_position_of_target4)]
        if idx2_end - idx2_begin > 2:
            text2, new_position_of_target2 = create_example(sentences, idx2_begin, idx2_end,
                                                            idx, position, word_to_check)
        idx3_begin = max(0, idx - 3)
        idx3_end = min(num_sent - 1, idx + 4)
        if (idx3_begin == 0 and idx3_end == num_sent - 1) or \
                (idx3_begin == idx2_begin and idx2_end == idx3_end) or \
                (idx3_begin == idx2_begin and idx3_begin == 0):
            return [(text1, new_position_of_target1), (text2, new_position_of_target2),
                   (text3, new_position_of_target3), (text4, new_position_of_target4)]
        if idx3_end - idx3_begin > 2:
            text3, new_position_of_target3 = create_example(sentences, idx3_begin, idx3_end,
                                                            idx, position, word_to_check)

        idx4_begin = max(0, idx - 4)
        idx4_end = min(num_sent - 1, idx + 5)

        if (idx4_begin == 0 and idx4_end == num_sent - 1) or \
                (idx4_begin == idx3_begin and idx4_end == idx3_end):
            return [(text1, new_position_of_target1), (text2, new_position_of_target2),
                   (text3, new_position_of_target3), (text4, new_position_of_target4)]
        if idx4_end - idx4_begin > 2:
            text4, new_position_of_target4 = create_example(sentences, idx4_begin, idx4_end,
                                                            idx, position, word_to_check)
    return [(text1, new_position_of_target1), (text2, new_position_of_target2),
            (text3, new_position_of_target3), (text4, new_position_of_target4)]


def append_augmented_text(augmented_df: list, augmented_text: str, text_label: int,
                          text_id: str, augmentation_id: int) -> pd.DataFrame:
    """

    Args:
        augmented_df: list with new versions of texts to add new text
        augmented_text: shortened version of original text
        text_label: newly calculated label
        text_id: original id of the text
        augmentation_id: id, that will be appended to text_id to mark its an augmented text

    Returns: updated dataframe with new versions of texts

    """
    if augmented_text != "":
        augmented_df.append({"id": f"{text_id}_{augmentation_id}", "text": augmented_text, "label": text_label})
    return augmented_df


def move_special_symbols_to_previous_sent(splitted_sentences):
    """
    Args:
        splitted_sentences: list of whitespace-split sentences

    Returns: whitespace-split sentences without special symbols at the beginning of each sentence
    """
    for i in range(1, len(splitted_sentences)):
        if re.match(r"[\r\n]+\w+", splitted_sentences[i][0]):
            continue
        if re.match(r"\r\n", splitted_sentences[i][0]) or re.match(r"[)\],;:]\D*", splitted_sentences[i][0]):
            splitted_sentences[i - 1][-1] = splitted_sentences[i - 1][-1] + splitted_sentences[i][0]
            splitted_sentences[i] = splitted_sentences[i][1:]
    return splitted_sentences


def process(data, set_text_id=None) -> list:
    """

    Args:
        data: texts to augment
        text_id: if necessary, only one text with particular text_id can be augmented

    Returns: dataframe of augmneted texts

    """
    augmented_data = []
    g = 0
    failed_flg = False
    for elem in data:
        idx = 0
        words_cnt = 0
        sent_idx = 0
        if set_text_id:
            if elem['id'] != set_text_id:
                continue
        text_id = elem['id']
        label = elem['label']
        text = elem['text']

        splitted_text = text.split(" ")

        sentences = split_into_sentences(text)
        splitted_sentences = [sentence.split(" ") for sentence in sentences]

        splitted_sentences = move_special_symbols_to_previous_sent(splitted_sentences)

        # iterate through sentence
        # if some whitespaces or words are missing, we insert them
        idx_of_sentence = 0
        idx_of_word_in_sent = 0

        for word_idx, word in enumerate(splitted_text):
            try:
                str1 = splitted_sentences[idx_of_sentence][idx_of_word_in_sent]
            except IndexError as err:
                failed_flg = True
                break
            str2 = word
            if str1 != str2:
                if str2 == '':
                    splitted_sentences[idx_of_sentence].insert(idx_of_word_in_sent, word)
                    idx_of_word_in_sent += 1
                    continue
                for i, s in enumerate(difflib.ndiff(str1, str2)):
                    if s[0] == ' ':
                        continue
                    elif s[0] == '+' and s[-1] == '\n':
                        splitted_sentences[idx_of_sentence].insert(idx_of_word_in_sent, word)
                        try:
                            str_to_del = ""
                            while len(str_to_del) < len(word):
                                str_to_del += splitted_sentences[idx_of_sentence].pop(idx_of_word_in_sent + 1)
                                str_to_del += '\n'
                        except IndexError as err:
                            splitted_sentences[idx_of_sentence + 1].pop(0)
                        break
                    elif s[0] == '+' and s[-1] == '\r':
                        splitted_sentences[idx_of_sentence].insert(idx_of_word_in_sent, word)
                        try:
                            str_to_del = ""
                            while len(str_to_del) < len(word):
                                str_to_del += splitted_sentences[idx_of_sentence].pop(idx_of_word_in_sent + 1)
                                str_to_del += '\r'
                        except IndexError as err:
                            splitted_sentences[idx_of_sentence + 1].pop(0)
                        break
                    elif s[0] == '+' and idx_of_word_in_sent == len(splitted_sentences[idx_of_sentence]) - 1:
                        splitted_sentences[idx_of_sentence][idx_of_word_in_sent] = word
                        splitted_sentences[idx_of_sentence + 1].pop(0)
                        splitted_sentences[idx_of_sentence] += splitted_sentences[idx_of_sentence + 1]
                        splitted_sentences.pop(idx_of_sentence + 1)
                        break
                    else:
                        splitted_sentences[idx_of_sentence].pop(idx_of_word_in_sent)
                        break

            if idx_of_word_in_sent == len(splitted_sentences[idx_of_sentence]) - 1:
                idx_of_sentence += 1
                idx_of_word_in_sent = 0
            else:
                idx_of_word_in_sent += 1
            if word_idx >= label:
                break

        if failed_flg:
            failed_flg = False
            continue

        shift_begin = False
        shift_end = False
        for i in range(len(sentences)):
            if words_cnt <= label <= words_cnt + len(splitted_sentences[i]) - 1:
                if label == words_cnt:
                    shift_begin = True
                if label == words_cnt + len(splitted_sentences[i]) - 1:
                    shift_end = True
                sent_idx = idx
                break
            idx += 1
            words_cnt += len(splitted_sentences[i])

        try:
            if shift_begin:
                check_trio = (text.split(" ")[label], text.split(" ")[label + 1], text.split(" ")[label + 2])
            elif shift_end:
                check_trio = (text.split(" ")[label - 2], text.split(" ")[label - 1], text.split(" ")[label])
            else:
                check_trio = (text.split(" ")[label - 1], text.split(" ")[label], text.split(" ")[label + 1])
            try:
                zipped_text_and_labels = create_new_examples(splitted_sentences, splitted_sentences[sent_idx], sent_idx,
                                                             check_trio, label)
            except TypeError as err:
                continue
            for idx, (text, label) in enumerate(zipped_text_and_labels):
                augmented_data = append_augmented_text(augmented_data, text, label, text_id, idx)
        except IndexError as err:
            print(f"Error in {text_id}: {err}")
        except AssertionError as err:
            print(f"Assertion in {text_id}: {err}")
    return augmented_data


if __name__ == '__main__':
    # read texts that will be augmented
    texts = []
    mode = 'train'  # can be changed to dev
    shuffle = True
    path_prefix = "."
    path_src = f'{path_prefix}/data/subtaskC_{mode}.jsonl'
    with open(path_src, 'r') as json_file:
        jsoned_texts = list(json_file)
    for jsoned_text in jsoned_texts:
        texts.append(json.loads(jsoned_text))

    augmented_texts = process(texts)
    if shuffle:
        random.shuffle(augmented_texts)
    records = pd.DataFrame(augmented_texts).to_dict("records")
    with open(f'{path_prefix}/data/augmented_{mode}.jsonl', "w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")
