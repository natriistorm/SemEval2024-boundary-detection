import re
import json
import pandas as pd
from splitter import split_into_sentences
import spacy


def find_index_of_word(splitted_change_sent, check_trio):
    position = 0
    if splitted_change_sent[0] == check_trio[1] and splitted_change_sent[1] == check_trio[2]:
        return 0
    if splitted_change_sent[len(splitted_change_sent) - 2] == check_trio[0] \
            and splitted_change_sent[len(splitted_change_sent) - 1] == check_trio[1]:
        return len(splitted_change_sent) - 1
    for i in range(1, len(splitted_change_sent) - 1):
        if splitted_change_sent[i - 1] == check_trio[0] and splitted_change_sent[i] == check_trio[1] and \
                splitted_change_sent[i + 1] == check_trio[2]:
            position = i
            break
    return position


def create_new_examples(splitted_sentences, splitted_change_sent, idx, check_trio, position=0):
    sentences = [" ".join(sentence) for sentence in splitted_sentences]
    num_sent = len(splitted_sentences)
    word_to_check = check_trio[1]
    text1, text2, text3, text4 = "", "", "", ""
    new_position_of_target1, new_position_of_target2, new_position_of_target3, new_position_of_target4 = position, \
                                                                                                         position, position, position
    if num_sent == 1:
        return (text1, new_position_of_target1), (text2, new_position_of_target2), \
               (text3, new_position_of_target3), (text4, new_position_of_target4)
    if idx == 0:
        idx1 = min(num_sent + 3, num_sent - 1)
        text1 = " ".join(sentences[:idx1])
        new_position_of_target1 = position
    elif idx == num_sent - 1:
        idx1 = num_sent // 2
        if idx1 != 0:
            text1 = " ".join(sentences[idx1:])
            position = find_index_of_word(splitted_change_sent, check_trio)
            num_of_words_before_last_sent = " ".join(sentences[idx1:idx]).split(" ")
            new_position_of_target1 = len(num_of_words_before_last_sent) + position
    else:
        position = find_index_of_word(splitted_change_sent, check_trio)
        idx1_begin = max(0, idx - 1)
        idx1_end = min(num_sent - 1, idx + 2)
        if idx1_end - idx1_begin > 1:
            text1 = " ".join(sentences[idx1_begin:idx1_end])
            num_of_words_before_last_sent = " ".join(sentences[idx1_begin:idx]).split(" ")
            new_position_of_target1 = len(num_of_words_before_last_sent) + position
            text1_word = text1.split(" ")[new_position_of_target1]
            assert text1_word == word_to_check
        idx2_begin = max(0, idx - 2)
        idx2_end = min(num_sent - 1, idx + 3)
        if (idx2_begin == 0 and idx2_end == num_sent - 1) or \
                (idx2_begin == idx1_begin and idx2_end == idx1_end) or \
                (idx1_begin == idx2_begin and idx1_begin == 0):
            return (text1, new_position_of_target1), (text2, new_position_of_target2), \
                   (text3, new_position_of_target3), (text4, new_position_of_target4)
        if idx2_end - idx2_begin > 2:
            text2 = " ".join(sentences[idx2_begin:idx2_end])
            num_of_words_before_last_sent = " ".join(sentences[idx2_begin:idx]).split(" ")
            new_position_of_target2 = len(num_of_words_before_last_sent) + position
            text2_word = text2.split(" ")[new_position_of_target2]
            assert text2_word == word_to_check
        idx3_begin = max(0, idx - 3)
        idx3_end = min(num_sent - 1, idx + 4)
        if (idx3_begin == 0 and idx3_end == num_sent - 1) or \
                (idx3_begin == idx2_begin and idx2_end == idx3_end) or \
                (idx3_begin == idx2_begin and idx3_begin == 0):
            return (text1, new_position_of_target1), (text2, new_position_of_target2), \
                   (text3, new_position_of_target3), (text4, new_position_of_target4)
        if idx3_end - idx3_begin > 2:
            text3 = " ".join(sentences[idx3_begin:idx3_end])
            num_of_words_before_last_sent = " ".join(sentences[idx3_begin:idx]).split(" ")
            new_position_of_target3 = len(num_of_words_before_last_sent) + position
            text3_word = text3.split(" ")[new_position_of_target3]
            assert text3_word == word_to_check

        idx4_begin = max(0, idx - 4)
        idx4_end = min(num_sent - 1, idx + 5)

        if (idx4_begin == 0 and idx4_end == num_sent - 1) or \
                (idx4_begin == idx3_begin and idx4_end == idx3_end):
            return (text1, new_position_of_target1), (text2, new_position_of_target2), \
                   (text3, new_position_of_target3), (text4, new_position_of_target4)
        if idx4_end - idx4_begin > 2:
            text4 = " ".join(sentences[idx4_begin:idx4_end])
            num_of_words_before_last_sent = " ".join(sentences[idx4_begin:idx]).split(" ")
            new_position_of_target4 = len(num_of_words_before_last_sent) + position
            text4_word = text4.split(" ")[new_position_of_target4]
            assert text4_word == word_to_check
    return (text1, new_position_of_target1), (text2, new_position_of_target2), \
           (text3, new_position_of_target3), (text4, new_position_of_target4)


def get_positions_for_slicing_text(window, idx, sentences, len_of_text):
    combined_sentences = [" ".join(s) for s in sentences]
    len_of_prefix = len(" ".join(combined_sentences[:idx]))
    start_pos = max(0, len_of_prefix - window)
    right_start_pos = len_of_prefix + len(combined_sentences[idx])
    end_pos = min(right_start_pos + window, len_of_text - 1)
    return start_pos, end_pos


def create_new_examples_based_on_chars(idx, sentences, text, check_trio):
    len_of_text = len(text)
    idx_of_sent_in_text = text.find(" ".join(sentences[idx]))
    position_label = find_index_of_word(sentences[idx], check_trio)
    textes = []
    window_sizes = [500, 350, 200]
    if idx != 0 and idx != len(sentences) - 1:
        for window in window_sizes:
            start_pos, end_pos = get_positions_for_slicing_text(window, idx, sentences, len_of_text)
            if start_pos == 0 and end_pos == len(text) - 1:
                continue
            else:
                new_text = text[start_pos:end_pos]
                start_idx = 0
                while new_text[start_idx] != " ":
                    start_idx += 1
                end_idx = len(new_text) - 1
                while new_text[end_idx] != " ":
                    end_idx -= 1
                new_text = new_text[start_idx:end_idx]
                textes.append(new_text)
    else:
        if idx == 0:
            for window in window_sizes:
                if len(text) - len(sentences[idx]) > window:
                    end_pos = window + len(sentences[idx])
                else:
                    continue
                new_text = text[:end_pos]
                end_idx = len(new_text) - 1
                while new_text[end_idx] != " ":
                    end_idx -= 1
                new_text = new_text[:end_idx]
                textes.append(new_text)
        if idx == len(sentences) - 1:
            for window in window_sizes:
                if len(text) - len(sentences[idx]) > window:
                    start_pos = len(text) - len(sentences[idx]) - window
                else:
                    continue
                new_text = text[start_pos:]
                start_idx = 0
                while new_text[start_idx] != " ":
                    start_idx += 1
                new_text = new_text[start_idx:]
                textes.append(new_text)
    return textes


#
def process(data, text_id=None):
    data_for_df = []
    for elem in data:
        idx = 0
        words_cnt = 0
        sent_idx = 0
        # text_id = elem['id']
        if elem['id'] != text_id:
            continue
        label = elem['label']
        # word where change happens
        text = elem['text']
        splitted_text = text.split(" ")
        # doc = nlp(text)
        # sentences = [sent.text for sent in doc.sents]
        sentences = split_into_sentences(text)
        splitted_sentences = [sentence.split(" ") for sentence in sentences]
        for i in range(1, len(sentences)):
            if re.match(r"[\r\n]+\w+", splitted_sentences[i][0]):
                continue
            if re.match(r"\r\n", splitted_sentences[i][0]) or re.match(r"[)\],;:]\D*", splitted_sentences[i][0]):
                splitted_sentences[i - 1][-1] = splitted_sentences[i - 1][-1] + splitted_sentences[i][0]
                splitted_sentences[i] = splitted_sentences[i][1:]
        # iteratr through sentence
        sent_iter_idx = 0
        word_sent_idx = 0
        for word_idx, word in enumerate(splitted_text):
            if splitted_sentences[sent_iter_idx][word_sent_idx] == word:
                if word_sent_idx == len(splitted_sentences[sent_iter_idx]) - 1:
                    sent_iter_idx += 1
                    word_sent_idx = 0
                else:
                    word_sent_idx += 1
                if word_idx > label:
                    break
                continue
            else:
                splitted_sentences[sent_iter_idx].insert(word_sent_idx, word)
                if word_sent_idx == len(splitted_sentences[sent_iter_idx]) - 1:
                    sent_iter_idx += 1
                    word_sent_idx = 0
                else:
                    word_sent_idx += 1
                if word_idx >= label:
                    break
        change_sent = ""
        for i in range(len(sentences)):
            if words_cnt <= label <= words_cnt + len(splitted_sentences[i]):
                sent_idx = idx
                change_sent = splitted_sentences[i]
                break
            idx += 1
            words_cnt += len(splitted_sentences[i])

        try:
            check_trio = (text.split(" ")[label - 1], text.split(" ")[label], text.split(" ")[label + 1])
            (new_text1, label1), \
            (new_text2, label2), \
            (new_text3, label3), \
            (new_text4, label4) = create_new_examples(splitted_sentences, splitted_sentences[sent_idx], sent_idx,
                                                      check_trio, label)
            if new_text1 != "":
                data_for_df.append({"id": f"{text_id}_1", "text": new_text1, "label": label1})
            if new_text2 != "":
                data_for_df.append({"id": f"{text_id}_2", "text": new_text2, "label": label2})
            if new_text3 != "":
                data_for_df.append({"id": f"{text_id}_3", "text": new_text3, "label": label3})
            if new_text4 != "":
                data_for_df.append({"id": f"{text_id}_4", "text": new_text4, "label": label4})
        except IndexError as err:
            print(f"Error in {text_id}: {err}")
        except AssertionError as err:
            print(f"{text_id}")
    return data_for_df


path_src = 'data/deberta_large/subtaskC_test.jsonl'
with open(path_src, 'r') as json_file:
    json_list = list(json_file)

preds = []
for json_str in json_list:
    preds.append(json.loads(json_str))
data = preds
data_for_df = process(data)
df = pd.DataFrame(data_for_df)
records = df.to_dict("records")
with open('augmented_dev.jsonl', "w") as f:
    for record in records:
        f.write(json.dumps(record) + "\n")
